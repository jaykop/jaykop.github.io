---
title: "Compiled & Interpreted"
classes: wide
categories: 
  - post
  - etc.
sidebar:
  nav: "main"
author_profile: true
---

## Compiled Language
* CPU가 바로 이해할 수 있는 기계어로 소스코드를 변환
* 소스코드 처리와 분석에 많은 시간 소요
* 일반적으로 실행이 빠름
* 컴파일된 기계어는 플랫폼 의존적

## Interpreted Language
* 소스코드를 Intermediate Code로 변환
* interpreter는 Intermediate Code를 바로 실행 가능
* 플랫폼에 상관없이 interpreter만 있으면 코드를 실행/플랫폼에 독립적
* CPU가 아닌 interpreter가 바로 이해할 수 있는 기계어로 소스코드를 변환
* 소스코드 처리와 분석에 적은 시간 소요
* 상대적으로 실행이 느림

## static typing vs. dynamic typing

### 동적 타이핑 dynamic typing
* Python, Ruby, php, ...
* 변수의 타입을 런타임에 정의
  * 컴파일시 타입을 명시해주지 않아도 되기 때문에 빠르게 코드를 작성할 수 있음
* 런타임에서 타입 에러가 발생하는 경우 이를 디버깅하기 까다로움

### 정적 타이핑 static typing
* C, C++, C#, ...
* 변수의 타입을 컴파일 타임에 정의
  * 타입 에러로 인한 문제를 실행 전에 발견해 에러를 미연에 방지
  * 컴파일 타임에 타입을 정했기 대문에 실행 속도가 빠름

### dynamic typing을 꺼려하는 이유 (static type을 사용하는 경우)
* 런타임에서 타입 에러가 발생하는 경우 이를 디버깅하기 까다로움
* 실행 프로그램의 속도가 현저하게 빠르다
* 동적 타이핑 언어도 내적으로는 타입이 정의되어 있고, 여기서 발생하는 에러를 체크해야한다

## 출처
* <https://ko.wikipedia.org/wiki/%EC%BB%B4%ED%8C%8C%EC%9D%BC_%EC%96%B8%EC%96%B4>
* <https://ko.wikipedia.org/wiki/%EC%9D%B8%ED%84%B0%ED%94%84%EB%A6%AC%ED%8A%B8_%EC%96%B8%EC%96%B4>
* <https://devuna.tistory.com/82>
* <https://pubul.tistory.com/153>
