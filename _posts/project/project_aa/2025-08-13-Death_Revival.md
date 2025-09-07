---
title: "[DevNote] 플레이어 캐릭터의 사망과 부활 처리"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## 플레이어 캐릭터 사망

```c++
bool UDamageCtrlComponent::ApplyDeadGA(UCustomAbilitySystemComponent* ASC, AActor* Attacker) const
{
  check(ASC);
  
  FGameplayEventData EventData;
  EventData.Instigator = Attacker;
  EventData.Target = GetOwner();

  if (FL::IsPlayerCharacter(ASC->GetOwner()))
  {
    EventData.EventTag = Tags.Ability.Die.Moribund;
    return ASC->TryActivateAbilitiesByTagWithData(FGameplayTagContainer(Tags.Ability.Die.Moribund), &EventData) > 0;
  }

  // ...
}

int32 UCustomAbilitySystemComponent::TryActivateAbilitiesByTagWithData(FGameplayTagContainer Tags, FGameplayEventData* EventData)
{
  TArray<FGameplayAbilitySpec*> Specs;
  GetActivatableGameplayAbilitySpecsByAllMatchingTags(Tags, Specs);

  int32 ActivatedCount = 0;
  for (const FGameplayAbilitySpec* Spec : Specs)
  {
    if (TriggerAbilityFromGameplayEvent(Spec->Handle, AbilityActorInfo.Get(), EventData ? EventData->EventTag : FGameplayTag(), EventData, *this))
    {
      ++ActivatedCount;
    }
  }

  return ActivatedCount;
}
```

* 피격 관리 컴포넌트에서 사망 판정이 나면, 플레이어에게 등록된 Die GA를 실행한다

```c++
// 호출 코드
EventData.EventTag = Tags.Event.Rescue.Ready;
OtherActorASC->HandleGameplayEvent(EventData.EventTag, &EventData);

// ...

// 호출당하는 GA의 Constructor 일부
FAbilityTriggerData TriggerData;
TriggerData.TriggerTag = Tags.Event.Rescue.Ready;
TriggerData.TriggerSource = EGameplayAbilityTriggerSource::GameplayEvent;
AbilityTriggers.Add(TriggerData);
```

* 일반적으로는 위와 같이 Event 전용 태그를 만들고 HandleGameplayEvent 함수를 호출해 GA를 트리거했다
  * 그에 대응하는 AbilityTriggers도 위와 같이 GA 생성자에 세팅해줘야 한다
* Die만 저렇게 트리거한 이유는 TryActivateAbilitiesByTagWithData를 통해 GA를 실행하는 방법을 썼기 때문인 것 같다

### 빈사 상태
* 위와 같은 기존 플레이어 사망 처리 플로우에 **빈사 상태**를 추가해달라는 요청이 생겼다
  * 엎드려서 이동 가능 (제한전 플레이 가능)
  * 일정 시간 내에 구조되지 않으면 사망
  * 마지막 세이브 포인트에서 이동 후 부활 등...

```c++
Tags.Status.Dead.Moribund
Tags.Status.Dead.Permanent
```

* 그래서 일단 사망 상태를 즉사와 빈사를 구분해 GA와 태그를 분리했다
  * Die.Moribund 태그를 보유하고 있는 경우에는 MoveInput을 받을 수 있도록 했다
  * [Input Mapping Context를 제어](https://jaykop.github.io/project/project_aa/PlayerRestriction/)하는 방법으로 플레이어의 입력을 제한했다

```c++
void UGA_Die_Moribund::Crouch()
{
  if (ACharacter* Character = Cast<ACharacter>(CurrentActorInfo->AvatarActor))
  {
    Character->Crouch();
  }	
}
```

* 빈사 상태의 Locomotion도 추가로 필요했다
* 전용 Anim Layer를 만드는 것을 고민했는데, 마침 ALS가 Crouch를 지원하고 우리 프로젝트에서 Crouch를 사용하지 않기에, 빈사 시 Animation적으로 Crouch 상태가 되도록 했다
  * 오버헤드를 고려하면 Crouch가 있어도 추가로 State를 만드는 게 더 나았을 지도 모르겠다

```c++
void UGA_Die_Moribund::PostCommitActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo, const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData)
{
  Super::PostCommitActivateAbility(Handle, ActorInfo, ActivationInfo, TriggerEventData);

  //...

  UAbilityTask_WaitGameplayEvent* Task_EventCrouch = UAbilityTask_WaitGameplayEvent::WaitGameplayEvent(this, Tags.Event.Notify.Crouch);
  Task_EventCrouch->EventReceived.AddDynamic(this, &UGA_Die_Moribund::OnReceivedEvent);
  Task_EventCrouch->ReadyForActivation();
  
  if (HasAuthority(&ActivationInfo))
  {
    // 부활 함수 Delegate 할당
    OnGameplayAttributeValueChange = ASC->GetGameplayAttributeValueChangeDelegate(UAttributeSet_PC::GetCurrentRevivalGaugeAttribute()).AddUObject(this, &UGA_Die_Moribund::OnRevive);
    
    // ...
    // 이동 멈춤 처리
    // Activated 된 GA들 중 종료해야 되는 GA들은 종료 처리
    // 사망 애니메이션 재생 등...

    // 사망 Effect를 먼저 적용해야 Die Abl의 Required Tag(Dead)를 만족시키고 실행된다
    // 빈사 상태 이펙트 실행
    if (MoribundEffectHandle.IsValid())
    {
      ASC->RemoveActiveGameplayEffect(MoribundEffectHandle);
      MoribundEffectHandle.Invalidate();
    }
    
    // 일정 시간 이후, 영구 사망 상태 적용
    const int32 CurrentRevivalCount = static_cast<int32>(ASC->GetNumericAttribute(UAttributeSet_PC::GetRevivalCountAttribute()));
    const int32 MaxRevivalCount = GetMaxRevivalCount();
    const int32 RevivalCount = FMath::Min(MaxRevivalCount, CurrentRevivalCount);
    if (RevivalCountTimeMap.Contains(RevivalCount) && RevivalCountTimeMap[RevivalCount] > 0.f)
    {
      const float MoribundTime = RevivalCountTimeMap[RevivalCount];
      TArray<FCustomGameplayEffectArgument> Arguments;
      Arguments.Add(FCustomGameplayEffectArgument(Tags.SetByCaller.Dead.MoribundTime, MoribundTime));
      MoribundEffectHandle = ASC->ApplyGameplayEffectToSelf(this, CurrentActorInfo->AvatarActor.Get(), MoribundEffect, -1, &Arguments);
    }
  }
  
  // ...
  // 사망한 캐릭터에 상호작용 가능한 인지범위 Sphere 생성
  
  if (IsLocallyControlled())
  {
    // 기존 IMC 바인딩 제거
    UEnhancedInputLocalPlayerSubsystem* InputSubsystem = FL::GetLocalPlayerSubsystemChecked<UEnhancedInputLocalPlayerSubsystem>(AvatarActor);
    InputSubsystem->ClearAllMappings();

    // 기본 조작 IMC 부여
    FL::PushSingleInputMappingContext(CurrentActorInfo->AvatarActor.Get(), ControlInputMappingContext, IMCPriority);
  }

  // ...
  // 사망 메시지 Publish ...
}
```

* 사망 GA를 실행하는 코드는 대략 위와 같다
* Notify.Crouch는 사망 몽타주 애니메이션에 Notify로 세팅되어 있고, 이 타이밍에 맞춰 캐릭터는 Crouch 함수를 호출한다
* 빈사 상태일 때 동반해야하는 GE도 실행한다
  * Dead.Moribund 태그를 부여
  * 빈사 상태는 일정 시간 유지 이후 해제되어야 하는데, 때문에 이 GE의 Duration Policy를 **Has Duration**으로 두고 값을 Set By Caller로 할당하도록 했다.
  * 조건에 따라 빈사 상태 유지 시간이 다르기 때문에...

> [!NOTE]
> PostCommitActivateAbility는 UE 오리지널 함수가 아닌 커스텀 함수이다  
> UGameplayAbility의 ActivateAbility를 override하고 이 함수에서 실행한다

## 플레이어 캐릭터 부활
* 부활 위치는 둘 중 하나로 선택된다
  * Moribund Timer가 0이 되면, 그러니까 구조 가능 시간이 0이 되면 마지막 세이브 포인트에서 부활한다
  * 그 전에 구조당하거나, 부활 아이템을 사용하면 제자리에서 그대로 부활한다

```c++
// 제자리에서 부활
void UGA_Die_Moribund::OnRevive(const FOnAttributeChangeData& ChangeData)
{
  // ...
  
  // Stack이 쌓였다면
  const float MaxRevivalGauge = ASC->GetNumericAttribute(UAttributeSet_PC::GetMaxRevivalGaugeAttribute());
  if (ChangeData.NewValue >= MaxRevivalGauge)
  {
    // 부활 GA 실행
    FGameplayEventData EventData;
    EventData.EventTag = Tags.Event.Revive.Here;
    EventData.Instigator = AvatarActor;
    EventData.Target = AvatarActor;

    ASC->HandleGameplayEvent(EventData.EventTag, &EventData);

    // 빈사 만료
    if (MoribundEffectHandle.IsValid())
    {
      ASC->RemoveActiveGameplayEffect(MoribundEffectHandle);
      MoribundEffectHandle.Invalidate();
    }
  }
}
```

* PostCommitActivateAbility 함수에서 할당한 OnRevive는 플레이어 캐릭터의 부활 게이지 값이 변경될 때마다 호출한다
  * 부활 게이지가 Max에 다다르면 GameplayEvent를 통해 부활 GA를 트리거한다

```c++
// 마지막 세이브 포인트에서 부활
void UGA_Die_Moribund::TickAbility(float DeltaTime)
{
  // ...
  
  if (HasAuthority(&CurrentActivationInfo))
  {
    // Moribund 타이머 업데이트
    // MoribundEffectHandle로 Active된 GE를 불러와 남은 Duration 검사
    const FActiveGameplayEffect* ActiveMoribund = ASC->GetActiveGameplayEffect(MoribundEffectHandle);
    float RemainingTime = ActiveMoribund->GetTimeRemaining(GetWorld()->GetTimeSeconds());
    AttributeSet_PC->SetMoribundTimer(RemainingTime);
  
    // Moribund 종료 여부 확인
    if (RemainingTime <= 0.f)
    {
      RemoveRescueSphere();
  
      // 빈사 만료
      ASC->RemoveActiveGameplayEffect(MoribundEffectHandle);
      MoribundEffectHandle.Invalidate();

      ASC->GetGameplayAttributeValueChangeDelegate(UAttributeSet_PC::GetCurrentRevivalGaugeAttribute()).Remove(OnGameplayAttributeValueChange);

      // 마지막 세이브 포인트로 이동 부활
      FGameplayEventData EventData;
      EventData.EventTag = Tags.Event.Revive.Camp;
      EventData.Instigator = SelfActor;
      EventData.Target = SelfActor;
      ASC->HandleGameplayEvent(EventData.EventTag, &EventData);
    }
  }

  // ...
}
```

* 위의 코드는 빈사 상태의 타이머를 체크하고 마지막 세이브 포인트로 이동시키는 로직이다
* 남은 시간이 얼마인지 활성화된 GE로부터 가져온다
* 시간이 만료되면 관련된 처리 후 마지막 세이브 포인트에서 부활하는 GA를 실행한다

### 구조 가능한 상태 부여
* 제자리에서 부활하는 조건은 특정 아이템을 사용하거나, 다른 플레이어 캐릭터가 구조해서 부활 게이지를 Max로 채워주는 2가지 방법이 있다
  * 구조 플로우에 대해서만 설명한다

```c++
void UGA_Die_Moribund::PostCommitActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo, const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData)
{
  // ...

  RescueSphere = FL::GetActorComponent<USphereComponent>(AvatarActor);
  if (IsValid(RescueSphere))
  {
    RescueSphere->OnComponentBeginOverlap.AddDynamic(this, &UGA_Die_Moribund::OnOverlapRescueSphereBegin);
    RescueSphere->OnComponentEndOverlap.AddDynamic(this, &UGA_Die_Moribund::OnOverlapRescueSphereEnd);

    // ...
  }

  // ...
}

void UGA_Die_Moribund::OnOverlapRescueSphereBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult & SweepResult)
{
  // ...
  
  // Rescue 가능 범위 내에 들어온 플레이어에게 어떤 액터가 타겟인지 설정
  if (UCustomAbilitySystemComponent* OtherActorASC = FL::GetActorComponent<UCustomAbilitySystemComponent>(OtherActor))
  {
    FGameplayEventData EventData;
    EventData.Instigator = ThisActor;
    EventData.Target = ThisActor;		// 이벤트를 받은 Actor가 Target으로서 Rescue해야하는 Actor는 ThisActor
    EventData.EventTag = Tags.Event.Rescue.Ready;

    // RescueSphere 영역 내로 진입하면 진입한 캐릭터의 RescueReady GA 실행
    OtherActorASC->HandleGameplayEvent(EventData.EventTag, &EventData);
  }
}
```

* 플레이어 캐릭터가 사망하면서 RescueSphere라는 영역을 만든다
  * 다른 플레이어 캐릭터가 이 영역 안에 진입하거나 벗어남에 따라 Tag로 구조 가능 상태를 부여 또는 제거되도록 한다
* 구조 가능 상태가 된 플레이어 캐릭터는 특정 Input 입력을 통해 Rescue InProgress GA를 실행한다
  * InProgress GA는 EventData를 통해 빈사 상태의 캐릭터를 Target으로 인지하고 있다
  * 이 GA의 GE를 통해 Target, 즉 빈사 상태의 캐릭터는 Attribute의 부활 게이지를 증가시키고, Max치에 다다르면 그 자리에서 부활한다

> [!NOTE]
> 데이터 연산 및 태그 부여 등 GE에서 할 수 있는 기능을 최대한 이용하고, 
> 그 외 기타 로직은 GA에서 코드로 구현해 실행하는 기조다  
>  
> Attribute는 단순히 캐릭터의 인게임 재화가 아닌, 
> 위의 부활 게이지와 같은 특정 로직 실행을 위한 값 버퍼로 쓸 수도 있다  
> 다만 타당성을 고려한 후에 Attribute에 포함시키는 것이 적절하겠다