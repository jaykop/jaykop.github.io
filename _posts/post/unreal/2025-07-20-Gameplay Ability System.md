---
title: "Gameplay Ability System"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## Gameplay Ability System (GAS)
* 캐릭터의 능력이나 속성 등을 관리할 수 있게 도와주는 프레임워크
* 캐릭터의 능력 또는 스킬의 구현
  * Gameplay Ability
* 액터의 수치화된 속성 관리
  * Atttibute
* 액터에 특정한 효과(Effect) 적용  
  * Gameplay Effect
* 액터에 상태(state)를 Tag로 관리 
  * Gameplay Tag
* 시각/음향 효과를 생성
  * Gameplay Cue
* 위 요소들의 Replication 및 Local Prediction

## Gameplay Ability System Component (ASC)
* 액터가 GAS Framework와 연동하기 위해서 반드시 attach 하고 있어야 하는 Component

### OwnerActor vs. Avatar Actor
* OwnerActor는 실제로 ASC가 attach 된 owner actor
* AvatarActor는 ASC의 물리적인 Representation
* 이 둘은 같은 액터를 가리킬 수도, 다른 액터를 가리킬 수도 있다
  * 플레이어의 경우 OwnerActor가 PlayerState인 경우가 있을 수 있다고 한다

```c++
// 1. ASC가 Pawn에 부착된 경우
void APACharacterBase::PossessedBy(AController * NewController)
{
	Super::PossessedBy(NewController);

	if (AbilitySystemComponent)
	{
		AbilitySystemComponent->InitAbilityActorInfo(this, this);
	}

	// ASC MixedMode replication requires that the ASC Owner's Owner be the Controller.
	SetOwner(NewController);
}

void APAPlayerControllerBase::AcknowledgePossession(APawn* P)
{
	Super::AcknowledgePossession(P);

	APACharacterBase* CharacterBase = Cast<APACharacterBase>(P);
	if (CharacterBase)
	{
		CharacterBase->GetAbilitySystemComponent()->InitAbilityActorInfo(CharacterBase, CharacterBase);
	}

	//...
}

// 2. ASC가 PlayerState에 부착된 경우
// Server only
void AGDHeroCharacter::PossessedBy(AController * NewController)
{
	Super::PossessedBy(NewController);

	AGDPlayerState* PS = GetPlayerState<AGDPlayerState>();
	if (PS)
	{
		// Set the ASC on the Server. Clients do this in OnRep_PlayerState()
		AbilitySystemComponent = Cast<UGDAbilitySystemComponent>(PS->GetAbilitySystemComponent());

		// AI won't have PlayerControllers so we can init again here just to be sure. No harm in initing twice for heroes that have PlayerControllers.
		PS->GetAbilitySystemComponent()->InitAbilityActorInfo(PS, this);
	}
	
	//...
}
// Client only
void AGDHeroCharacter::OnRep_PlayerState()
{
	Super::OnRep_PlayerState();

	AGDPlayerState* PS = GetPlayerState<AGDPlayerState>();
	if (PS)
	{
		// Set the ASC for clients. Server does this in PossessedBy.
		AbilitySystemComponent = Cast<UGDAbilitySystemComponent>(PS->GetAbilitySystemComponent());

		// Init ASC Actor Info for clients. Server will init its ASC when it possesses a new Actor.
		AbilitySystemComponent->InitAbilityActorInfo(PS, this);
	}

	// ...
}
```

### Replication
* ASC는 GameplayEffect, GameplayTag, GameplayCue의 복제를 담당한다
* Attribute는 AttributeSet에 의해 복제된다
  * Full
    * 싱글플레이어에서 사용 
    * 모든 이펙트가 모든 클라에 복제
  * Mixed
    * 멀티플레이어, 플레이어에 의해 컨트롤되는 액터에서 사용
    * 이펙트는 owning client에게만 복제되며, 태그와 큐는 모두에게 복제
    * 이 때 OwnerActor의 Owner가 컨트롤러여야 한다
  * Minimal 
    * 멀티플레이어, AI에 의해 컨트롤되는 액터에서 사용
    * 이펙트는 복제되지 않고 태그와 큐는 모두에게 복제

## Gameplay Tag
* GameplayTagManager에 등록되며, 계층구조를 가진다
* 사실 GAS와는 독립적으로 사용 가능한 기능

```c++
// 태그 레퍼런스 얻기
FGameplayTag::RequestGameplayTag(FName("Your.GameplayTag.Name"))
```

## Attribute
* Smart floating point numbers
* Current + Base values
  * Base Value는 Effect가 끝나고 나면 복구 용도의 기준 수치
  * Current Value는 Effect가 적용된 용도로 사용하는 현재 수치

### Attribute Set
* 하나의 ASC는 여러 개의 Attribute Set을 가질 수 있따
  * 굉장히 낮은 오버헤드로 부담없이 사용 가능
  * **다만 같은 종류의 Attribute Set을 여러 개 넣는 것은 불가능**

```c++
// Current value의 변경이 일어나기 전 반응할 수 있는 함수
PreAttributeChange(const FGameplayAttribute& Attribute, float& NewValue);

//  BaseValue가 변경된 이후 트리거
PostGameplayEffectExecute(const FGameplayEffectModCallbackData & Data);
```

## Gameplay Effect
* Attribute의 수치 변경 혹은 Tag 적용 등 가능
* Duration Policy에 따라 적용되는 Value가 다르다
  * Instance -> BaseValue
  * Duration / Infinite -> CurrentValue

![post_thumbnail](/assets/images/Replication/ge.png)

## Gameplay Cue
* FX 효과들의 Wrapper 역할
* 보통은 Client Only의 audio, visual 효과를 실행한다

### Local Gameplay Cue
* Gameplay Cue의 트리거 함수는 기본적으로 멀티캐스트 RPC
* 많은 RPC 호출을 예방하기 위해 Local Gameplay Cue를 사용할 수 있다
* 주로 프로젝타일 효과, 근접 충돌 효과, animattion montage 출력 등의 상황에서 사용된다

```c++
UFUNCTION(BlueprintCallable, Category = "GameplayCue", Meta = (AutoCreateRefTerm = "GameplayCueParameters", GameplayTagFilter = "GameplayCue"))
void ExecuteGameplayCueLocal(const FGameplayTag GameplayCueTag, const FGameplayCueParameters& GameplayCueParameters);

UFUNCTION(BlueprintCallable, Category = "GameplayCue", Meta = (AutoCreateRefTerm = "GameplayCueParameters", GameplayTagFilter = "GameplayCue"))
void AddGameplayCueLocal(const FGameplayTag GameplayCueTag, const FGameplayCueParameters& GameplayCueParameters);

UFUNCTION(BlueprintCallable, Category = "GameplayCue", Meta = (AutoCreateRefTerm = "GameplayCueParameters", GameplayTagFilter = "GameplayCue"))
void RemoveGameplayCueLocal(const FGameplayTag GameplayCueTag, const FGameplayCueParameters& GameplayCueParameters);

void UPAAbilitySystemComponent::ExecuteGameplayCueLocal(const FGameplayTag GameplayCueTag, const FGameplayCueParameters & GameplayCueParameters)
{
	UAbilitySystemGlobals::Get().GetGameplayCueManager()->HandleGameplayCue(GetOwner(), GameplayCueTag, EGameplayCueEvent::Type::Executed, 
    
    GameplayCueParameters);
}

void UPAAbilitySystemComponent::AddGameplayCueLocal(const FGameplayTag GameplayCueTag, const FGameplayCueParameters & GameplayCueParameters)
{
	UAbilitySystemGlobals::Get().GetGameplayCueManager()->HandleGameplayCue(GetOwner(), GameplayCueTag, EGameplayCueEvent::Type::OnActive, GameplayCueParameters);
	UAbilitySystemGlobals::Get().GetGameplayCueManager()->HandleGameplayCue(GetOwner(), GameplayCueTag, EGameplayCueEvent::Type::WhileActive, GameplayCueParameters);
}

void UPAAbilitySystemComponent::RemoveGameplayCueLocal(const FGameplayTag GameplayCueTag, const FGameplayCueParameters & GameplayCueParameters)
{
	UAbilitySystemGlobals::Get().GetGameplayCueManager()->HandleGameplayCue(GetOwner(), GameplayCueTag, EGameplayCueEvent::Type::Removed, GameplayCueParameters);
}
```

* GameplayCue가 Local로 추가된다면, 반드시 Local에서 Remove 처리도 되어야 한다

## 출처
* https://www.youtube.com/watch?v=tc542u36JR0&t=296s
* https://velog.io/@dltmdrl1244/UE5-Gameplay-Ability-SystemGAS
* https://kkadalg.tistory.com/37
* https://github.com/tranek/GASDocumentation?tab=readme-ov-file#concepts-gc-local