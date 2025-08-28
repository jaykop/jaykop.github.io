---
title: "Truth About Value Type"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---

## Value type이면 모두 stack에 저장된다?
* Value type은 stack에 저장**될 수 있다**
  * **항상 stack에 저장되는 것은 아니다**
* 프로그래머는 특정 객체에 대해 stack에 저장되는지 heap에 저장되는지를 알아야할 필요가 있었다
  * 사용자에게 노출되지 않은 상태로 메모리를 관리하는 Managed Heap이 있는 환경은 다르다
* 참조 Reference는 값 타입도 아니고 참조 타입의 객체도 아니다
  * 그 자체로 값이다
  * 이 값들은 어디에 저장되어 있는가?
  * C#의 타입 시스템에서 정해준 타입이 없다고 해서 무시될 수는 없는데 말이다

## Value type과 stack에 대한 오해
* 여러 다른 벤더에 의해 제공되는 C#의 할당 규약 중, **값 타입의 임시 변수(로컬 변수)를 stack이라는 공간에 할당해야 한다는 언어적 요구사항은 없다**
* 임베디드 시스템, 웹 등에서 작동하는 CLI가 있는데 여기서 어떤 할당 방법을 사용할지는 모른다
  * 쓰레드 당 stack을 사용할 수도, 그냥 heap을 사용할 수도, stack이란 저장소 자체가 없을 수도 있다
* 람다와 익명 함수에서의 지역변수는 heap에 저장된다
* 오늘날의 C# iterator block은 지역 변수를 heap에 할당한다
  * 반드시 그런 것은 아니다
* 스택과 힙 그 이상의 메모리 관리 방식이 존재한다
  * 일례로 레지스터는 스택도 힙도 아니다
  * 값 타입이 사이즈만 맞다면 레지스터에 할당되어도 문제가 없다
  * 이같이 레지스터의 스케줄링 알고리즘이 사용자에게 딱히 중요하지 않게 다가간다면, stack도 마찬가지여도 되지 않은가?

## 메모리 할당 메커니즘은 저장소의 생명 주기에 의해 결정된다
* 3 종류의 메모리 값이 있다
  * value type 객체, reference type의 객체, reference 그 자체
  * C#의 코드는 reference type의 객체를 직접 수정할 수 없다
  * unsafe code에서 포인터 타입은 값 타입으로 취급된다
* 메모리를 값을 저장할 수 있는 **저장 위치(주소)** 개념이 있다
* 프로그램에 의해 변조될 수 있는 값들은 저장 위치 어딘가에 존재한다
* 모든 참조는 저장 위치를 참조한다 (null은 제외)
  * 모든 저장 위치는 생명주기가 있다
  * 해당 저장 위치, 즉 주소가 유효한 기간이 있다
* 특정 메서드의 실행 시작 시점부터, 메서드가 반환되는 시점 또는 예외를 던지는 시점 까지가 Life Cycle이다
* 메서드 코드는 주소 사용을 필요로 할 수 있다
  * 저장 위치의 생명주기보다 더 긴 시간을 현재 작동하는 메서드가 요구하면, 더 보존한다 (long lived)
  * 그렇지 않으면 short lived

## CLR 구현의 디테일
* 3 종류의 저장 위치가 있다
  * stack, heap, register
* long-lived는 항상 heap에 저장된다
* short-lived는 항상 register 혹은 stack에 저장된다
* 컴파일러 혹은 런타임이 long-lived인지 short-lived인지 구분하기 어려운 경우도 있다
  * 보수적으로 결정한다면, long-lived로 구분한다
  * 참조 타입의 객체는 실제로 short-lived더라도, 항상 long-lived로 설정한다
  * 즉, 항상 heap에 할당된다

## 결론
* value type의 객체나 reference는 저장 위치를 고려할 때 본질적으로 모두 동일하다
  * long-lived와 short-lived를 구분해 heap에 할당할지, stack이나 register에 할당할지만 다를 뿐
* 배열 원소, 참조 타입의 멤버변수, iterator block의 지역 변수, 람다 혹은 익명변수의 지역 변수는 모두 메서드의 활성화 기간보다 생명주기가 더 길어야 한다
  * 그렇지 않은 상황에서 이를 알아채도록 하는 컴파일러를 구현하는 것은 매우 어렵거나 불가능하다
  * 따라서 이런 경우는 무조건 heap으로 할당한다
* 지역 변수 혹은 임시 값들이 메서드의 활성화 기간이 끝나고 나면 사용되지 않도록 컴파일 타임 분석을 거치게 된다
  * 따라서 이들은 short-lived로 분류되어 stack 혹은 register에 할당된다

## 출처
* <https://ericlippert.com/2010/09/30/the-truth-about-value-types/>