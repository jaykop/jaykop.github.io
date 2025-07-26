---
title: "Blueprint"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## Blueprint란?
* Unreal 엔진에 내장된 컴파일식 비주얼 스크립팅 시스템
* 하나의 프리팹 혹은 아키타입으로 정의하는 단위일 수도 있다

## Blueprint 사용 시 주의할 점
* 복잡한 연산 및 작업을 매 프레임마다 실행하지 않을 것
  * C++ 코드로 대신 실행할 것
* Blueprint는 가상 머신을 사용해 Blueprint 노드를 네이티브 C++ 코드로 변환하는 과정에서 비용이 발생
* 당연히 C++ 코드 실행이 Blueprint보다 빠르다
* Blueprint로 하지 못하는 작업은 C++로 가능
* Blueprint는 이벤트 기반 시스템
* Blueprint는 레퍼런스를 사용하여 다른 Blueprint의 데이터와 기능에 엑세스
  * 부적절한 순환 종속 디자인은 유효하지 않은 레퍼런스로의 참조를 야기하고 오류를 발생시킬 수 있다
  * 2개의 Blueprint가 있고 이것이 서로 형변환을 통해 함수를 호출하거나 변수에 엑세스하는 경우
    * 둘 중 어느 Blueprint를 로드할 때, 해당 Blueprint의 모든 종속성을 로드하면서 에러가 발생

## CPP vs. Blueprint
* 퍼포먼스가 중요 요소가 될 것인지?
* 개발하려는 파트가 로우레벨인지, 하이레벨인지?
  * 시스템인지, 또는 컨텐츠인지?
* 한 방법을 채택해 개발했을 때, 미래 코스트가 얼마인지?
* 어느 방법이 더 개발하기에 용이한지?

### cpp
* 실행 시 빠른 퍼포먼스 제공
* diff / merge 가능

### Blueprint
* 에셋 의존성 관리
* C++보다 직관적
  * 난 프로그래머라 그런지 공감 안된다
* 테스팅 및 반복 작업이 수월
* C++보다 더 낮은 허들

### Programming Level
* Engine Programming
  * 로우레벨에서 다뤄야 하는 문제
  * 게임 개발에 있어 핵심적인 기술 개발
  * 게임 장르, 컨텐츠 등의 직접적인 고민은 하지 않는 단계
* Game Programming
  * 게임 전켄트 및 장르를 확정하고, 이 게임을 위한 개발 단계
  * 게임을 플레이 가능하도록 하거나 빌드하는 시스템을 구축
* Scripting
  * 게임을 플레이하는 유저가 즐기는 컨텐츠 개발
  * 게임 디자인, 컨텐츠에 대한 세부 조정
* High-Level -> Low-Level
* Scripting -> Engine Programming
* Bluerpint -> C++

## Performance
* C++
  * 코드 작성 후 cpp 파일로 저장
  * CPU가 바로 실행할 수 있는 머신 코드로 컴파일
  * 함수를 직접 호출한다
* Blueprint
  * 스크립트 작성 후, .uasset 파일로 저장
  * 스크립트 컴파일러가 스크립트 바이트코드로 컴파일
    * 엔진 스크립트 버추얼 머신이 런타임에 실행할수 있는 intermeditate 형태
  * C++로 구현한 함수를 호출할 때 bridge 함수를 이용한다
    * 스크립트 VM을 통해 native helper function을 호출
  * C++ 코드보다 오버헤드가 발생한다
    * C++ 코드가 퍼포먼스적으로 더 우세
    * CPU 명령 실행 단계에서 최적화
    * 오버헤드가 발생하지 않는다

### Nativization
* 블루프린트로 작성한 스크립트에서 스크립트 바이트코드를 거치지 않고 C++로 변한돼 머신코드로 변환하는 기능
* UE5로 업데이트 되면서 해당 기능은 사라졌다
  * <https://forums.unrealengine.com/t/why-was-blueprint-nativization-removed-no-code-preaching/232490>
  * <https://dev.epicgames.com/documentation/ko-kr/unreal-engine/nativizing-blueprints?application_version=4.27>

### 파레토 법칙
* **게읨의 작동 시간 중 80%는 구현된 코드의 20%만으로 작동한다**

## 출처
* <https://www.youtube.com/watch?v=S2olUc9zcB8>