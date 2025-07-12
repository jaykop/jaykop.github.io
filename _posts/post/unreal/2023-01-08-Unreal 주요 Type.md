---
title: "Unreal 주요 Type"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## UCLASS와 USTRUCT의 차이?
* 각 매크로는 Reflection 시스템에 클래스와 구조체를 등록하는 데 사용한다
  * Unreal Editor가 사용자 정의의 클래스 또는 구조체를 인식하기 위한 방법이다
* 메모리 관리 시스템에 포함시켜 Garbage Collection할 수 있도록 한다
* UHT(Unreal Header Tool)이 C++ 헤더 파일을 찾고, Unreal 매크로 관련 코드를 생성한다
* 결과 코드를 C++ 컴파일러가 컴파일한다

### UCLASS
```C++
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
// UHT에 의해 생성된 코드를 포함
#include "TutoProjectCollectable.generated.h"

UCLASS(Blueprinatble, BlueprintType)
class TUTOPROJECT_API UTestUClass : public UObject
{
  // UHT에서 자동으로 constructor 를 declaration & define
	GENERATED_BODY()
	
};
```
* **Blueprinatble**
  * 이 Class를 상속해서 새로운 Blueprint를 생성할 수 있다
* **BlueprintType**
  * 이 Class를 Blueprinte의 멤버 변수 설정할 수 있다

### USTRUCT
```C++
USTRUCT(BlueprintType)
struct FStructExample
{
  GENERATED_BODY()

public:
  
  UPROPERTY(EditAnywhere, BlueprintReadWrite)
  int32 IntegerVariable;
  
  UPROPERTY(EditAnywhere, BlueprintReadWrite)
  float FloatVariable;
  
  //Other variables...
};
```

## 게임에서 UObject, Actor xkdlqdml 객체를 순회하는 방법
### Actor 순회
```c++
// 특정 타입의 Actor를 순회할 때
for (TActorIterator<AActor> ActorIt(GetWorld()); ActorIt; ++ActorIt)
{
  AActor* MyActor = *ActorIt;
}
// 또는
for (const auto& ActorIt: TActorRange<AActor>())
{
  AActor* MyActor = *ActorIt;
}

// 모든 Actor를 순회할 때
for (FActorIterator(GetWorld()) ActorIt; ActorIt; ++ActorIt)
{
  AActor* MyActor = *ActorIt;
}
// 또는
for (const auto& ActorIt: FActorRange(GetWorld()))
{
  AActor* MyActor = *ActorIt;
}
```

* Unreal은 Built-In Actor Iteractor가 있다
  * 당연히 매 프레임 사용하지 않는다
  * 로딩 씬 등에서만 사용한다 

### UObject 순회
```c++
// 특정 타입의 Object를 순회
const UWorld* MyWorld = GetWorld();
for (TObjectIterator<UObject> ObjectIter; ObjectIter; ++ObjectIter)
{
  if (ObjectIter->GetWorld() != MyWorld)
  {
    continue;
  }
  else
  {
    // do something...
  }
}
// 또는
for (const auto& ObjectIter: TObjectRange<UObject>(GetWorld()))
{
  if (ObjectIter->GetWorld() != MyWorld)
  {
    continue;
  }
  else
  {
    // do something...
  }
}

// 모든 Object를 순회할 때
for (FObjectIterator ObjectIter; ObjectIter; ++ObjectIter)
{
  if (ObjectIter->GetWorld() != MyWorld)
  {
    continue;
  }
  else
  {
    // do something...
  }
}
// 또는
for (const auto& ObjectIter: FObjectRange(GetWorld()))
{
  if (ObjectIter->GetWorld() != MyWorld)
  {
    continue;
  }
  else
  {
    // do something...
  }
}
```

* UObject Iterator는 UWorld를 참조하지 않고, **메모리상에 존재하는 모든 UObject를 순호**한다
  * 에디터에서 실행중인 게임이라면 editor-only object, 멀티 게임 중이라면 다른 클라이언트의 Object 등까지도 순회하는 데 쓰일 수 있다
  * 그러나 일반적으로는 사용자 게임에서 존재하는 Object만 참조하는 경우가 많으므로, World를 확인하고 로컬에만 한정하도록 필터링할 수 있다

## UE에서 사용하는 타입 이름의 Prefix
**[Coding Stanrad](https://docs.unrealengine.com/5.0/en-US/epic-cplusplus-coding-standard-for-unreal-engine/#namingconventions)**
**[권장하는 에셋 명명 규칙](https://oceandrive.atlassian.net/wiki/spaces/~630b86f46856bdd60a9e1bef/pages/732135435)**
* 탬플릿 클래스 - T
* UObject에서 파생 - U
* AActor에서 파생 - A
* SWidget에서 파생 - S
  * Slate Widget의 Base 클래스
* Abstract Interface 파생 - I
* 열거형 - E
* bool 변수 - b
* C++ 베이스 - F

## 출처
* <https://romeroblueprints.blogspot.com/2020/11/the-ustruct-macro.html>
* <https://romeroblueprints.blogspot.com/2020/10/the-uclass-macro.html>
* <https://forums.unrealengine.com/t/what-is-generated-h-header-file/346873>
* <https://bbagwang.com/unreal-engine/ue4-%EC%97%90%EC%84%9C%EC%9D%98-property-system/>