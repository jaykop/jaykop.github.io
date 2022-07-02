---
title: "Abstract Data Type"
classes: wide
categories: 
  - post
  - CSharp
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## 추상적 자료형 ADT
* 자료 자체의 형태와 연산을 수학적으로만 정의한 것

### stack으로 본 추상적 자료형의 예시
* 삽입한 순서대로 쌓이는 값들의 모임
* 추가해서 스택의 맨 위에 새로운 데이터를 쌓는 push 연산
* 스택의 맨 위에 있는 기존의 데이터를 제거하는 pop 연산
* 그러나 이 **stack의 구현을 array로 할지, linkedlist로 할지는 중요하지 않다**
  * 자료형에 대한 정의와 연산 방법에 대한 설명이 전부
  * 집합, 리스트, 큐, 트리 등도 추상적 자료형에 해당한다  

### map으로 본 추상적 자료형의 예시
* map의 데이터는 key와 value로 이루어진다
* position으로 데이터에 접근할 수 있다
  * 포인터 오브젝트
* iterator로 navigate와 reference를 할 수 있다
  * *p를 통해 dereference로 가능
* put, erase, begin, end, find 등의 연산을 포함한다
* key에 대한 중복 value를 허용하지 않기 때문에 overwrite 한다

### 자료구조와의 차이
* 추상적 자료형이 정의한 연산들을 실제로 구현한 것
  * 위의 예시로든 stack을 array로든, linkedlist로든 코드로써 구현할 수 있다

## 추상 자료형의 장점
* OOP에서 클래스 정의가 이에 해당하므로, 그 특성도 같다
  * 구현 부분은 숨기고 인터페이스만 제공함으로써 캡슐화가 가능
  * 핵심 기능을 선언해 제공함으로써 코드 재사용성과 가독성 증가
  * 내부 구현을 사용자에게 맡김으로서 사용의 유연성 제공

### 코드에 대입해보면...
* class를 통해 추상 자료형을 구현
* private, protected, public 등을 사용해 캡슐화 가능
* class를 상속을 통해 재정의 가능
* interface 혹은 abstract class의 경우는 직접 구현해야 함

## 출처
* <https://namu.wiki/w/%EC%B6%94%EC%83%81%EC%A0%81%20%EC%9E%90%EB%A3%8C%ED%98%95>
* <https://gamedevlog.tistory.com/3>