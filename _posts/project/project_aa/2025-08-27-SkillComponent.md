---
title: "Character Skill"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## Skill Data

```c++
UENUM(BlueprintType)
enum class ESkillState : uint8
{
  None = 0,
  Added,      // 스킬이 추가된 상태. 미장착
  Equipped,		// 스킬이 장착된 상태. 비활성 상태. 예: A 무기 스킬이면서 스킬트리에서 장착. 그러나 현재 무기는 B
  Activated,	// 스킬이 활성화 된 상태. 
};

USTRUCT(BlueprintType)
struct FSkillData
{
  GENERATED_BODY()

  // 진짜 Skill 정보 접근 GUID
  UPROPERTY()
  FGuid SkillJournalID;
  
  UPROPERTY()
  TWeakObjectPtr<class USkillJournal> SkillJournal;
  
  UPROPERTY()
  int32 CurrentSkillLevel = 0;

  UPROPERTY()
  int32 MaxSkillLevel = 0;

  UPROPERTY()
  ESkillState SkillState = ESkillState::None;
};
```

* 위의 Skill Data는 실제 스킬 정보보다는, 그 정보에 접근할 수 있는 포인터를 가진다
  * 실제 Skill 정보는 별도의 데이터 형식으로 관리했다 (DataTable, 또는 Journal)
  * 그리고 이 **실제 Skill 정보**는 출력시킬 Abl과 조건, 이름, Description 정보 등을 가진다
* 또한 해당 Skill의 상태를 enum으로 구분했다

> [!NOTE]  
> 이게 조금 직관적이지 않다는 생각이 아직도 든다  
> 버그 상황이긴 하지만 A 무기 착용 시 B 무기 전용 스킬이 출력되는 현상이 있었다  
> 출력 조건에서 현재 무기 타입을 체크하고 출력하는 게 더 낫지 않았을까?  
> 그럼 State 하나가 줄어들고 타입을 boolean으로 변경할 수 있을 것 같은데...  

### Skill Journal

```c++
UCLASS(meta=(DisplayName="Skill"))
class AACLIENT_API USkillJournal : public UJournalContainerEntry
{
  GENERATED_BODY()
  
public:

  //...

  UPROPERTY(EditDefaultsOnly, BlueprintReadOnly)
  int32 ID;

  // 활성화되어 있어야 할 Skill Node ID, 없으면 세팅 안 하면 됨...
  UPROPERTY(EditDefaultsOnly, BlueprintReadOnly)
  TArray<int32> ActivatePrerequisiteIDs;
  
  UPROPERTY(EditAnywhere)
  FText DisplayName;

  UPROPERTY(EditDefaultsOnly, meta=(categories="Skill"))
  FGameplayTagContainer SkillTraits;
  
  // ...
  
  // 스킬 실행 시 실행할 Able
  // Active Skill
  UPROPERTY(EditAnywhere)
  TSubclassOf<class UAblAbility> SkillAbl;
  
  // 스킬 장착 시 실행할 GA
  // Passive Skill
  UPROPERTY(EditAnywhere)
  TArray<TSubclassOf<class UGameplayAbility>> SkillGA;
  
};
```

* 위의 Skill Data는 Skill Journal(DT의 일종) 타입으로서, 실제 Skill 정보들이 정의되어 있다
* 실행할 Abl, 선행 스킬 ID 목록, Icon 이미지, Trait, Granted GA 등이 여기에 포함된다
  * 특히 Skill Trait은, 태그로서 Skill의 Passive/Active, Slot1/Slot2 등 스킬 고유의 속성을 

## Skill Component
* 플레이어의 스킬을 관리하는 컴포넌트
  * PlayerState의 Component
* 스킬 추가, 제거, 상태 변경 등 기능
  * 무기 등 장비 변경과 UI를 통한 스킬 변경 등 메시지를 받는다

> [!NOTE]  
> 처음 Skill 객체를 Item으로 만들어 Inventory에서 관리하도록 했는데, 이는 잘못된 선택이었던 듯...  
> 단순히 Skill의 습득 여부 이외에도 상태 관리를 별도로 해줘야 한다는 점에서 굳이 아이템과 동일하게 처리할 필요는 X  
> 괜히 Item Category만 늘어나고 관리만 더 힘들어졌다...  

### Skill 실행

```c++
bool UComboNode::CanSelect() const
{
  UComboNodeData* NodeData = CastChecked<UComboNodeData>(ComboNodeData);
  UAblComponent* AblComponent = FL::GetActorComponent<UAblComponent>(OwnerActor);
  if (IsValid(NodeData) && IsValid(AblComponent))
  {
    // ...
    
    // NodeData가 가진 스킬 정보에 접근해 State 확인
    if (APlayerState* PlayerState = FL::GetPlayerState(OwnerActor))
    {
      if (USkillComponent* SkillComponent = PlayerState->FindComponentByClass<USkillComponent>())
      {
        return SkillComponent->IsSkillActivated(NodeData->Journal.Guid);
      }
    }

    // ...
  }

  return false;
}
```

* 실제로 스킬을 출력하는 부분은 ComboComponent
  * ComboComponent에서 ComboAseet을 통해 CurrentNode 실행
  * CurrentNode는 정의된 데이터에 Skill 정보가 있는지 확인

```c++
bool UComboNode::Select()
{
  if (UAblAbility* AblCDO = GetAblAbility())
  {
    if (UAblComponent* AblComponent = FL::GetActorComponent<UAblComponent>(OwnerActor))
    {
      UAblAbilityContext* AblAbilityContext = UAblAbilityContext::MakeContext(AblCDO, AblComponent, OwnerActor, OwnerActor->GetInstigator());
      check(AblAbilityContext);
      
      if (UComboNodeData* NodeData = CastChecked<UComboNodeData>(ComboNodeData))
      {
        AblAbilityContext->SetCopyFromPrevAblContext(NodeData->bCopyTargetsFromPrevNode);	
      }

      AblCDO->SetupTargeting(AblAbilityContext);

      EAblAbilityStartResult Result;
      if(ComboAsset->IsComboPlaying())
      {
        Result = AblComponent->BranchAbility(AblAbilityContext);
      }
      else
      {
        Result = AblComponent->ActivateAbility(AblAbilityContext);
      }

      if(Result == EAblAbilityStartResult::Success)
      {
        Super::Select();
        return true;
      }
    }
  }

  return false;
}
```

* 실행 로직은 어차피 ComboNode가 가지고 있는 Abl 데이터를 AblComponent를 통해 실행시키는 로직
  * Skill을 실행하든 일반 공격을 실행하든 동일하다