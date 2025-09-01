---
title: "Anim Layer로 캐릭터 상태별 Locomotion 관리"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## Linked Anim Layer
* 하나의 AnimBP에서 캐릭터가 필요한 모든 상태 관리를 할 수도 있다
  * 하지만 동일한 상태에 대해 다른 애니메이션, 다른 로직이 필요하다면?
  * 캐릭터가 그냥 달리는 애니메이션과, 무기를 들고 달리는 애니메이션이 달라야 한다면?
  * State Machine 구조는 동일한데 애니메이션만 다르다

### Anim Layer Interface
* Anim BP에서 애니메이션을 오버라이드 할 수 있는 기능
* Base AnimBP는 State Machine과 애니메이션 플로우 등 주요 구조를 유지하고, 실제 애니메이션 출력 등 세부 로직은 Link된 AnimLayer에서 실행하게 할 수 있다
* 사용하려면 Base AnimBP와 오버라이드하는 AnimLayer 모두 이 ALI를 추가해야 한다

### 무기 교체 시 애니메이션 교체 플로우

![post_thumbnail](/assets/images/ALS/ALS_AnimLayer_1.png)

* ABP_ALSCharacter
* 로직의 구조 및 플로우 등이 구현되어 있는 Anim Instance다
* 실제 로직이 포함될 AnimLayer와 동일한 ALSInterface를 가진다

![post_thumbnail](/assets/images/ALS/ALS_AnimLayer_2.png)

* ABP_ALSCharacterAnimLayer
* 여기에도 Base Anim Instance와 동일한 ALSInterface를 가진다
  * 이 프로젝트의 경우에는, 노드의 실제 구현부는 Override하는 이 Layer에 있었다

![post_thumbnail](/assets/images/ALS/ALS_AnimLayer_3.png)

* ABP_ALSCharacterAnimLayer를 상속한 BP를 추가한다
  * 가장 Leaf 단계의 Anim BP이다
  * 이 BP에는 실제로 출력할 애니메이션을 할당한다
  * 로직은 중간 단계인 ABP_ALSCharacterAnimLayer, 출력 애니메이션은 이 BP
  * 무기별, 상태별 다른 Locomotion이 필요한 경우 ABP_ALSCharacterAnimLayer를 상속해 여러 BP를 생성해 사용했다

```c++
void UAbilityTask_SetWeaponAnimLayer::DoTask()
{
  if(RepOwner.IsValid())
  {
    if (UCustomCharacterComponent* CharacterComponent = FL::GetActorComponent<UCustomCharacterComponent>(RepOwner.Get()))
    {
      const EActionStanceType ActionStance = (WeaponActionType == EWeaponActionType::Undraw) ? EActionStanceType::Normal : EActionStanceType::Battle;
      if(bForceChange)
      {
        CharacterComponent->ForceLinkAnimClassLayer(ActionStance);
      }
      else
      {
        CharacterComponent->LinkAnimClassLayer(ActionStance);
      }
    }
  }
}

void UCustomCharacterComponent::LinkAnimClassLayer(EActionStanceType NewActionStanceType)
{
  // ...

  switch (NewActionStanceType)
  {
    case EActionStanceType::Normal:
    {
      AnimLayerClass = CharacterTableRow->CharacterFoundationDataSet->NormalAnimLayerClass.Get();
    }
    break;
      
    case EActionStanceType::Battle:
    {
      const EWeaponType CurrentWeaponType = FL::GetCurrentWeaponType(GetOwner());
      
      // ...

      if (auto Founder = CharacterTableRow->CharacterFoundationDataSet->WeaponAnimLayerClasses.Find(CurrentWeaponType))
      {
        AnimLayerClass = Founder->Get();
      }
    }
    break;
  }


  if (AnimLayerClass)
  {
    ActionStanceType = NewActionStanceType;
    OwnerCharacter->GetMesh()->LinkAnimClassLayers(AnimLayerClass);
  }
}
```

* 실제 사용할 AnimLayer를 적용한다
  * 무기 교체 시, GameplayAbility를 통해 착용하고 있던 무기를 Undraw 하는 애니메이션을 재생한다
  * 동시에 GameplayAbilityTask로 AnimLayer를 교체하는 Task 실행한다
  * 전투 <-> 비전투 상태 변경 시에도 동일하게 작동한다

