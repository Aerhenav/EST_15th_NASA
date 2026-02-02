===========================================================================
NASA C-MAPSS 터보팬 엔진 열화 시뮬레이션 데이터셋 (README 한글 번역)
===========================================================================

[데이터셋 개요]
이 데이터셋은 NASA의 C-MAPSS(Commercial Modular Aero-Propulsion System Simulation)
시뮬레이터를 사용하여 생성된 터보팬 엔진의 열화(Degradation) 데이터입니다.

데이터는 여러 개의 다변량 시계열(Multivariate Time Series)로 구성되어 있습니다.
데이터셋은 학습(Training) 세트와 테스트(Test) 세트로 나뉩니다.
각 시계열 데이터는 서로 다른 엔진(Unit)에서 얻은 데이터이며, 동일한 유형의 엔진들로 간주할 수 있습니다.

[실험 시나리오]
1. 초기 상태: 각 엔진은 정상 상태에서 작동을 시작합니다.
   - 단, 사용자에게는 알려지지 않은 수준의 초기 마모(Initial Wear)와 제조 공차(Variation)가 존재합니다.
     (이는 결함이 아닌 정상적인 범주입니다.)
2. 고장 진행: 어느 시점부터 결함(Fault)이 발생하여 시간이 지날수록 상태가 악화됩니다.
3. 데이터 범위:
   - 학습 세트 (Train): 결함 발생부터 시스템 고장(Failure) 시점까지의 모든 데이터가 포함됩니다.
   - 테스트 세트 (Test): 고장 발생 전 임의의 시점에서 데이터 기록이 중단됩니다.

[목표 (Objective)]
테스트 세트에 포함된 각 엔진의 **잔여 유효 수명(RUL: Remaining Useful Life)**을 예측하는 것입니다.
즉, 테스트 데이터가 끊긴 시점으로부터 엔진이 고장 날 때까지 몇 사이클(Cycle)이 더 남았는지 맞히는 것이 목표입니다.

---------------------------------------------------------------------------
[파일 구성 및 형식]
데이터는 공백으로 구분된 텍스트 파일로 제공되며, 총 26개의 열(Column)로 구성됩니다.
각 행(Row)은 한 번의 운전 사이클 동안 수집된 데이터 스냅샷을 의미합니다.

* 열(Column) 순서 및 의미:
  1.  Unit Number (유닛 번호): 엔진 고유 ID (1, 2, 3...)
  2.  Time in Cycles (시간): 비행 사이클 수
  3.  Operational Setting 1 (운전 설정 1): 고도 등 운전 조건
  4.  Operational Setting 2 (운전 설정 2): 마하수 등 운전 조건
  5.  Operational Setting 3 (운전 설정 3): 스로틀 등 운전 조건
  6.  Sensor Measurement  1 (센서 1)
  7.  Sensor Measurement  2 (센서 2)
  ...
  26. Sensor Measurement 21 (센서 21)

---------------------------------------------------------------------------
[데이터셋 상세 설명 (FD001 ~ FD004)]

1. FD001 (Train: train_FD001.txt / Test: test_FD001.txt / RUL: RUL_FD001.txt)
   - 학습 엔진 수: 100개
   - 테스트 엔진 수: 100개
   - 운전 조건 (Conditions): 1가지 (해수면 - Sea Level)
   - 고장 모드 (Fault Modes): 1가지 (HPC 열화 - HPC Degradation)

2. FD002 (Train: train_FD002.txt / Test: test_FD002.txt / RUL: RUL_FD002.txt)
   - 학습 엔진 수: 260개
   - 테스트 엔진 수: 259개
   - 운전 조건 (Conditions): 6가지 (다양한 고도, 속도, 부하 조건)
   - 고장 모드 (Fault Modes): 1가지 (HPC 열화)

3. FD003 (Train: train_FD003.txt / Test: test_FD003.txt / RUL: RUL_FD003.txt)
   - 학습 엔진 수: 100개
   - 테스트 엔진 수: 100개
   - 운전 조건 (Conditions): 1가지 (해수면)
   - 고장 모드 (Fault Modes): 2가지 (HPC 열화 및 Fan 열화)

4. FD004 (Train: train_FD004.txt / Test: test_FD004.txt / RUL: RUL_FD004.txt)
   - 학습 엔진 수: 248개
   - 테스트 엔진 수: 248개
   - 운전 조건 (Conditions): 6가지
   - 고장 모드 (Fault Modes): 2가지 (HPC 열화 및 Fan 열화)

---------------------------------------------------------------------------
[참고 사항]
* RUL_FDxxx.txt 파일에는 테스트 세트 각 엔진의 실제 정답 RUL 값이 들어 있습니다.
* 모델 성능 평가는 예측된 RUL과 실제 RUL의 오차를 기반으로 수행됩니다.