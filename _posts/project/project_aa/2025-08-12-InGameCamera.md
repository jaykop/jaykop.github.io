---
title: "[DevNote] InGame Camera"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## ALS Plugin 카메라

![post_thumbnail](/assets/images/Camera/Camera_1.png)

* 기존 ALS 플러그인에서 사용하는 카메라 데이터를 확장해 사용하고 있었다
* CameraComponent를 사용하지 않고, CameraManager를 상속해 로직을 확장했다
* Camera 전용 AnimBlueprint를 만들어 카메라 State 간의 트랜지션을 관리했다
  * Animation에서 Blending 하는 로직을 응용한 것이다
  * Modify Curve 노드를 이용해 각 변수들의 값이 Target을 향해 Interpolocation 된다

### CameraComponent 없어도 되는 거였나

```c++
void APlayerCameraManager::UpdateViewTarget(FTViewTarget& OutVT, float DeltaTime)
{
  // ...
  else
  {
    UpdateViewTargetInternal(OutVT, DeltaTime);
  }
  // ...
}

void APlayerCameraManager::UpdateViewTargetInternal(FTViewTarget& OutVT, float DeltaTime)
{
  if (OutVT.Target)
  {
    // ...

    else
    {
      OutVT.Target->CalcCamera(DeltaTime, OutVT.POV);
    }
  }
}

void AActor::CalcCamera(float DeltaTime, FMinimalViewInfo& OutResult)
{
  if (bFindCameraComponentWhenViewTarget)
  {
    // ...
    for (UCameraComponent* CameraComponent : Cameras)
    {
      if (CameraComponent->IsActive())
      {
        CameraComponent->GetCameraView(DeltaTime, OutResult);
        return;
      }
    }
  }

  // ...
}
```

* CameraComponent가 실제로 카메라에 영향을 미치려면 APlayerCameraManager의 UpdateViewTarget 함수를 통해 CalcCamera에서 OutResult의 값을 변경해주는 플로우로 진행해야 된다
* 그러나 ALSPlayerCamera에서 UpdateViewTargetInternal 함수를 호출하지 않고 있다
  * PlayerController는 당연히 CameraManager 클래스로 ALSPlayerCamera를 상속한 CustomPlayerCamera를 쓰는 중
* FTViewTarget는 CameraComponent의 존재 여부와 상관없이 APlayerCameraManager에 의해 관리 및 프로세싱 되고 있다
  * 카메라 로직을 PlayerCameraManager 안에서만 관리하고 싶었나 보다...

## 카메라 기획
* 카메라 구도 기획 단계에서 몇몇 조건이 필요했다
  * 캐릭터의 상태(비전투, 전투, 특수 액션 등) 케이스별로 구도를 잡을 수 있어야 한다
  * 몇몇 캐릭터 상태는 게임 전체에 걸쳐 동일한 값을 사용하지만, 또 몇몇은 무기 혹은 지역에 따라 바뀐다
  * Base가 되는 구도가 있고, 그 구도를 기준으로 Offset을 추가하거나 Override 하는 방식이어야 했다

### 카메라 State와 트랜지션 

```c++
USTRUCT(BlueprintType)
struct FCameraViewData
{
  GENERATED_BODY()

public:
  static FCameraViewData Interp(const FCameraViewData& Source, const FCameraViewData& Target, float DeltaTime, float InterpSpeed);
  static bool IsDoneInterp(const FCameraViewData& Source, const FCameraViewData& Target);

  FCameraViewData operator+(const FCameraViewData& RHS) const;
  void SetAsDefault();
  
public:
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Offset")
  FVector CameraOffset = FVector(-350.f, 0.f, 75.f);

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Offset")
  FVector PivotOffset = FVector::ZeroVector;

  // 카메라가 피봇을 따라가는 스피드
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Lag Speed")
  FVector PivotLagSpeed = FVector(5.f, 5.f, 15.f);

  // 카메라 회전 속도 - 이동모드에서의 기본값은 20이다. 이 값이 너무 작을 경우 카메라의 회전이 너무 늦게 따라와서 조작이 불편할 수도 있음. 사격모드에서는 20을 유지하도록 하자.
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Lag Speed")
  float RotationLagSpeed = 15.f;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FOV", AdvancedDisplay)
  float CameraFOV = 90.f;

  // 카메라가 최대로 올려다볼 수 있는 각도 
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Pitch",DisplayName="PitchMax", meta=(UIMin=-89.9f, UIMax=89.9f, ClampMin=-89.9f, ClampMax=89.9f))
  float CameraPitchMax = 89.f;
  
  // 카메라가 최대로 내려다볼 수 있는 각도 
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Pitch",DisplayName="PitchMin", meta=(UIMin=-89.9f, UIMax=89.9f, ClampMin=-89.9f, ClampMax=89.9f))
  float CameraPitchMin = -89.f;
};
```
* 기본 인게임 백뷰 카메라 데이터 구조는 위와 같다
  * 하드락인 경우에는 별도의 구조체 데이터를 사용한다

<figure class="half">
    <a href="/assets/images/Camera/Camera_2.png"><img src="/assets/images/Camera/Camera_2.png"></a>
    <a href="/assets/images/Camera/Camera_3.png"><img src="/assets/images/Camera/Camera_3.png"></a>
</figure>

* AnimGraph에서는 BlendPoses 노드나 BooleanPoses를 사용해 전환
* State 안에서트 Transition을 사용해 전환한다
* State 변경 시, 변경할 State 값을 미리 가지고 있다
  * AnimGraph에서는 Pose Cache로 Target State Value를 정의한다
  * State 안에서는 각 값에 대한 Target을 ModifyCurve 노드로 정의한다
* 다행히 게임 전체에 걸쳐 State와 구도가 1:1인 경우에는 이렇게 할 수 있다
  * 그런데 State와 사용할 구도가 1:N인 경우라면?

### 같은 State, 다른 구도
* 캐릭터는 크게 전투, 비전투 State를 나눠 구도를 관리한다
* 전투 상황은 Walk, Run, Sprint 3가지 상태로 각각 구분한다
* 그런데 이 3가지 상태를 무기별로 다른 구도로 적용하고 싶다는 기획 요청이 있었다
  * 이게 위에서 설명한 State와 카메라 구도의 1:N 상황이다

```c++
void UCustomALSPlayerCameraBehavior::NativeUpdateAnimation(float DeltaSeconds)
{
  Super::NativeUpdateAnimation(DeltaSeconds);

  if (IsValid(CameraBehaviorDataAsset))
  {
    // Interp 하지 않거나 Interp를 하다가 완료한 경우에는 중도 return
    if (bTickInterp == false
      || (IsDoneInterp() && bTickInterp))
    {
      bTickInterp = false;
      return;
    }
    
    CurrentBehavior.NormalView_VelocityDirection_Default = FCameraViewData::Interp(CurrentBehavior.NormalView_VelocityDirection_Default,
      CameraBehaviorDataAsset->CameraBehavior.NormalView_VelocityDirection_Default.GetViewData(), DeltaSeconds, BehaviorBlendSpeed);
    CurrentBehavior.NormalView_VelocityDirection_Running = FCameraViewData::Interp(CurrentBehavior.NormalView_VelocityDirection_Running,
      CameraBehaviorDataAsset->CameraBehavior.NormalView_VelocityDirection_Running.GetViewData(), DeltaSeconds, BehaviorBlendSpeed);
    
    // ...
  }
}
```

* 코드로 일일이 밀어넣어줘야 했다
  * 모든 데이터를 캐싱할 수는 없으니까..
  * 결국 초기화 타이밍 이외에 다시 알맞은 데이터 에셋으로부터 값을 읽어와야 한다
* 또 특정 지역이나 이벤트 발생으로 인한 인게임 카메라 구도는 Stack으로 관리 즉 누적된다는 기획 요청도 있었다

```c++
UCLASS(Blueprintable, BlueprintType)
class UCustomPlayerCameraBehavior : public UALSPlayerCameraBehavior
{
  // ...
  // 카메라 적용 및 해제
  const FCameraInfoHandle& AddCameraBehavior(const FCameraInfo& CameraInfo);
  void RemoveCameraBehavior(const struct FCameraInfoHandle& CameraInfoHandle);
  void ClearCameraBehaviors();
  bool HasCameraBehavior(const FCameraInfoHandle& CameraInfoHandle);

  // ...
  protected:
    void ApplyCameraInfo();

  // ...

  UPROPERTY(Transient)
  TArray<struct FCameraInfo> CameraStack;
  // ...
}
```

* AnimInstance에서 카메라 데이터를 누적 관리하는 구조체를 만들고, 할당 및 해제가 필요한 경우를 처리했다
* 어떤 카메라 데이터를 가지고 있는지 여부 확인 및 카메라 우선순위에 따라 Sort하는 등의 이유로 Stack 대신 Array를 사용했다
  * 레벨에 배치한 지역 카메라 볼륨, 특정 몬스터와 전투 시 구도 변경 레벨 이벤트 호출 등 타입이 있었고 이에 따른 우선순위가 달랐다

```c++
const FCameraInfoHandle& UCustomPlayerCameraBehavior::AddCameraBehavior(const FCameraInfo& CameraInfo)
{
  CameraElements.Add(CameraInfo);
  ApplyCameraInfo();
  return CameraInfo.Handle;
}

void UCustomPlayerCameraBehavior::ApplyCameraInfo()
{
  // Array에 카메라 데이터 남아있다면 남아있는 것 중 최우선 순위의 카메라 데이터 적용
  CameraElements.Sort(FCameraInfo::FSortPredicate());
  if (CameraElements.IsEmpty() == false)
  {
    CameraBehaviorDataAsset = CameraElements[0].CameraBehaviorAsset;	
  }
  // 없으면 기존 카메라로 복귀
  else
  {
    CameraBehaviorDataAsset = DefaultCameraBehaviorDataAsset;
  }

  // ...
}

void UCustomPlayerCameraBehavior::RemoveCameraBehavior(const struct FCameraInfoHandle& CameraInfoHandle)
{
  // ...

  if (CameraInfoHandle.IsValid())
  {
    // ...

    // 카메라 데이터 삭제
    CameraElements.RemoveAll([&CameraInfoHandle] (const FCameraInfo& Element)
    {
      return Element.Handle == CameraInfoHandle;
    });
    
    CameraElements.Sort(FCameraInfo::FSortPredicate());
  }

  // ...
  
  // 지연 삭제가 아니라면 즉시 적용
  ApplyCameraInfo();	
  
  // ...
}

bool UCustomPlayerCameraBehavior::HasCameraBehavior(const struct FCameraInfoHandle& CameraInfoHandle)
{
  if (CameraInfoHandle.IsValid())
  {
    CameraElements.FindByPredicate([&CameraInfoHandle] (const FCameraInfo& Element)
    {
      return Element.Handle == CameraInfoHandle;
    });
  }
  
  return false;
}
```

* 위의 메서드들이 카메라 구도 적용 및 해제 상황에서 CameraAnimInstance를 통해 직접 호출된다
* 카메라 데이터 할당 시 Handle을 생성하고 구조체가 Handle을 가지고 있으며, 탐색 시 Handle로 구분하도록 했다
  * Map으로 할 수도 있었겠지만, Array로 Sort한 결과를 그대로 쓰는게 더 쉬울 듯

### 기본 카메라 응용 기능

![post_thumbnail](/assets/images/Camera/Camera_4.png)

* 상기한 카메라 구조체는 하나의 데이터 에셋으로서 존재한다

![post_thumbnail](/assets/images/Camera/Camera_5.png)

* 그리고 이런 하나의 카메라 구도 에셋을 여러 개 모아 상황별 카메라 데이터 에셋을 만든다

![post_thumbnail](/assets/images/Camera/Camera_6.png)

* 이 데이터 에셋에서 기준이 되는 카메라 구도 + 오프셋 혹은 오버라이드가 필요하다
* 위 그림에서 Loaded View Data + View Data Offset = View Data 로 연산된다
  * View Data가 실제 인게임에서 로드되어 적용할 카메라 데이터이다
  * 에디터 상에서 Loaded View Data의 값이 바뀌면 View Data도 바뀌어야 한다

```c++
void UCameraBehaviorDataBundleAsset::PostEditChangeChainProperty(FPropertyChangedChainEvent& PropertyChangedEvent)
{
  const bool bChangedViewDataOffset = FindEqualFieldName(PropertyChangedEvent, TEXT("ViewDataOffset"));
  
  // 일반 번들의 ViewDataAsset가 변경된 경우
  if (PropertyChangedEvent.Property->GetName() == TEXT("ViewDataAsset")
    || bChangedViewDataOffset)
  {
    for (TFieldIterator<FStructProperty> CameraBehaviorPropIt(FCameraBehaviorDataBundle::StaticStruct())
      ; CameraBehaviorPropIt; ++CameraBehaviorPropIt)
    {
      const FString FieldName = *CameraBehaviorPropIt->GetName();
      const bool bIsEqualProperty = FindEqualFieldName(PropertyChangedEvent, FieldName);
      if (FCameraViewDataBundle* ViewDataBundle = CameraBehaviorPropIt->ContainerPtrToValuePtr<FCameraViewDataBundle>(&CameraBehavior)
        ; nullptr != ViewDataBundle && bIsEqualProperty)
      {
        ViewDataBundle->Refresh();
        
        Super::PostEditChangeChainProperty(PropertyChangedEvent);
        return;
      }
    }
  }
  
  Super::PostEditChangeChainProperty(PropertyChangedEvent);
}

bool UCameraBehaviorDataBundleAsset::FindEqualFieldName(FPropertyChangedChainEvent& PropertyChangedEvent, const FString& FieldName) const
{
  auto* ChainNode = PropertyChangedEvent.PropertyChain.GetTail();
  while (ChainNode != nullptr)
  {
    if (const auto* ChainNodeValue = ChainNode->GetValue())
    {
      const FString PropertyName = ChainNodeValue->GetName();
      if (PropertyName.Equals(FieldName))
      {
        return true;
      }
    }
    
    ChainNode = ChainNode->GetPrevNode();
  }

  return false;
}
```

* 위의 DataAsset 클래스는 ViewDataBundle이라는 구조체를 들고 있다
* ViewDataOffset에 변경이 있거나, 변경이 있는 에셋의 이름이 ViewDataAsset이라고 판단되는 경우, ViewDataBundle에서 Refresh 함수를 호출한다

```c++
USTRUCT(BlueprintType)
struct FCameraViewDataBundle
{
  GENERATED_BODY()

  // ...
  
#if WITH_EDITOR
  // 번들의 ViewData가 변경되는 경우, LoadedData를 변경하기 위해 사용하는 함수
  void Refresh();

private:
  void OnUpdateViewData();
#endif
  
public:	
  UPROPERTY(EditAnywhere, Category=DataAsset, BlueprintReadOnly, meta=(ShowOnlyInnerProperties))
  TObjectPtr<class UCameraViewDataAsset> ViewDataAsset = nullptr;

  UPROPERTY(VisibleAnywhere, Category=DataAsset, BlueprintReadOnly)
  FCameraViewData LoadedViewData;
  
  UPROPERTY(EditAnywhere, Category=Offset, BlueprintReadOnly)
  FCameraViewData ViewDataOffset;

  // ...
}

#if WITH_EDITOR
void FCameraViewDataBundle::Refresh()
{
  if (IsValid(ViewDataAsset))
  {
    if (!RefreshHandle.IsValid())
    {
      // 해제 시 할당된 이벤트 제거하기 위해 포인터 버퍼 저장
      BufferPtr = ViewDataAsset;
      RefreshHandle = ViewDataAsset->OnViewDataChanged.AddRaw(this, &FCameraViewDataBundle::OnUpdateViewData);
    }
    
    OnUpdateViewData();
  }
  // 핸들에 람다식이 할당되어 있다면 해제한다
  else if (RefreshHandle.IsValid() && IsValid(BufferPtr))
  {
    BufferPtr->OnViewDataChanged.Remove(RefreshHandle);
    RefreshHandle.Reset();
  }
}

void FCameraViewDataBundle::OnUpdateViewData()
{
  if (IsValid(ViewDataAsset))
  {
    // 에셋 데이터로부터 보여줄 데이터에 로드 및 오프셋과 더해 최종 값 연산
    LoadedViewData = ViewDataAsset->CameraView;
    ViewData = LoadedViewData + ViewDataOffset;
  }
}
#endif
```

* Refresh는 최종 값이 ViewData를 업데이트하기 위해 OnUpdateViewData를 호출한다
* 또 Base가 되는 ViewDataAsset의 값이 변경되는 타이밍을 잡기 위해 Delegate 할당도 한다
* 이 때 할당된 Delegate는 OnUpdateViewData로, ViewData를 다시 연산하는 함수다

```c++
UCLASS(BlueprintType)
class UCameraViewDataAsset : public UDataAsset
{
  GENERATED_BODY()

#if WITH_EDITOR
public:
  virtual void PostEditChangeProperty(FPropertyChangedEvent& PropertyChangedEvent) override;
#endif
  
public:
  UPROPERTY(EditAnywhere, meta=(ShowOnlyInnerProperties))
  FCameraViewData CameraView;
  
#if WITH_EDITORONLY_DATA
  FOnCameraViewDataAssetChanged OnViewDataChanged; 
#endif
};

#if WITH_EDITOR
void UCameraViewDataAsset::PostEditChangeProperty(FPropertyChangedEvent& PropertyChangedEvent)
{
  Super::PostEditChangeProperty(PropertyChangedEvent);

  if (OnViewDataChanged.IsBound())
  {
    OnViewDataChanged.Broadcast();	
  }
}
#endif
```

* 카메라 데이터의 값 변경이 발생하면 할당한 Delegate를 실행한다
  * 이 카메라 데이터를 사용하고 있는 DataAsset에서 연산을 다시 하는 역할이다

## 다시 카메라 시스템을 만든다면
* 기본적으로 A <-> B State를 2개만 두고 전환시킬 것 같다
* 이렇게 하면 A -> B로 전환할 때
  * 전환될 값을 B state에 미리 할당한다
  * Blend는 AnimGraph든 Transition을 통해서 하고
* 메시지 시스템으로 카메라 데이터 적용 및 해제
  * 메서드와 변수를 직접 접근하고 노출하다보니 코드간의 의존성이 높아졌다
  * GmaeplayMessage Plugin을 카메라 시스템 구현 후 적용했다
  * 우선순위가 낮아 카메라 시스템에 GmaeplayMessage를 적용하지 못했지만, 도입했다면 더 깔끔하게 만들 수 있었을 것 같다