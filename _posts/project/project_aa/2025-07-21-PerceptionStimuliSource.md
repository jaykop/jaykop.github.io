---
title: "[DevNote] Perception Stimuli Source"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## Perception Component
* 주로 AI의 타겟 인지 및 해제를 관리하는 목적의 컴포넌트
* 자극(stimulus)을 인지하면서 호출하는 대표적인 delegate는 아래와 같다
  * OnPerceptionUpdated
    * 자극을 처리하는 과정에서 자극을 제공한 모든 액터를 어레이로 받는다
  * OnTargetPerceptionInfoUpdated / OnTargetPerceptionUpdated
    * 위의 delegate는 모두 자극을 제공한 단일 대상에 대해 업데이트가 필요할 때 호출된다
    * 다만 OnTargetPerceptionInfoUpdated는 자극 제공 대상이 valid하지 않은 경우에도 호출된다
    * 반대로 OnTargetPerceptionUpdated는 자극 제공 대상이 valid한 경우에만 호출한다

## AIPerceptionStimuliSourceComponent
* Perception System을 통해 인지할 자극(stimulus)을 제공하는 컴포넌트
* **이 컴포넌트가 없는 Actor를 인지 못하는 것은 아니다**
  * AIPerceptionSystem은 게임을 시작하면서 모든 Pawn에 대한 자극 대상을 각 Sensor에 등록한다

```c++
void UAIPerceptionSystem::StartPlay()
{
  for (UAISense* Sense : Senses)
  {
    if (Sense != nullptr && Sense->ShouldAutoRegisterAllPawnsAsSources())
    {
      FAISenseID SenseID = Sense->GetSenseID();
      RegisterAllPawnsAsSourcesForSense(SenseID);
    }
  }

  //...
}

void UAIPerceptionSystem::RegisterAllPawnsAsSourcesForSense(FAISenseID SenseID)
{
  UWorld* World = GetWorld();
  for (TActorIterator<APawn> PawnIt(World); PawnIt; ++PawnIt)
  {
    RegisterSource(SenseID, **PawnIt);
  }
}
```

* 하지만 몇몇 함수로 Perception System에서 특정 액터를 아주 제외하거나 다시 등록할 수 있다

```c++
UFUNCTION(BlueprintCallable, Category = "AI|Perception")
AIMODULE_API void RegisterWithPerceptionSystem();

UFUNCTION(BlueprintCallable, Category = "AI|Perception")
AIMODULE_API void UnregisterFromPerceptionSystem();
```

* 이 Component를 사용한다면, 아마 위의 함수를 사용할 목적으로 class를 override해서 사용하지 않을까 싶다
* 플레이어 사망 및 부활, 그리고 테스트 단계에서 적이 플레이어 캐릭터를 인지하지 못하게 하는 치트 구현 등에 사용할 수 있다

```c++
// 현재 활성화된 AICharacter 불러와서 잡고 있는 타겟이 PlayerCharacter인지 확인하고 강제로 해제
const UActorManagerSubsystem* ActorManager = GetWorld()->GetSubsystem<UActorManagerSubsystem>();
const TArray<ACharacter*>& AICharacters = ActorManager->GetAllAICharacters();
for (auto& AICharacter : AICharacters)
{
  AAIController* AIController = Cast<AAIController>(AICharacter->GetController());
  check(AIController);
  UCustomAIPerceptionComponent* PerceptionComponent = Cast<UCustomAIPerceptionComponent>(AIController->GetAIPerceptionComponent());
  check(PerceptionComponent);
  if (PerceptionComponent->GetTargetActor() == GetOwner())
  {
    PerceptionComponent->ForceReleaseTarget();
  }
}

// Stimuli 리스트에서 제외
UnregisterFromPerceptionSystem();
```

```c++
// 현재 인지 중인 타겟 강제 해재 함수
void UCustomAIPerceptionComponent::ForceReleaseTarget()
{
  if (TargetActor.IsValid())
  {
    LostTarget(TargetActor.Get());
  }
}
```

* 다만, 이미 인지하고 있는 AI들은 UnregisterFromPerceptionSystem를 호출한다고 하더라도 Target을 유지한다
  * 그래서 현재 인지중인 Target을 명시적으로 해제해줘야 한다

## 출처
* <https://econo-my.tistory.com/39>
