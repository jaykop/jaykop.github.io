---
title: "template class 사용의 장단점"
classes: wide
categories: 
  - blog
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## 장점
* 타입마다 중복되는 코드를 줄일 수 있음
* 컴파일 타임에 다형성을 부여할 수 있음 
  * vtable이 없으므로 런타임 속도가 빨라질 수 있음
* 컨테이너에 여러 타입의 객체를 저장할 수 있음

## 단점
* 가독성을 떨어뜨림
* 매개변수를 늘릴수록 컴파일 타임이 느려짐
* 실행 파일의 크기가 너무 커지면 퍼포먼스에 영향
