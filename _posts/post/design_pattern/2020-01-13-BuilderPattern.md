---
title: "빌더 패턴(Builder Pattern)"
classes: wide
categories: 
  - post
  - design_pattern
sidebar:
  nav: "main"
author_profile: true
---

## 빌더 패턴(Builder Pattern)
* 빌더 패턴은 객체 생성을 보다 유연하게 하기 위한 방법 중 하나
* 복잡한 기존 생성자를 별도로 실행한 뒤 조합
  - Builder 클래스를 이용해 각 파츠를 생성 후 조합
  - 클래스는 Builder에 객체에 object 생성을 맡기고, 직접 수행하지 않음
* 한번에 모든 생성 데이터를 가질 수 없어 순차적으로 정보 수집 후 마지막에 생성자 호출을 할때 사용

### 장점
  - 하나의 클래스를 내부적으로 다양하게 디자인 가능
  - 생성 코드 캡슐화
  - 객체 생성 과정을 제어 가능
  
### 단점
  - 각 파츠마다 ConcreteBuilder를 디자인해야 함
  - 구조적으로 복잡한 dependency가 될 수 있음

```csharp
/// <summary>
/// 빌더를 통해 생성되는 객체
/// </summary>
public class Bicycle
{
    public string Make { get; set; }
    public string Model { get; set; }
    public int Height { get; set; }
    public string Colour { get; set; }

    public Bicycle(string make, string model, string colour, int height)
    {
        Make = make;
        Model = model;
        Colour = colour;
        Height = height;
    }
}

/// <summary>
/// 추상 빌더
/// </summary>
public interface IBicycleBuilder
{
    string Colour { get; set; }
    int Height { get; set; }

    Bicycle GetResult();
}

/// <summary>
/// 실제 객체 생성 빌더
/// </summary>
public class GTBuilder : IBicycleBuilder
{
    public string Colour { get; set; }
    public int Height { get; set; }

    public Bicycle GetResult()
    {
        return Height == 29 ? new Bicycle("GT", "Avalanche", Colour, Height) : null;        
    }
}

/// <summary>
/// 객체 생성하는 Director
/// </summary>
public class MountainBikeBuildDirector
{
    private IBicycleBuilder _builder;
    public MountainBikeBuildDirector(IBicycleBuilder builder) 
    {
        _builder = builder;
    }

    public void Construct()
    {
        _builder.Colour = "Red";
        _builder.Height = 29;
    }
}

public class Client
{
    public void DoSomethingWithBicycles()
    {
        var builder = new GTBuilder(); // 빌더 생성
        var director = new MountainBikeBuildDirector(builder); // 디렉터에 빌더 할당

        director.Construct(); // 디렉터가 빌더에게 정보 전달
        Bicycle myMountainBike = builder.GetResult(); // 빌더가 최종 객체 생성
    }
}
```

## 출처
* <https://en.wikipedia.org/wiki/Builder_pattern>
