---
title: "GetType과 typeof의 차이"
classes: wide
categories: 
  - post
  - CSharp
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## typeof
* 클래스 자체의 타입을 반환

```csharp
class Animal {}

System.Type t1 = typeof(Animal); // t1에 Animal이 타입으로서 반환
```

## GetType
* 런타임시 생성되는 객체 본래의 타입을 반환

```csharp
class Animal {}
class Dog : Animal {}

void PrintType (Animal a)
{
  bool b1 = a.GetType() == typeof(Animal);  // a 인자의 본래 타입은 Dog -> false
  bool b2 = a is Animal;                    // a 인자의 클래스는 Animal이기도 함
  bool b3 = a.GetType() == typeof(Dog);     // a 인자의 본래 타입은 Dog -> True
}

Dog d = new Dog();
PrintType(d);
```

## 출처
* <https://guslabview.tistory.com/270>