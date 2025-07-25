---
title: "Unreal Reflection"
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
