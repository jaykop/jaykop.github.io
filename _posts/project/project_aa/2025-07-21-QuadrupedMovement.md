---
title: "[DevNote] 4족 Movement"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## Biped Movement
* 직립 2족 보행 플러그인은 ALS plugin으로 디테일을 표현할 수 있다
* Unreal에서 공식적으로 지원하는 [Motion Matching](https://dev.epicgames.com/documentation/ko-kr/unreal-engine/motion-matching-in-unreal-engine) 플러그인도 있다
* 그렇다면 4족 보행은?

## Quadruped Movement
* 빠른 방향 전환 시, 몸을 비틀며 자연스럽게 도는 모션을 만들어 줘야 했다
* 하지만 Unreal에서의 Character는 Character Capsule 1개에 대해 SkeletalMesh 1개가 대응하는 구조
  * 다른 게임에서 상반신과 하반신을 나눠서 작업하기에는 너무 많은 코스트

### Solution?
1. **캐릭터의 Forward 기준으로 Yaw가 일정 각도 이상으로 회전해야 하는 경우, Path point를 만든다**
* 이 경우, MoveTo 작동 방식에 착안해 Custom BT Task ndoe를 만들어 작업
* 최종 목적지까지 몇 개의 waypoint를 추가해야 자연스러울지가 이슈
  * waypoint에 도착하자마자 다음 waypoint를 향해 방향을 확 틀어서 부자연스러워 보인다
    * 이는 **Catmull-Rom Spline**으로 Waypoint를 만들어주면 해결할 수 있긴 했다
  * 그러나 충분히 짧은 거리에 충분히 많은 waypoint를 만들어줘야 하는데, 이걸 정의하기 애매했다

2. **캐릭터의 Rotation Rate를 조절해 한 프레임에 회전할 수 있는 최대 회전각도를 낮춘다**
* 이 경우에는 위의 작업보다 work load가 더 적다
  * 생각보다 결과물도 자연스럽다
* 단, 목적지에 도착할 수 없는 경우가 있다
  * 이동 속도와 지향 방향은 기존과 동일한데 그만큼 Rotation Rate가 빠르지 않기 때문에, 목적지 주변을 맴돌기만하는 버그가 발생할 수 있다
* 그래서 빠른 회전이 필요한 경우만 한정에 Rotation Rate를 조절해주거나, 전용 애니메이션을 재생해 캐릭터를 빠르게 회전시켜주어야 했다

```c++
// 특정 방향 MoveInput으로 이동 Request를 받는다
void UCustomCharacterMovementComponent::RequestPathMove(const FVector& MoveInput)
{
  if(IsValid(GetOwner()) == false)
  {
    return;
  }

  // 4족인 경우에만 진행
  if (bQuadrupedMovement == false)
  {
    Super::RequestPathMove(MoveInput);
    return;
  }
  
  FVector AdjustedMoveInput(MoveInput);
  const FVector Forward = GetOwner()->GetActorForwardVector();
  const FVector Right = GetOwner()->GetActorRightVector();
  const FVector2d Right2D { Right.X, Right.Y };
  const FVector2D Forward2D { Forward.X, Forward.Y };
  FVector2D MoveInput2D { MoveInput.X, MoveInput.Y };
  MoveInput2D.Normalize();
  
  const double DotDirectionMoveInput = FVector2d::DotProduct(bMoveBackward ? -Forward2D : Forward2D, MoveInput2D);
  // 현재 바라보는 방향(혹은 후면 방향)과 이동 입력의 각도 차이가 11.5도(Acos(0.98)) 이내이면 같은 방향으로 간주
  constexpr double MINIMUM_DOT = 0.98;
  if(DotDirectionMoveInput > MINIMUM_DOT && bMoveBackward
    || DotDirectionMoveInput < MINIMUM_DOT && bMoveBackward == false)
  {
    verify(RotationRate.Yaw > UE_KINDA_SMALL_NUMBER);
    check(GetWorld());
    const float DeltaSeconds = GetWorld()->GetDeltaSeconds();

    // 한 프레임 동안 회전할 각도(도 단위)를 계산
    float AngleDeg = DeltaSeconds * RotationRate.Yaw;
    if (bMoveBackward)
    {
      // 뒷걸음질할 때는 회전을 조금 더 빨리 
      constexpr float BACKWARD_ROTATION_MULTIPLIER = 1.5f;
      AngleDeg *= BACKWARD_ROTATION_MULTIPLIER;
    }

    // 좌우 방향 구분
    const double DotRightMoveInput = FVector2d::DotProduct(Right2D,MoveInput2D);
    if (DotRightMoveInput < 0.0f)
    {
      AngleDeg *= -1.0;
    }

    // AngleDeg만큼 돌려준다
    AdjustedMoveInput = bMoveBackward
      ? (-Forward).RotateAngleAxis(AngleDeg, FVector::UpVector)
      : Forward.RotateAngleAxis(AngleDeg, FVector::UpVector);
  }
  
  Super::RequestPathMove(AdjustedMoveInput);
}
```

## 기타 참고
* <https://youtu.be/9Su5es3mL7c>
* <https://youtu.be/Bs046-TWMhA>
