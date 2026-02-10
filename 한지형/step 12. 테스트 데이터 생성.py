from scipy.signal import savgol_filter 
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

def prepare_test_data_final(test_df, train_df, train_norm):
    print("🚀 Test Data 전처리 시작...")
    
    test_working = test_df.copy()

    # ---------------------------------------------------------
    # [Step A] 센서 매핑 (Train Cell 12와 100% 동일)
    # ---------------------------------------------------------
    sensor_mapping = {
        'sensor_1': 'T2[R]',          'sensor_2': 'T24[R]',        'sensor_3': 'T30[R]', 
        'sensor_4': 'T50[R]',         'sensor_5': 'P2[psi]',       'sensor_6': 'P15[psi]', 
        'sensor_7': 'P30[psi]',       'sensor_8': 'Nf[rpm]',       'sensor_9': 'Nc[rpm]', 
        'sensor_10': 'epr[-]',        'sensor_11': 'phi[pph/psi]', 'sensor_12': 'Ps30[psi]',
        'sensor_13': 'NRf[rpm]',      'sensor_14': 'NRc[rpm]',     'sensor_15': 'BPR[-]',
        'sensor_16': 'farB[-]',       'sensor_17': 'htBleed[]',    'sensor_18': 'Nf_dmd[rpm]',
        'sensor_19': 'PCNfR_dmd[Pct]','sensor_20': 'W31[lbm/s]',   'sensor_21': 'W32[lbm/s]',
        'op_setting_1': 'Alt[kft]',   'op_setting_2': 'Mn[-]',     'op_setting_3': 'TLA[deg]'
    }
    rename_map = {k:v for k,v in sensor_mapping.items() if k in test_working.columns}
    test_working.rename(columns=rename_map, inplace=True)

    # ---------------------------------------------------------
    # [Step B] 파생변수 생성 (물리 공식)
    # ---------------------------------------------------------
    test_working["P50[psi]"]  = test_working["epr[-]"] * test_working["P2[psi]"]
    test_working["HPC.TR[-]"] = test_working["T30[R]"] / test_working["T24[R]"]
    test_working["OPR[-]"]    = test_working["P30[psi]"] / test_working["P2[psi]"]
    t2_safe = test_working["T2[R]"].replace(0, 518.67) 
    test_working["WfP3C[pph/psi]"] = test_working["phi[pph/psi]"] / np.sqrt(t2_safe / 518.67)

    # ---------------------------------------------------------
    # [Step C] Cluster & Mode (Train 원본 기준 재구축)
    # ---------------------------------------------------------
    print("   ... Clustering & Mode Matching")
    cluster_cols = ['Alt[kft]', 'Mn[-]', 'TLA[deg]']
    
    kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
    train_with_cluster = train_df.copy()
    train_with_cluster['cluster'] = kmeans.fit_predict(train_df[cluster_cols])
    
    test_working['cluster'] = kmeans.predict(test_working[cluster_cols])
    for i in range(6):
        test_working[f'cluster_{i}'] = (test_working['cluster'] == i).astype(int)

    # Mode_ID
    test_working['Mode_ID'] = 0
    train_with_cluster['Mode_ID'] = 0
    mask_c1_train = (train_with_cluster['cluster'] == 1)
    farb_c1_train = train_with_cluster.loc[mask_c1_train, ['farB[-]']].values
    
    mode_farb_centers = None
    if len(farb_c1_train) > 10:
        km_mode = KMeans(n_clusters=2, random_state=42, n_init=10)
        mode_labels = km_mode.fit_predict(farb_c1_train)
        centers = km_mode.cluster_centers_.reshape(-1)
        if centers[1] < centers[0]:
            mode_labels = 1 - mode_labels
        train_with_cluster.loc[mask_c1_train, 'Mode_ID'] = mode_labels
        train_with_cluster['Mode_ID'] = train_with_cluster['Mode_ID'].fillna(0).astype(int)
        mode_farb_centers = train_with_cluster[mask_c1_train].groupby('Mode_ID')['farB[-]'].mean()
        
        mask_c1_test = (test_working['cluster'] == 1)
        if mask_c1_test.sum() > 0:
            farb_vals = test_working.loc[mask_c1_test, ['farB[-]']]
            mode_dists = euclidean_distances(farb_vals, mode_farb_centers.values.reshape(-1, 1))
            predicted_idx = np.argmin(mode_dists, axis=1)
            test_working.loc[mask_c1_test, 'Mode_ID'] = mode_farb_centers.index[predicted_idx]
    
    test_working['condition_id'] = test_working['cluster'] * 10 + test_working['Mode_ID']
    train_with_cluster['condition_id'] = train_with_cluster['cluster'] * 10 + train_with_cluster['Mode_ID']

    # ---------------------------------------------------------
    # [Step D] 조건부 정규화 (기본 센서 컬럼만)
    # ---------------------------------------------------------
    print("   ... Normalizing based on Train Statistics")
    
    numeric_features = SENSOR_FEATURES  # 7개 수치형 센서
    cond_stats = train_with_cluster.groupby('condition_id')[numeric_features].agg(['mean', 'std'])
    
    for col in numeric_features:
        if col in test_working.columns:
            means = test_working['condition_id'].map(cond_stats[col]['mean'])
            stds  = test_working['condition_id'].map(cond_stats[col]['std']).replace(0, 1e-6)
            if means.isnull().any():
                means.fillna(train_with_cluster[col].mean(), inplace=True)
                stds.fillna(train_with_cluster[col].std(), inplace=True)
            test_working[col] = (test_working[col] - means) / stds
            test_working[col] = test_working[col].clip(-3, 3)

    # ---------------------------------------------------------
    # [Step E] 노이즈 제거 (Savgol Filter) - 기본 센서에 적용
    # ---------------------------------------------------------
    print("   ... Applying Smoothing Filter")
    for col in numeric_features:
        grouped = test_working.groupby('unit_number')[col]
        try:
            test_working[col] = grouped.transform(
                lambda x: savgol_filter(x, window_length=11, polyorder=2) if len(x) > 11 else x
            )
        except: pass

    # ---------------------------------------------------------
    # [Step F] ★ 파생변수 생성 (EMA, Rolling) - Train Cell 55와 동일
    # ---------------------------------------------------------
    print("   ... Generating Derived Features (EMA, Rolling)")
    for col in numeric_features:
        grouped = test_working.groupby('unit_number')[col]
        
        test_working[f"{col}_ema_20"]  = grouped.transform(lambda x: x.ewm(span=20).mean())
        test_working[f"{col}_mean_5"]  = grouped.transform(lambda x: x.rolling(window=5, min_periods=1).mean())
        test_working[f"{col}_std_5"]   = grouped.transform(lambda x: x.rolling(window=5, min_periods=1).std())
        test_working[f"{col}_mean_20"] = grouped.transform(lambda x: x.rolling(window=20, min_periods=1).mean())
        test_working[f"{col}_std_20"]  = grouped.transform(lambda x: x.rolling(window=20, min_periods=1).std())

    # NaN 처리 (rolling 초기 구간)
    test_working.fillna(0, inplace=True)

    # ---------------------------------------------------------
    # [Step G] 최종 데이터 추출 (Last Row)
    # ---------------------------------------------------------
    test_last = test_working.groupby('unit_number').last().reset_index()
    
    if 'unit_number' not in rul_df.columns:
        rul_df['unit_number'] = range(1, len(rul_df) + 1)
    test_final = pd.merge(test_last, rul_df, on='unit_number')
    
    # ★ ALL_FEATURES (48개) 사용
    X_test = test_final[ALL_FEATURES].copy()
    y_test = test_final['RUL']
    
    X_test.fillna(0, inplace=True)
    
    return X_test, y_test

# 실행
X_test, y_test = prepare_test_data_final(test_df, train_df, train_norm)

print(f"\n✅ [결과 확인]")
print(f"👉 X_test shape: {X_test.shape}")
print(f"👉 X_train shape와 일치 여부: {X_test.shape[1]} == {len(ALL_FEATURES)} -> {X_test.shape[1] == len(ALL_FEATURES)}")
print(f"👉 컬럼 일치 여부: {set(X_test.columns) == set(ALL_FEATURES)}")
