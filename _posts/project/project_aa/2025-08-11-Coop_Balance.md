---
title: "멀티 상황에서의 AI 수치 밸런싱"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## 멀티 상황에서 필요한 정보 정의

```c++
USTRUCT(BlueprintType)
struct FCoopSettings
{
  GENERATED_BODY()

  /**
   * 멀티플레이어 인원 수에 따라 특정 Stat에 적용할 Coefficient 세팅
   * ( 1.0 + (CoopBalanceCoefficient * AIGradeMultiplier) = Multiplier으로 적용 )
   */
  UPROPERTY(EditAnywhere)
  TMap<int32, FCoopBalanceCoefficient> CoopBalanceCoefficient;
	
  /**
   * CoopBalanceCoefficient의 배율을 얼마나 적용할지 결정
   * ECharacterType에 몬스터의 등급도 포함되어 있어 이를 Key로 한다
   * ( 1.0 + (CoopBalanceCoefficient * AIGradeMultiplier) = Multiplier으로 적용 )
   */
  UPROPERTY(EditAnywhere)
  TMap<ECharacterType, float> AIGradeMultiplier;

  // 실제로 적용할 Balance GE
  UPROPERTY(EditAnywhere)
  TSubclassOf<class UGameplayEffect> BalanceMonsterStatsEffect;
};

// ...

UCLASS(Config = Game, defaultconfig)
class UCustomGameplaySettings : public UDeveloperSettings
{
  GENERATED_BODY()

public:
  // ...

  UPROPERTY(EditAnywhere, config)
  FCoopSettings CoopSettings;
```

* 위와 같이 코옵 전용, 즉 멀티 상황에서 적용 및 참고할 정보를 구조체로 만들었다
* 위 구조체는 UDeveloperSettings를 상속한 커스텀 GameplaySettings에 추가되어 있으며, GetDefault 함수를 통해 참조할 수 있다

## 밸런싱 적용

```c++
// 적 AI인지 확인한다
if (FL::GetTeamType(GetOwner()) == ETeamType::Enemy)
{
  // 이전 적용 중인 GE가 있으면 해제하고 Handle을 초기화한다
  if (BalanceStatEffectHandle.IsValid())
  {
    RemoveActiveGameplayEffect(BalanceStatEffectHandle);
    BalanceStatEffectHandle.Invalidate();
  }
  
  // GE를 적용한다
  // BalanceMonsterStatsEffect에는 몬스터의 Health, Stamina 등 멀티 상황에서 Attribute에 대해 스케일링을 적용하는 MMC를 가지고 있다
  BalanceStatEffectHandle = ApplyGameplayEffectToSelf(this, GetOwner()->GetInstigator(), GetDefault<UCustomGameplaySettings>()->CoopSettings.BalanceMonsterStatsEffect, -1, nullptr);
}
```

* 캐릭터 초기화 시 GE를 적용하는 타이밍에, 적 AI 인지 체크하고 밸런싱을 적용한다

```c++
float UMMC_BalanceMonsterMaxHealth::CalculateBaseMagnitude_Implementation(const FGameplayEffectSpec& Spec) const
{
  FAggregatorEvaluateParameters EvaluationParameters;
  EvaluationParameters.SourceTags = Spec.CapturedSourceTags.GetAggregatedTags();
  EvaluationParameters.TargetTags = Spec.CapturedTargetTags.GetAggregatedTags();
	
  // 연산할 Coefficient Map을 GlobalSetting에서 불러오기
  const UAbilitySystemComponent* InstigatorASC = Spec.GetEffectContext().GetInstigatorAbilitySystemComponent();
  const auto& CoopBalanceCoefficientMap = GetDefault<UCustomGameplaySettings>()->CoopSettings.CoopBalanceCoefficient;
	
  // 몇명의 플레이어 캐릭터가 참가중인지 확인
  const int32 PlayerNum = FMath::Clamp(InstigatorASC->GetWorld()->GetGameState()->PlayerArray.Num(), 1, GetDefault<UCustomGameplaySettings>()->MaxConnections);
  const float MaxMonsterHealthCoefficient = CoopBalanceCoefficientMap.Contains(PlayerNum) ? CoopBalanceCoefficientMap[PlayerNum].MaxMonsterHealthCoefficient : 0.f;

  // 연산할 AI Grade 별 Multiplier 불러오기
  const UCustomCharacterComponent* SourceCharacterComponent = FL::GetActorComponent<UCustomCharacterComponent>(InstigatorASC->GetOwner());
  const ECharacterType CharacterType = SourceCharacterComponent->GetCharacterType();
  const auto& AIGradeMultiplierMap = GetDefault<UCustomGameplaySettings>()->CoopSettings.AIGradeMultiplier;
  const float AIGradeMultiplier = AIGradeMultiplierMap.Contains(CharacterType) ? AIGradeMultiplierMap[CharacterType] : 0.f;
	
  // MaxHealth Balance 적용
  float MaxHealth = 0.f;
  ensure(GetCapturedAttributeMagnitude(MaxHealthDef, Spec, EvaluationParameters, MaxHealth));

  // @note. 기존 MaxHealth에는 이미 Init되어 있고, 그 값에 Add하기 때문에 Multiplier에 또 1.0을 더하지 않는다
  // 프로젝트에서 Base 값만 사용하기 때문에, GE BP에서 Modifier Op는 Add(Base)로 적용한다
  const float AdditionalMaxHealth = MaxHealth * (MaxMonsterHealthCoefficient * AIGradeMultiplier);
	
  return AdditionalMaxHealth;
}
```

* 위의 식대로 연산된 수치는 GE에서 Add로 몬스터 AI의 Attribute에 적용된다

## MMC vs. EC

![post_thumbnail](/assets/images/dev_note/EC_MMC.png)

### UGameplayModMagnitudeCalculation (MMC)
* 게임플레이 이펙트의 모디파이어(Modifier)가 가지는 단일 값(크기)을 계산
  * 특정 Attribute를 얼마나 변경할지를 결정하는 계산 로직

### UGameplayEffectExecutionCalculation (EC)
* 게임플레이 이펙트가 적용될 때 실행되는 복잡하고 종합적인 계산
* 다중 Attribute에 동시에 영향을 줄 수 있다
* Gameplay Cue 또는 Gameplay Effect를 실행하는 등 게임 로직 제어도 가능하다