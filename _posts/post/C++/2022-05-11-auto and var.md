---
title: "auto and var"
classes: wide
categories: 
  - post
  - C++
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---

## var in C#

```csharp
var i = 30; // 암시적 타입 선언
```
* C#에서의 var 키워드는 지역 변수에 한해서만 사용이 가능하다

## auto in C++
* C++에서의 auto는 변수의 타입을 추정할 뿐만 아니라, 일반함수와 탬플릿 함수의 반환 값도 추정할 수 있다

```c++
auto i = 10;

auto foo() { //deduced to be int
    return 5;
}

template<typename T, typename U>
auto add(T t, U u) {
    return t + u;
}
```

## 퍼포먼스 이슈?
* C++ auto 변수도 컴파일 타임에 타입을 정의(stripped)하기 때문에 퍼포먼스에 별도의 영향은 없다
* C#의 var 역시 IL로 컴파일하는 과정에서 익명 타입을 처리하는 것과 같은 추가적인 결과물이 없으므로, 별 영향이 없다
  * 애초에 IL 컴파일이 불가능한 코드라면 컴파일 에러가 발생했을 것이다

## 출처  
* <https://stackoverflow.com/questions/40781475/differences-between-c-sharp-var-and-c-auto>
* <https://stackoverflow.com/questions/19618759/does-auto-deduce-the-type-at-compile-time-or-runtime-in-c-11>
* <https://stackoverflow.com/questions/356846/will-using-var-affect-performance?rq=1>
* 
