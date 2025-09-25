---
title: "[Unreal] Node Memory"
classes: wide
categories: 
  - post
  - Unreal
  - game_ai
sidebar:
  nav: "main"
author_profile: true
---

## BT를 사용하는 인스턴스의 데이터 캐싱 
* AI 캐릭터들이 BT를 사용하면서, 인스턴스 별로 가져야 할 데이터가 있다
  * Target과의 거리를 기록해두어야 한다든가..
  * Timer를 재기 위해 체크하는 현재 남은 시간이라든가..
  * 즉, 캐싱(Cache)을 해야 하는 데이터가 있을 것이다

### Member 변수로 저장해도 되는가?

```c++
UCLASS()
class MYGAME_API UBTTask_MyCustomTask : public UBTTaskNode
{
    GENERATED_BODY()

public:
  // ...

private:
  // ...

  // 남은 시간
  float ElapsedTimer = 0;
}

EBTNodeResult::Type UBTTask_MyCustomTask::TickTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
    Super::TickTask(OwnerComp, NodeMemory, DeltaSeconds);
    // ...

    // 이렇게 해도 되나??
    ElapsedTimer -= DeltaSeconds;

    // ...
    return EBTNodeResult::InProgress;
}
```

* BT를 사용하는 Instance가 ElapsedTimer를 체크하고 특정 행동을 해야한다고 하자
* 위와 같이 Task의 멤버변수로 두고 관리하는 게 맞을까?
  * **당연히 안된다**
* **여러 AI가 같은 BTTask 인스턴스를 공유하기 때문**
  * member 변수 값이 덮어씌울 수 있다
  * 이로써 다른 AI의 행동에 의도치 않은 영향을 미칠 수 있다

### 올바른 방법은?

**Blackboard**
* Blackboard의 데이터는 객체 별로 관리되므로 안전한 방법이다
  * 단, 캐싱해야 하는 데이터가 너무 많은 경우에는 관리가 힘들어질 수 있다

**Pawn/Controller**
* AI Controller나 Controlled Pawn에 필요한 변수들을 선언하고 접근할 수도 있다
  * 데이터가 원래 해당 클래스에 있다면 상관없겠지만, 상관없는 데이터를 넣어둔다면 구조적으로 별로다

**NodeMemory 사용**

```c++
UCLASS()
class MYGAME_API UBTTask_MyCustomTask : public UBTTaskNode
{
    GENERATED_BODY()

public:
    // NodeMemory 구조체 정의
    struct FMyTaskMemory
    {
        AActor* TargetActor;
        float StartTime;
        bool bIsInitialized;
        
        FMyTaskMemory()
        {
            TargetActor = nullptr;
            StartTime = 0.0f;
            bIsInitialized = false;
        }
    };

    virtual uint16 GetInstanceMemorySize() const override;
    virtual EBTNodeResult::Type ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) override;
    virtual EBTNodeResult::Type AbortTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) override;
};

// BTTask_MyCustomTask.cpp
uint16 UBTTask_MyCustomTask::GetInstanceMemorySize() const
{
    return sizeof(FMyTaskMemory);
}

EBTNodeResult::Type UBTTask_MyCustomTask::ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
    FMyTaskMemory* MyMemory = reinterpret_cast<FMyTaskMemory*>(NodeMemory);
    
    if (!MyMemory->bIsInitialized)
    {
        // 초기화 로직
        MyMemory->TargetActor = /* 타겟 찾기 로직 */;
        MyMemory->StartTime = GetWorld()->GetTimeSeconds();
        MyMemory->bIsInitialized = true;
    }
    
    // 메모리의 데이터 사용
    if (MyMemory->TargetActor)
    {
        // 작업 수행
    }
    
    return EBTNodeResult::InProgress;
}
```

* C++을 사용할 수 있다면 이것이 가장 일반적이고 안전한 방법이다
  * Blueprint로는 사용할 수 없는 듯하다
* BT의 Task, Decorator, Service 등 여러 타입에 대해서 NodeMemory를 인스턴스 별로 관리할 수 있다
* 복잡도에 따라 위의 3가지 중 1가지 방법을 선택해 사용하면 된다고 하는데, Blueprint로만 작업한느 환경이 아니라면 기능 의존성을 고려해 NodeMemory 기능을 구현하는 것이 가장 적절해 보인다