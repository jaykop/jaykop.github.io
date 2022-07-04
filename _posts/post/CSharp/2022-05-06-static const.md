---
title: "static과 const"
classes: wide
categories: 
  - post
  - CSharp
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## static const in C++

### terminology
* Translation Unit
  * 컴파일러는 번역을 단위별로 실행하는데, 이때 컴파일러가 문장을 번역하는 단위를 Translation Unit라 한다
  * 모듈이라고 생각하면 될 것 같다
* Static linkage
  * 이는 해당 모듈 안에서만 접근이 가능하다
* Extenal linkage
  * 다른 모듈에서도 접근이 가능하다

### namespace에서의 static

```c++
static const int sci = 0; // sci is explicitly static
const int ci = 1;         // ci is implicitly static
extern const int eci = 2; // eci is explicitly extern
extern int ei = 3;        // ei is explicitly extern
int i = 4;                // i is implicitly extern
static int si = 5;        // si is explicitly static
```
* 위의 전역변수들의 타입은 주석과 같다
* C++ namespace에서 const의 default는 static이다
  * 둘 다 컴파일 타임에 초기화되며, const-initilaize 혹은 zero-initialize를 시행한다
  * 각각 Data segment와 BSS로 나뉜다

## static const in C#

```csharp
public static const string CONST_NAME = "blah";
```

* 위의 코드는 에러를 발생시킨다
* **C#에서의 const는 기본적으로 static이다**
  * 그럼에도 불구하고, const에 static 키워드를 추가할 수는 없다

### C++과의 차이점?
* static은 read/write 가능하며 메모리에 할당할 저장 공간이 필요하고 런타임에 초기화되어야 한다
  * 해당 static 변수에 접근하기 전까지 정적 생성자는 호출하지 않는다
  * static 변수가 저장되는 공간은 Heap이다
* const는 값 변경이 불가능하고 (대개) 컴파일 타임에 초기화된다
  * 컴파일 타임에 곧장 생성 코드에 임베드 되며, 런타임에 이를 위한 변수가 필요하지 않다

## 출처   
* <https://quick-adviser.com/are-static-variables-initialized-at-compile-time/>
* <https://stackoverflow.com/questions/177437/what-does-const-static-mean-in-c-and-c>
* <https://stackoverflow.com/questions/408192/why-cant-i-have-public-static-const-string-s-stuff-in-my-class>
* <https://stackoverflow.com/questions/842609/why-does-c-sharp-not-allow-const-and-static-on-the-same-line>
* <https://www.codeproject.com/Questions/1223199/Static-members-initialized-or-invoked-at-compile-t>
