---
title: "[DevNote] Mouse Select & Hover"
classes: wide
categories: 
  - project
  - project_o
sidebar:
  nav: "main"
author_profile: true
---

### 마우스로 인게임 오브젝트를 Hover하거나 Select 해야하는 상황
* 보통은 이 경우에 Screen 좌표상에서 InGame World로 Deprojection을 통해 Ray를 쏴서, 해당 Ray에 Hit되는 첫번째 Object를 반환하는 것 같다
* Select야 Mouse 클릭할 때만 하면 된다지만, 이 방식대로라면 Hover는 매번 Ray를 쏴야한다

### PrimitiveComponent 탑재 기능

```c++
UCLASS(abstract, HideCategories=(Mobility, VirtualTexture), ShowCategories=(PhysicsVolume), MinimalAPI)
class UPrimitiveComponent : public USceneComponent, public INavRelevantInterface, public IInterface_AsyncCompilation, public IPhysicsComponent
{
	GENERATED_BODY()

  // ...

	/** Event called when the mouse cursor is moved over this component and mouse over events are enabled in the player controller */
	UPROPERTY(BlueprintAssignable, Category="Input|Mouse Input")
	FComponentBeginCursorOverSignature OnBeginCursorOver;
		 
	/** Event called when the mouse cursor is moved off this component and mouse over events are enabled in the player controller */
	UPROPERTY(BlueprintAssignable, Category="Input|Mouse Input")
	FComponentEndCursorOverSignature OnEndCursorOver;

	/** Event called when the left mouse button is clicked while the mouse is over this component and click events are enabled in the player controller */
	UPROPERTY(BlueprintAssignable, Category="Input|Mouse Input")
	FComponentOnClickedSignature OnClicked;

	/** Event called when the left mouse button is released while the mouse is over this component click events are enabled in the player controller */
	UPROPERTY(BlueprintAssignable, Category="Input|Mouse Input")
	FComponentOnReleasedSignature OnReleased;

  // ...
}
```

* PrimitiveComponent에는 마우스 감지에 대한 이벤트를 이미 처리하고 있다
  * Generates Overlap Event 활성화 필수 및 Visibility Channel로 감지했던 걸로 기억한다
* InGame Object를 마우스로 상호작용 처리해야하는 상황이 있다면 이를 사용하는 방법도 고려할만하다