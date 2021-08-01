---
title: "C의 malloc과 C++ new의 차이"
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

## 출처
* <https://geekhub.tistory.com/68>