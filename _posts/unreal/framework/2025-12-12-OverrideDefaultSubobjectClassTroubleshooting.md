---
title: "[DevNote] Override DefaultSubobjectClass Troubleshooting"
classes: wide
categories:
  - unreal
  - framework
sidebar:
  nav: "main"
author_profile: true
---

## Component를 다른 타입으로 교체

```c++
class AMyCharacter : public ACharacter
{
  GENERATED_BODY()
    
public:
  AMyCharacter(const FObjectInitializer& ObjectInitializer);
};

// MyCharacter.cpp
AMyCharacter::AMyCharacter(const FObjectInitializer& ObjectInitializer)
  : Super(ObjectInitializer.SetDefaultSubobjectClass<UMyCustomCapsuleComponent>(TEXT("CollisionCylinder")))
{
  // 이제 GetCapsuleComponent()는 UMyCustomCapsuleComponent를 반환
}
```
* 기본 CapsuleComponent로 사용하던 ***"CollisionCylinder"***를 UMyCustomCapsuleComponent 클래스로 교체한다
  * 여기까지 좋다..

### 복구
* 개발이 진행되면서, UMyCustomCapsuleComponent를 더 이상 사용할 필요가 없어졌다
* 그래서 UMyCustomCapsuleComponent 코드 및 파일들을 삭제하고, UCustomCapsuleComponent로 복원 했다

```c++
// MyCharacter.cpp
AMyCharacter::AMyCharacter(const FObjectInitializer& ObjectInitializer)
  : Super(ObjectInitializer)
{
    
}
```

* 위와 같이 ***복원해주면 될 줄 알았다***
* 그런데 게임을 실행하니, 크래시가 발생했다
  * 정확히는, GetCapsuleComponent 즉, CollisionCylinder에 접근하니 nullptr이 반환되었다
* 캐릭터의 Blueprint에서 확인하니, RootComponent도 "CollisionCylinder"가 아닌 그냥 "RootComponent"로 명명되어 있었다

### 해결 방법?
* 삭제한 UMyCustomCapsuleComponent 파일들을 복구만 해줘도, 정상적으로 작동했다
  * 프로젝트에서 제외됐으면 다시 추가해주든지, 휴지통에 버렸다면 다시 복원해주든지...
  * UMyCustomCapsuleComponent를 다시 사용할 필요는 없고, 진짜 그냥 .h, .cpp만 복원해주면 된다
* 영향을 받은 Blueprint들을 켜서 CollisionCylinder의 DefaultClass를 모두 수동으로 UCapsuleComponent로 변경한 뒤 저장해줬다

### 해결 방법2
* 그런데 다른 pc에서 pull을 받고 확인해보니, 또 몇몇 BP 클래스에서는 여전히 CapsuleComponent 접근 시 nullptr을 반환하는 문제가 발생했다
  * 해당 BP도 CollisionCylinder의 DefaultClass가 수동으로 제대로 변경되었는지는 확인하기 어려웠다
  * **그래서 그냥 BP를 다시 만들었다**
* 그래서 결론은... **DefaultComponent의 타입을 변경하려 한다면, 신중히 결정해야 할 것이라는 거다**
  * 예전 프로젝트에서도 AIController 쪽에서 PathFollowingComponent를 UCrowdFollowingComponent로 바꾼 뒤 복구했다가 같은 문제를 겪었다
  * 앞으로는 진짜 좀 조심해야지..