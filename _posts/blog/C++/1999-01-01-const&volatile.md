---
title: "const & volatile 키워드"
classes: wide
categories: 
  - blog
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## Read-Only
* 변수의 값을 변경할 수 없다
* 메서드에서 클래스의 멤버 변수를 변경할 수 없다

## const 표현식
```c++
// read-only integer
const int a; 

// read-only integer
int const a; 

// pointer to const integer: (*a) 
// 못바꿈 a = &b (possible if b = const int)
const int *a; 

// const pointer to integer: (*a) 
// 바꿈  a = &b 
// 다른 데 못 가리킴
int * const a; 

// const pointer to const integer: 값도 못 바꾸고, 주소값도 못 바꿈
const int const* a; 
```

## volatile
* 컴파일러가 자동으로 최적화하는 것을 방지
* interruption 핸들링 또는 멀티스레딩에서 공유되는 변수에 사용

## volatile const
* 컴파일러 최적화 불가능
* 프로그래머의 쓰기/변경 불가능
* ex)
  * 하드웨어마다 레지스터 주소값이 다른데 컴파일러의 임의 변환을 막기 위해 volatile
  * 또한 하드웨어 주소값은 사용자가 지멋대로 바꾸면 안됨, 그래서 const

## 출처
* <https://geekhub.tistory.com/68>
