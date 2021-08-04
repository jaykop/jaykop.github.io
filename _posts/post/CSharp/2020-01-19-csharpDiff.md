---
title: "C# 개요"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---

## C#
![post_thumbnail](/assets/images/Common_Language_Runtime_diagram_korean.png)
* CLR(Common Language Runtime) 환경을 필요로 함
  - .Net의 언어(C#, VB.NET 등)가 컴파일러를 통해 CIL(Common Intermediate Language)로 변환
  - CIL이 다시 CLR을 통해 Native Code로 변환
  - 플랫폼에 독립적인 개발 환경을 보장
  - 저수준 언어보다 다소 떨어지는 퍼포먼스
    - 더 많은 메모리와 느린 속도
  - 모든 기본 변수 타입이 **object** 타입에서 파생
  - **자체적인 Memory Management**
    1. 메모리를 할당해 오브젝트를 생성, Contructor 실행(considered live)
    2. Destructor를 호출하는 방법 외에 해당 오브젝트에 접근할 수 없으면, 미사용 오브젝트로 분류(Destroy 후보군으로 분류)
    3. 불특정 시간 이후, Destructor 실행
    4. Destructor가 한번 호출되면, 어떤 접근도 불가능해짐
    5. Garbage Collection에 귀속되는 후보군으로 분류
    6. 불특정 시간 이후, 메모리로 반환

## 출처
* <https://ko.wikipedia.org/wiki/%EA%B3%B5%ED%86%B5_%EC%96%B8%EC%96%B4_%EB%9F%B0%ED%83%80%EC%9E%84>
* <https://guslabview.tistory.com/185>
* <https://www.informit.com/articles/article.aspx?p=474652&seqNum=9>
* <https://docs.microsoft.com/ko-kr/dotnet/standard/clr>