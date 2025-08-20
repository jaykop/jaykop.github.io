---
title: "Common UI와 Dualsense Input 아이콘 적용"
classes: wide
categories: 
  - dev_note
  - project
sidebar:
  nav: "main"
author_profile: true
---

## Common UI

### 사용하는 이유?

* **콘솔 별 UI Element**
  * 이 플러그인을 사용한 가장 큰 이유
  * 멀티 플랫폼을 지원할 때, 같은 Input에 대해 다른 UI 아이콘을 표시하기 용이
* **멀티 레이어 메뉴 탐색**
  * 여러 Widget이 화면에 노출돼있는 경우, 어떤 Widget만 Active한 상태인지 우선순위에 의해 구분 가능
* **적합한 Widget으로 돌아가기**
  * 특정 Widget에서의 상호작용 후 죵료 시, 다시 돌아갈 곳을 찾기에 용이

### 인풋 이미지 불러오기

```c++
UCLASS(BlueprintType, Blueprintable)
class COMMONUI_API UCommonActionWidget: public UWidget
{
  GENERATED_UCLASS_BODY()

public:

  /// ...
  
  UFUNCTION(BlueprintCallable, Category = CommonActionWidget)
  virtual FSlateBrush GetIcon() const;

  // ...
}
```

* UCommonActionWidget을 사용하면 GetIcon 함수로 Key에 대응하는 Input 이미지를 불러온다

![post_thumbnail](/assets/images/CommonUI/CommonUI_1.png)

* UCommonInputBaseControllerData 클래스로 데이터 에셋을 만들고, 여기서 Input Device에 따른 키 및 이미지 데이터를 제공한다

### 기존 방식의 한계
* UCommonInputBaseControllerData가 제공하는 Key 매핑은 한계가 있다
  * 조합 키를 지원하지 않는다
  * Hold / Release 등 인풋 트리깅 방식에 따라 구분하는 것을 지원하지 않는다
* 심지어 Key의 Hold 및 Release 등 트리깅 방식은 InputAction이 아닌 IMC에서 정의된다

```c++
USTRUCT(Blueprintable)
struct FCustomKeyTrigger
{
  GENERATED_BODY()

public:
  UPROPERTY(EditAnywhere)
  FKey Key;
  
  // Hold 트리거가 포함되어 있는지 여부
  UPROPERTY(EditAnywhere)
  bool bIsHold = false;

  // Release 트리거가 포함되어 있는지 여부
  UPROPERTY(EditAnywhere)
  bool bIsRelease = false;

  // 조합 키가 있는지 여부
  TArray<FCustomKeyTrigger> ChordedActions;

  // ...
};

USTRUCT(Blueprintable)
struct FCustomCommonInputKeySetBrushConfiguration
{
  GENERATED_BODY()

public:
  FCustomCommonInputKeySetBrushConfiguration();

  const FSlateBrush& GetInputBrush() const { return KeyBrush; }

public:
  UPROPERTY(EditAnywhere, Category = "Key Brush Configuration", Meta = (TitleProperty = "KeyName"))
  TArray<FCustomKeyTrigger> Keys;

  UPROPERTY(EditAnywhere, Category = "Key Brush Configuration")
  FSlateBrush KeyBrush;
};

// ...

UCLASS()
class AACLIENT_API UCustomCommonInputBaseControllerData : public UCommonInputBaseControllerData
{
  GENERATED_BODY()

  // ...

  bool TryGetInputBrushByTrigger(FSlateBrush& OutBrush, const struct FCustomKeyTrigger& KeyTrigger) const;
  bool TryGetInputBrushByTrigger(FSlateBrush& OutBrush, const TArray<FCustomKeyTrigger>& KeyTriggers) const;

  // ...

public:
  UPROPERTY(EditDefaultsOnly, Category = "Display", Meta = (TitleProperty = "Key"))
  TArray<FCommonInputKeyBrushConfiguration> HoldInputBrushDataMap;

  UPROPERTY(EditDefaultsOnly, Category = "Display", Meta = (TitleProperty = "Key"))
  TArray<FCommonInputKeyBrushConfiguration> ReleaseInputBrushDataMap;
  
  UPROPERTY(EditDefaultsOnly, Category = "Display", Meta = (TitleProperty = "Keys"))
  TArray<FCustomCommonInputKeySetBrushConfiguration> InputBrushKeySetMap;
  
};

// ...

bool UAACommonInputBaseControllerData::TryGetInputBrushByTrigger(FSlateBrush& OutBrush, const struct FCustomKeyTrigger& KeyTrigger) const
{
  if (KeyTrigger.bIsHold)
  {
    const FCommonInputKeyBrushConfiguration* DisplayConfig = HoldInputBrushDataMap.FindByPredicate([&KeyTrigger](const FCommonInputKeyBrushConfiguration& KeyBrushPair) -> bool
    {
      return KeyBrushPair.Key == KeyTrigger.Key;
    });

    if (DisplayConfig)
    {
      OutBrush = DisplayConfig->GetInputBrush();
      return true;
    }
  }
  else if (KeyTrigger.bIsRelease)
  {
    const FCommonInputKeyBrushConfiguration* DisplayConfig = ReleaseInputBrushDataMap.FindByPredicate([&KeyTrigger](const FCommonInputKeyBrushConfiguration& KeyBrushPair) -> bool
    {
      return KeyBrushPair.Key == KeyTrigger.Key;
    });

    if (DisplayConfig)
    {
      OutBrush = DisplayConfig->GetInputBrush();
      return true;
    }
  }

  // ...
}
```

* Hold 및 Release 트리깅을 체크하고 이에 맞는 이미지를 반환하는 함수를 추가한다

```c++
TArray<FCustomKeyTrigger> GetKeyTriggers(const ULocalPlayer* LocalPlayer, ECommonInputType InputType, const UInputAction* Action)
{
  TArray<FCustomKeyTrigger> MappedKeys;
  
  // ...

  if (UCustomEnhancedPlayerInput* PlayerInput = Cast<UCustomEnhancedPlayerInput>(EnhancedInputLocalPlayerSubsystem->GetPlayerInput()))
  {
    const auto EnhancedActionMappingSet = PlayerInput->GetEnhancedActionMappingSet();
    for (const FEnhancedActionKeyMapping& Mapping : EnhancedActionMappingSet)
    {
      if (Mapping.Action == Action)
      {
        bool bIsHold = false;
        bool bIsRelease = false;
        TArray<FCustomKeyTrigger> ChordedActionKeys;
        for (const auto& Trigger : Mapping.Triggers)
        {
          if (Trigger->GetClass() == UInputTriggerHold::StaticClass())
          {
            bIsHold = true;	
          }
          else if (Trigger->GetClass() == UInputTriggerReleased::StaticClass())
          {
            bIsRelease = true;	
          }

          // ...
        }
      }

      MappedKeys.AddUnique({Mapping.Key, bIsHold, bIsRelease, ChordedActionKeys});
    }
  }
}
```

* GetKeyTriggers 함수 안에서 구분해야할 트리거를 위와 같이 구분했다
* 그리고 반환 결과에 Hold인지, Release인지, 조합 키가 필요한 지 등의 정보를 추가했다

```C++
  TArray<FCustomKeyTrigger> KeyTriggers = GetKeyTriggers(LocalPlayer, InputType, InputAction);
  KeyTriggers.Sort([](const FCustomKeyTrigger& A, const FCustomKeyTrigger& B)
  {
    return A.Key.IsMouseButton() == false && B.Key.IsMouseButton();
  });
```

* 반환할 FCustomKeyTrigger를 Sort하는 코드도 추가했다
  * Mouse 인풋은 다른 디바이스 인풋보다 더 뒤로...
* InputAction과 Input의 매핑이 1 : N인 경우, 위의 인풋 아이콘의 우선순위가 중요한 경우가 있었다
  * KeyTriggers를 loop로 돌면서 조건이 맞으면 즉시 return하는 구조를 변경해도 됬겠지만, 이 쪽이 더 수월해보여 이렇게 했다

## DualSense 인풋
* 기본적으로 Unreal은 어떤 InputDevice든 Wire로 연결하면 USB Wired Input Device로 받아서 인식한다
  * 그래서 서드파티 게임패드도 별 세팅없이 잘 작동하는 듯
* 하지만 DualSense는, 상기한 것처럼 무언가 더 필요하다...
  * 그걸 해주는 게 DualSense 플러그인들이다

![post_thumbnail](/assets/images/CommonUI/CommonUI_2.png)

* Wired가 필수이며, DualSense를 인식시키는 PlugIn도 필요하다
  * 상기한 Plugin이라 함은 비공식, 그러니까 ***어쩌면 안전하지 않은 플러그인***일 수도 있겠다
  * Wireless는 PS의 공식 플러그인을 지원받아야 한다는데, 이를 사용할 기회는 없었다...
    * Windows DualShock 플러그인이라고 한다
    * PS 개발자로 등록 후 LibScrePad.dll을 받아야 듀얼쇼크 및 듀얼센스 기능을 활성화할 수 있다고 한다
* GitHub에 게시된 비공식 플러그인을 사용했는데, 나중에 기회가 된다면 RawInput을 적용해보고 싶다
  * 아무 세팅도 적용하지 않고 Steam Input으로 돌리면 작동은 될까? 싶기도 하다

### 자잘한 버그 및 Troubleshooting
* DualSense를 Wired 상태로 연결하면, RecentUsedInputDevice가 계속 업데이트되는 현상이 발생했다
  * 처음에는 플러그인 이슈인줄 알았는데, 다른 출시된 게임에서도 동일한 증상을 확인했다
* DualSense를 지원하는 다른 게임을 실행하다 우리 프로젝트를 실행하면 이상한 타이밍에서 진동이 온다는 리포트가 있었다
  * 이건 다른 출시한 게임끼리에서도 발생한다니 이것 역시 DualSense 자체의 이슈인 듯
* 적절한 타이밍에서 AvtiveInput의 리스트가 Refresh 되지 앟으면, UI가 표시되어야 할 자리에 아무 이미지도 나타나지 않는다

```c++
class ENHANCEDINPUT_API UEnhancedPlayerInput : public UPlayerInput
{
  // ...

protected:

  /** This player's version of the Action Mappings */
  const TArray<FEnhancedActionKeyMapping>& GetEnhancedActionMappings() const { return EnhancedActionMappings; }
}

// ...

class UCustomEnhancedPlayerInput : public UEnhancedPlayerInput
{
  GENERATED_BODY()
  
public:
  const TArray<FEnhancedActionKeyMapping>& GetEnhancedActionMappingSet() const
  {
    return GetEnhancedActionMappings();
  }
};
```

* CustomEnhancedPlayerInput 클래스를 만들어 EnhancedActionMappings에 직접 접근할 수 있도록 했다
  * 그리고 이 ActiveMappingSet 리스트에 있는 Input 중에서만 조건 체크 후 이미지를 반환하는 로직을 추가했다
  * 기존 GetKeyTriggers 함수의 로직이 이렇게 작동하고 있었는데, GetEnhancedActionMappings 함수를 불러올 수 없어서 차선책을 썼다
* 이 방법이 상기한 ***인풋 UI가 표시되지 않는 문제***의 해결책은 아니다
  * 이게 문제라고 추측했지만, 아니었다
  * 플레이어 캐릭터의 State에 따라 IMC가 추가되었다가 제거되는 구조였는데, 이 때 UI 로드 시점이 해당 IMC가 없는 순간이면 발생하는 버그였다
  * 당시에는 타이밍을 조절해서 해결했지만, 확실하게 하려면 UI가 로드되지 않은 걸 확인하고 다시 로드하는 구조로 풀 수 있었지 않나 싶다

