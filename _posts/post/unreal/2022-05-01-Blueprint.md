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

## Blueprint의 타입

### Level Blueprint
* 특정 레벨 스크립팅에만 사용도는 Blueprint
* 타 레벨에 재사용 불가

### Class Blueprint
* 액터를 대상으로 적용되는 Blueprint
* 인스턴싱 및 재사용 가능

### Widget Blueprint

## Blueprint 사용 시 주의할 점

### 복잡한 연산 및 작업을 매 프레임마다 실행하지 않을 것
* C++ 코드로 대신 실행할 것

### Blueprint는 가상 머신을 사용해 Blueprint 노드를 네이티브 C++ 코드로 변환하는 과정에서 비용이 발생

### 당연히 C++ 코드 실행이 Blueprint보다 빠르다

### Blueprint로 하지 못하는 작업은 C++로 가능

### Blueprint는 이벤트 기반 시스템

### Blueprint는 레퍼런스를 사용하여 다른 Blueprint의 데이터와 기능에 엑세스
* 부적절한 순환 종속 디자인은 유효하지 않은 레퍼런스로의 참조를 야기하고 오류를 발생시킬 수 있다
* 2개의 Blueprint가 있고 이것이 서로 형변환을 통해 함수를 호출하거나 변수에 엑세스하는 경우
  * 둘 중 어느 Blueprint를 로드할 때, 해당 Blueprint의 모든 종속성을 로드하면서 에러가 발생