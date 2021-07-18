---
title: "팩토리 패턴(Factory Pattern)"
classes: wide
categories: 
  - blog
  - etc
---
## 탬플릿 메소드 패턴(template method pattern)
* 소프트웨어 공학에서 동작 상의 알고리즘의 프로그램 뼈대를 정의하는 행위 디자인 패턴
* 알고리즘의 구조를 변경하지 않고 알고리즘의 특정 단계들을 다시 정의할 수 있게 해준다
  * base class가 알고리즘 구조의 주요 골조를 확립
  * subclass가 나머지 부분을 채워주면서 특정 알고리즘을 수행하도록 확장

## 팩토리 패턴(Factory Pattern)
* 팩토리 패턴은 템플릿 메소드 패턴의 일종으로, 부모 클래스에서 상속된 여러 자식 클래스 중 하나를 리턴하는 디자인 패턴
* 사전 정의되지 않은, 또는 인터페이스로서 제공되거나 동적으로 정의된 컴포넌트를 가진 클래스를 생성 
    - ex) 
    - 탈것 클래스에서 모터 컴포넌트가 존재하지만, 모터의 구체적인 타입은 정의되지 않은 상태. 
    - 추후 탈것 생성자에서 전기모터/가솔린모터 등으로 구체화 가능.
    - 탈 것 생성자 내부에서 모터 팩토리를 콜함
* 사전 정의되지 않은 컴포넌트의 부모 클래스에 의해 동적 선언되는 또는 인터페이스만 제공되는 하위 클래스를 생성할 수 있도록 허용.  
    - ex) 
    - 탈것 클래스는 전기비행선과 구형차량 따위의 하위클래스로 선언될 수 있고, 멤버로 동적 할당될 타입의 모터를 가지고 있음. 
    - 하위 클래스가 생성되는 시점에 모터도 어떤 타입이 선언될 지 결정됨.
    - 모터 타입이 히든으로 제공된다는 전제로 탈 것 팩토리를 이용해 하위 클래스를 선언하는 것이 가능
* 여러 개의 생성자가 존재하더라도, 코드 가독성을 보장
    - ex)  
      ```csharp
      // 아래 2개 보다는
      Vehicle(make:string, motor:number);
      Vehicle(make:string, owner:string, license:number, purchased:date);

      // 이 2개가 더 이해하기 쉬움
      Vehicle.CreateOwnership(make:string, owner:string, license:number, purchased: date);
      Vehicle.Create(make:string, motor:number);
      ```
* 상위 클래스의 접근을 차단하고 바로 하부 클래스의 객체화를 하도록 디자인 
    - ex) 
    - 탈것 클래스에 대한 생성자 접근을 외부로부터 차단
    - 오직 하위클래스에 대한 접근만을 허용하여 팩토리 메서드를 통해 생성되도록 허용
  
```csharp
public abstract class Pizza
{
    public abstract decimal GetPrice();

    public enum PizzaType
    {
        HamMushroom, Deluxe, Seafood
    }
    public static Pizza PizzaFactory(PizzaType pizzaType)
    {
        switch (pizzaType)
        {
            case PizzaType.HamMushroom:
                return new HamAndMushroomPizza();

            case PizzaType.Deluxe:
                return new DeluxePizza();

            case PizzaType.Seafood:
                return new SeafoodPizza();

        }

        throw new System.NotSupportedException("The pizza type " + pizzaType.ToString() + " is not recognized.");
    }
}
public class HamAndMushroomPizza : Pizza
{
    private decimal price = 8.5M;
    public override decimal GetPrice() { return price; }
}

public class DeluxePizza : Pizza
{
    private decimal price = 10.5M;
    public override decimal GetPrice() { return price; }
}

public class SeafoodPizza : Pizza
{
    private decimal price = 11.5M;
    public override decimal GetPrice() { return price; }
}

// Somewhere in the code
...
  Console.WriteLine( Pizza.PizzaFactory(Pizza.PizzaType.Seafood).GetPrice().ToString("C2") ); // $11.50
...
```

## 빌더 패턴와 팩토리 패턴의 차이
* 빌더 패턴은 복잡한 구조를 순차적으로 생성하는 데 초점이 맞춰져 있다. 가장 팩토리 패턴은 객체의 파생 그룹 자체에 중점을 둔다.
* 빌더는 여러 단계를 거쳐 마지막에 완성된 객체를 반환하지만, 추상 팩토리는 객체를 즉각 반환한다.
* 빌더는 조합된 결과물을 생성한다.

## 추상 팩토리 패턴
* 다양한 구성 요소 별로 '객체의 집합'을 생성해야 할 때 유용하다. 
* 이 패턴을 사용하여 상황에 알맞은 객체를 생성할 수 있다.
* 이 패턴의 가장 밑바탕은 ***"하위 클래스들의 실구현 없이 오직 interface를 통해 객체의 연관 집합을 생성하는 것"***이다.

## 추상 팩토리 패턴과 팩토리 메서드의 차이
* 팩토리 메서드는 ***메서드***이고, 추상 팩토리는 ***객체***다.
* 팩토리 메서드는 메서드이며, 다른 하위 클래스에 의해 overriding이 가능하다.
  - ***... the Factory Method pattern uses inheritance and relies on a subclass to handle the desired object instantiation.***  
    ```csharp
    class A {
      public void doSomething() {
          Foo f = makeFoo();
          f.whatever();   
      }

      protected Foo makeFoo() {
          return new RegularFoo();
      }
    }

    class B extends A {
        protected Foo makeFoo() {
            // 하위 클래스가 다른 객체를 반환하기 위해 overrding
            return new SpecialFoo();
        }
    }
    ```
* 추상 팩토리는 여러 팩토리 메서드가 얽힌 하나의 객체다.
  - ***... with the Abstract Factory pattern, a class delegates the responsibility of object instantiation to another object via composition ...***  
    ```csharp
    class A {
      private Factory factory;

      public A(Factory factory) {
          this.factory = factory;
      }

      public void doSomething() {
          //객체 f는 constructor에서 할당받은 factory에 의존한다.
          //만약 다른 factory를 할당했다면, foo의 값도 달라질 것이다.
          Foo f = factory.makeFoo();
          f.whatever();
      }
    }

    interface Factory {
        Foo makeFoo();
        Bar makeBar();
        Aycufcn makeAmbiguousYetCommonlyUsedFakeClassName();
    }

    //이하 interface Facotry를 실구현하는 concrete factory...
    ```

## 출처
* <https://ko.wikipedia.org/wiki/%ED%85%9C%ED%94%8C%EB%A6%BF_%EB%A9%94%EC%86%8C%EB%93%9C_%ED%8C%A8%ED%84%B4>
* <https://en.wikipedia.org/wiki/Factory_method_pattern>
* <https://en.wikipedia.org/wiki/Abstract_factory_pattern>
* <https://stackoverflow.com/questions/757743/what-is-the-difference-between-builder-design-pattern-and-factory-design-pattern>
