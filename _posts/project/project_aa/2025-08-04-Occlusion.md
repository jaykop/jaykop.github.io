---
title: "[DevNote] 카메라를 가리는 장애물 투명화"
classes: wide
categories: 
  - project
  - project_aa
sidebar:
  nav: "main"
author_profile: true
---

## 문제 상황
* 카메라와 캐릭터 사이에 어떤 장애물이 있고, 시야를 가리는 오브젝트가 특정 타입인 경우 이 오브젝트를 투명화 시켜야 했다
* 그런데, 게임 내의 대부분의 레벨 액터는 Nanite Naterial을 사용 중이다

### Nanite의 Opacity?
* 일반적인 경우, 캐릭터의 Pivot과 카메라 중점 사이 공간을 체크해 HitResult가 있으면 그 오브젝트들의 Opacity 값을 낮추는 알고리즘으로 작동할 것이다
* 이런 로직을 적용하려고 했는데, 레벨에 배치된 StaticMesh가 전부 Nanite를 사용하면 문제가 있다
  * **Nanite는 작성일 기준으로 Translucent 모드를 지원하지 않는다.** 
    * 즉, 투명도를 변경하는 기능을 지원하지 않는다
  * Material Mode를 Translucen로 세팅하면 기본 텍스쳐가 표시되어 버린다

> [!NOTE]
> * 작성일 기준 GameplayCamera Plugin에서도 카메라 장애물 감지 알고리즘은 유사하다  
> * Ray거 어나러 Sphere로 체크하고, 모든 Object가 아닌 카메라에 가장 가까운 1개 Object만 투명화한다는 차이가 있다  

### Nanite Override Material
* Material Instance 에디터에서 bDisallowNanite 토글 세팅을 조정하면, 자동으로 Material을 Override할 것을 기대했다
  * 실제로 Override를 하긴 하지만, refresh가 되지 않았다
  * MF나 Material에 업데이트를 주고 저장을 누르면 그제서야 적용이 되었다
  * 그리고 그 상태가 계속 유지된다

```c++
bool HideActor(FCameraOccludedActor& OccludedActor)
{
  // NonNanite Material로 변경
  if (UStaticMeshComponent* StaticMesh = Cast<UStaticMeshComponent>(OccludedActor.Mesh))
  {
    StaticMesh->bDisallowNanite = true;
  }

  bool bOcclude = false;
  const int32 NumOfMaterials = OccludedActor.Mesh->GetNumMaterials();
  OccludedActor.Materials.Empty();
  for (int32 Idx = 0; Idx < NumOfMaterials; ++Idx)
  {
    OccludedActor.Materials.Add(OccludedActor.Mesh->GetMaterial(Idx));
    UMaterialInstanceDynamic* DynMaterial = OccludedActor.Mesh->CreateAndSetMaterialInstanceDynamicFromMaterial(Idx, OcclusionMaterial);
  
    // 투명화 처리하는 Material을 사용하는지 여부 확인
    // inline static const FName NAME_OCCLUDED = TEXT("bOccluded");
    float OutValue = 0.f;
    const bool bHasParam = DynMaterial->GetScalarParameterValue(NAME_OCCLUDED, OutValue);
    bOcclude |= bHasParam && OutValue == 1.f;
    OccludedActor.Mesh->SetMaterial(Idx, DynMaterial);
    OccludedActor.DynMaterials.Add(DynMaterial);
  }

  return bOcclude;
}
```

* 그래서 결곡 NonNanite일 때의 Material을 불러와 Dynamic Material Instance를 생성해 사용하는 로직을 추가했다
  * 액터의 UID를 Key로 하고 FCameraOccludedActor를 Value로 갖는 Map을 관리한다
* 이 Map을, 매 Tick 카메라를 가렸다고 판단하는 액터 목록과 비교하고, Opcaity 값 또는 기타 상태 관리가 필요한 플래그를 업데이트 해준다
* Mesh 투명도를 조정하는 쪽에 부하가 큰 것으로 알고 있는데, 레벨 디자인 차원에서 어떤 오브젝트가 추명화될 것이고 어떤 오브젝트가 카메라 Boom 길이를 자르는 방식으로 처리할 것인지 등 기획도 보강하면 더 퍼포먼스를 기대할 수 있을 것 같다

### 기타 문제점
* Opacity 조절 시 그림자도 같이 사라져버리는 이슈가 있다.
  * Material -> Cast Shadow as Masked 토글을 체크하고 LightingMode를 Surface Transparency Wolume으로 변경하니 해결되었다
* Mesh가 겹치는 부분 등으로 인해 일부가 투명화 되지 않는 현상도 있었다
  * Backface Culling으로 보이지 않아도 되는 면의 Surface는 가리는 방법으로 해결했다

## Dithering
* 단순히 Opacity를 낮추는 것이 아닌, Material을 듬성듬성 오비지 않게 처리하는 방법도 시도했다
  * 그런데 이 때는 디더링 처리된 오브젝트 너머로 움직이는 액터가 있을 때, 고스팅 즉 잔상을 남기는 현상이 발생했다
* 안티얼라이징 세팅을 TAA/TSR -> FXAA로 변경하지 훨씬 찾아들었다
  * 하지만 프로젝트가 Nanite 및 Lumen을 사용하므로, 이에 최적화된 TSR을 사용하는 것이 맞다는 결론에 따라 안티얼라이징 세팅은 변경하지 못했다
* Opacity Mask Clip Value를 조절하면 일부 잦아들긴 하지만, 해결 수준은 아니었다


