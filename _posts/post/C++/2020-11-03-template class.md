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
// 아래와 같은 클래스 템플릿 정의
template <typename A, typename B, typename C>
class test {};

// 일부만 특수화 하거나
// => 부분 특수화
template <typename B>
class test<int, B, double> {};

// 모든 특수화가 가능
// => 완전 특수화
template <>
class test<int, int, double> {};

// 위와 같은 특수화된 탬플릿에 대해 
// 오리지널 클래스 템플릿과는 다른 별도의 처리를 수행
```

### 명시적 특수화
* 특정 타입의 매개변수에 대해 별도로 처리하고 싶을 때 사용
* 호출 순서
  * 일반 함수 >> 명시적 특수화 탬플릿 함수 >> 탬플릿 함수

```c++
// 일반 함수
int add(int a, int b)
{
  return a+b;
}

// 탬플릿 함수
template <typename T>
T add(T a, Tb)
{
  return a+b;
}

// 명시적 특수화 탬플릿 함수
template<>
double add<double>(double a, double b)
{
  return a+b;
}

...

int main()
{
  // 명시적 특수화 add 함수를 호출
  auto sum = add(10.1, 20.5);
}
```

### 탬플릿 클래스의 부분 특수화

```c++
// 아래와 같은 탬플릿 클래스가 있다고 할 때,
template <typename T1, typename T2>
class MyClass
{
        ...
};

// 아래와 같은 부분 특수화가 가능하다

// 1) 동일한 타입의 인자를 2개 받는 부분 특수화
template <typename T>
class MyClass<T, T>
{
    ...
};

// 2) 두 번째 인자를 정수형으로 받는 부분 특수화
template <typename T>
class MyClass<T, int>
{
    ...
};

// 3) 두 인자를 모두 타입의 포인터로 받는 부분 특수화
template <typename T1, typename T2>
class MyClass<T1*, T2*>
{
    ...
};

// 아래와 같이 선언했을 때, 
MyClass<int, int> m;    // MyClass<T, T>와 MyClass<T, int> 긴의 모호성으로 인한 에러 발생
MyClass<int*, int*> m;  // MyClass<T, T>와 MyClass<T1*, T2*> 긴의 모호성으로 인한 에러 발생

// 아래 부분 특수화를 선언해주면 해결 가능
template <typename T>
class MyClass<T*, T*>
{
    ...
};
```

### 탬플릿 함수의 부분 특수화
* 기존벅으로 불가능하다
* 탬플릿 클래스의 멤버 함수 전체를 특수화할 수는 있으나, 일부만 특수화는 불가능하다
* 함수 탬플릿 자체도 부분 특수화는 불가능하다

## 비형식 매개변수
* 상수를 템플릿 인자로 받는 것

```c++
template<typename T, template<typename U, int I> class Arr>
class MyClass2
{
    T t; // OK, T는 있습니다.
    Arr<T, 10> a;
    
    U u; //Error, U는 스코프 내에 없어요.
    // Arr 클래스에서 받는 인자
    // 위의 Arr<T, 10> a;에서 10 = U
};
```

## 구체화

### 암시적 구체화
* 일반적으로 탬플릿 함수를 구현하고 이를 사용할 때 발생

```c++
// 탬플릿 함수
template <typename T>
T add(T a, Tb)
{
  return a+b;
}

int main()
{
  // T = int로 하는 탬플릿 함수의 구현이 필요하다고 컴파일러에게 전달
  add(10, 5);
}
```

### 명시적 구체화
* 탬플릿 함수의 정의를 이용하여 특정 타입을 사용하는 함수를 정의하라고 컴파일러에게 명시적으로 전달
* 이를 전달받은 컴파일러는 해당 함수의 사용 여부에 상관없이 정의 코드를 생성한다
  * 원래는 탬플릿 함수를 정의하고, 이를 특정 타입에 대해 사용하는 경우에만 컴파일러가 코드를 생성한다

```c++
// 명시적 특수화
// 탬플릿 함수 template<typename T> T add(...)를 사용하지만,
// double 타입을 사용하는 경우에는 다른 정의로 사용하고 싶을 때
template<>
double add<double>(double a, double b)
{
  return a+b;
}

// 명시적 구체화
// 사용 여부에 상관없이 double을 사용하는 탬플릿 함수 정의 코드를 
// 생성하도록 컴파일러에게 전달
template
double add<double>(double a, double b)
{
  return a+b;
}
```

## 탬플릿 사용의 장단점

### 장점
* 타입마다 중복되는 코드를 줄일 수 있음
  * **불필요한 타입 변형을 막을 방법은 없음 (-> 단점)**
  * 제네릭 함수를 정의할 때도 짧게 유지할 필요가 있음
* 컴파일 타임에 다형성을 부여할 수 있음 
  * vtable이 없으므로 런타임 속도가 빨라짐
* 컨테이너에 여러 타입의 객체를 저장할 수 있음

### 단점
* 코드의 가독성을 떨어뜨리고 디버깅이 어려워질 수 있음
* 컴파일러가 컴파일 도중에 각 템플릿 인스턴스에 대한 코드를 생성
  * 컴파일 타임이 더 많이 소요되고, 템플릿 매개 변수를 추가할 수록 더 느려짐
* 코드가 많아지면서 실행 파일의 크기가 너무 커져도 퍼포먼스에 영향을 줄 수 있음

## 출처
* <https://jjeongil.tistory.com/1033>
* <https://blockdmask.tistory.com/43>
* <https://wikidocs.net/410>
* <https://openmynotepad.tistory.com/34>
* <https://hombody.tistory.com/307>
