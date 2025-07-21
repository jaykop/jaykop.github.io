---
title: "Unreal Behavior Tree"
classes: wide
categories: 
  - post
  - Unreal
  - A.I.
sidebar:
  nav: "main"
author_profile: true
---

## Behavior Tree Service
* Composite 혹은 Task에 Attach 되어 분기가 실행중인 동안 정의된 빈도로 실행
* **Blackboard 값 확인 및 업데이트 목적으로 사용**

### Default Focus
* 

### Run EQS
* 

### Custom Service
* **블루프린트 서비스는 C++ 서비스에 비해 퍼포먼스가 떨어진다고 한다**
	* 최적화가 중요하다면 네이티브 서비스를 사용하는 것이 좋다

```c++
void UBTService::OnBecomeRelevant(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
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

void UBTService::OnCeaseRelevant(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
	// ...
	
	FBTEnemyMasterServiceMemory* MyMemory = CastInstanceNodeMemory<FBTEnemyMasterServiceMemory>(NodeMemory);
	ASC->UnregisterGameplayTagEvent(MyMemory->GameplayTagEventHandle, Tags.Status.OutOfControl, EGameplayTagEventType::NewOrRemoved);
}
```

* Attach된 노드가 활성화 또는 비활성화 되는 시점에 태그 업데이트를 감지하는 람다를 등록해서 블랙보드 값을 변경할 수도 있다
* 블루프린트로는 위의 로직을 구현하기 어렵다
	* 적어도 난 그랬다...

## Behavior Tree Decorator


## 출처
* https://dev.epicgames.com/documentation/ko-kr/unreal-engine/unreal-engine-behavior-tree-node-reference-services
* 