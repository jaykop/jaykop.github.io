---
title: "클래스 Deprecated 처리하기"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

```c++
UCLASS(BlueprintType, Deprecated)
class CLIENT_API UDEPRECATED_CameraBehaviorDataAsset: public UDataAsset
{
  GENERATED_BODY()

  public:
    UPROPERTY(EditAnywhere, meta=(ShowOnlyInnerProperties))
    FCameraBehaviorData CameraBehavior;
};
```

* 기존에 사용하던 클래스를 통째로 Deprecated 처리해야 하는 경우, UCLASS 매크로에 Deprecated를 넣어주면 된다.
* 위의 클래스는 DataAsset 용도의 클래스였는데, 새로운 에셋을 만들 경우 노출되지 않았다
* 클래스의 이름 역시 prefix로  UDEPRECATED_ 를 붙여  UDEPRECATED_CameraBehaviorDataAsset 로 수정해줘야 하는데,이 때 내부 데이터가 날아가지는 않았다.