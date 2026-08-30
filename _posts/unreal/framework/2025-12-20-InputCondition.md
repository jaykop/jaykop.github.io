---
title: "[DevNote] Input Condition"
classes: wide
categories:
  - unreal
  - framework
sidebar:
  nav: "main"
author_profile: true
---

## 조건부 Input 트리거
* IMC에서 설정하는 Input Trigger를 커스텀하게 추가할 수 있다

### GameplayTag로 Input Trigger 판단

```c++
UCLASS(NotBlueprintable, MinimalAPI, meta = (DisplayName = "Check Tag Condition"))
class UInputTriggerTag : public UInputTrigger
{
  GENERATED_BODY()

public:
  // 다른 Explicit 타입과 조합해서 사용하기 위해, Implicit 으로 설정
  virtual ETriggerType GetTriggerType_Implementation() const override { return TriggerType::Implicit; }

  virtual ETriggerEventsSupported GetSupportedTriggerEvents() const override { return ETriggerEventsSupported::Instant; }

protected:
  virtual ETriggerState UpdateState_Implementation(const UEnhancedPlayerInput* PlayerInput, FInputActionValue ModifiedValue, float DeltaTime) override;

public:
  /* 체크 Tag */
  UPROPERTY(EditAnywhere, meta = (Categories = "Status"))
  FGameplayTagContainer TagContainer;

  /**
   * 확인 조건
   * False : TagContainer의 모든 태그가 있어야 Trigger Fire
   * True : TagContainer의 태그 중 하나도 없어야 Trigger Fire
   */
  UPROPERTY(EditAnywhere, Config, BlueprintReadWrite, Category = "Trigger Settings")
  bool bNegate = false;

};

ETriggerState UInputTriggerTag::UpdateState_Implementation(const UEnhancedPlayerInput* PlayerInput, FInputActionValue ModifiedValue, float DeltaTime)
{
  if (PlayerInput->GetOuterAPlayerController() == nullptr || PlayerInput->GetOuterAPlayerController()->GetPawn() == nullptr)
  {
    return ETriggerState::None;
  }

  ACharacter* CurrentCharacter = Cast<ACharacter>(PlayerInput->GetOuterAPlayerController()->GetPawn());
  if (IsValid(CurrentCharacter))
  {
    if (bNegate)
    {
      // negate면 하나도 없는 경우에 트리거 되어야 함
      if (FL::HasTagsAny(CurrentCharacter, TagContainer))
      {
        return ETriggerState::None;
      }
      return ETriggerState::Triggered;
    }
    else
    {
      // negate == false면 전부 있어야 트리거 됨
      if (FL::HasTagsAll(CurrentCharacter, TagContainer))
      {
        return ETriggerState::Triggered;
      }
      return ETriggerState::None;
    }
  }

  return ETriggerState::None;
}
```

### Trigger 종류
* [출처](https://daisy0461.tistory.com/77)
* 3가지 유형의 Input Trigger가 있다
	* Explicit(명시적) Type은 Input Trigger가 들어오면 입력이 수행되도록 한다 (e.g. 이동)
	* Implicit(암시적) Type은 Input Trigger 및 lmplicit Trigger가 모두 충족될 때만 수행을 한다 (e.g. 기모아 공격)
	* Blocker(차단) Type은 Input Trigger가 들어오면 입력이 실패하도록 한다
* 이렇게 되면 Trigget는 세가지 상태를 나타낼 수 있다
	* None: Input Trigger의 조건이 만족되지 않아 Input Trigger가 실패함
	* Ongoing: Input Trigger의 조건이 일부 충족이 되었고 다른 Input Trigger를 처리중이지만 성공은 아님
	* Triggered: Input Trigger의 조건이 모두 충족이 되었고 Input Trigger가 성공함