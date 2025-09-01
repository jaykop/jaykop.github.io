---
title: "Animation 최적화 Troubleshooting"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## Update Rate Optimization 이슈

### 문제 상황
* 특정 몬스터에게 하드락을 걸었다
* 몬스터는 이동 시 투명 상태로 전환할 수 있었다
* 투명 상태의 몬스터에게 하드락을 건 경우, 카메라가 뚝뚝 끊기면서 추적하는 현상이 발생했다

### 원인과 해결

![post_thumbnail](/assets/images/Animation/URO.png)

* 몬스터 SkeletalMesh의 옵션 중 Enable Update Rate Optimization 옵션이 켜져 있었다
  * 옵션이 켜져 있으면 Owner가 Animation의 Tick Rate를 결정 (**URO를 활성화**)
  * AnimUpdateRateTick() 구조체로 틱 속도 설정이 가능하다고 한다
* 해당 옵션을 끄니 해결되었다
* 보이지 않는 Mesh에 대해 매번 Tick을 할 필요가 없다고 판단, 이동 시 최적화로 인해 뚝뚝 끊기는 현상이 발생했고, 카메라는 순수하게 이 위치를 추적하면서 발생한 현상이었다

## Level of Detail 이슈

### 문제 상황

![post_thumbnail](/assets/images/Animation/ViewportScalability.png)

* 특정 Viewport Scalability에서 몬스터의 이동 거리가 달라지는 현상
  * 해당 몬스터는 RootMotion이 아닌, 애니메이션에 정의된 커브에 의해 이동
* 몇 번의 테스트 후, View Distance 세팅이 Low인 상황에서만 발생하는 것까지 추적
* 로컬 플레이어가 메시에 얼마나 가까울지에 따라, 메시를 표현할 디테일 수준을 결정한다
  * 가까우면 아주 세밀하고 복잡하게, 멀면 간단하게 표시해도 상관없다

### 원인과 해결
* 해당 캐릭터만 2개 이상으로 LOD 세팅이 되어 있었다
  * LOD 세팅을 별도로 건드리지 않은 캐릭터에서는 발생하지 않았다
* Low에 매칭되는 LOD로 애니메이션 출력 시, 애니메이션에서 정의한 커브대로 이동하지 않는 현상
* Low에 매칭되는 LOD로 애니메이션 출력 시, 애니메이션 Tick 타이밍이 달라져서 발생한 문제
  * 이동량을 정기적으로 여러 번에 걸쳐 업데이트하지 않고, 한 Tick에 몰아서 연산하다보니 AI의 위치가 튀는 이슈
  * Animation Tick 이슈이다보니, 이 역시 URO 옵션을 꺼서 헤결되기는 했다
* URO, LOD, 이동량 연산 로직 등이 엮여 발생한 이슈
  * 근본적으로 이동량 연산 로직에 문제가 있다고 판단해, 담당 프로그래머가 수정 작업 후 해결되었다

## Visibility Based Anim Tick Option

```c++
enum class EVisibilityBasedAnimTickOption : uint8
{
    // 항상 애니메이션 틱 실행 (화면에 보이지 않더라도 항상)
    // **항상 정확한 본 업데이트가 필요한 경우 (ex: 네트워크 리플리케이션, 물리 기반 본 업데이트)**
    // 네트워크 리플리케이션이 필요한 캐릭터는 AlwaysTickPoseAndRefreshBones을 유지해야 한다.
    AlwaysTickPoseAndRefreshBones,		

    // 항상 애니메이션 틱 실행 (포즈 연산은 한다)
    // 그러나 본(뼈대) 업데이트는 안 함
    // **본 업데이트 없이 애니메이션 포즈만 유지해도 되는 경우**
    AlwaysTickPose,						        

    // 일반적인 애니메이션은 화면에 보일 때만 틱 실행
    // 보이지 않을 때는 몽타주(Montage)은 반드시 틱 실행 
    // 네트워크 리플리케이션에서 애니메이션 몽타주(공격, 특수 액션 등)만 유지하고 싶을 때 유용)
    OnlyTickMontagesWhenNotRendered,	

    // 화면에 보일 때만 애니메이션 틱 실행
    // 멀티플레이어나 물리 연산이 필요한 경우 문제 발생 가능
    // **싱글플레이어 게임에서 많은 NPC가 있을 때 최적화용**
    // **보이지 않다가 다시 화면에 나타났을 때 애니메이션 싱크가 맞지 않을 수 있다.**
    OnlyTickPoseWhenRendered,			    

    // 화면에 보일 때만 몽타주(Montage) 틱 실행
    // **특정 이벤트에서만 애니메이션이 필요한 경우 (ex: 카메라에 잡힐 때만 액션 재생)**
    OnlyTickMontagesWhenRendered		  
};
```

### 출처 
* <https://corma642.tistory.com/585>