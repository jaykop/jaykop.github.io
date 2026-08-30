---
title: "[DevNote] 카메라 락온 시 타겟 과한 추적 Troubleshooting"
classes: wide
categories:
  - unreal
  - camera
sidebar:
  nav: "main"
author_profile: true
---

## 하드락 카메라
* 액션 게임에서 특정 적을 대상으로 락온을 걸 수 있다
* 이 때 카메라는 대상을 계속 추적한다

### 이슈 상황
* 타겟의 락온 위치, 그러니까 추적 위치는 ActorLocation 혹은 특정 소켓이다
* 특정 소켓을 추적하는 경우, 대상 캐릭터가 애니메이션을 재생하면서 불필요한 소켓의 위치 이동까지 추적한다
	* 특히 Idle 애니메이션 재생 시, 대부분의 소켓 위치가 위 아래로 움직이는 사소한 차이에도 카메라 추적이 발생해 불쾌감을 준다

### 1. ActorLocation을 사용한다면?
* 이 경우, 소켓을 추적하는 게 아니기 때문에 불필요한 소켓의 움직임을 추적하지 않는다
* 그러나 대상 캐릭터가 쓰러지는 등 SkeletalMesh가 애니메이션으로 인해 ActorLocation과 과하게 다른 위치로 이동하면 위화감이 발생한다
* 하나의 캐릭터에 여러 개의 락온 포인트가 있는 경우에도 대응하기 어렵다
  * 거대 몬스터의 양 팔에 락온 포인트가 있다면...?

### 2. 락온 포인트의 키를 애니메이션 단계에서 잡아준다면?
* 가장 이상적인 방법이다
* 락온 포인트 전용 소켓을 캐릭터 스켈레톤에 정의하고, 애니메이션에서 직접 이 소켓의 움직임을 키로 잡는다면 모든 상황에 대응이 가능하다
* 하지만 **모든 상황에 대응해야 한다**. 즉, 공수가 많이 든다
* 이 기능을 고려하지 않고 이미 애니메이션 에셋이 제작된 상황이라면 더욱 힘들다

### Deadzone 적용

```c++
//...

// RotationToTarget - 하드락인 경우 카메라가 바라봐야 할 방향
// ControlRotation - 플레이어 카메라가 실제로 바라보고 있는 방향
// 둘의 차를 구한다
const FRotator DeltaRotator {
  FMath::Abs(FMath::UnwindDegrees(RotationToTarget.Pitch - ControlRotation.Pitch)),
  FMath::Abs(FMath::UnwindDegrees(RotationToTarget.Yaw - ControlRotation.Yaw)),
  FMath::Abs(FMath::UnwindDegrees(RotationToTarget.Roll - ControlRotation.Roll)),
};

// TargetRotation 초기화
// 즉, 카메라가 타겟을 향해 바라봐야 하는지 여부
// 락온을 걸지 않은 상태에서 최초 락온을 걸었을 때 타이밍을 잡기 위한 플래그
if (CameraBuffer.bInitTargetRotation)
{
  CameraBuffer.TargetRotation = RotationToTarget;
  CameraBuffer.bInitTargetRotation = false;
}
else
{
  // ...

  // DeltaRotator의 Pitch가 Tolerance 즉 임계값을 넘었거나, 
  // 계속 타겟을 추적 중인지 플래그 확인
  if (DeltaRotator.Pitch > HardlockData.PitchSleepTorlerance || CameraBuffer.bTraceTargetPitch)
  {
    // Pitch에 대해서만 업데이트하여 Pitch 값은 타겟을 추적하도록 허용
    CameraBuffer.TargetRotation.Pitch = RotationToTarget.Pitch;

    // PitchSleepTolerance와 SafePitchTolerance의 비교가 합당하지 않으면 실제로 추적을 하지 않는다
    // SafePitchTolerance - 추적을 완료했다고 판단하는 Pitch 값
    // PitchSleepTolerance - 이 수치보다 높으면 카메라가 타겟 추적을 시작
    // 즉, 필수적으로 SafePitchTolerance의 값은 PitchSleepTolerance보다 작아야 한다 (ensure로 처리하는 게 좋았을 듯)
    const bool bValidPitchComparizon = HardlockData.PitchSleepTolerance > HardlockData.SafePitchTolerance;

    // Delta가 SafeAngularTolerance 미만인지 확인
    // 즉, Pitch 추적이 "완료"되지 않았다면 계속 추적
    CameraBuffer.bTraceTargetPitch = DeltaRotator.Pitch > HardLockData.SafePitchTolerance && bValidPitchComparison;

    // ...
    // Yaw에 대해서도 동일한 처리가 필요하다면 위의 코드와 똑같이 처리해준다

    // 더 이상 추적하지 않아도 된다면
    if (CameraBuffer.bTraceTargetPitch == false)
    {
      // 추적을 종료되면 플래그 초기화
      CameraBuffer.bInitRotationSpeed = true;
    }
  }
}

// 최총 TargetRotation 할당
TargetRotation = CameraBuffer.TargetRotation;
```

* 카메라가 특정 소켓을 추적하기 위한 임계값과 완료했다고 판단하는 기준값을 정의하고, 소켓의 위치가 매 프레임 그 기준을 충족하는지 확인한다
  * 만약 기준 범위를 벗어나면 추적을 시작한다
* 이 방법으로 특정 범위 내로 Socket이 움직이는 경우, 카메라의 불필요한 추적을 막을 수 있었다
  * 다만 가장 자연스러운 Magic Number를 찾는 것은 기획자의 몫...
  * 가장 이상적인 방법은 역시 애니메이션 제작 단계에서 카메라 락온 소켓의 키를 잡는 게 아닐까 한다
* 위의 코드에서는 World Position을 기준으로 범위를 체크하지만, Socket Location을 Screen Projection해서 Screen 상의 Position을 기준으로 체크하는 것도 좋을 거 같다
