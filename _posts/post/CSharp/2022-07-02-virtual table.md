---
title: "Method & Virtual Table"
classes: wide
categories: 
  - post
  - CSharp
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## Virtual Table의 구조
* C#에서 모든 클래스는 System.Object 클래스에서 상속되므로 VTable을 갖는다
  * 기본적으로 ToString, Equals, GetHashCode, Finalize 메서드를 VTable에 갖는다
* Base클래스가 가상 메서드가 없다면 이외의 메서드들은 VTable Slot에 추가되지 않는다

```csharp
class A
{
    public virtual void BaseMeth1() { }
    public virtual void BaseMeth2() { }
}
class B : A
{
    public void DerivedMeth1() { }
    public void DerivedMeth2() { }
}
```

![image](/assets/images/derived-vtable.png)

* 위 상속 클래스 A, B의 메서드 테이블


## Method Overriding

```csharp
class A
{
    public virtual void Run1() 
    {
        Console.WriteLine("A.Run1");
    }
    public virtual void Run2() { }
}
class B : A
{
    public override void Run1() 
    {
        Console.WriteLine("B.Run1");
    }        
    public void OtherRun() {}
}

// 케이스-A
A a = new A();
a.Run1(); 

// 케이스-B
A x = new B();
x.Run1();  
```

![image](/assets/images/VTable-view-range.png)
* 상속 계층에 따라 메서드 테이블이 다르게 구성된다

![image](/assets/images/derived-vtable-baseonly.png)
* Base Class인 A의 메서드 테이블 구성

![image](/assets/images/derived-vtable-overriding.png)
* Derived Class인 B의 메서드 테이블 구성
* Object class의 메서드, A의 메서드, B의 메서드 순서로 VTable이 구성되어 있을 거라 예상됐지만, B.Run1이 A 메서드 자리에 들어와 있고, A.Run1이 보이지 않는다
  * override 되었기 때문이다
* 파생 클래스의 VTable에 있는 base class의 가상 메서드 슬롯을 override된 메서드 포인터로 대체한다
  * 추가적인 메서드 슬롯을 만들지 않는다
  

## Method Hiding

```csharp
class A
{
    public virtual void Run1()
    {
        Console.WriteLine("A.Run1");
    }
    public virtual void Run2() 
    {
        Console.WriteLine("A.Run2");
    }
}
class B : A
{
    public override void Run1()
    {
        Console.WriteLine("B.Run1");
    }
    public new void Run2()
    {
        Console.WriteLine("B.Run2");
    }
}
class Program
{
    static void Main(string[] args)
    {
        //케이스-A
        A a = new B();        
        a.Run2();  // 베이스의 Run2 실행

        //케이스-B
        B b = (B) a;
        b.Run2(); // 파생클래스 Run2 실행
    }
}
```

* 위의 예시에서는 파생 클래스 B가 A의 가상 메서드인 Run2를 무시하고 새로운 Run2를 정의 및 구현했다
  * 이 경우 파생 클래스인 B는 Base 클래스인 A의 Run2를 사용할 수 없다

![image](/assets/images/method-hiding.png)

* IL 상으로는 메서드 테이블에는 A의 Run2가 목록에 있지만 override 되지 않은 B의 Run2도 동일한 이름으로 생성되었다
* 다시 위의 예시에서, 케이스-A는 A 타입으로 할당된 객체 B를 생성한다
  * 타입 A로 정의된 객체 a가 사용할 수 있는 메서드 테이블은 A의 메서드 테이블이다
  * System.Object의 테이블과 A.Run1, A.Run2 메서드가 있다
* 케이스-B는 a를 다시 B타입으로 변환했다
  * 이 경우 타입 B로 변환된 객체 b의 메서드 테이블은 B의 메서드 테이블이다
  * System.Object, A, B의 메서드 테이블을 사용할 수 있으나, A의 Run2 메서드는 숨김처리된다

## 메서드 호출 방식
* C# 컴파일러와 CLR에 의해 공등으로 실행된다

### Type Object
* C#에서의 메서드 호출의 기초를 이해하기 위해서는 CLR이 어떻게 타입을 관리하는지부터 알아야 한다
* 프로그램 구동에 필요한 모든 타입에 대해 CLR은 그에 해당하는 managed heap의 타입 오브젝트를 유지 관리한다
* 타입 오브젝트는 메서드 테이블을 가진다
  * 메서드가 어느 타입에 의해 구현되어 있는지, 어셈블리 상에서 어디에서 구현 코드를 찾을 수 있는지 알 수 있다
  * 메서드 테이블은 virtual method를 호출하는 데에 필수이다
  * 빠르고 간단한 참조를 위해, managed heap의 모든 객체는 type object pointer라는 것을 가지고 있고, 이를 통해 타입 오브젝트로의 직접 엑세스할 수 있다

### Type Object Pointer
* System.Type의 object는 object 그 자체로 Type의 객체(instance)이다
* Type Object Pointer도 object의 멤버로 있다
  * 이 포인터는 Type Object 스스로를 가리키고 있다
* <https://docs.microsoft.com/en-us/dotnet/api/system.type?view=net-6.0>

### 다형성과 가상 메서드 Polymorphism and virtual methods
* C# 프로그램의 함수 호출은 가상으로 실행된다

```csharp
static void Main(string[] args)
{
    Console.WriteLine(GetString("Hello World"));
}

string GetString(object arg)
{
    return arg.ToString();
}
```

* GetString 안에서 ToString은 object에 의해 호출되지만, ToString 메서드 구현은 System.String에 정의되어 있다
* 작동 순서는 다음과 같다
  1. 프로세스가 C# 컴파일러에 의해 실행된다
  2. arg.ToString() 메서드는 callvirt 를 통해 호출된다
  3. 이는 CLR이 ToString 함수를 virtual로 호출하도록 한다

* ToString이 호출될 때, 런타임은 arg의 타입 오브젝트를 통해 type object pointer에 접근한다
  * arg 자체는 string 타입이므로, System.String에 접근한다
* 거기서 메서드 테이블에 들어가 System.String이 제공하는 ToString의 Implementation을 찾는다
  * 이로써 메서드 코드에 접근하는 것이고, 필요하다면 컴파일을 거친 뒤 실행한다

![image](/assets/images/vtable.png)

* 만약 ToString을 지원하지 않는 object가 인자로 들어왔다면?
  * CLR은 상속 계층을 확인하며 해당 메서드를 가진 class를 찾는다
  * 이는 타입 오브젝트가 그 베이스 클래스의 타입에 대한 참조를 가지고 있기 때문에 가능하다
  * 상속 체인은 모든 .NET 프로그램에서 모든 타입에 대해 생성되고, 그 뿌리에는 System.Object가 있다

### Value types
* 상기한 방식은 타입 오브젝트와 type object pointer에 대해 지나치게 의존적이라는 약점이 있다 
* 값 타입의 메서드를 호출하는 데 managed heap이 없고, 그래서 type object pointer가 없는 타입이라면?

```csharp
static void Main(string[] args)
{
    var sb = new StringBuilder("Hello world.");
    sb.ToString();
    6.ToString();
    GetString(sb);
    GetString(6);
}

static string GetString(object arg)
{
    return arg.ToString();
}
```

* StringBuilder는 참조 타입이므로, 런타임은 ToString 함수를 호출할 때 type object를 사용할 것이다
  * 그리고 당연하게도, 정상적으로 작동할 것이다
  * C# 컴파일러는 거의 아무일도 하지않고, CLR이 알아서 메서드를 invoke 하도록 둘 것이다
* Int32 타입인 6은 어떨까?
  * value type인 int32는 navigate 할 type object pointer가 없다
  * 이 경우 C# 컴파일러는 CLR에게 nonvirtual call Systen.Int32에 작성된 ToString 구현 코드를 직접 호출하도록 명령한다
    * 때문에 CLR은 type object pointer가 필요없다
* GetString에 인자로 들어갈 때는 어떨까?
  * StringBuilder인 sb는 상기한 바와 동일하게 type object pointer를 통해 vtable을 참조한다
  * **C# 컴파일러가 Int32를 boxing하면서, type object pointer가 생성되어 heap에 있는 구현 코드에 포함된다**
  * 이제 GetString 안에 인자로 들어온 int32는 ToString을 호출할 때 type object pointer를 사용할 수 있다

## 요약
* 메서드 호출은 C# 컴파일러와 CLR에 의해 실행된다
* Virtual Method Call은 C# 프로그램 내에서 가장 흔하고 빈번하게 일어나는 호출 방식이며, CLR과 변수에 대응하는 타입 오브젝트에 의해 실행된다
* Nonvirtual Method Call은 실행되는 데 C# 컴파일러가 큰 역할을 하며, CLR의 역할도 일부 포함된다

### 근데 Boxing은 좀...
* 불필요한 boxing은 피하는 게 맞다
  * 그래서 상기 예시는 어떻게 boxing을 피하는 게 맞는지?

```csharp
static string GetString(int arg)
{
    return arg.ToString();
}
```

* 값 타입 자체로 인자를 받도록 하면 된다
  * 간단 그 자체다
  * IL 코드를 확인해보면 System.Object의 ToString이 아닌 System.Int32의 ToString이 호출됨을 확인할 수 있다
* 함수 overload에 의해 object 인자를 GetString에 넣는다고 하면 
  * static string GetString(object arg)이 호출될 것이다
  * object 타입의 인자를 int 타입을 받는 함수에 넣을 수는 없다
* int32가 값 타입이므로, int32의 하위 타입이 이 함수에 인자로 들어갈 일이 없다

## Managed Heap vs. Unmanaged Heap
### Managed Heap
* 프로세스가 런타임에 생성하는 주소 공간을 처리하는 구조
* 이 주소공간은 OS에 의해 특정 방식으로 처리될 때, Managed Heap이라 불린다
* .Net 프레임 워크에서 자동 메모리 관리 프로세스의 일부로 이 힙 모델을 사용한다
* Gargabe Collection이 주소공간에서 재할당 및 반환 여부를 평가하는 알고리즘이 포함된다

### Unmanaged Heap
* Managed Heap의 반대 개념
* 개발자들이 직접 할당 및 관리하는 주소 공간

## Vritual table의 위치

* 객체 레퍼런스가 가리키는 Heap에서 Type Handle이 Method table을 가리킨다

## 출처
* <https://www.csharpstudy.com/DevNote/Article/28>
* <https://www.levibotelho.com/development/how-method-calling-works/>
* <https://www.techopedia.com/definition/27305/managed-heap>
* <https://stackoverflow.com/questions/21852355/c-sharp-type-object-pointer>