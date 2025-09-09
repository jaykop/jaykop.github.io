---
title: "[Unreal] MassSystem"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## Mass System

![post_thumbnail](/assets/images/MassEntity/MassEntity_1.png)
![post_thumbnail](/assets/images/MassEntity/MassEntity_2.png)

* Fragment라는 이름의 데이터로 구성된 Mass Entity를 Processor가 구현된 로직대로 처리하는 시스템
  * [ECS 구조](https://jaykop.github.io/post/unity/ECS/)로 동작한다

**Fragment**
* 로직에 사용할 최소한의 데이터 단위

**Archetype**
* Fragment의 조합으로 정의된 타입

**Entity**
* 특정 Archetype의 객체(instance)

**Chunk**
* 메모리상으로 Entity들이 배치된 데이터 블록

**Chunk Fragment**
* Fragment는 아키타입 또는 Entity에 대응하는 데이터 단위다
* Chunk는 Chunk 블록에 대응하는 데이터 단위다
	* 즉, 같은 Chunk 내의 Entity 모두가 공유하는 데이터

### Processor
* Fragment로 프로세싱 로직을 실행하는 클래스

```c++
void UMassEntitySettings::BuildProcessorList()
{
	ProcessorCDOs.Reset();
	for (FMassProcessingPhaseConfig& PhaseConfig : ProcessingPhasesConfig)
	{
		PhaseConfig.ProcessorCDOs.Reset();
	}

	TArray<UClass*> SubClassess;
	GetDerivedClasses(UMassProcessor::StaticClass(), SubClassess);

	for (int i = SubClassess.Num() - 1; i >= 0; --i)
	{
		if (SubClassess[i]->HasAnyClassFlags(CLASS_Abstract))
		{
			continue;
		}

		UMassProcessor* ProcessorCDO = GetMutableDefault<UMassProcessor>(SubClassess[i]);
		// we explicitly restrict adding UMassCompositeProcessor. If needed by specific project a derived class can be added
		if (ProcessorCDO && SubClassess[i] != UMassCompositeProcessor::StaticClass()
#if WITH_EDITOR
			&& ProcessorCDO->ShouldShowUpInSettings()
#endif // WITH_EDITOR
		)
		{
			ProcessorCDOs.Add(ProcessorCDO);
			if (ProcessorCDO->ShouldAutoAddToGlobalList())
			{
				ProcessingPhasesConfig[int(ProcessorCDO->GetProcessingPhase())].ProcessorCDOs.Add(ProcessorCDO);
			}
		}
	}

	ProcessorCDOs.Sort([](UMassProcessor& LHS, UMassProcessor& RHS) {
		return LHS.GetName().Compare(RHS.GetName()) < 0;
	});
}

void FMassPhaseProcessorConfigurationHelper::Configure(TArrayView<UMassProcessor* const> DynamicProcessors
	, EProcessorExecutionFlags InWorldExecutionFlags, const TSharedPtr<FMassEntityManager>& EntityManager
	, FMassProcessorDependencySolver::FResult* OutOptionalResult)
{
	FMassRuntimePipeline TmpPipeline(InWorldExecutionFlags);
	TmpPipeline.CreateFromArray(PhaseConfig.ProcessorCDOs, ProcessorOuter);

  // ...
}
```

* Processor 클래스를 생성하면 CDO를 수집해서 리스트에 넣고, 이 리스트를 순회하며 Processor 객체를 만들어 사용한다

```c++
 UCLASS()
class UGroundCheckProcessor : public UMassProcessor
{
 	GENERATED_BODY()

public:
	UGroundCheckProcessor();

protected:
	virtual void ConfigureQueries() override;
	virtual void Execute(FMassEntityManager& EntityManager, FMassExecutionContext& Context) override;

  FMassEntityQuery GroundCheckQuery;

  // ...
};

void UGroundCheckProcessor::ConfigureQueries()
{
	GroundCheckQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadWrite);
	GroundCheckQuery.AddRequirement<FMZMassGravityFragment>(EMassFragmentAccess::ReadWrite);
	GroundCheckQuery.AddRequirement<FMassRepresentationFragment>(EMassFragmentAccess::ReadOnly);
	GroundCheckQuery.AddSharedRequirement<FMassRepresentationSubsystemSharedFragment>(EMassFragmentAccess::ReadWrite);
	GroundCheckQuery.RegisterWithProcessor(*this);
}
```

* Entity는 Processor가 쿼리로 요구하는 Fragment 혹은 Tag를 가지고 있어야 한다

**엔티티 쿼리(Entity Query)**
* 프로세서가 지정하는, 작업 수행에 필요한 Fragment 타입

![post_thumbnail](/assets/images/MassEntity/MassEntity_3.png)

* Mass Entity Configuration(MEC) 에셋을 통해 Entity에 Fragment를 등록한다
* MEC에서는 Entity에 부여할 Trait을 할당한다

**Trait**
* Trait은 로직 구동 시 필요한 Fragment와 Processor의 묶음이다

> [!NOTE] Fragment와 Tag의 차이?  
> * Tag는 정보의 여부 표기, 이른바 flag (존재 여부 자체가 데이터로 활용된다)  
> * Entity를 데이터로 제어하고자 할 경우 Fragment를 사용  

```c++
void UGroundCheckProcessor::Execute(FMassEntityManager& EntityManager, FMassExecutionContext& Context)
{
  // ...

  // 쿼리로  Mass entity 싹 순회
  GroundCheckQuery.ForEachEntityChunk(EntityManager, Context, [this, World, NavSys, &EntityManager](FMassExecutionContext& Context)
      {
        
        // ...

        for (int32 EntityIndex = 0; EntityIndex < NumEntities; ++EntityIndex)
        {
          // ...
        }

        // ...
		  }
	  });
  // ...
}
```

* 요구되는 타입별 핸들을 쿼리에 등록하고 Context에서 타입에 해당하는 Fragment 데이터 접근
* EntityChunk는 같은 구조(같은 Fragment/Tag)를 가진 Entity들을 묶어 둔 메모리 블록
  * 블록을 받아온 다음 개별 엔ㄷ티티에 접근해 루프를 돈다

### Evaluator

![post_thumbnail](/assets/images/MassEntity/MassEntity_4.png)
![post_thumbnail](/assets/images/MassEntity/MassEntity_5.png)

* 파라미터 또는 컨텍스트 데이터로는 StateTree에 제공할 수 없었던 데이터에 접근을 제공
* StateTree에 시작 및 중지 시, 그리고 각 틱마다 커스텀 코드를 실행

```c++
struct FAIStateEvaluator : public FMassStateTreeEvaluatorBase
{
	GENERATED_BODY()

	using FInstanceDataType = FAIStateEvaluatorInstanceData;

	FAIStateEvaluator();

protected:
	virtual bool Link(FStateTreeLinker& Linker) override;
	
  // ..
  
	TStateTreeExternalDataHandle<FStatFragment> StatFragmentHandle;
};

bool FAIStateEvaluator::Link(FStateTreeLinker& Linker)
{
	Linker.LinkExternalData(StatFragmentHandle);

	return true;
}

```

* Evaluator에서 사용할 Fragment의 struct 타입을 핸들로 등록
* StateTree에서 Tick 수행
  * 변수 최신화
  * 따로 interval을 부여해 관리할 필요까지는 없다

### Task

```c++
struct FChangeStateTask : public FMassStateTreeTaskBase
{
	GENERATED_BODY()

	using FInstanceDataType = FMZChangeStateTaskInstanceData;

protected:
	virtual bool Link(FStateTreeLinker& Linker) override;
  
  // ...

	TStateTreeExternalDataHandle<struct FTransformFragment> TransformHandle;
	TStateTreeExternalDataHandle<struct FMassMoveTargetFragment> MoveTargetHandle;
	TStateTreeExternalDataHandle<struct FStatFragment> StatFragmentHandle;
};

bool FChangeStateTask::Link(FStateTreeLinker& Linker)
{
	Linker.LinkExternalData(TransformHandle);
	Linker.LinkExternalData(MoveTargetHandle);
	Linker.LinkExternalData(StatFragmentHandle);
	
	return true;
}
```

* Task에서 사용할 Fragment의 struct 타입을 핸들로 등록
  * Evaluator와 동일하게 FStateTreeNodeBase strcut로부터 상속한 구조체