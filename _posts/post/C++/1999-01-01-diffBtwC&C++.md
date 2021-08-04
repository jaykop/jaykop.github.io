---
title: "C와 C++ 차이 몇 가지"
classes: wide
categories: 
  - blog
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## C의 malloc과 C++ new의 차이
* **malloc**
* malloc은 함수(function)
* 할당할 메모리의 사이즈를 매개변수로 받음size as input
* header file을 포함시켜야 함
* 실 사용할 타입으로 casting 필요
    * 메모리 청크만 heap에서 받아 옴
* 자동으로 constructor를 호출하지 않음

* **new**
* new는 연산자(operator)
* C++ 빌트인 키워드이기 때문에 별도로 헤더파일 필요 없음
* 실 사용할 타입으로 바로 메모리 할당 받아올 수 있음
    * 자동으로 constructor를 호출

## class와 struct
* **class**
  * 기본적으로 다 프라이빗
  * class는 object 역할 (관습적인 차이)
* **struct**
  * 기본적으로 다 퍼블릭
  * struct는 데이터의 묶음 (관습적인 차이)
  * **C에서의 struct는….**
    * 안에 함수를 직접 만들 수 없음
    * function pointer를 할당하여 사용
    * 다형성,  상속성이 없음
    * constructor, destructor가 없음

## 컴파일러에 의해 자동 생성되는 class 생성자 및 연산자 
* default constructor
* default destructor
* copy constructor
* assignment operator
* move constructor
  ```c++
  A (A&& rhs) { ... };
  ```
* move assignment operator
  ```c++
  A& operator=(A&& rhs) { ... };
  ```

## 패러다임의 차이
* **C**
  * 절차지향적
    * 순차적인 처리가 중요
    * 프로그램이 함수화
    * 함수의 유기적인 연결로 프로그램이 구성
  * 하향식 접근
    * 순차적인 실행이 가능하도록 단계적 세분화 작업을 거침
    * 수행되는 함수들끼리의 연결을 중요시
* **C++**
  * 객체지향적
    * 유사한 데이터나 함수를 클래스라는 하나의 그룹으로 묶음
    * 그룹의 객체에 의해서 프로그램이 구동되게 한다
  * 상향식 접근
    * 추상 객체를 디자인하고 이들을 조합하는 방식
    * 언어는 언어 일뿐 개발 방식 및 개발 패러다임은 개발자가 정하는 것
    * C++가 객체지향적이라면 friend 같은 키워드는 만들지 않았을 것

## 객체지향 프로그래밍이란?
* **캡슐화**
  * 데이터와 메서드를 하나의 클래스라는 단위로 묶음
  * 클래스 내부 정의에 대해 외부에서 볼 수 없음
  * methods + data = object(class)
* **추상화/상속성**
  * base (추상,일반) -----------> derived (고유,구체)
  * 객체의 공통적이고 일반적인 특징을 상위클래스에 디자인
  * 파생된 하위클래스는 고유의 성질
  * 기존의 클래스를 바탕으로 특징을 추가해 새로운 클래스를 만들 수 있음
  * ex) 동물
    * 개/호랑이/닭/….
* **다형성** 
  * virtual function description
  * 같은 함수여도, 클래스에 따라 다르게 작동할 수 있음
  ```c++
  class Vehicle {
    virtual void move_forward()
  }
  class Train: public Vehicle {
    virtual void move_forward();
  }
  class Bus: public Vehicle {
    virtual void move_forward();
  }
  class KTX: public Train {
    virtual void move_forward();
  }
  ```

## 출처
* <https://geekhub.tistory.com/68>