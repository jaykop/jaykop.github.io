---
title: "[Unreal] Motion Matching 개요"
classes: wide
categories:
  - unreal
  - character
sidebar:
  nav: "main"
author_profile: true
---

## Motion Matching 개념
* 현재 캐릭터의 동작과 상태를 기준으로, 가장 적절한 다음 동작을 선택하는 로직
  * ABP의 StateMachine과 BlendSpace를 대체 가능
  * 자연스러운 Blend를 위한 작업 Cost 감소
* 여러 상황에 대응되는 애니메이션 에셋이 여러 개 있고, 테이블이 이 애니메이션을 리스트로 들고 있다
  * 이 애니메이션 리스트 중에, 조건에 맞는 애니메이션을 하나 선택해 출력하는 것이다

### 작동 원리

|에셋|Prefix|설명|
|:---:|:---:|:---|
|Anim Blueprint|ABP|모션매칭 노드 세팅|
|Chooser Table|CHT|PSD 로 채워진 테이블|
|Pose Search Database|PSD|선택될 애니메이션 목록|

![post_thumbnail](/assets/images/MotionMatching/01.png)

**!. 캐릭터 상태 전달**

![post_thumbnail](/assets/images/MotionMatching/02.png)

* ABP가 CHT로 정보를 전달한다
  * Gait, Speed, MovementMode, IsMoving, IsStarting, ...

**2. 조건에 맞는 PSD 선택**

![post_thumbnail](/assets/images/MotionMatching/03.png)

* ABP에서 전달된 정보를 기준으로 적절한 PSD를 선택한다

**3. 조건에 맞는 동작 찾기**

![post_thumbnail](/assets/images/MotionMatching/04.png)

* PSD는 여러 애니메이션을 프레임 단위로 나눠, 각 프레임의 포즈 정보를 추출해 저장한 데이터이다
  * 현재 캐릭터의 상태에서 다음 동작으로 이어질 가장 적절한 포즈를 여기서 찾는다

### Pose Search Schema  
* PSD에서 포즈를 선택할 때 비교 및 검색하는 기준을 정의  

> [!NOTE] Channel  
> 여러 Feature들의 묶음  
> 포즈를 비교하는 묶음 단위  
> Trajectory Channel, Position Channel 등

> [!NOTE] Feature  
> 포즈를 비교하는 개별 단위  
> Bone, Origin Bone, Weight 등  

|주요 Feature|설명|
|:---|:---|
|Default with Root Bone|Origin 본이 비어 있을 때, Root 본을 기준으로 적용|
|Bone|위치를 비교할 대상 본 <br/>‘Origin Bone’ 기준으로 해당 본의 상대 위치 계산|
|Sample Role|다중 캐릭터 애니메이션에서, 어떤 캐릭터의 포즈를 참조할지 여부<br/>None → 단일 캐릭터 기준<br/>Primary → 주된 캐릭터 기준<br/>Secondary → 보조 캐릭터 기준|
|Origin Bone|기준이 되는 본<br/>해당 본 기준으로 ‘Bone’의 상대 위치 계산|
|Origin Role|다중 캐릭터 애니메이션에서, 어떤 캐릭터의 포즈를 참조할지 여부<br/>None → 단일 캐릭터 기준<br/>Primary → 주된 캐릭터 기준<br/>Secondary → 보조 캐릭터 기준|
|Weight|유사도 계산 시 곱해지는 가중치|
|Sampling Attribute Id|샘플링 시 특정 Attribute (ex. Jump 상태) 만 추출할 때 사용<br/>-1 : 특정 Attribute 제한 없음|
|Sample Time Offset|‘Bone’ 위치를 참조할 때, 현재 프레임 몇 초 뒤/앞 위치 참조<br/>0 : 현재 프레임 위치 참조|
|Origin Time Offset|Origin Bone’ 위치를 참조할 때, 현재 프레임 몇 초 뒤/앞 위치 참조<br/>0 : 현재 프레임 위치 참조|
|Input Query Pose|런타임 중 어떤 포즈를 기준으로 사용할지 여부<br/>Use Continuing Pose : 현재 재생 중인 애니메이션의 계속 된 포즈<br/>Use Character Pose : 캐릭터의 현재 포즈<br/>Use Interpolated Continuing Pose : 이전 프레임 포즈와 현재 프레임 포즈를 보간하여 사용|
|Component Stripping|특정 축 방향을 무시 (None / Strip XY / Strip Z)|
|Permutation Time Type|시간 기준을 어떤 방식으로 해석할지 |
|Max Position Distance Squared|특정 거리 이상 차이 나는 검색에서 제외<br/>0 : 제한 없음|
|Normalize Displacement|위치 차이를 정규화할지 여부|
|Normalization Group|여러 Feature 를 같은 정규화 그룹으로 묶어서 상대 비교|

* Cost가 가장 낮은 포즈를 선택한다
* Cost = 각 Feature들 간의 거리 x Weight

![post_thumbnail](/assets/images/MotionMatching/05.png)
* foot_r 을 기준으로 foot_l 이 어디에 있는지 판별하고 포즈를 매칭

### 너무 많은 Animation 개수 줄이기

**1. Idle 상태 애니메이션**

|PSD|애니메이션|설|
|:---|:---|:---|
|PSD_Dense_Stand_Idles|Stand_Idle_Loop|Idle 모션|

**2. 기본 이동 애니메이션**

|PSD|애니메이션|설|
|:---|:---|:---|
|PSD_Dense_Stand_Run_Starts|Run_Start_F_Lfoot<br/>Run_Start_F_Rfoot|달리기 시작 모션|
|PSD_Dense_Stand_Run_Loops|Run_Loop_F|달리는 모션|
|PSD_Dense_Stand_Run_Stops|Stand_Idle_Loop|모션|

* 이 때, 출발 방향이 L/R/B 이면 발이 크게 미끄러지는 현상 발생
  * Start_F 애니메이션이 재생

**3. 방향 회전 적용된 이동 애니메이션**

|PSD|애니메이션|설|
|:---|:---|:---|
|PSD_Dense_Stand_Run_Starts|Run_Reface_F_L_090<br/>Run_Reface_F_R_090|F->L, F->R 으로 90도 회전하는 모션|

* F->L / F->R 애니메이션을 추가하면서 출발 시 정면 방향이 아닌 때에도 자연스러움
  * B로 출발할 때도 커버됨
* 다만, 달리는 중 방향 전환 시에도 재생되는 문제

**4. 달리던 중 방향 전환 애니메이션**

|PSD|애니메이션|설|
|:---|:---|:---|
|PSD_Dense_Stand_Run_Pivots|Run_Turn_L_090_Lfoot<br/>Run_Turn_L_090_Rfoot<br/>Run_Turn_R_090_Lfoot<br/>Run_Turn_R_090_Rfoot|달리다가 L/R로 90도 방향 전환 모션|

* 3에서 발생하던, 달리던 중 방향 전환 시에 발을 짧게 디디는 현상 수정
* 180도 회전 상황에서는 굳이 측면을 도드라지게 바라보며 회전하는 현상
  * 이것 자체는 어색하지 않다고 생각하는데...

**5. 큰 방향 회전 적용된 이동 애니메이션**

|PSD|애니메이션|설|
|:---|:---|:---|
|PSD_Dense_Stand_Run_SpinTransition|Run_Reface_Start_F_L_180<br/>Run_Reface_Start_F_R_180|F->B 로 180도 회전 모션 시계/반시계 방향으로 회전|

* 4에서 기존 방향과 반대로 급커브시 조금 더 자연스럽게 방향 전환
* 특정 모션 재생이 끝나기 전 빠르게 방향을 전환하는 경우, 문워크하는 현상은 여전히 발생
  * 일정 시간 동안 방향 전환을 막는 버퍼 시간을 추가하거나, 전용 애니메이션 추가 필요

**6. 속도 변경**

|PSD|애니메이션|설|
|:---|:---|:---|
|PSD_Dense_Stand_Run_Starts|Walk_Start_F_Lfoot<br/>Walk_Start_F_Rfoot|걷기 시작 모션|
|PSD_Dense_Stand_Run_Loops|Walk_Loop_F|걷는 모션|
|PSD_Dense_Stand_Run_Stops|Walk_Stop_F_Lfoot<br/>Walk_Stop_F_Rfoot|걷다가 멈추는 모션|

* 뛰다가 걷는 속도로 변경 시, 걷는 속도에 맞는 모션 추가 필요
  * CHT에 Walking 상태에 대해 만들고, 걷기 애니메이션 전용 PSD를 한 세트 추가

##
* <https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-matching-in-unreal-engine#%EC%83%98%ED%94%8C%EC%BD%98%ED%85%90%EC%B8%A0>