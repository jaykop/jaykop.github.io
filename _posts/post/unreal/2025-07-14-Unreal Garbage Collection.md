---
title: "Unreal Reflection & Garbage Collection"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---
   
## Reflection
* ***프로그램이 런타임, 그러니까 실행중에 자기 자신의 구조를 검사하고 조작할 수 있는 능력***
* 일반적인 C++에서는 컴파일 시점에 모든 정보가 결정
  * 어떤 class A가 어떤 멤버 변수 혹은 함수를 가지고 있는지 알 수 없다
  * 리플랙션이 지원되는 언어에서는 이게 가능하다

### C++와 리플랙션
* RTTI를 지원하기는 하지만, 다른 언어에서의 리플랙션보다는 제한적이다
  * 런타임에 객체의 동적 타입을 확인하는 데 그친다
  * 값을 조작하거나 구조의 내부(멤버 변수 또는 멤버 함수 정보)를 알수 없다

### 언리얼에서의 리플랙션
* 언리얼은 자체적인 리플랙션 시스템을 구축
* 대표적인 예시가 UFUNCTION 또는 UPROPPERTY
  * 언리얼 에디터 -> 디테일 패널에서 특정 오브젝트의 값을 변경할 수 있다.
    * 에디터가 이미 실행 중인 프로그램이라고 생각할 때, 이는 클래스에서 정의한 값을 동적으로 변경하는 것이다.
  * specifier로 마킹된 메타데이터를 런타임에 파악해 작동
    * 블루프린트에서 사용할 수 있는 변수와 함수 판단
    * UPROPERTY 매크로를 통해 UObject를 참조하는 포인터를 수집해 Garbage Collection에 활용
* **프로퍼티 시스템**이라 부르기도 한다

### 작동 순서
1. 개발자의 코드 작성
2. UBT가 컴파일러 호출 전, 그러니까 실제 빌드 전에 UHT를 호출
3. 호출된 UHT가 헤더파일을 스캔하고 사용된 언리얼 매크로를 파싱 및 분석해 메타데이터 추출
4. UHT는 이를 바탕으로 .generated.h 및 .generated.cpp를 생성해, 아래 코드들을 생성한다
  * 클래스와 멤버를 리플랙션에 등록하는 코드
  * StaticClass 함수 정의
  * 런타임용 함수 호출 코드
  * UPROPERTY로 선언된 UObject* 들을 추적하는 코드 등
5. UBT가 컴파일러를 호출 리플랙션 목적으로 추가된 코드까지 포함해 컴파일


## Garbage Collection

![post_thumbnail](/assets/images/Reflection_GC/Rootset.png)

* 언리얼은 사용자가 아닌 엔진에서 Heap 메모리를 관리하는 기능을 제공한다
* UPROPERTY 매크로로 선언된 UObject 객체들이 대상이다
  * int32, float 등의 타입은 해당하지 않는다
* GC Tick을 돌면서 아래 순서로 작동한다

### 작동 순서
1. GC 사이클 시작 (초기화)
  * GC가 실행될 준비를 하면서, 이전에 Reachable로 마킹된 모든 UObject들의 Reachable 플래그를 해제
  * 모든 UObject는 잠정적으로 Unreachable 상태

2. Root Set 마킹
  * RootSet은 여러 개의 Root로 이루어진 컨테이너
  * GC의 "출발점"인 Root Set에 등록된 모든 UObject들을 Reachable 상태로 마킹

3. 참조 그래프 순회 및 Reachable 전파 (Marking Phase)
  * Reachable로 마킹된 객체들(Root Set 포함)로부터 시작하여, 모든 UPROPERTY로 명시된 UObject* 참조를 재귀적으로 순회
  * 이 참조를 통해 새롭게 발견되는 모든 UObject 인스턴스들도 Reachable 상태로 마킹
  * 이 단계가 끝나면, Root Set으로부터 UPROPERTY 체인을 통해 도달 가능한 모든 객체들이 Reachable로 마킹

4. Unreachable 객체 식별
  * 이제 GC가 관리하는 모든 UObject 인스턴스들을 한 번 순회하면서, 아직 Reachable로 마킹되지 않은 객체들을 식별
  * 이들이 바로 "더 이상 참조되지 않아" Unreachable로 분류된 객체들

5. 메모리 해제 (Sweep Phase)
  * GC는 최종적으로 Unreachable로 판단된 모든 UObject들의 소멸자를 호출하고, 해당 메모리를 해제

### UObject들이 참조가 끊기는 순간
  * 명시적으로 nullptr가 대입되거나 컨테이너로부터 제거된 객체들
  * 상위 UObject가 파괴될 때
  * 위의 경우들은 더 이상 RootSet을 통해 순회하지 못한다
  * 참조가 끊긴 순간에 바로 메모리가 해제되는 것은 아니다