---
title: "[DevNote] CollisionResponse Troubleshooting"
classes: wide
categories:
  - unreal
  - framework
sidebar:
  nav: "main"
author_profile: true
---

### 문제 상황
* 언리얼 엔진 5.4 버전에서 Projectile Movement Component 사용 시, 전 게임에 걸쳐서 액터들의 Collision Response가 오염되는 현상

### 원인과 해결

```c++
struct FSuggestProjectileVelocityParameters
{
  // ...
  
  public:
    FCollisionResponseParams& ResponseParam = FCollisionResponseParams::DefaultResponseParam; 
}
```

* 위의 구조체에서, ResponseParam 변수를 레퍼런스로 받으면서 프로젝트 전체의 Collision이 의도한 세팅과 다르게 영구적으로 달라진다
* 이슈는 [리포트](https://issues.unrealengine.com/issue/UE-224510) 되었지만, ~~문서 작성일 기준으로 아직 해결되지 않았다~~
* ~~5.8 릴리즈 타겟으로 수정 예정이라고 적혀있는데, ~~ 현재 릴리즈된 엔진 5.6 이상에서는 해당 코드가 수정된 것으로 확인
* 문제 상황 당시에는 엔진 프로젝트로 직접 관리하고 있었어서 해당 코드를 수정하는 걸로 해결

## Default Collision Preset
* 위 내용과 상관은 없지만, 같은 이슈를 트래킹하면서 알게된 내용이라 여기에 남긴다

![post_thumbnail](/assets/images/CollisionResponseTroubleshooting/01.png)  

* 엔진에서 정의하는 Default라는 이름의 Collision Preset은 대체 뭘까?  
* 코드를 확인해보니, 각 액터의 생성자에서 지정한 CollisionProfileName은 Default로 표기되는 듯하다  

```c++
AStaticMeshActor::AStaticMeshActor(const FObjectInitializer& ObjectInitializer)
  : Super(ObjectInitializer)
{
  // ...

  StaticMeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(StaticMeshComponentName);
  StaticMeshComponent->SetCollisionProfileName(UCollisionProfile::BlockAll_ProfileName);
)
```
* StaticMeshActor를 하나 레벨에 배치하면 Default로 표기되지만, 코드를 확인해보면 위와 같이 실제로는 BlockAll을 사용하고 있다
  * 헷갈리게 해놨네...