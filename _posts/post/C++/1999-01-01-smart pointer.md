---
title: "스마트 포인터"
classes: wide
categories: 
  - blog
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## RAII
* **Resource Acquisition Is Initialization**
  * 자원 관리를 스택에 할당한 객체를 통해 수행
  * stack unwinding을 통해 예외가 발생하더라도 stack frame을 빠져나갈 때 소멸자를 호출

## unique_ptr
* 객체에 대한 유일한 소유권을 보장
  * **복사 금지**
* Memory leak과 double free를 방지
* std::move를 이용해 소유권 이전은 가능
  * 이동 전의 dangling pointer를 다시 사용하지 않는다는 확신하에 사용
```c++
std::unique_prt<A> pa(new A);
```

## shared_ptr
* control block을 할당하여 복사를 허용
* reference count가 0이 되면 자원을 해제

## weak_ptr
* 객체를 안전하게 참조할 수 있게 해주지만, 참조 개수를 늘리지 않음
* shared_ptr를 인자로 받아 값을 저장
  * valid한 값이 있다면 사용 가능
  * 이미 해제된 shared_ptr값이면 false값을 리턴
