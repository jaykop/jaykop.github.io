---
title: "Blittable & Unblittable"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## [Managed vs. Unmanaged Code](https://jaykop.github.io/post/etc/compiled&interpreted/)
* Unmanaged code란 컴퓨터 구조, 프로세서에 특화되어 그에 의존하는 코드
  * C#에서는 unsafe 키워드를 이용하는 코드
  * 프로그래머에 의해 직접 관리
* Managed code란 .NET 프레임워크에서 구동하는 C# 코드 자체
  * 메모리 관리, 컴파일러로부터 독립적

## Blittable vs. Non-Blittable
* Blittable 
  - Managed / Unmanaged 양 쪽 모두에서 마샬러에 의한 처리 없이 공통된 표현을 사용
* Non-Blittable 
  - Managed와 Unmanaged memory에서의 표현이 달라 별도의 데이터 처리가 필요함(마샬링)

## 마샬링
* 한 객체의 메모리에서의 표현방식을 저장 또는 전송에 적합한 다른 데이터 형식으로 변환하는 과정
* 프로그램 간 데이터를 전달하는 경우 사용
* 직렬화 된 객체를 멀리 떨어진 객체와 통신하기 위해 사용
* 복잡한 데이터 통신을 하도록 하느 것

## 직렬화 (Serialization)
![post_thumbnail](/assets/images/serialization-process.gif)
* 개체를 저장하거나 메모리/DB/파일 전송을 위해 개체를 바이트 스트림으로 변환하는 프로세스
* 프로세스 이후 다시 개체로 만들기 위함
* 객체의 인스턴스 변수들의 값을 일렬로 나열하는 것

```csharp
// 직렬화가 불가능한 클래스
class A
{
    // ..
}

[Serializable]
class B
{
    [NonSerialized]
    // 본래 직렬화가 가능하지만, 직렬화 되지 않게 막음
    // object 타입은 Serializable이 적용
    object o; 

    [NonSerialized]
    // 직렬화가 불가능한 멤버는 별도로 직렬화를 막아야 함
    A a;

}
```

## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/framework/interop/blittable-and-non-blittable-types>
* <https://hwanine.github.io/network/Marshalling/>
* <https://scvtwo.tistory.com/14>
* <https://m.blog.naver.com/gmldbsdl6/80195745104>
* <https://www.partech.nl/en/publications/2021/03/managed-and-unmanaged-code---key-differences#>