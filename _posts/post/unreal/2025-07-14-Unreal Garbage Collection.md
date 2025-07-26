---
title: "Garbage Collection"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---
   
## Garbage Collection

![post_thumbnail](/assets/images/Reflection_GC/Rootset.png)

* 언리얼은 사용자가 아닌 엔진에서 Heap 메모리를 관리하는 기능을 제공한다
* UPROPERTY 매크로로 선언된 UObject 객체들이 대상이다
  * int32, float 등의 타입은 해당하지 않는다
* GC Tick을 돌면서 아래 순서로 작동한다

### 개요
* Ureanl은 모든 UObject의 참조 개수를 카운팅한다
  * 참조 그래프를 만들어, 어떤 UObject가 사용되고 있는지 아닌지를 참조 여부로 판단한다
  * class A가 멤버 변수로 class B를 가리키는 포인터를 가지고 있는 것과 같은~
* 그래프의 Root는 Root 레벨에 해당하는 UObject의 집합이며, 이후 참조되는 UObject들은 여기에 추가한다

![post_thumbnail](/assets/images/GC/GC1.png)

* CG가 발생하면 엔진은 ROOT에서 출발해 Tree를 검색하며 참조하는 모든 UObject를 추적한다

![post_thumbnail](/assets/images/GC/GC2.png)

* 이 중, 참조되지 않은 오브젝트, 즉 검색 과정에서 찾지 못한 오브젝트들은 제거한다
  * 이를 Mark & Sweep라 한다
  * Root Set으로부터 참조된 Object들은 Mark 한다
  * Mark 되지 않은 오브젝트들은 Sweep하는 방식

### 작동 순서
1. GC 사이클 시작 (초기화)
  * GC가 실행될 준비를 하면서, 이전에 Reachable로 마킹된 모든 UObject들의 Reachable 플래그를 해제
  * **모든 UObject는 잠정적으로 Unreachable 상태**

2. Root Set 마킹 
  * Root Set은 여러 개의 Root로 이루어진 컨테이너
  * GC의 "출발점"인 Root Set에 등록된 모든 UObject들을 Reachable 상태로 마킹

3. 참조 그래프 순회 및 Reachable 전파
  * Reachable로 마킹된 객체들(Root Set 포함)로부터 시작하여, 모든 UPROPERTY로 명시된 UObject* 참조를 재귀적으로 순회
    * 모든 Root Object를 돌면서 UPROPERTY를 Recursive Search
  * 이 참조를 통해 새롭게 발견되는 모든 UObject 인스턴스들도 Reachable 상태로 마킹
    * 이 과정에서 Pending Kill이 아닌 UObject들은 Unreachable Mark를 지워준다
    * 즉, 지우지 않을 Object로 분류한다
  * 이 단계가 끝나면, Root Set으로부터 UPROPERTY 체인을 통해 도달 가능한 모든 객체들이 Reachable로 마킹

4. Unreachable 객체 식별
  * 이제 GC가 관리하는 모든 UObject 인스턴스들을 한 번 순회하면서, 아직 Reachable로 마킹되지 않은 객체들을 식별
  * 이들이 바로 "더 이상 참조되지 않아" Unreachable로 분류된 객체들

5. 메모리 해제
  * GC는 최종적으로 Unreachable로 판단된 모든 UObject들의 소멸자를 호출하고, 해당 메모리를 해제

6. Shrink Hash Table
  * Object Type을 Key로 해서 UObject들을 저장하는 Hash Table이 있다
  * 이 Hash Table을 압축한다

### UObject들이 참조가 끊기는 순간
* 명시적으로 nullptr가 대입되거나 컨테이너로부터 제거된 객체들
* 상위 UObject가 파괴될 때
* 위의 경우들은 더 이상 RootSet을 통해 순회하지 못한다
* 참조가 끊긴 순간에 바로 메모리가 해제되는 것은 아니다

### GC 규칙
* 생명 주기를 함께 하는 멤버 변수는 UPROPERTY로 선언
* 멤버 변수 포인터는 항상 UObject 혹은 거기에 딸린 멤버 변수로 한정한다

### GC 주의점
* UObject에서 파생한 Raw Pointer 멤버 변수는 항상 UPROPERTY 키워드를 추가한다
  * GC 대상으로 분류 목적
* UObject에서 파생하지 않은 오브젝트는?
  * TWeakObjectPtr과 FWeakObjectPtr을 사용한다
  * scalar type들은 관련 X
* TArray는 유일하게 UObject*를 담을 수 있는 컨테이너
  * 따라서 TArray는 UPROPERTY 매크로를 붙여주는 것을 권장한다
  * Reference 혹은 Pointer가 destroy 된다면, 이들을 validate할 방법이 없다
  * null check를 해도 null 초기화가 된 것이 아니라 쓰레기 값을 가지고 있어, 정상적으로 check되지도 않는다

### TWeakObjectPtr
* UPROPERTY는 멤버 변수를 소유하는 객체가 강한 참조를 통해 GC되지 않도록 하지만, 이는 퍼포먼스적으로 불리한 경우를 야기하기도 한다
  * 객체 A가 객체 B를 강한 참조로 붙잡고 있고 객체 B가 명시적으는 Destroy 되었다고 하자
  * 객체 A가 사라지지 않는 한, 객체 B가 차지하는 실질적 메모리는 해제되지 않는다
  * 즉 GC의 퍼포먼스를 저하시킨다
* Root Set에 포함되지 않아 비록 GC 대상으로 분류되지는 않지만, 적어도 Destroy 시 nullptr로 초기화되며 IsValid로 정상적인 결과를 반환한다

## 출처
* <https://algorfati.tistory.com/75>
* <https://hyo-ue4study.tistory.com/272>
* <https://husk321.tistory.com/392>
* <https://forums.unrealengine.com/t/knowledge-base-garbage-collector-internals/501800>
* <https://forums.unrealengine.com/t/gc-messing-up-tarray-without-uproperty/320560/3>