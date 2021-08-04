---
title: "Action & Func"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## Action 
* 매개 변수를 0~16개 가질 수 있음 
* 값을 반환하지 않는 메서드를 캡슐화
* Action<T1, T2, ...>
  - T1, T2, ...는 파라미터
  - 공통된 파라미터 갯수 및 타입을 공유하는 delegate를 할당할 수 있음

## Func 
* 매개 변수를 0~16개 가질 수 있음 
* 값을 반환하는 메서드를 캡슐화
* Func<R, T1, T2, ...>
  - R은 Return Type
  - T1, T2, ...는 파라미터
  - 공통된 Return Type, 파라미터 갯수 및 타입을 공유하는 delegate를 할당할 수 있음
   
## 출처
* <https://scvtwo.tistory.com/52>
* <https://docs.microsoft.com/ko-kr/dotnet/api/system.action-1?view=net-5.0>
* <https://docs.microsoft.com/ko-kr/dotnet/api/system.func-2?view=net-5.0>
