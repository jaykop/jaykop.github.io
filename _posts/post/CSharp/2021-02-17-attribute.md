---
title: "Reflaction & Attribute"
classes: wide
categories: 
  - post
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

      // 해당 형식의 생성자 목록
      // Void .ctor(System.String, Int32)
      ConstructorInfo[] coninfo = type.GetConstructors(); 
      Console.Write("생성자(Constructor) : "); 
      foreach (ConstructorInfo tmp in coninfo) 
        Console.WriteLine("\t{0}", tmp); 
      Console.WriteLine(); 

      // 해당 형식의 메서드 목록
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

      // 해당 형식의 변수들 목록
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

## 메타데이터란?
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

## 커스텀 애트리뷰트 예시
```csharp
// 아래 두 코드는 개념적으로 동일
[Author("P. Ackerman", version = 1.1)]  
class SampleClass  // ...

Author anonymousAuthorObject = new Author("P. Ackerman");  
anonymousAuthorObject.version = 1.1;  

// 이하 완성된 예제
// Multiuse attribute.  
[System.AttributeUsage(System.AttributeTargets.Class |  
                       System.AttributeTargets.Struct,  
                       AllowMultiple = true)  // Multiuse attribute.  
]  
public class Author : System.Attribute  
{  
    string name;  
    public double version;  
  
    public Author(string name)  
    {  
        this.name = name;  
  
        // Default value.  
        version = 1.0;  
    }  
  
    public string GetName()  
    {  
        return name;  
    }  
}  
  
// Class with the Author attribute.  
[Author("P. Ackerman")]  
public class FirstClass  
{  
    // ...  
}  
  
// Class without the Author attribute.  
public class SecondClass  
{  
    // ...  
}  
  
// Class with multiple Author attributes.  
[Author("P. Ackerman"), Author("R. Koch", version = 2.0)]  
public class ThirdClass  
{  
    // ...  
}  
  
class TestAuthorAttribute  
{  
    static void Test()  
    {  
        PrintAuthorInfo(typeof(FirstClass));  
        PrintAuthorInfo(typeof(SecondClass));  
        PrintAuthorInfo(typeof(ThirdClass));  
    }  
  
    private static void PrintAuthorInfo(System.Type t)  
    {  
        System.Console.WriteLine("Author information for {0}", t);  
  
        // Using reflection.  
        System.Attribute[] attrs = System.Attribute.GetCustomAttributes(t);  // Reflection.  
  
        // Displaying output.  
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
  
## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/concepts/attributes/accessing-attributes-by-using-reflection>
* <https://nowonbun.tistory.com/496>
* <https://blog.hexabrain.net/152>
* <https://docs.microsoft.com/ko-kr/dotnet/api/system.attribute?view=net-5.0>
* <https://docs.microsoft.com/ko-kr/dotnet/standard/attributes/writing-custom-attributes>
* <https://treeroad.tistory.com/entry/메타데이터란>