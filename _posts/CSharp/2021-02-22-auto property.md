---
title: "Auto Property"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## Property
* 정보은닉을 더 간결하고 간단하게 구현하도록 허용
* get / set 메서드를 대신해 가독성을 보완

```csharp
// MyClass 원형
class MyClass
{
  private string name;
  public string GetName() {return name;}
  public void SetName(string name) {this.name = name;}
}

// Property 사용
class MyClass
{
  private string name;
  public string Name {
    get { return name; }
    set { name = value;}
  }
}

// 자동 Property 사용
class MyClass
{
  public string Name { get; set; }
}

// 클래스 외부에서 접근할 시 set 불가능
class MyClass
{
  public string Name { get; private set; }
}

// 초기화
class MyClass
{
  public string Name { get; set; } = "MyName";
}

// set 메서드 조건 추가
class MyClass
{
  public int day
  {
    get { return day; }
    set { if (1 <= value && value <= 31) day = value; }
  }
}
```
  
## public 필드와의 차이

```csharp
public class myint
{
    public int value{get;set;}
}

public class myint
{
    public int value;
}
```
* 사실 상기 두 클래스의 기능적 차이는 없음
* get/set에 대해 property 보다 더 제한된 aceess level을 부여하는 것만 가능

  ```csharp
  // error!
  private int maxTime { public get; public set; }

  // ok
  public int maxTime { get; private set; }
  ```

* property에 접근하는 데 더 많은 overhead가 발생
* 자동 프로퍼티는 .Net 프레임워크에서 데이터 바인딩에 많이 사용
* Reflection 사용 시 다르게 작동

## 출처
* <https://dobby-the-house-elf.tistory.com/298>
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/auto-implemented-properties>
* <https://constructionsite.tistory.com/38>
* <https://stackoverflow.com/questions/22497088/c-sharp-get-set-vs-without-get-set>