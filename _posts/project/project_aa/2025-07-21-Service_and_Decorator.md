---
title: "Service & Decorator 커스터마이즈"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## Behavior Tree Service
* Composite 혹은 Task에 Attach 되어 분기가 실행중인 동안 정의된 빈도로 실행
* **Blackboard 값 확인 및 업데이트 목적으로 사용**
  * TaskNode를 통해서 업데이트 하기도 한다

```c++
void UCustomBTService::OnBecomeRelevant(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
  // ...

  FBTEnemyMasterServiceMemory* MyMemory = CastInstanceNodeMemory<FBTEnemyMasterServiceMemory>(NodeMemory);

  auto UpdateMovementRestriction = [BlackboardComponent, MovementRestrictionKeyName = MovementRestrictionKey.SelectedKeyName](const FGameplayTag InTag, int32 NewCount)
  {
    if(NewCount > 0)
    {
      BlackboardComponent->SetValueAsBool(MovementRestrictionKeyName, true);
    }
    else
    {
      BlackboardComponent->SetValueAsBool(MovementRestrictionKeyName, false);
    }
  };

  // ASC를 통해 Tags.Status.OutOfControl 태그가 추가 또는 제거될 때마다 해당 람다 호출
  MyMemory->GameplayTagEventHandle = ASC->RegisterGameplayTagEvent(Tags.Status.OutOfControl, EGameplayTagEventType::NewOrRemoved).AddWeakLambda(&OwnerComp, UpdateMovementRestriction);

  // 현 시점의 상태 체크 후 업데이트
  int32 TagCount = ASC->GetTagCount(Tags.Status.OutOfControl);
  UpdateMovementRestriction(Tags.Status.OutOfControl, TagCount);
}

void UCustomBTService::OnCeaseRelevant(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
  // ...
  
  FBTEnemyMasterServiceMemory* MyMemory = CastInstanceNodeMemory<FBTEnemyMasterServiceMemory>(NodeMemory);
  ASC->UnregisterGameplayTagEvent(MyMemory->GameplayTagEventHandle, Tags.Status.OutOfControl, EGameplayTagEventType::NewOrRemoved);
}
```

* 위와 같이 특정 태그가 AI Actor에 할당 또는 제거되는 타이밍에 태그 업데이트를 감지하는 람다를 등록해서 블랙보드 값을 변경할 수도 있다
  * 위의 코드는 MovementRestrictionKeyName가 Boolean이고, 이 Boolean 값을 체크하는 TaskNode가 마스터 BT의 맨 앞에 있어서 BT의 실행을 멈추거나 재개하는 역할을 했다
  * 특수 상황 시 코드에서 BrainComponent를 Pause하거나 Resume하기보단, BT 에셋에서 확인이 가능하므로 보다 직관적이고 유연하다
  * 비단 BT를 멈추는 것 뿐만 아니라, TaskNode의 우선순위를 어떻게 배치하느냐에 따라 다른 행동 패턴을 추가할 수도 있다
* 블루프린트로는 위의 로직을 구현하기 어려웠다 (적어도 난 그랬다)
  * Custom Service의 경우 BP 구현 시 C++ Service 보다 오버헤드가 더 커서 성능에 더 큰 영향을 미친다고 한다
  * BP화하면서 BT Service의 유연성을 제공하고자 하더라도, 위의 코드는 남기는 것이 좋아보였다

## Behavior Tree Decorator

### Observer aborts
* None - 아무것도 중단하지 않는다
* Self - 자신과 Child 노드, Subtree를 모두 중단한다
* Low Priority - 이 노드의 오른쪽 (동일 Level이면서 후순위 노드)의 노드를 중단한다
* Both - Self, Low Priority에 해당하는 것들을 중단한다

### Notify Observer
* Decorator가 Blackboard의 값을 기반으로 이하 노드로 진입할지 여부를 결정하는 조건의 형태
* On Result Change는 동일한 값으로의 변경을 감지하지 않는다
* On Value Change는 동일한 값으로의 변경도 감지한다

### OnBecomeRelevant
* 평가를 진행할 때 호출
  * Service, Decorator 등에서 실행
* OnCeaseRelevant로 마감 처리

### OnNodeActivation
* 노드가 실제로 실행될 때 호출
  * 주로 TaskNode에서 실행
* OnNodeDeactivation로 마감 처리

### Decorator의 역할
* Decorator는 결국 TaskNode에 Attach되어 TaskNode의 실행 조건을 검사하는 역할을 한다
* 그래서 몇몇 Decorator를 제외하고, UObject화된 Condition 객체를 받아 이 조건을 검사하는 Decorator_CheckCondition을 만드는 게 효율적이라 생각했다

```c++
class UBTDecorator_CheckCondition : public UBTDecorator_BlackboardBase
{
  GENERATED_BODY()

public:
  UAABTDecorator_CheckCondition(const FObjectInitializer& ObjectInitializer);

// ...

protected:
  UPROPERTY(EditAnywhere, Instanced)
  class UAACondition* DecoratorCondition;

// ...

bool UBTDecorator_CheckCondition::CalculateRawConditionValue(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const
{
  if (IsValid(DecoratorCondition))
  {
    AActor* SelfActor = OwnerComp.GetAIOwner()->GetPawn();
    AActor* TargetActor = nullptr;
    if (UBlackboardComponent* BlackboardComponent = OwnerComp.GetBlackboardComponent())
    {
      TargetActor = Cast<AActor>(BlackboardComponent->GetValueAsObject(BlackboardKey.SelectedKeyName));	
    }
    
    FConditionContext ConditionContext = FConditionContext::MakeContext(SelfActor, TargetActor);
    return DecoratorCondition->CheckCondition(ConditionContext);	
  }

  return false;
}
```

* 위와 같은 커스텀 Decorator를 만들고, DecoratorCondition에서 특정 Condition을 선택해 조건을 확인하는 구조다
* 이렇게 하면 새로운 Decorator를 만드는 대신, 새로운 Condition 구조체만 추가하면 된다
  * CheckCondition 함수가 virtual이기 때문에 FConditionContext를 받아 여러 방식의 조건으로 커스텀할 수 있다
  * SelfActor와 TargetActor만 있으면 대부분의 상황에서 조건 확인이 가능해서, 일단 Context 내용은 저 2개 뿐이다
* 이 작업을 하면서 CustomCondition 구조체를 프로젝트 내의 모든 조건이 필요한 상황에서 사용할 수 있도록 범용적으로 만드려 했지만, 불가능하다는 걸 알았다
  * BT, ABL, Dialogue 등 기능과 상황에 맞게 사용하고자 하는 Condition이 모두 달랐다
  * Condition 구조체를 모두 사용할 수 있게 하면, 오히려 불필요하거나 사용 불가능한 Condition도 선택지에 포함되어 혼란을 야기했다
  * 코드 사이드에서 조건을 체크하는 함수는 Function Library화해서 범용적으로 두고, 각 Condition은 Wrapper 역할로 두어 분명히 구분하는 것이 더 효율적이라는 결론


## 출처
* <https://dev.epicgames.com/documentation/ko-kr/unreal-engine/unreal-engine-behavior-tree-node-reference-services>
