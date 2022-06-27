---
title: "Update의 비용"
classes: wide
categories: 
  - post
  - Unity
sidebar:
  nav: "main"
author_profile: true
---

## Update function

![image](/assets/images/table11.png)

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

## Update 함수 사용은 반드시 지양해야 하는가?
* 상황에 알맞게 사용하는 것이 중요하지, 사용하지 않는다고 능사는 아니다
  * Input 키의 Up/Down을 확인하는 것과 같은 것은 문제가 되지 않는다
  * 하지만 ***매 프레임 호출되어야 하는지 의문을 가질 필요***는 있다
* GetComponent나 GameObject.Find 함수를 매 프레임 사용하는 것이 퍼포먼스에 더 치명적이다

## 출처
* <https://thegamedev.guru/unity-ui/sprite-vs-image/>
* <https://www.reddit.com/r/Unity3D/comments/4mh51a/how_to_avoid_using_update/>
* <https://blog.unity.com/technology/1k-update-calls>
* <https://velog.io/@leehs27/UpdateCallsCost>
* <https://bradkeys.com/2017/01/30/Avoiding-Unity-Update-Loops/>