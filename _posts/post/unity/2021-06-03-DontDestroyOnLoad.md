---
title: "DontDestroyOnLoad"
classes: wide
categories: 
  - blog
  - unity
sidebar:
  nav: "main"
author_profile: true
---
  
## DontDestroyOnLoad
* 새로운 Scene이 로드될 때, 자동으로 파괴되지 않는 target 오브젝트를 생성
* 새 레벨이 로드되면 Scene의 모든 오브젝트들은 파괴되고, 새 레벨의 오브젝트들이 로드된다.
* 레벨 스위치 중에 오브젝트를 보존하기 위해 **DontDestroyOnLoad** 사용
* 해당 오브젝트가 component이거나 gameobject인 경우, 그 오브젝트가 포함된 전체 hierarchy는 파괴되지 않는다.

```csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour {

    // scene이 로드될 때 불린다
    void Awake() {
        // 이때, ExampleClass는 파괴되지 않는다
        DontDestroyOnLoad(transform.gameObject);
    }
}
```
* 여전히 이 오브젝트는 **Destroy** 함수를 통해 파괴할 수 있다
* 싱글턴 패턴 구현의 한 방법
* **객체 중복 생성 방지는 프로그래머의 몫**

## 출처
* <http://docs.unity3d.com/kr/530/ScriptReference/Object.DontDestroyOnLoad.html>
* <https://wergia.tistory.com/191>