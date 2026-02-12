## AI 모델 개발 15회차 1차 팀프로젝트 - NASA Turbofan Jet Engine Data Set 터보엔진 유지보전 문제_FD001
[문제 개요]     
NASA C-MAPSS(Commercial Modular Aero-Propulsion System Simulation) 데이터셋은 예지 보전(Predictive Maintenance) 분야의 'Hello World'와 같은 매우 유명하고 중요한 데이터셋입니다.    

[문제의 배경]     
IEEE PHM 2008 챌린지: 이 데이터는 2008년 PHM(Prognostics and Health Management, 고장 예지 및 건전성 관리) 데이터 챌린지 대회에서 처음 공개되었습니다.    
 (IEEE(전기전자공학자협회)는 전 세계 전기, 전자, 컴퓨터, 통신 분야의 표준화와 기술 발전을 주도하는 세계 최대 규모의 전문가 기술 단체)   

데이터셋의 탄생 배경은 **"비싼 제트 엔진을 실제로 고장 날 때까지 돌려보는 것은 불가능에 가깝다"**는 현실적인 문제에서 출발
NASA는 실제 엔진과 매우 유사한 물리적 특성을 가진 고정밀 시뮬레이터 소프트웨어(C-MAPSS)를 개발했습니다. 이 소프트웨어로 수만 번의 비행 시뮬레이션을 돌려 가상의 '고장 데이터'를 만들어낸 것이 바로 이 데이터셋입니다.

[문제의 목표]
이 문제의 핵심 목표는 **"엔진이 언제 고장 날지 맞히는 것"**입니다.
    구해야 하는 것: RUL (Remaining Useful Life, 잔여 수명)

[실험 시나리오]
1. 초기 상태: 각 엔진은 정상 상태에서 작동을 시작합니다.
   - 단, 사용자에게는 알려지지 않은 수준의 초기 마모(Initial Wear)와 제조 공차(Variation)가 존재합니다.
     (이는 결함이 아닌 정상적인 범주입니다.)
2. 고장 진행: 어느 시점부터 결함(Fault)이 발생하여 시간이 지날수록 상태가 악화됩니다.
3. 데이터 범위:
   - 학습 세트 (Train): 결함 발생부터 시스템 고장(Failure) 시점까지의 모든 데이터가 포함됩니다.
   - 테스트 세트 (Test): 고장 발생 전 임의의 시점에서 데이터 기록이 중단됩니다.

[데이터 셋의 특징]
1. 시계열 데이터 (Time-Series): 엔진이 작동하는 동안 센서(온도, 압력, 속도 등 21개) 값이 시간(Cycle) 순서대로 기록되어 있습니다.
2. FD-001 부터 FD-004 까지 난이도 별로 데이터셋이 구성되어 있습니다.


[난이도 별 차이]
FD-001: 운전 조건(고도, 속도, 쓰로틀 각도) 1개, 고장모드 (HPC, 고압압축기) 1개    
FD-002: 운전 조건(고도, 속도, 쓰로틀 각도) 6개, 고장모드 (HPC, 고압압축기) 1개    
FD-003: 운전 조건(고도, 속도, 쓰로틀 각도) 1개, 고장모드 (HPC, 고압압축기 / LPT, 저압 터빈) 2개    
FD-004: 운전 조건(고도, 속도, 쓰로틀 각도) 6개, 고장모드 (HPC, 고압압축기 / LPT, 저압 터빈) 2개    
난이도는 FD-001, FD-003, FD-002, FD-004 순서로 어렵다.

-> 이번 프로젝트에서는 FD-001과 FD-002 2가지를 다룬다.

![엔진 부위 설명.jpg](https://media.discordapp.net/attachments/1451496750023049256/1471382306882191543/692429fcd40a4838.jpg?ex=698ebb0e&is=698d698e&hm=73b58b97fe5ba9593b3ab8f639653753449fe1a61c4ef8b635c563f563cd85ad&=&format=webp)

> FD001 (Train: train_FD001.txt / Test: test_FD001.txt / RUL: RUL_FD001.txt)
   - 학습 엔진 수: 100개
   - 테스트 엔진 수: 100개
   - 운전 조건 (Conditions): 1가지 (해수면 - Sea Level)
   - 고장 모드 (Fault Modes): 1가지 (HPC 열화 - HPC Degradation)
   - 이 문제의 데이터셋의 특징은 초기 마모와 계측 노이즈를 반영해 노이즈가 굉장히 심한것이 특징입니다.

[문제 채점 방식 - nasa score]
- 항공기의 경우 남은 수명을 더 적게 예측해 미리 사용정지 할경우 생기는 문제는 심각하지 않지만 반대 경우 운전 중 사고가 나서 심각한 문제가 발생할 수 있습니다.
- 따라서 작은 RUL 예측(early prediction)에 비해 큰 RUL 예측(late prediction)에 대해 훨씬 큰 페널티를 매기는 nasa scroring 방식을 사용합니다.

![nasa scoring 공식.jpg](https://cdn.discordapp.com/attachments/1451496750023049256/1471382306181611520/nasa_scoring_.jpg?ex=698ebb0e&is=698d698e&hm=3fd9f5508b18505ce3c085dbb8bc3c004ad3625b717483fec383e7ff811b5eb0&)

![nasa scoring 그래프.jpg](https://cdn.discordapp.com/attachments/1451496750023049256/1471382306441920764/nasa_scoring_.jpg?ex=698ebb0e&is=698d698e&hm=5300f1623be7b6e78f1c273ad42ec547186abe2d8a621146b73b34d9ce11a183&)

[FD-001 문제해결 핵심 전략]

   - 노이즈 제거
      1. roliing window 방식
      2. Savitzky-Golay 필터
      3. EMA(지수이동평균)
      * 아래 이미지는 FD-002에서 나올 클러스터링과 노이즈 제거의 효과를 시각화 한 것이다.
         
<img width="583" height="143" alt="노이즈 제거" src="https://github.com/user-attachments/assets/2ab11cb1-822c-4c76-95a8-3e292c7e6299" />

   - 컬럼 라벨링 및 파생 컬럼 생성
      1. op_setting_1, sensor_1 등의 컬럼 명이 아닌 실제 센서 내용을 알수있는 컬럼 명으로 라벨링
      2. 공기 유동 비율, 압력 비 등의 비율 파생 컬럼을 만들어 무차원수가 되어 온도나 압력등의 외부 요인의 영향을 제거한다. 현상을 해석하기 쉬워진다.
     
```PS
rain_df["P50[psi]"] = train_df["epr[-]"]*train_df["P2[psi]"]

train_df["Fan.PR[-]"] = train_df["P15[psi]"]/train_df["P2[psi]"]
train_df["LPC.TR[-]"] = train_df["T24[R]"]/train_df["T2[R]"] # Fan core + LPC
train_df["HPC.TR[-]"] = train_df["T30[R]"]/train_df["T24[R]"]

train_df["OPR[-]"] = train_df["P30[psi]"]/train_df["P2[psi]"]

train_df["Wf[pph]"] = train_df["phi[pph/psi]"]*train_df["Ps30[psi]"]
train_df["Wa36[lbm/s]"] = train_df["Wf[pph]"]/3600.0 / train_df["farB[-]"]
train_df["W24[lbm/s]"] = train_df["Wa36[lbm/s]"] + train_df["W31[lbm/s]"] + train_df["W32[lbm/s]"] # core. htBleed ? 
train_df["W15[lbm/s]"] = train_df["W24[lbm/s]"]*train_df["BPR[-]"] # bypass
train_df["W2[lbm/s]"] = train_df["W15[lbm/s]"] + train_df["W24[lbm/s]"] # overall

train_df["WfP3C[pph/psi]"] = train_df["phi[pph/psi]"]/np.sqrt(train_df["T2[R]"]/518.67)
```

   - RUL Clipping
      1. 이 문제의 핵심 전처리 전략이다.
      2. 엔진은 서서히 고장나는게 아니라 특정 시점부터 급격히 나빠지는 특징이 있고 이후 시각화 그래프에서도 확인이 가능하다.
      3. 초기 건강한 사이클의 경우 센서값은 일정한데 RUL(남은 수명)이 줄어 들어 센서와 RUL의 관게에 대해 모델이 혼란을 겪게 된다.
      4. 실제 RUL보다 더 큰 RUL을 모델이 예측하게 되면 late prediction으로 인해 nasa score가 매우 나빠지는데 clipping으로 한계점을 만들어줄수 있습니다.
         
            1) 고정 클리핑 (Fixed Clipping)
                  - 설명: 경험적 수치인 120-130으로 RUL 상한선을 제한 (Heimes et al. 2008 우승 논문 기준 125-130 사용)
                  - 장점: 단순하며 데이터 노이즈에 강함
                  - 단점: 엔진별 최대 RUL 차이가 클 경우, 수명이 긴 엔진의 예측 정확도가 저하됨
                    
            3) CUSUM: 초기 정상 상태의 평균값에서 벗어나는 오차를 누적하다가 특정 임계치를 넘는 순간을 감지한다.    
                  장점: 미세한 변화를 감지하는데에 탁월하다. 엔진별로 별개 RUL 클리핑 할 경우 사용가능하다.      
                  단점: 변화가 발생 이후 감지되기 때문에 반응이 느려 late prediction의 원인이 된다.

            4) CV 기반 최적화: Clipping Ppint를 하이퍼파라미터로 취급하고 특정 값을 입력해 최고 nasa score가 나오는 최적 포인트를 찾는다.     
                  장점: 수학적으로 가장 적합한 값을 찾는다.     
                  단점: 트레인 데이터에 과적합해 테스트 데이터 예측 정확도가 쩔어진다.

            5) 이외에 기하학적 특징을 사용하는 kneed point 등이 있다.

      -> FD-001에서는 'CV 기반 최적화' 방식을 사용

* 엔진 별 최대 수명이 125-130 정도에서 시작하는 것을 볼수 있다.
![fd-001 엔진 별 최대 수명 (3)](https://github.com/user-attachments/assets/2fb5f17e-18da-4779-b819-9c8f9bd7af70)

   - GroupShuffleSplit
      1. 이 데이터 셋은 시계열 데이터이기 때문에 data leakage를 방지하기 위해 Train_test_split 대신 GroupShuffleSplit을 사용한다.

   - Safe margin 
      1. nasa score는 late prediction에 큰 감점을 매기기 때문에 예측 값에 마이너스 수치를 반영해 이를 예방하는 safe margin을 사용한다.

   - EDA 및 Feature Selection
      1. RUL 과 컬럼과의 산점도를 보면 아래와 같이 직선형과 일정 추세를 같은 분포도로 구분 된다. 직선형은 상수형 데이터로 RUL와 관계성이 낮아 드롭한다. 단, 선택에 따라 운전조건 등의 메타데이터 컬럼은 이후 분석을 위해 모델 학습에서만 배제할수도 있다.

      ![FD-001 산점도 (2)](https://github.com/user-attachments/assets/3cc071a1-f1a7-4467-a44c-2ed55316c3eb)

      2. 이 문제에서는 엔진 고장시 온도나 압력이 동반 상승하는 효과로 인해 단순히 RUL과 상관 계수가 너무 크다고 삭제할수 없다.
      3. 상관계수가 0.1 미만이거나 위 파생 컬럼 생성에 의해 중간 과정 발생 컬럼, 중복 컬럼은 삭제한다. 이는 다중공선성 체크나 RUL에 따른 변화도 차이를 비교하여 판단할수 있다.
     
      ![컬럼 별 중복성 체크 (2)](https://github.com/user-attachments/assets/e08b108f-64bc-41ab-8941-8d577ed9b623)



[추가 설명]
1. 시계열 데이터: **시계열 데이터(Time-Series Data)**란 **"시간의 흐름에 따라 순서대로 기록된 데이터"**
일반 데이터가 사진이라면 시계열 데이터란 동영상
시계열 데이터를 배운 머신러닝 모델 (randomforest, xgboost 등으로 푸는 방식을 경험해 보고자 이 문제를 선택)

2. Rolling Window: 이 데이터셋은 시계열 데이터이기 때문에 시간에 따른 추세(trend)를 학습해야 합니다.   
특정 시점의 데이터만으로는 증가 중인지 감소 중인지 알수가 없다.
작동 방식은 예를 들어 size가 10이면 앞에 9개는 결측치 10개 미만이니까 10번째 부터 앞에 1-10까지의 평균, 11번째는 2-11까지의 평균 이런 식으로 진행하고 덩어리가 미끄러지듯 진행하기때문에 rolling window. 평균치를 내기 때문에 이상치가 희석되어 노이즈가 줄어드는 스무딩(smoothing) 효과를 냅니다. 

    단기 추세(작은 사이즈):노이즈가 적당히 제거, 데이터 손실 적음, 변화에 민감(갑자기 고장에 적합)
    장기 추세(큰 사이즈):노이즈가 크게 제거, 데이터 손실 크다, 변화에 둔감(서서히 고장에 적합)

3. Savitzky-Golay (사비츠키-골레이) 필터는 데이터의 노이즈를 제거하여 매끄럽게 만들면서도(Smoothing), 신호의 원래 모양(특히 피크의 높이나 폭)을 훼손하지 않고 유지하는 데 특화된 디지털 필터입니다.데이터의 일부분(윈도우)을 잘라내어 평균을 구하는 것이 아니라, 그 구간의 점들을 가장 잘 표현하는 **곡선(다항식)**을 그립니다.

4. **EMA (지수이동평균, Exponential Moving Average)**는 "최근 데이터일수록 더 높은 가중치(중요도)를 주는" 이동평균 방식입니다. 일정 시점에서 갑자기 고장나는 이 데이터셋에 적합합니다.

5. GroupShuffleSplit: 학습용(Train)과 검증용(Validation)으로 나눌 때 사용하는 교차 검증(Cross-Validation) 기법 중 하나. 일반적인 train_test_split이나 ShuffleSplit은 데이터를 무작위로 섞어서 나눕니다. 하지만 시계열 데이터나 특정 대상(엔진, 환자 등)의 데이터가 여러 행에 걸쳐 있는 경우, 이것은 치명적인 문제(Data Leakage)를 일으킵니다. 따라서 **"엔진 번호(Unit Number)"**를 그룹으로 지정하고, 그룹 단위로 나눕니다.

[목표 점수]

본 문제는 시계열 데이셋이라서 이에 강한 딥러닝 방식이 더 좋은 점수를 받는다. 
하지만 이 문제가 처음 공개된 당시와 마찬가지로 머신러닝 모델로 예측한다.

![FD-001 점수 표.png](https://cdn.discordapp.com/attachments/1451496750023049256/1468508260284764222/image.png?ex=698e29a4&is=698cd824&hm=5c040b76080a4a45a753e5a22b2a86ddd729d568d79f35858edae3c64f459ed6&)

출처 : 제미나이

### 컬럼 설명 (Data Dictionary)

| 컬럼명 | 설명 | 타입 |
|---|---|---|
| **unit_number** | 엔진 고유 식별자 (Unit Number) | int64 |
| **time_in_cycles** | 운전 사이클 (Time in Cycles) | int64 |
| **Alt[kft]** | 고도 (Altitude) | float64 |
| **Mn[-]** | 마하 수 (Mach Number) | float64 |
| **TLA[deg]** | 스로틀 레버 각도 (Thrust Lever Angle) | float64 |
| **T2[R]** | 팬 입구 전온도 (Total temperature at fan inlet) | float64 |
| **T24[R]** | LPC 출구 전온도 (Total temperature at LPC outlet) | float64 |
| **T30[R]** | HPC 출구 전온도 (Total temperature at HPC outlet) | float64 |
| **T50[R]** | LPT 출구 전온도 (Total temperature at LPT outlet) | float64 |
| **P2[psi]** | 팬 입구 압력 (Pressure at fan inlet) | float64 |
| **P15[psi]** | 바이패스 덕트 전압력 (Total pressure in bypass-duct) | float64 |
| **P30[psi]** | HPC 출구 전압력 (Total pressure at HPC outlet) | float64 |
| **Nf[rpm]** | 물리적 팬 속도 (Physical fan speed) | float64 |
| **Nc[rpm]** | 물리적 코어 속도 (Physical core speed) | float64 |
| **epr[-]** | 엔진 압력비 (Engine pressure ratio) | float64 |
| **phi[pph/psi]** | 연료 유량 대 Ps30 비율 (Ratio of fuel flow to Ps30) | float64 |
| **Ps30[psi]** | HPC 출구 정압 (Static pressure at HPC outlet) | float64 |
| **NRf[rpm]** | 보정된 팬 속도 (Corrected fan speed) | float64 |
| **NRc[rpm]** | 보정된 코어 속도 (Corrected core speed) | float64 |
| **BPR[-]** | 바이패스 비 (Bypass Ratio) | float64 |
| **farB[-]** | 연소기 연료-공기 비 (Burner fuel-air ratio) | float64 |
| **htBleed[]** | 블리드 엔탈피 (Bleed Enthalpy) | int64 |
| **Nf_dmd[rpm]** | 요구 팬 속도 (Demanded fan speed) | int64 |
| **PCNfR_dmd[Pct]** | 요구 보정 팬 속도 (Demanded corrected fan speed) | float64 |
| **W31[lbm/s]** | HPT 냉각 블리드 (HPT coolant bleed) | float64 |
| **W32[lbm/s]** | LPT 냉각 블리드 (LPT coolant bleed) | float64 |
| **condition** | 운전 조건 문자열 (Operational Condition String) | object |
| **P50[psi]** | LPT 출구 전압력 (Total pressure at LPT outlet) | float64 |
| **Fan.PR[-]** | 팬 압력비 (Fan pressure ratio) | float64 |
| **LPC.TR[-]** | LPC 전온도비 (LPC total temperature ratio) | float64 |
| **HPC.TR[-]** | HPC 전온도비 (HPC total temperature ratio) | float64 |
| **OPR[-]** | 전체 압력비 (Overall pressure ratio) | float64 |
| **Wf[pph]** | 연료 유량 (Fuel flow) | float64 |
| **Wa36[lbm/s]** | 코어 공기 유량 (Core airflow) | float64 |
| **W24[lbm/s]** | LPC 공기 유량 (LPC airflow) | float64 |
| **W15[lbm/s]** | 바이패스 공기 유량 (Bypass airflow) | float64 |
| **W2[lbm/s]** | 팬 유입 공기 유량 (Fan inlet airflow) | float64 |
| **WfP3C[pph/psi]** | P3 압력 대비 연료 유량 (Fuel flow to P3 pressure ratio) | float64 |
| **RUL** | 엔진의 남은 수명 (Remaining Useful Life) | int64 |

[시행착오 내용]
1. RUL Clipping 순서 변경 
초기에는 RUL clipping을 테스트 데이터 생성 전에 진행
그러나 RUL Clipping 을 EDA 전에 반영 시 히트맵에서 RUL과의 상관계수가 변하는 것을 확인
이유는 초기 건강한 구간이 반영되면 RUL과 센서와의 관계성이 낮게 측정된다.
이후 초기 단계로 이동

2. linear regression, svr이 직선으로 나오고 점수가 3000점이 넘는 문제 발생
이유는 rolling window에서 큰 size와 작은 size의 5,20 두 가지를 사용하다보니    
파생 컬럼 수가 많아져 linear regrssion에 적합하지 않게 됨.
또한, 데이터 누수를 방지하고자 train data, test data, 시각화 데이터(RUL 예측은 최종 사이클 기준으로 진행하지만 real RUL과 예측 RUL 비교 그래프를 위해 전체 사이클을 기준으로 하는 시각화 데이터도 따로 생성)를 따로 전처리 하였는데 이 과정에서 미스매치가 발생해 svr이 망가졌음.

3. 위 전처리를 통일 시키고 safe margin -3 을 적용
4. 노이즈가 나쁜 점수의 원인이라는 것을 파악하고 기존 rolling window에서 Savitzky-Golay 필터, EMA(지수이동평균)의 두 가지 노이즈 제거 방식 추가 

5. 결과 svr 기준 490점 나머지 모델은 600-800점 대로 준수한 결과 도출
6. 더 점수를 개선해보고자 여러 시행착오를 진행
    1) rul에 따라 엔진 마다 다른 safe margin을 매기는 코드 -> 과도한 margin으로 rmse가 0으로 나와 버림.
    2) 0,1,2,3,4,5 중에 가장 rmse가 잘 나오는 safe margin을 찾음, svr의 튜닝 횟수를 3배 이상 늘림 -> svr 이 너무 real rul에 근사해지다가 late prediction이 늘어 점수 악화
7. 강사님의 조언으로 하이퍼튜닝에서 xgboost와 lightgbm에 objectives로 nasa score 커스텀 함수를 넣어 최적화 학습하게 하였습니다.    
optuna 하이퍼 튜닝에서도 nasa score를 기준으로 학습되게 수정하여 아래 최고 성적 도출

![FD-001 최고 점수.png](https://cdn.discordapp.com/attachments/1451496750023049256/1469198194100539514/image.png?ex=698e0931&is=698cb7b1&hm=9b5f11fc293621e85b3eb3a3fc4f7edf625b68520911852e7f817580c31503aa&)


[모델별 결과 시각화 자료]

![FD-001 Real RUL 비교 SVR (2)](https://github.com/user-attachments/assets/f57c28a2-7465-4ac6-89ea-f9487253e1f1)

![FD-001 Real RUL 비교 가중치 앙상블 (2)](https://github.com/user-attachments/assets/08d72344-4786-457a-bf44-403a849617fc)

<img width="2151" height="1183" alt="output" src="https://github.com/user-attachments/assets/d9d93258-2495-4da7-91f9-a4a33de28332" />

* 위 빨간 대각선은 실제 RUL 이고 RUL 클리핑에 의해 수평으로 예측 되다가 대각선에 밀착하는 형태를 볼수있다.    
그래프만 보면 가중치 앙상블이 점수가 좋을것 같지만 late prediction 감점이 큰 nasa score 특성 때문에 svr의 점수가 더 좋다.


* 아래가 모델별 late prediction의 비율을 볼수 있는 자료로 빨간 영역이 late prediction 이다.






## AI 모델 개발 15회차 1차 팀프로젝트 - NASA Turbofan Jet Engine Data Set 터보엔진 유지보전 문제_FD002

**[데이터 셋의 특징]**

* **다변량 시계열**: 21개의 센서 데이터와 3개의 운전 설정값이 기록되어 있습니다.
* **복합 운전 조건**: FD001과 달리 6가지의 다른 환경 조건이 섞여 있어, 센서 값이 환경에 따라 크게 요동칩니다.

> **FD002 (Train: train_FD002.txt / Test: test_FD002.txt / RUL: RUL_FD002.txt)**
> * 학습 엔진 수: 260개
> * 테스트 엔진 수: 259개
> * 운전 조건 (Conditions): **6가지 (다양한 고도, 속도, 부하 조건)**
> * 고장 모드 (Fault Modes): 1가지 (HPC 열화)

**[FD-002 문제해결 핵심 전략]**

1. **데이터 정규화 (Z-Score/Min-Max)**:
* 6가지 운전 조건에 따라 센서 데이터의 스케일이 다르므로, 이를 보정하기 위한 정규화 과정이 필수적입니다.

2. **노이즈 제거 및 스무딩**:
* FD001과 동일하게 **Savitzky-Golay 필터** 및 **EMA(지수이동평균)**를 사용하여 센서 데이터의 급격한 변동(노이즈)을 완화합니다.

3. **모델 최적화 (Optuna & Custom Loss)**:
* **XGBoost, LightGBM** 등 머신러닝 모델을 사용하며, **NASA Scoring 방식**에 최적화되도록 커스텀 목적 함수(Custom Objective Function)를 적용하여 학습합니다.

4. **유닛별 NASA Score 기여도 계산**:
* NASA Score 악화의 원인이 일부 긴 RUL을 갖는 소수의 장수 엔진이 원인이라는 것을 확인.
```PS
errors = test_df['pred'].values - y_test
specific_nasa_scores = []
for e in errors:
    s = np.exp(e/13)-1 if e < 0 else np.exp(e/10)-1
    specific_nasa_scores.append(s)

test_df['nasa_penalty'] = specific_nasa_scores
print(test_df.sort_values(by='nasa_penalty', ascending=False).head(10))
```
![NASA Score 기여도 계산.png](https://cdn.discordapp.com/attachments/388576721634590720/1471498168024699043/image.png?ex=698f26f6&is=698dd576&hm=f501cb3e426847e83cd7609898e0af01ccc7b430a3afc7194534f393bc96000d&)

* **운전 조건별 분리 처리**: 단순히 데이터를 합쳐 학습했을 때보다, 운전 조건(6개)을 식별하여 특징(Feature)에 반영했을 때 예측 성능이 향상됨을 확인했습니다.
* **하이퍼파라미터 튜닝**: 데이터 양이 FD001보다 많으므로(엔진 260개), 과적합을 방지하기 위해 더 정교한 교차 검증(GroupShuffleSplit)과 Optuna를 통한 파라미터 최적화를 수행했습니다.

**[목표 점수]**

![FD-002 점수 표.png](https://cdn.discordapp.com/attachments/1451496750023049256/1470417377551450134/image.png?ex=698e8425&is=698d32a5&hm=e4b18ce31530a3362a1dd85e15096c16536479edca437f59799f4fd9c6c85cbb&)

**[시행착오 및 개선 사항]**

[시행착오 내용]
1. 초기에 FD-001 노트북 베이스로 작업 시작
2. FD-002는 동일 운전 조건이 아니라서 고도, 속도가 바뀌어 모델이 고장 진행에 대한 센서값의 추세를 읽을수 없음.
따라서 아래와 같은 전처리를 진행함.

[전처리]
1) 운전조건에 따라 클러스터링

<img width="450" height="340" alt="클러스터링 이미지" src="https://github.com/user-attachments/assets/72b099a5-1c90-4715-93c8-7526d0ab66f4" />

2) 각 클러스터별로 정규화 (k-means 방식,하드 클러스터링)
3) z-score가 ±3을 벗어나는 이상치를 clipping 한다
4) 노이즈 제거함수 add_advanced_features를 이용해 스무딩을 하고 EMA를 생성한다.
5) 정규화된 데이터를 다시 합쳐 모델에 넣는다.

3. 그런데 정규화 이후 노이즈 제거 과정에서 파생된 컬럼이 너무 많아 히트맵 가독성이 떨어지고 EDA나 feature selection 과정이 번거로워졌다. 따라서 테스트 데이터 생성 전으로 이동
4. farB[-] 산포도에서 특정 클러스터만 두 가지 상수 값을 같는 이봉 분포 현상을 발견 (특정 고도등의 조건으로 작동하는 전자식 밸브 또는 이상 계측값이 원인)    
이로 인해 파생 컬럼인  W15, W24, W2, Wa36 에도 직선형이 혼재

![FD_002_운전 조건으로만 클러스터링 결과 (2)](https://github.com/user-attachments/assets/ff30fd9c-eec7-453e-b97a-54adb2dca9db)

5. 이를 클러스터 안에 세부 정규화 조건인 mode_id 를 추가 해 정규화 과정에서 한 상수값을 제거. 또한, 모델이 학습할때 어느 클러스터인지 알 수 있게 'cluster' 컬럼을 onehot encoding으로 추가한다.
6. 머신러닝 모델 학습 결과 에측 결과가 rul 직선 그래프를 전혀 따라가지 않음.
7. rul clipping이 데이터 학스에 사용되는 데이터프레임이 아니라 원본 데이터프레임에 적용된 것을 확인. 이를 수정
8. 일부 엔진에서는 길이가 20보다 짧은 데이터가 있다고 하여 잘못된 예측이 원인이 될 수 있어 기존 rolling window size 5,20 중 20 삭제, EMA는 span을 20에서 10으로 축소
9. svr애서만 런닝 시간이 20분 넘게 소요. svr의 coach number를 ram 20gb인 20000까지 할당 그러나 해결 되지 않아 svr 대신 Nystroem 근사 + Ridge 조합 사용
10. rul clipping 의 cv 최적치 계산 기준을 nasa score로 변경, 노이즈 제거 함수에 최근 5사이클 열화 속도 학습 내용 추가.
11. 그러나 30000점대 나쁜 결과
12. 초기에는 노이즈 제거를 위해 필터를 썼으나, FD002의 복합 조건에서는 오히려 고장 징후를 뭉개버리는 결과를 초래해 최종적으로 제거함.
13. 특정 운전 조건 내에서의 평균 센서값을 구한 뒤, 현재 측정값 - 조건별 평균값의 절대값을 새로운 컬럼으로 생성.
14. Low-Variance Drop 방식을 도입해 모든 센서 데이터에 대해 분산을 계산하고, 값이 아예 변하지 않는 변수나, 변화량이 너무 적어 정보로서 가치가 없는 변수를 자동으로 찾아내고, 기준치 미달(0.01)인 변수들을 일괄 삭제.
15. Safe Margin 적용: NASA Score의 특성(Late Prediction 페널티)을 고려하여 예측값에 일정한 마진을 두어 안정적인 점수 확보.
16. 최종 모델: K-Fold 앙상블과 Optuna, AutoGluon을 통해 단일 모델 대비 Score를 개선.

![FD-002 점수 표.png](https://cdn.discordapp.com/attachments/388576721634590720/1471499295021731882/image.png?ex=698f2803&is=698dd683&hm=2f003254024fdb3939aee05f7f8f5cc3b07eb809d609fbb575e1492d2c6843dc&)
    
![FD-002 점수 표.png](https://cdn.discordapp.com/attachments/388576721634590720/1471498825725251731/image.png?ex=698f2793&is=698dd613&hm=6bfbed584b8b0cdad35980fc686dce1dd78185077960a86dcf8a01a1791c40f9&)



## AI 모델 개발 15회차 1차 팀프로젝트 - NASA Turbofan Jet Engine Data Set 터보엔진 유지보전 문제_FD002-딥러닝

**1.초기[CNN + LSTM + Attention 구조로 시계열 패턴 학습]** 

**-Conv1D:** 짧은 구간 센서 변화(패턴/노이즈) 포착

<img width="505" height="73" alt="1  초기-Conv1D" src="https://github.com/user-attachments/assets/7625a004-1e8a-4f8f-afe3-2bb82bba1756" />

**-BiLSTM** : 시간 흐름(열화 진행)을 학습

<img width="545" height="85" alt="1  초기-BiLSTM " src="https://github.com/user-attachments/assets/e0cb04a6-740d-4dac-891a-0632b47bd30e" />

**-Attention** : 중요한 시점(특히 고장 직전)을 강조

<img width="533" height="102" alt="1  초기-Attention " src="https://github.com/user-attachments/assets/a54f9802-db18-491a-a74a-b3a708441b1c" />

**-GAP + Dense :** 전체 시퀀스를 요약해서 RUL로 회귀

<img width="379" height="212" alt="1  초기-GAP + Dense" src="https://github.com/user-attachments/assets/3fc2c72e-f5fb-4d90-8cd0-a34d6ed970dd" />

**● 결론**: 이 구조는 RMSE/MAE 개선엔 강하지만 NASA 스코어 기준으로 폭탄을 제어하는 장치가 없어서 딥러닝 모델로 평균 RUL 예측을 만들었지만 NASA 점수는 폭탄 엔진 때문에 매우 높았다.

**NASA Score:** 수만~수백만


**2. 중기[NASA 비대칭(Asymmetric) + 가중 Loss 도입]** 

**- NASA 비대칭 Loss :** NASA는 over를 더 싫어한다는 규칙을 딥러닝 loss에 직접 주입한 순간, 점수가 본격적으로 내려가기 시작
over 폭탄을 줄임 → NASA 점수가 크게 내려감 →low RUL 구간의 불안정 예측을 줄임 → 폭탄 unit 감소 → 그래서 ~14,000대까지 내려가는 계기가 됨

<img width="602" height="372" alt="2  중기-NASA 비대칭 Loss" src="https://github.com/user-attachments/assets/fbde8266-5e79-42c2-86f2-dd1ca13b4f51" />

**- Multi-seed 앙상블(폭탄 유닛 줄이기) :** seed마다 “폭탄 유닛이 생기는 위치”가 달라지는 경향이 있음, 앙상블은 이를 평균내서 극단 오차를 줄임

 <img width="418" height="513" alt="2  중기-Multi-seed 앙상블(폭탄 유닛 줄이기)" src="https://github.com/user-attachments/assets/72d0510f-1159-4518-90af-8fd2a9f5eeb2" />

**• 결론 :** NASA는 over에 더 가혹 → loss에서 over를 더 강하게 벌주기 시작 결과적으로 “폭탄 엔진의 over/under 극단”이 줄어듦 NASA의 비대칭 구조(특히 over 벌점)를 loss에 반영하고 앙상블로 분산을 줄여 14,000대까지 낮췄다.

**NASA Score:** 수만 → 14,000점대



**3. 후기[위험 센서 억제(감쇠/드랍), TOP-10 엔진 분석, 후처리 (squash/piecewise), unit-last robust 집계(median_lastk]**

**• 모델CNN/LSTM(+Attention) 구조 유지/개선**
**1. Loss는 동일**
**2. CNN :** 센서 데이터의 “짧은 구간 패턴(국소 변화)” 추출

<img width="494" height="328" alt="3  후기-CNN, LSTM(Attention) 구조 유지,개선" src="https://github.com/user-attachments/assets/96f9097c-6081-4091-96ad-acd678b739ce" />

**3. LSTM :** 시간 흐름(열화 진행)을 학습

<img width="288" height="65" alt="3  후기-LSTM(열화 진행의 시간 흐름 학습) 코드" src="https://github.com/user-attachments/assets/ddabecdc-db7c-4478-ba93-9e7ec64d659b" />

**4. Attention(MultiHeadAttention):** “어떤 시점이 중요한지” 자동으로 강조(특히 고장 직전 구간)고장 직전 예측 흔들림이 줄어듦

<img width="433" height="65" alt="3  후기-Attention(MultiHeadAttention)" src="https://github.com/user-attachments/assets/d04a968b-f5fc-4728-80e2-d3bf7f474f48" />

**• 핵심 후처리:**

**1. 위험 센서 억제(감쇠/드랍) :** FD002는 운영조건별 센서 분포가 달라서, op_cluster별 정규화로 조건발 튐을 눌렀다.

<img width="713" height="381" alt="3  후기-위험 센서 억제(op_cluster 기반 정규화로 감쇠)" src="https://github.com/user-attachments/assets/368ea584-166c-4b54-b8f8-bc74b5448568" />

**2. TOP-10 엔진 분석 :** NASA는 최악 몇 개 엔진이 점수 대부분을 차지해서, penalty 상위 엔진을 먼저 찾았다.

<img width="840" height="140" alt="3  후기-TOP-10 엔진 분석" src="https://github.com/user-attachments/assets/ec4b836f-3aa9-404b-9d67-258b1fdeb1e5" />

**3. 후처리(squash/piecewise) :** 과대예측 꼬리를 눌러 over 지수벌점을 줄여 TOP-10 폭탄을 꺾었다.

<img width="595" height="348" alt="3  후기-후처리(squash, piecewise)" src="https://github.com/user-attachments/assets/5a97ccd6-ba67-459b-b214-54e03a47aa70" />

**4. unit-last robust 집계(median_lastk) :** 마지막 1개가 아니라 last-k의 median으로 이상치를 줄여 폭탄 엔진을 안정화했다.

<img width="773" height="280" alt="3  후기-unit-last robust 집계(median_lastk)" src="https://github.com/user-attachments/assets/d5cc1060-0f08-4a30-abf5-45ca6d66a103" />


**● 결론 :** 모델이 NASA 친화적이 되면서 평균적으로 좋아짐 (14k → 7k)

**NASA Score :** 약 14,000 → 10,000 → 7,000대



**4. 현재**

**1) 운영조건(op_cluster) 별 스케일링을 “train과 test 모두”에 적용 :** op_cluster별 스케일링으로 “조건발 센서 튐”을 줄였고

<img width="581" height="291" alt="4  현재-운영조건(op_cluster) 별 스케일링을 train, test 모두에 적용" src="https://github.com/user-attachments/assets/953004f1-9d74-4847-b96f-5847464c7dc6" />

**2) unit-last를 “마지막 1개”가 아니라 최근 K개(last-k) median으로 바꿈 :** unit-last를 last-k median으로 바꿔 “마지막 구간 이상치”를 제거했고

<img width="631" height="203" alt="4  현재-unit-last를 “마지막 1개”가 아니라 최근 K개(last-k) median으로 변경" src="https://github.com/user-attachments/assets/c77d3e7d-f426-4af4-9c6f-2c9fefb46dfe" />

**3) squash/piecewise를 “감으로”가 아니라 (th, gamma) 탐색으로 최적화 :** squash를 탐색 최적화해서 “꼬리 폭탄”을 직접 눌렀다

<img width="598" height="283" alt="4  현재-squash, piecewise를 “감으로”가 아니라 (th, gamma) 탐색으로 최적화" src="https://github.com/user-attachments/assets/5a2d51f3-4725-4ec1-984c-0595efe5ac67" />



**● 결론**: TOP-10 폭탄 엔진을 직접 겨냥해, 조건별 정규화 + median_lastk + squash 최적화로 꼬리를 제거함” (7k → 5k)

**NASA Score** : 약 5,000점대

<img width="173" height="73" alt="딥러닝 점수" src="https://github.com/user-attachments/assets/fe7bcd8b-8b0d-40a0-81c2-70e099ec75bf" />



**(결론)**
현재 단계의 성과는 모델 복잡화가 아니라, 조건별 스케일링 + last-k median + squash 최적화로 NASA 점수를 터뜨리는 ‘꼬리’를 체계적으로 제거한 결과다.

<img width="740" height="170" alt="머신러닝 한계" src="https://github.com/user-attachments/assets/a9ebbbc3-49d4-479c-a348-98468a9d81c3" />











