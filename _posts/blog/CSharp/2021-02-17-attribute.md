---
title: "Reflaction & Attribute"
classes: wide
categories: 
  - blog
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## 리플렉션(Reflaction)
* 프로그램 실행 도중 객체 정보를 조사
* 다른 모듈에 선언된 인스턴스를 생성
* 기존 개체에서 형식을 가져오고 해당하는 메서드를 호출 또는 해당 필드와 속성에 접근할 수 있는 기능을 제공

|형식|메서드|설명|
|:---:|:---::---:|
|Type|GetType()|지정된 형식의 Type 개체를 가져옴|
|MemberInfo[]|GetMembers()|해당 형식의 멤버 목록을 가져옴|
|MethodInfo[]|GetMethods()|해당 형식의 메서드 목록을 가져옴|
|FieldInfo[]|GetFields()|해당 형식의 필드 목록을 가져옴|

## 애트리뷰트(Attribute)

  
## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/concepts/attributes/accessing-attributes-by-using-reflection>
* <https://nowonbun.tistory.com/496>
* <https://blog.hexabrain.net/152>
