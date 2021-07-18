---
title: "C#과 C++의 차이"
classes: wide
categories: 
  - blog
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
C# (*difference between C++)
C# needs CLR environment 
primitive variable types are actually encapsulated objects
requires more memory and slower speed
memory management
how it manages the memory?
object is created memory allocated, constructor runs (considered live)
if any part of object is not accessible other than calling destructor,
		considered no longer in use -> becomes eligible for destruction
at some unspecified time later, the destructor runs
once destructor is called no access is possible, 
		then make the object is eligible for collection
at some time later, it is returned to the memory
인터페이스 vs. 추상
클래스는 multiple interface 상속 가능, but single abstract 상속 가능
constructor for abstract, not for interface
interface는 메서드만메소드만, abstract는 필드 안에 변수 선언 가능
interface는 선언만, abstract는 구현 제공
둘 다 객체 선언 불가능
interface는 비추상 메소드 선언 불가, abstract는 가능
interface는 접근 지정자는 public; 변경 불가
상대적으로 abstract가 더 빠르게 작동

  
---  
출처:   
<https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/delegates/>  
<https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/concepts/covariance-contravariance/using-variance-in-delegates>
