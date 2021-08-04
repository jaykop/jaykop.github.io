---
title: "Extension Method"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## 확장 메서드란
* 기존 제공되는 클래스/구조체/인터페이스의 구현을 직접 변경하지 않고 긴으을 확장해 사용
* 기존 데이터 타입 (int, float 등)의 class에도 적용 가능

## 사용 시 주의할 점
* static 클래스의 메서드로 정의
* 메서드의 첫 매개 변수**는** this 키워드 한정자를 사용
* 메서드의 첫 매개 변수**만** this 키워드 한정자를 사용
* 메서드 호출은 객체에서 직접 부를 수도, .static 클래스를 통해 부를 수도 있다

```csharp
public static class MyExtension
{
  public static void ShowMyInt(this int n)
  {
    Console.WriteLine("{0}", n);
  }
}

class Program
{
  static void Main(string[] args)
  {
    int n = 100;
    n.ShowMyInt();
  }
}
```
  
## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/extension-methods>
* <https://durubiz.tistory.com/entry/Net-C-%ED%99%95%EC%9E%A5%EB%A9%94%EC%84%9C%EB%93%9C-extension-method>