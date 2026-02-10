# =========================================================
# [Cell 61] test_working 전처리 + 시각화 함수 정의
# =========================================================
# 용도: 나중에 ML 6종, AutoGluon, 앙상블에서 호출하여
#       특정 엔진의 RUL 예측 궤적 vs 실제 RUL을 비교
# =========================================================

import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# ---------------------------------------------------------
# 1. test_working 생성 (전체 시계열 유지, 파생변수 포함)
#    Cell 60은 마지막 행만 추출하지만, 시각화는 전체 궤적이 필요
# ---------------------------------------------------------
def build_test_working(test_df, train_df):
    """
    Test 데이터 전체 시계열에 대해:
    센서 매핑 → 파생변수(물리) → Cluster/Mode → 정규화 → Savgol → EMA/Rolling
    """
    print("🔧 test_working 생성 중 (전체 시계열 + 파생변수)...")
    
    tw = test_df.copy()
    
    # [A] 센서 매핑 (Train Cell 12와 동일)
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
    rename_map = {k:v for k,v in sensor_mapping.items() if k in tw.columns}
    tw.rename(columns=rename_map, inplace=True)
    
    # [B] 물리 파생변수
    tw["P50[psi]"]       = tw["epr[-]"] * tw["P2[psi]"]
    tw["HPC.TR[-]"]      = tw["T30[R]"] / tw["T24[R]"]
    tw["OPR[-]"]         = tw["P30[psi]"] / tw["P2[psi]"]
    t2_safe              = tw["T2[R]"].replace(0, 518.67)
    tw["WfP3C[pph/psi]"] = tw["phi[pph/psi]"] / np.sqrt(t2_safe / 518.67)
    
    # [C] Cluster & Mode
    cluster_cols = ['Alt[kft]', 'Mn[-]', 'TLA[deg]']
    kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
    train_wc = train_df.copy()
    train_wc['cluster'] = kmeans.fit_predict(train_df[cluster_cols])
    
    tw['cluster'] = kmeans.predict(tw[cluster_cols])
    for i in range(6):
        tw[f'cluster_{i}'] = (tw['cluster'] == i).astype(int)
    
    tw['Mode_ID'] = 0
    train_wc['Mode_ID'] = 0
    mask_c1_tr = (train_wc['cluster'] == 1)
    farb_c1 = train_wc.loc[mask_c1_tr, ['farB[-]']].values
    
    if len(farb_c1) > 10:
        km_mode = KMeans(n_clusters=2, random_state=42, n_init=10)
        mode_labels = km_mode.fit_predict(farb_c1)
        centers = km_mode.cluster_centers_.reshape(-1)
        if centers[1] < centers[0]:
            mode_labels = 1 - mode_labels
        train_wc.loc[mask_c1_tr, 'Mode_ID'] = mode_labels
        train_wc['Mode_ID'] = train_wc['Mode_ID'].fillna(0).astype(int)
        mode_farb_centers = train_wc[mask_c1_tr].groupby('Mode_ID')['farB[-]'].mean()
        
        mask_c1_te = (tw['cluster'] == 1)
        if mask_c1_te.sum() > 0:
            vals = tw.loc[mask_c1_te, ['farB[-]']]
            mode_dists = euclidean_distances(vals, mode_farb_centers.values.reshape(-1, 1))
            tw.loc[mask_c1_te, 'Mode_ID'] = mode_farb_centers.index[np.argmin(mode_dists, axis=1)]
    
    tw['condition_id'] = tw['cluster'] * 10 + tw['Mode_ID']
    train_wc['condition_id'] = train_wc['cluster'] * 10 + train_wc['Mode_ID']
    
    # [D] 조건부 정규화
    cond_stats = train_wc.groupby('condition_id')[SENSOR_FEATURES].agg(['mean', 'std'])
    for col in SENSOR_FEATURES:
        if col in tw.columns:
            means = tw['condition_id'].map(cond_stats[col]['mean'])
            stds  = tw['condition_id'].map(cond_stats[col]['std']).replace(0, 1e-6)
            if means.isnull().any():
                means.fillna(train_wc[col].mean(), inplace=True)
                stds.fillna(train_wc[col].std(), inplace=True)
            tw[col] = ((tw[col] - means) / stds).clip(-3, 3)
    
    # [E] Savgol 노이즈 제거
    for col in SENSOR_FEATURES:
        grouped = tw.groupby('unit_number')[col]
        try:
            tw[col] = grouped.transform(
                lambda x: savgol_filter(x, window_length=11, polyorder=2) if len(x) > 11 else x
            )
        except: pass
    
    # [F] 파생변수 (EMA, Rolling) - Train Cell 55와 동일
    for col in SENSOR_FEATURES:
        grouped = tw.groupby('unit_number')[col]
        tw[f"{col}_ema_20"]  = grouped.transform(lambda x: x.ewm(span=20).mean())
        tw[f"{col}_mean_5"]  = grouped.transform(lambda x: x.rolling(window=5, min_periods=1).mean())
        tw[f"{col}_std_5"]   = grouped.transform(lambda x: x.rolling(window=5, min_periods=1).std())
        tw[f"{col}_mean_20"] = grouped.transform(lambda x: x.rolling(window=20, min_periods=1).mean())
        tw[f"{col}_std_20"]  = grouped.transform(lambda x: x.rolling(window=20, min_periods=1).std())
    
    tw.fillna(0, inplace=True)
    
    # [G] RUL 붙이기 (시각화용)
    max_cycles = tw.groupby('unit_number')['time_in_cycles'].transform('max')
    rul_map = rul_df.copy()
    if 'unit_number' not in rul_map.columns:
        rul_map['unit_number'] = range(1, len(rul_map) + 1)
    tw = tw.merge(rul_map, on='unit_number', suffixes=('', '_true'))
    
    # RUL = (마지막 사이클의 실제 RUL) + (마지막 사이클 - 현재 사이클)
    rul_col = 'RUL_true' if 'RUL_true' in tw.columns else 'RUL'
    tw['RUL'] = tw[rul_col] + (max_cycles - tw['time_in_cycles'])
    if 'RUL_true' in tw.columns:
        tw.drop(columns=['RUL_true'], inplace=True)
    
    print(f"✅ test_working 완성: {tw.shape} (ALL_FEATURES {len(ALL_FEATURES)}개 포함)")
    return tw

# ---------------------------------------------------------
# 2. 시각화 함수 정의
# ---------------------------------------------------------
def plot_engine_trajectory_v2(model_name, pipeline, test_full_df, unit_id, feature_cols, margin=0):
    """
    특정 엔진(unit_id)의 전체 시계열에 대해 RUL 예측 궤적을 시각화
    
    Parameters:
        model_name: 모델 이름 (표시용)
        pipeline: 학습 완료된 sklearn Pipeline
        test_full_df: test_working (전체 시계열 + ALL_FEATURES 포함)
        unit_id: 시각화할 엔진 번호
        feature_cols: 학습에 사용된 피처 리스트 (ALL_FEATURES)
        margin: Safety Margin (기본 0, best_margin 전달 가능)
    """
    engine_data = test_full_df[test_full_df['unit_number'] == unit_id].copy()
    
    if len(engine_data) == 0:
        print(f"⚠️ Unit {unit_id} 데이터가 없습니다.")
        return

    X_engine = engine_data[feature_cols]
    y_true = engine_data['RUL']
    
    y_pred = pipeline.predict(X_engine)
    y_pred = y_pred + margin  # margin이 음수면 예측을 낮춤
    y_pred = np.maximum(y_pred, 0)

    plt.figure(figsize=(10, 4))
    plt.plot(engine_data['time_in_cycles'], y_true, 'r--', label='True RUL', linewidth=2)
    
    margin_label = f" (Margin {margin:+.1f})" if margin != 0 else ""
    plt.plot(engine_data['time_in_cycles'], y_pred, 'b-', 
             label=f'Pred by {model_name}{margin_label}', alpha=0.8)
    
    plt.title(f"Unit #{unit_id} RUL Trajectory - {model_name}")
    plt.xlabel("Time (Cycles)")
    plt.ylabel("RUL")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# ---------------------------------------------------------
# 3. 실행: test_working 생성
# ---------------------------------------------------------
test_working = build_test_working(test_df, train_df)

print("\n📌 시각화 호출 예시:")
print("   plot_engine_trajectory_v2('XGBoost', pipeline, test_working, 24, ALL_FEATURES, margin=best_margin)")