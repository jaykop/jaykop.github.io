---
title: "Nullable and Tenary"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## 물음표 연산자
* 두개가 연속적으로 쓰이는 예시

```csharp
// 아래 두 식 A, B는 동일하게 작동

// 식 A
MyClass ab = a ?? b;

// 식 B
MyClass ab = (a != null) ? a : b;
```

## 타입 뒤의 물음표 연산자
* 변수의 Boxing(참조 형식) 여부를 뜻함
* 쉽게 말하자면, nullable 여부를 뜻함

```csharp
int i1=1; //ok
int i2=null; //not ok
int? i3=1; //ok

// int? 는, "boxed" 정수 값을 의미한다
// 참조형 정수 값이므로, nullable이다
int? i4=null; //ok
```

### nullable type

```csharp
Nullable<int> a; // int? a; 와 동일
```

* null 을 가질 수 없는 값 형식 타입을 null이 될 수 있도록 변환
* int 등과 같은 데이터 타입에 대해 값이 없음을 표현하고자 하는 의도

```csharp
Nullable<int> a; // int? a; 와 동일
a = null;
Console.WriteLine(a);                     // null
Console.WriteLine(a.HasValue);            // false
Console.WriteLine(a.Value);               // throw an exception
Console.WriteLine(a.GetValueOrDefault()); // default value of int type


Nullable<int> b; // int? b; 와 동일
b = 10;
Console.WriteLine(b);                     // 10
Console.WriteLine(b.HasValue);            // true
Console.WriteLine(b.Value);               // 10
Console.WriteLine(b.GetValueOrDefault()); // 10
```
  
## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/language-reference/operators/conditional-operator>
* <https://social.msdn.microsoft.com/Forums/vstudio/en-US/4107d47b-b1c4-495d-a67a-6ad3f2e7adbc/what-does-int-mean?forum=csharpgeneral>
* <https://blockdmask.tistory.com/360>
