---
title: "Template vs. Generic"
classes: wide
categories: 
  - post
  - C++
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---

## C++ Template vs. C# Generic
* C++ 은 컴파일이 1번 일어나고, C# 제네릭은 컴파일이 2번 일어난다.
  * C++ 템플릿은 사용하지 않으면 컴파일하지 않는다. 
  * 하지만, C# 제네릭은 사용하지 않더라도 그에 관련된 정보를 저장하기 위한 메타데이터가 생성된다.
* 제네릭은 [비형식 탬플릿 매개변수](https://jaykop.github.io/post/c++/template-class/#%EB%B9%84%ED%98%95%EC%8B%9D-%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98)를 허용하지 않는다
* 제네릭은 [명시적 특수화](https://jaykop.github.io/post/c++/template-class/#%EB%AA%85%EC%8B%9C%EC%A0%81-%ED%8A%B9%EC%88%98%ED%99%94)를 지원하지 않는다
* 제네릭은 [부분적 특수화](https://jaykop.github.io/post/c++/template-class/#%ED%83%AC%ED%94%8C%EB%A6%BF-%ED%81%B4%EB%9E%98%EC%8A%A4%EC%9D%98-%EB%B6%80%EB%B6%84-%ED%8A%B9%EC%88%98%ED%99%94)를 지원하지 않는다
* 템플릿은 템플릿-템플릿 매개 변수를 지원하지만 제네릭은 지원하지 않습니다.
  * C++: template<template<class T> class X> class MyClass
* 제네릭은 제네릭 형식의 기본 클래스로 형식 매개 변수를 허용하지 않지만 템플릿은 허용합니다.

  ```c++
  class A
  {
      // ...
  };

  template <class T>
  class B : T
  {
      // ...
  };
  ```

  * C++에서는 위와 같은 코드가 작동한다

  ```csharp
  class A
    {
        // ...
    };

    class B<T> : T
    {
        // ...
    };
  ```
  * C#에서는 위의 코드가 에러를 발생 시킨다
  * ***형식 매개변수이므로 T에서 파생될 수 없습니다***

## 차이가 발생하는 이유
* C++ 템플릿의 경우, 한 번의 컴파일로 최종 결과물 생성
  * 현재 컴파일하는 시점에 해당 코드가 유효한 지 모두 검증 가능
* 하지만 제너릭의 경우에는 IL 혹은 ByteCode로 컴파일 되더라도 최종이 아님
  * 이를 이용하여 다른 결과물을 도출 가능
  * 때문에 해당 제네릭이 어떻게 사용될 지 첫번째 컴파일에서 결정 불가

## 형식 매개변수와 실 매개변수

```c++
void func(int a)
{
  // a를 가지고 막 뭐를 함
}

// main에서는 func 함수에 인자로 num 변수를 넣음
int main()
{
  int num = 5;
  func(num):
  return 0;
}
```

* 위의 코드에서 형식 매개변수는 a
* 실 매개변수는 num
* **실 매개변수는 함수 호출 시 실제로 인자로 넣어주는 변수**
* **형식 매개변수는 함수 선언 시 매개 변수로 정의한 변수**

## 출처  
* <https://docs.microsoft.com/ko-kr/cpp/extensions/generics-and-templates-visual-cpp?view=msvc-170#:~:text=%EC%A0%9C%EB%84%A4%EB%A6%AD%EA%B3%BC%20C%2B%2B%20%ED%85%9C%ED%94%8C%EB%A6%BF%EC%9D%98,%EA%B0%80%20%EC%9E%88%EB%8A%94%20%ED%98%95%EC%8B%9D%EC%9D%B4%20%EC%95%84%EB%8B%99%EB%8B%88%EB%8B%A4.&text=%EC%A0%9C%EB%84%A4%EB%A6%AD%EC%9D%80%20%EB%AA%A8%EB%93%A0%20%EC%B0%B8%EC%A1%B0%20%ED%98%95%EC%8B%9D,%EC%BD%94%EB%93%9C%20%EC%A1%B0%EA%B0%81%EC%9C%BC%EB%A1%9C%20%EC%83%9D%EC%84%B1%EB%90%A9%EB%8B%88%EB%8B%A4.>
* <https://velog.io/@katze9027/C-%ED%85%9C%ED%94%8C%EB%A6%BF%EA%B3%BC-C-%EC%A0%9C%EB%84%A4%EB%A6%AD%EC%9D%98-%EC%B0%A8%EC%9D%B4>
* <https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=hotleader&logNo=221504268966>