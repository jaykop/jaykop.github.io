---
title: "Update Function"
classes: wide
categories: 
  - post
  - Unity
sidebar:
  nav: "main"
author_profile: true
---

## Update의 비용

![image](/assets/images/updateFunction.png)

* Monobehaviour이 Enable한 상태하면 매 프레임마다 호출하는 함수
* gameobject가 많아질수록 이 함수의 호출도 많아진다

## Resolution?

```csharp
private CustomUpdateBehaviour[] customUpdateBehaviour;

private void Update()
{
  foreach (var obj in customUpdateBehaviour)
    obj.CustomUpdate();
}
```

* Update를 호출해야 할 object가 너무 많다면, 이들을 통합해서 관리하는 Manager를 구현하라
  * 그리고 그 Update를 사용하라

```csharp
private void Start()
{
  StartCoroutine(UpdateCoroutine());
}

private IEnumerator UpdateCoroutine()
{
  // update something...
}
```

* Coroutine을 사용할 수도 있다

* 위의 방법으로 일반 Update를 호출하는 방식보다 훨씬 적은 비용이 든다
* 아무것도 하지 않는 Update를 호출하는 것만으로도 비용은 발생한다
  * 사용하지 않는 업데이트 함수는 반드시 제거할 것

### Update를 선언하지 않으면 작동하지 않는가?
* Update 함수가 선언되어 있지 않으면 호출되지 않는다
  * 선언되어 있으면 비어있는 함수라도 호출된다
* Mono 혹은 IL2CPP가 MonoBehaviour에 접근해 파악하고 그 정보를 캐싱한다
  * 이 MonoBehaviour의 메서드는 알맞은 호출 리스트에 들어가게 되고, Unity는 이 리스트를 iterate한다

## Update 함수가 호출되는 순서 (IL2CPP)
![image](/assets/images/table5.png)

1. 유니티가 모든 업데이트할 모든 Behaviour를 iterate한다
  * iterate 도중 후위의 Behaviour가 삭제되는 게 아니라는 가정하에
2. 유니티가 호출한 메서드를 validate한다
  * 이 유효성 검사는 gameObject가 active되어 있고, 초기화되었으며, Started 함수가 불린 데 한해서 시행된다
3. 네이티브로에서 Managed쪽 함수를 호출하기 위해 ScriptingInvocationNoArgs와 ScriptingArguments객체가 생성되고 메서드를 Invoke하기 IL2CPP VM을 정렬한다
4. 인수 체크 IL2CPP VM이 Runtime:Invoke를 호출한다
  * 메서드 자체가 있는지 확인하고
  * method signature를 위해 생성된 RuntimeInvoker를 call
  
### method signature
* 함수 이름과 param list
* 함수의 declaration 부분

## Update 함수 사용은 반드시 지양해야 하는가?
* 상황에 알맞게 사용하는 것이 중요하지, 사용하지 않는다고 능사는 아니다
  * Input 키의 Up/Down을 확인하는 것과 같은 것은 문제가 되지 않는다
  * 하지만 ***매 프레임 호출되어야 하는지 의문을 가질 필요***는 있다
* GetComponent나 GameObject.Find 함수를 매 프레임 사용하는 것이 퍼포먼스에 더 치명적이다

## new in Update
* 새로운 class를 매 프레임 객체 생성하는 것은 퍼포먼스에 엄청난 영향을 미친다
  * 매번 새로운 객체가 heap에 쌓이게 될 것이다
  * Garbage Collector가 메모리를 회수할 때까지 기다려야 하고, GB가 바쁘게 일하도록 만든다
  * 이는 스레드가 멈추도록 하는 문제를 발생시킨다

### value type은?
* 대표적으로 Vector는 value type이므로, new 를 사용해 객체를 생성하면 stack에 할당된다
  * 객체 생성 및 파괴 소요가 적다
* 재사용 가능한 buffer를 둬도 상관없다

## 출처
* <https://thegamedev.guru/unity-ui/sprite-vs-image/>
* <https://www.reddit.com/r/Unity3D/comments/4mh51a/how_to_avoid_using_update/>
* <https://blog.unity.com/technology/1k-update-calls>
* <https://velog.io/@leehs27/UpdateCallsCost>
* <https://bradkeys.com/2017/01/30/Avoiding-Unity-Update-Loops/>
* <https://www.thoughtco.com/method-signature-2034235>
* <https://gamedev.stackexchange.com/questions/138574/is-it-wrong-to-be-creating-new-objects-in-update>
* <https://www.reddit.com/r/Unity3D/comments/2b5rtp/should_i_create_reusable_vector2vector3_objects/>
* <https://forum.unity.com/threads/vector3-and-other-structs-optimization-of-operators.477338/>