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

   - 컬럼 라벨링 및 파생 컬럼 생성
      1. op_setting_1, sensor_1 등의 컬럼 명이 아닌 실제 센서 내용을 알수있는 컬럼 명으로 라벨링
      2. 공기 유동 비율, 압력 비 등의 비율 파생 컬럼을 만들어 무차원수가 되어 온도나 압력등의 외부 요인의 영향을 제거한다. 현상을 해석하기 쉬워진다.

   - RUL Clipping
      1. 이 문제의 핵심 전처리 전략이다.
      2. 엔진은 서서히 고장나는게 아니라 특정 시점부터 급격히 나빠지는 특징이 있고 이후 시각화 그래프에서도 확인이 가능하다.
      3. 초기 건강한 사이클의 경우 센서값은 일정한데 RUL(남은 수명)이 줄어 들어 센서와 RUL의 관게에 대해 모델이 혼란을 겪게 된다.
      4. 실제 RUL보다 더 큰 RUL을 모델이 예측하게 되면 late prediction으로 인해 nasa score가 매우 나빠지는데 clipping으로 한계점을 만들어줄수 있습니다.
         
            1) 고정 클리핑 (Fixed Clipping)
               
                  - 설명: 경험적 수치인 120~130으로 RUL 상한선을 제한 (Heimes et al. 2008 우승 논문 기준 125~130 사용)
                  - 
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

   - GroupShuffleSplit
      1. 이 데이터 셋은 시계열 데이터이기 때문에 data leakage를 방지하기 위해 Train_test_split 대신 GroupShuffleSplit을 사용한다.

   - Safe margin 
      1. nasa score는 late prediction에 큰 감점을 매기기 때문에 예측 값에 마이너스 수치를 반영해 이를 예방하는 safe margin을 사용한다. 

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
