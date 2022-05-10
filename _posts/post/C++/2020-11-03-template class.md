---
title: "Template"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## 템플릿(Template)이란
* 함수나 클래스를 개별적으로 다시 작성하지 않아도, 여러 자료 형으로 사용할 수 있도록 하게 만들어 놓은 틀
* 함수 템플릿(Function Template)와 클래스 템플릿(Class Template)으로 분류

```c++
// 같은 기능을 하는, 다른 타입을 인자로 받는 두 함수
int sum(int a, int b)
{
    return a + b;
}
double sum(double a, double b)
{
    return a + b;
}

// 아래의 하나의 함수로 변환 가능
// 함수 템플릿
template <typename T>
T sum(T a, T b)
{
    return a + b;
}

// 배열 Vector를 직접 만든 경우,
// 어떤 타입이든지 받아 사용할 수 있음
// 클래스 템플릿
template <typename T>
class Vector {
  T* data;
  int capacity;
  // ...
}
```

## 특수화

```c++
// 아래와 같은 클래스 템플릿이 정의
template <typename A, typename B, typename C>
class test {};

// 일부만 특수화 하거나
template <typename B>
class test<int, B, double> {};

// 모든 특수화가 가능
template <>
class test<int, int, double> {};

// 위와 같은 특수화된 탬플릿에 대해 
// 오리지널 클래스 템플릿과는 다른 별도의 처리를 수행
```

## 비형식 인자
* 상수를 템플릿 인자로 받는 것

## 장점
* 타입마다 중복되는 코드를 줄일 수 있음
  * **불필요한 타입 변형을 막을 방법은 없음 (-> 단점)**
  * 제네릭 함수를 짧게 유지할 필요
* 컴파일 타임에 다형성을 부여할 수 있음 
  * vtable이 없으므로 런타임 속도가 빨라질 수 있음
* 컨테이너에 여러 타입의 객체를 저장할 수 있음

## 단점
* 코드의 가독성을 떨어뜨림
  * 디버깅이 어려워질 수 있음
* 컴파일러가 컴파일 도중에 각 템플릿 인스턴스에 대한 코드를 생성
  * 컴파일 타임은 비교적 느려짐
  * 템플릿 매개 변수를 추가할 수록 더 느려짐
* 실행 파일의 크기가 너무 커지면 퍼포먼스에 영향

## 출처
* <https://jjeongil.tistory.com/1033>
* <https://blockdmask.tistory.com/43>
* <https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=ruvendix&logNo=220950843517>