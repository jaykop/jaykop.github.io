---
title: "Reflection & Attribute"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## 리플렉션의 개념
* 일반적으로는 클래스를 통해 객체를 생성
  * 사용자(프로그래머)는 클래스의 필드와 메서드를 알고 있고, 사용하는 데 불편함이 없다

### 리플렉션(Reflection)
* 프로그램 실행 도중 객체 정보를 조사
* 형식의 이름을 통해 인스턴스를 생성하고 그 인스턴스의 메서드를 호출할 수도 있다
* 필드와 속성에 접근할 수 있는 기능을 제공

|형식|메서드|설명|
|:---:|:---::---:|
|Type|GetType()|지정된 형식의 Type 개체를 가져옴|
|MemberInfo[]|GetMembers()|해당 형식의 멤버 목록을 가져옴|
|MethodInfo[]|GetMethods()|해당 형식의 메서드 목록을 가져옴|
|FieldInfo[]|GetFields()|해당 형식의 필드 목록을 가져옴|

```csharp
using System; 
using System.Collections.Generic; 
using System.Linq; using System.Text; 
using System.Reflection; 
using System.Threading.Tasks; 
namespace ConsoleApplication43 { 

  // 예시 클래스와 그 변수, 메서드
  class Animal { 
    public int age; 
    public string name; 
    public Animal(string name, int age) 
    { 
      this.age = age; 
      this.name = name; 
    } 
    
    public void eat() 
    { 
      Console.WriteLine("먹는다!"); 
    } 
    
    public void sleep() 
    { 
      Console.WriteLine("잔다!"); 
    } 
  } 
  
  // 엔트리 포인트
  class Program 
  { 
    static void Main(string[] args) 
    { 
      Animal animal = new Animal("고양이", 4); 
      Type type = animal.GetType(); // 해당 형식의 타입

      // 해당 형식의 생성자 목록을 알아낼 수 있다
      // Void .ctor(System.String, Int32)
      ConstructorInfo[] coninfo = type.GetConstructors(); 
      Console.Write("생성자(Constructor) : "); 
      foreach (ConstructorInfo tmp in coninfo) 
        Console.WriteLine("\t{0}", tmp); 
      Console.WriteLine(); 

      // 해당 형식의 메서드 목록을 알아낸다
      // Void eat() 
      // Void sleep()    
      // System.String ToString()
      // Boolean Equals(System.Object)
      // Int32 GetHashCode()
      // System.Type GetType()
      MemberInfo[] meminfo = type.GetMethods(); 
      Console.Write("메소드(Method) : "); 
      foreach (MethodInfo tmp in meminfo) 
        Console.Write("\t{0}", tmp); 
      Console.WriteLine(); 

      // 해당 형식의 변수들 목록을 출력한다
      // Int32 age 
      // System.String name
      FieldInfo[] fieldinfo = type.GetFields(); 
      Console.Write("필드(Field) : "); 
      foreach (FieldInfo tmp in fieldinfo) 
        Console.Write("\t{0}", tmp); 
      Console.WriteLine(); 
    } 
  } 
}
```

### 리플렉션을 사용하는 이유?
* 리플렉션은 어셈블리, 타입, 그 멤버를 읽어낼 수 있다
* 런타임에서 unknown object나 assembily를 구분해낸다는 것은 강력한 기능임에 틀림없다
  * 다만 작동방식이 프로세스에서 작동하는 스태틱 코드와 비교할 때는 현저히 느리기도 하다

### 리플렉션 사용 예시
* 어셈블리의 의존성을 파악할 때
* interface, derived class from base/abstract, member method/variable 의 type 탐색 탐색
* 여러모로 디버깅하는 데에 있어 도움이 된다고 생각하면 될 듯
* 그 외에도
  *  런타임에 클래스나 코드를 생성할 수 있다
  *  IDE 같은 코드를 검사하는 프로그램에서 리플렉션 기능은 필수이다

## [메타데이터](https://jaykop.github.io/post/csharp/.Net-Compatible/#%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0)란?
* Data에 대한 구조화된 Data
* 다른 Data를 설명해주는 Data
* 대량의 정보 가운데 찾고 있는 정보를 효율적으로 찾아내서 이용하기 위해 일정한 규칙에 따라 콘텐츠에 대하여 부여되는 데이터
* 어떤 데이터 즉 구조화된 정보를 분석, 분류하고 부가적 정보를 추가하기 위해 그 데이터 뒤에 함께 따라가는 정보

## 애트리뷰트(Attribute)
* 클래스에 메타데이터를 추가할수 있도록 제공
* **Conditional**
  - Conditional은 메소드에만 적용
  - 메소드를 컴파일 할지 말지의 여부를 조건부로 결정
  - 기호가 정의되어 있으면 호출, 아니라면 생략
* **Obsolete**
  - 메서드 사용 시 경고 또는 에러를 발생
  - 두번째 boolean 인자
    - false: 경고 발생 (default 값)
    - true: 에러 발생
* **DllImport**
  - 외부 DLL에 정의된 함수를 사용

### 커스텀 애트리뷰트 예시
```csharp
// 아래 두 코드는 개념적으로 정의하는 바가 동일
[Author("P. Ackerman", version = 1.1)]  
class SampleClass : Author
{
  // ...
} 

SampleClass anonymousAuthorObject = new SampleClass("P. Ackerman");  
anonymousAuthorObject.version = 1.1;  

//======================================================//
// 이하 예시
[System.AttributeUsage(System.AttributeTargets.Class |  
                       System.AttributeTargets.Struct,  
                       AllowMultiple = true)  // 여러 개의 어트리뷰트를 명시하도록 허용
]  
public class Author : System.Attribute  
{  
    string name;  
    public double version;  
  
    public Author(string name)  
    {  
        this.name = name;  
  
        // 초기화  
        version = 1.0;  
    }  
  
    public string GetName()  
    {  
        return name;  
    }  
}  
  
// Author attribute가 명시된 Class
[Author("P. Ackerman")]  
public class FirstClass : Author
{  
    // ...  
}  
  
// Author attribute가 명시되지 않은 Class
public class SecondClass : Author
{  
    // ...  
}  
  
// 복수 개의 Author attribute가 명시된 Class
[Author("P. Ackerman"), Author("R. Koch", version = 2.0)]  
public class ThirdClass : Author 
{  
    // ...  
}  
  
class TestAuthorAttribute  
{  
    // 위의 예시로 든 클래스들의 타입 정보를 차례대로 출력한다
    static void Test()  
    {  
        PrintAuthorInfo(typeof(FirstClass));  
        PrintAuthorInfo(typeof(SecondClass));  
        PrintAuthorInfo(typeof(ThirdClass));  
    }  
  
    private static void PrintAuthorInfo(System.Type t)  
    {  
        System.Console.WriteLine("Author information for {0}", t);  
  
        // 타입 인자 t의 어트리뷰트를 추출한다
        // 런타임에서 타입을 확인하는 방식, 즉 리플렉션이다
        System.Attribute[] attrs = System.Attribute.GetCustomAttributes(t); 
  
        // 결과를 출력한다
        foreach (System.Attribute attr in attrs)  
        {  
            if (attr is Author)  
            {  
                Author a = (Author)attr;  
                System.Console.WriteLine("   {0}, version {1:f}", a.GetName(), a.version);  
            }  
        }  
    }  
}  
/* Output:  
    Author information for FirstClass  
       P. Ackerman, version 1.00  
    Author information for SecondClass  
    Author information for ThirdClass  
       R. Koch, version 2.00  
       P. Ackerman, version 1.00  
*/  
```
  
* 위의 예시에서 AllowMultiple는 조금 이상하게 소개되었다
  * AllowMultiple 는 = false로 선언함으로써(default) 중복 attribute를 차단할수 있다
  * 혹은 여러 attribute의 속성을 가지도록 허용할 수 있다

## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/concepts/attributes/accessing-attributes-by-using-reflection>
* <https://nowonbun.tistory.com/496>
* <https://blog.hexabrain.net/152>
* <https://docs.microsoft.com/ko-kr/dotnet/api/system.attribute?view=net-5.0>
* <https://docs.microsoft.com/ko-kr/dotnet/standard/attributes/writing-custom-attributes>
* <https://treeroad.tistory.com/entry/메타데이터란>
* <https://nomad-programmer.tistory.com/201>
* <https://stackoverflow.com/questions/1458256/why-is-the-use-of-reflection-in-net-recommended>
* <https://stackoverflow.com/questions/723328/c-can-someone-explain-the-practicalities-of-reflection>
* <https://you-rang.tistory.com/270>
* <https://world.optimizely.com/forum/developer-forum/CMS/Thread-Container/2019/3/what-is-the-role-ofallowmultipletruefalse/>