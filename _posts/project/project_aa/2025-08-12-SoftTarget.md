---
title: "SoftTarget 기능"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## 소프트타겟, 소프트락 개념

* 플레이어 공격 버튼 입력 시, 플레이어 정면을 기준으로 일정 거리 및 각도 내에 적이 있을 때 그 적을 향해 회전 및 다가가면서 공격하는 기능
  * 충분히 가까운 걱리에서 적 캐릭터를 향해 속도와 방향을 준다 (AutoDash 기능)
* 시점 고정은 하지 않고, 캐릭터들의 위치 및 방향에 따라 그때 그때 달라진다는 점에서 하드락과 다르다

## 문제 상황

### 1. 공격 시 계속 적 캐릭터에 붙어서 비비는 현상
* 플레이어의 목표 지점은 적 캐릭터의 ActorLocation이다
* 적 몬스터의 캐릭터 크기가 클수록, 목표 지점을 향해 다가가려 하면서 비빈다
  * 캐릭터 간의 거리가 일정 거리 이내가 되면 멈추게 하더라도, 이 거리 값 설정을 플레이어 캐릭터 공격 모션 에셋에 설정하기에, 적 캐릭터 크기가 크면 의미가 없다

### 2. 플레이어 캐릭터의 공격 모션 재생 중, 적 캐릭터가 이동하면서 타겟 위치가 바뀌거나 타겟 액터 자체가 바뀌는 현상
* 특정 속도로 접근하도록 세팅된 값인데, 거리가 멀어지니 이동 시간이 짧아진다
  * 겁나 빠르게 이동한다
* 처음 목표로 한 지점을 플에이어 공격 모션이 끝날 때까지 유지해줘여 한다

## 해결 방법

### 적 캐릭터의 중앙이 아닌 가장 가까운 위치를 타겟 위치로 잡는다
* 각 캐릭터는 캡슐 형태의 피격 볼륨을 가진다
* 플레이어 캐릭터가 공격 모션을 재생하면, 적 캐릭터에 Attach된 피격 CapsuleComponent를 조사한다
  * 이 Component들 중 캐릭터의 Forward를 기준으로 즉, ***플레이어 캐릭터 정면에서 가장 가까운 캡슐 표면 위치***를 구한다
  * 그리고 이 CapsuleComponent, 그리고 Capsule의 Owner Actor를 플레이어 캐릭터의 공격 모션이 끝날 때까지 유지한다

```c++
void UCustomTargetingComponent::SoftTarget_Init(bool bUseTopPriorityPolicy)
{
  if (FL::HasTag(OwnerCharacter, Tags.Status.Dead))
  {
    SoftTarget_Clear();
    return;
  }

  // SoftTarget 탐색 세팅을 순회한다
  const int32 Size = bUseTopPriorityPolicy ? 1 : SoftTargetSettings.Num(); 
  for (int32 Index = 0; Index < Size; ++Index)
  {
    const auto& CurrentSoftTargetSettings = SoftTargetSettings[Index];
    if (CurrentSoftTargetSettings.bEnable == false)
    {
      SoftTarget_Clear();
      continue;
    }

    // ...

    const FVector OwnerLocation = OwnerCharacter->GetActorLocation();
    const FQuat ActorQuat = OwnerCharacter->GetActorRotation().Quaternion();
    
    // SoftTarget을 체크하는 기점은 플레이어 캐릭터의 발끝지점
    const FVector SoftTargetCheckLocation = OwnerLocation - FVector(0.f, 0.f, OwnerCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight());
    
    // 기준 위치로부터 조건을 충족하는 CapculeComponent 리스트를 받는다
    const TArray<FOverlapResult> OverlapResults =
      CheckOverlap(SoftTargetCheckLocation, ActorQuat,
      CurrentSoftTargetSettings.CollisionChannels, CurrentSoftTargetSettings.InitTraceHalfHeight, CurrentSoftTargetSettings.InitTraceDistance);

    // 검출된 대미지 캡슐이 있다면
    if (OverlapResults.IsEmpty() == false)
    {
      bool bFoundTarget = false;
      
      const FVector TargetedActorLocation = OverlapResults[0].GetActor()->GetActorLocation();
      float NearestDist = MAX_FLT;
      FVector NearestPoint = TargetedActorLocation;
      UCapsuleComponent* NearestCapsule = nullptr;
      
      // Segment를 정의한다
      const FVector SelfActorForward = OwnerCharacter->GetActorForwardVector();
      const FVector SegmentStart = OwnerLocation;
      const FVector SegmentEnd = OwnerLocation + (bHasInput ? InputVector : SelfActorForward) * MAX_FLT;
      
      // Intersection이 전혀 없는지 확인
      bool bFoundAnyIntersection = false;
      
      // 피격 캡슐을 Iterate해서 가장 가까운 포인트를 찾는다
      for (const auto& OverlapResult_Capsule : OverlapResults)
      {
        if (UCapsuleComponent* TargetCapsule = Cast<UCapsuleComponent>(OverlapResult_Capsule.Component))
        {
          // ...
          
          const FVector TargetCenter = TargetCapsule->GetComponentLocation(); 
          const float CapsuleRadius = TargetCapsule->GetScaledCapsuleRadius();
          const float CapsuleHalfHeight = TargetCapsule->GetScaledCapsuleHalfHeight();
          const FVector UpVector = TargetCapsule->GetUpVector(); 

          // 캡슐의 위 아래 반구 모양을 제외하고 원통형 부분만 고려했을 때, 맨 위와 아래 지점을 구한다
          // 이는 아래의 SegmentCapsuleIntersections 함수에 필요한 인자를 구하기 위함
          const FVector BeginPoint = TargetCenter - UpVector * (CapsuleHalfHeight - CapsuleRadius);
          const FVector EndPoint = TargetCenter + UpVector * (CapsuleHalfHeight - CapsuleRadius);
      
          // 직선과 캡슐의 교차점을 구하는 함수 실행
          TArray<FVector> OutIntersections;
          const bool bFoundIntersections = FL::SegmentCapsuleIntersections(BeginPoint, EndPoint, CapsuleRadius, SegmentStart, SegmentEnd, OutIntersections);

          // 여태껏 아무런 교차점을 못 찾았는지 기록
          bFoundAnyIntersection |= bFoundIntersections;
          if (bFoundIntersections)
          {
            // 해당 지점이 소프트 타겟 체크 범위 내에 있는지와 중간에 장애물이 있는지 확인
            if (SoftTarget_FoundTarget(OutIntersections[0], SoftTargetCheckLocation, TargetCapsule, NearestDist, NearestPoint, NearestCapsule))
            {
              bFoundTarget = true;
            }
          }
          else
          {
            // 교차점이 하나도 없었다면 끼인각이 가장 작은 위치를 다시 탐색 
            // 앞서 정의한 Segment와 캡슐의 중심축 Segment와 가장 가까운 지점 탐색
            const FVector ClosestPoint = FMath::ClosestPointOnSegment(SegmentEnd, BeginPoint, EndPoint);
            if (FL::SegmentCapsuleIntersections(BeginPoint, EndPoint, CapsuleRadius, SegmentStart, ClosestPoint, OutIntersections)
              && SoftTarget_FoundTarget(OutIntersections[0], SoftTargetCheckLocation, TargetCapsule, NearestDist, NearestPoint, NearestCapsule))
            {
              bFoundTarget = true;
            }
          }
        }
      }
      
      // Target으로 삼을 CapsuleComponent와 표면 상의 Target 위치를 잡았는지 확인
      if (bFoundTarget)
      {
        // 캡슐 표면 위치 및 해당 캡슐의 Owner 반환
        TargetLocationOnSoftTarget = NearestPoint;
        TargetCapsuleOnSoftTarget = NearestCapsule;
        bActiveSoftTarget = true;
        CurrentSoftTargetSettingIndex = Index;

        FL::ActorMessage::Publish(OwnerCharacter, FGM_Character_ActivatedSoftTarget { true, TargetCapsuleOnSoftTarget->GetOwner() });
        
        break;
      }
    }
  }

  // SoftTarget 탐색을 시도했으나 실패했을 경우
  if (bActiveSoftTarget == false)
  {
    SoftTarget_Clear();
  }
}
```

* 플레이어 캐릭터의 Forward 방향으로 캡슐과의 접점을 탐색한다
  * 없다면 캡슐의 중앙을 관통하는 선분 위의 점 중, 플레이어 캐릭터의 Forward Vector와 가장 가까운 위치를 찾는다
* 감지된 모든 CapculeComponent를 모두 순회한 뒤, 가장 가까운 지점을 최종 타겟으로 확정한다

### 일정 거리 내로 더 다가오지 못하게 막기
* 우리 프로젝트는 [Abl](https://www.fab.com/listings/2e9a2754-183c-4d62-a12b-0ea013f50017)이라는 플러그인을 사용해 캐릭터의 액션 단위를 정의했다
* 캐릭터의 액션 하나를 실행하기 위해 애니메이션 실행, 위치 보정, GE 적용 등을 AblTask 또는 AblAction 이라는 단위로 실행했다
* 아래는 그 중 AblAction에 해당하는, 타겟으로 삼은 Actor와의 거리를 유지하기 위한 로직의 일부이다

```c++
void UAblAction_KeepDistance::OnActionStart(const TWeakObjectPtr<const UAblAbilityContext>& Context) const
{
  if (AActor* SelfActor = Context->GetSelfActor()
    ; IsValid(SelfActor) && FL::IsLocalPlayerCharacter(SelfActor))
  {
    // 최초 소프트 타겟 대상 지정
    if(UCustomTargetingComponent* TargetingComponent = FL::GetActorComponent<UCustomTargetingComponent>(SelfActor))
    {
      TargetingComponent->SoftTarget_Init(bUseTopPriorityPolicy);
      // ...

    }
  }
}

void UAblAction_KeepDistance::OnActionTick(const TWeakObjectPtr<const UAblAbilityContext>& Context, float DeltaTime) const
{
  Super::OnActionTick(Context, DeltaTime);
  
  // 전방 일정 범위 내에 타겟이 있는 경우, CombatMove를 실행시키지 않는 옵션 처리 
  if (AActor* SelfActor = Context->GetSelfActor()
    ; IsValid(SelfActor) && FL::IsLocalPlayerCharacter(SelfActor))
  {
    if (UCombatMoveComponentBase* CombatMoveComponent = FL::GetActorComponent<UCombatMoveComponentBase>(SelfActor)
      ; CombatMoveComponent->IsEnableCombatMove() && bDisableCombatMoveWithTarget)
    {
      FVector TargetLocation;		
      UCapsuleComponent* CapsuleComponent = nullptr;
      const bool bHasLockTarget = FL::GetTargetInfo(SelfActor, TargetLocation, CapsuleComponent);
      if (bHasLockTarget && IsValid(CapsuleComponent))
      {
        const float OffsetDistance = KeepDistance + CapsuleComponent->GetScaledCapsuleRadius();
        bool bInsideDistance = false;
        switch (DistanceType)
        {
        case EAistanceType::XYZ:
          {
            const float ActualDistSq = FVector::DistSquared(SelfActor->GetActorLocation(), TargetLocation);
            bInsideDistance = ActualDistSq <= OffsetDistance * OffsetDistance;
          }
          break;
        
          // ...
        }

        if (bInsideDistance)
        {
          // 타겟이 잡히면 CombatMove Velocity를 0으로 
          CombatMoveComponent->SetOverrideVelocity(FVector::ZeroVector);	
        }
        else
        {
          // 타겟이 없으면 OverrideVelocity 적용을 멈추고, 다시 애니메이션 커브 데이터에 기반한 Velocity를 적용한다
          CombatMoveComponent->ClearOverrideVelocity();
        }
      }
    }
  }
}
```

* CombatMoveComponent는 이동량을 메타 데이터르 갖고 있는 애니메이션의 커브를 추출해 캐릭터의 이동에 관여하는 Component이다
  * 애니메이션을 재생하면서 실제로 이동할 때, 이동량을 조정하는 기능을 추가하기 위한 목적이다
* GetTargetInfo 함수를 통해 SelfActor의 현재 SoftTarget Actor를 가져오는 역할을 한다
  * OnActionStart에서 초기화한 SoftTarget 정보는 UCustomTargetingComponent에 계속 유지되고 있다
* 위 로직은 **문제 상황** 발생 전부터 있던 로직이다
  * 매 Tick SoftTarget을 찾던 로직을 AblAction Start 타이밍에 1번만 하도록 수정했다
  * 기존에는 플레이어 캐릭터 공격 시, 적 캐릭터와의 거리를 유지하는 역할만 했다
    * 가장 가까운 캡슐의 표면으로 TargetLocation을 정의하도록 변경했다
    * 이로써, 상기한 큰 스케일의 적 캐릭터를 향해 공격 시 CombatMoveComponent에 의해 비비는 현상을 막는 역할까지 한다
