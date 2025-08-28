---
title: "Hard Reference & Soft Reference"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## Asset을 참조할 때의 Hard Reference와 Soft Reference

### Hard Reference
* 로드할 오브젝트의 경로 같은 문자열 형태의 간접 매커니즘을으로 오브젝트 A가 오브젝트 B를 참조하게 만드는 참조
1. TSoftObjectPtr를 사용해 프로퍼티를 String으로 저장해 에셋을 수동으로 로드한다
```c++
UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category=Building)
TSoftObjectPtr<UStaticMesh> BaseMesh;

// 실행 시간에 Mesh를 지연시켜 로드
UStaticMesh* GetLazyLoadedMesh()
{
    if (BaseMesh.IsPending())
    {
        const FSoftObjectPath& AssetRef = BaseMesh.ToStringReference();
        BaseMesh = Cast< UStaticMesh>(Streamable.SynchronousLoad(AssetRef));
    }
    return BaseMesh.Get();
}
```

2. 런타임에서 String을 만들어 그 오브젝트로의 Reference를 구하려는 경우
* 이미 생성 또는 로드된 UObject 만 사용하려는 경우, FindObject<>() 사용
* 이미 로드되어 있지 않은 오브젝트를 로드하려면, LoadObject<>() 사용
  * LoadObject<>()는 내부적으로 FindObject와 동일한 역할을 하므로, Find 후 Load를 할 필요가 없다

### Soft Reference
* 오브젝트 A가 오브젝트 B를 참조하여, 오브젝트 A를 로드할 시 오브젝트 B도 함께 로드되게 만드는 참조
1. UPROPERTY 매크로를 통해 노출
```C++
/** construction start sound stinger */
// 이를 테면, 아래 멤버 변수를 갖고 있는 클래스 A는
// 생성할 때마다 월드에 배치한 인스턴스와 연결 
// 또는 블루프린트 상속을 통해 지정할 수 있다
UPROPERTY(EditDefaultsOnly, Category=Building)
USoundCue* ConstructionStartStinger;
```
2. 프로퍼티를 생성의 일부로 설정
* 프로그래머가 에셋을 로드할 타이밍을 알고, 어떤 오브젝트를 생성할 때 그 생성 과정에서 추가적으로 에셋을 로드하도록 설정
```c++
UPROPERTY()
class UTexture2D* BarFillTexture;

// 아래 ConstructorHelpers는 메모리에서 에셋을 미리 탐색한 뒤, 없으면 로드한다
// 불가피하게 nullptr로 설정되는 경우, 텍스쳐로 접근하면 크래시가 발생한다
AStrategyHUD::AStrategyHUD(const FObjectInitializer& ObjectInitializer) :
    Super(ObjectInitializer)
{
    static ConstructorHelpers::FObjectFinder<UTexture2D> BarFillObj(TEXT("/Game/UI/HUD/BarFill"));

    ...

    BarFillTexture = BarFillObj.Object;

    ...

}
```
* 오브젝트가 로드 및 초기화되면서 강 참조인 에셋도 함께 로드되는데, 다수의 에셋이 한꺼번에 로드되어 메모리가 부족해지는 경우가 발생할 수 있다

### 그래서 Sotf Reference란?
* 쉽게 설명하자면 존재할지 안할지 모르는 에셋 또는 오브젝트에 대한 참조하는 것이며, 이 과정에서 로딩은 없다
* 오브젝트가 있는지 없는지는 게임 혹은 프로그램에 ***큰 영향***을 주지 않는다
  * null check를 통해 처리가 가능하고, 이후 진행에도 별 문제가 없다
* 에셋의 경우에는 런타임에서도 존재하지 않는 경우가 있고 이를 위해 약 참조가 사용된다
  * 최적화를 위해 아직 필요하지 않은 게임의 일부를 로드하지 않는다든가...

### Asset Redirector의 역할과 생성 시점은?
* Redirector - 이름 혹은 경로가 변경된 Asset을 가리키던 Reference를 현재 위치로 재지정해주는 오브젝트
  * 오브젝트의 이름 혹은 경로가 변경되면서 오류가 발생할 수 있다
  * 따라서 **Fix Redirectors**로 이를 재지정해주어야 한다
* UE의 Contents Browser에서 파일을 옮기거나 이름을 변경할 때마다 Redirector가 자동으로 생성된다
  * 이 때 [Core Director](https://www.unrealdirective.com/articles/core-redirectors-what-you-need-to-know)를 통해 Redirector 세팅을 수동으로 재지정해야 한다

## 출처
* <https://docs.unrealengine.com/4.26/ko/ProgrammingAndScripting/ProgrammingWithCPP/Assets/ReferencingAssets/>
* <https://hyo-ue4study.tistory.com/435>
* <https://docs.unrealengine.com/4.27/ko/ProductionPipelines/Redirectors/>
* <https://forums.unrealengine.com/t/can-someone-explain-soft-variable-references/444524/2>