---
title: "perfect forwarding"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---


## 완벽한 전달 perfect forwarding
* wrapper 함수가 필요한 경우

```c++
// ex1) wrapper 함수의 예시
vec.push_back(A(1, 2, 3));

// 위와 동일한 작업을 수행한다
vec.emplace_back(1, 2, 3);  

// push_back 함수를 사용할 경우 컴파일러가 알아서 최적화를 해준다
// 불필요한 복사-이동을 수행하지 않고 emplace_back 을 사용했을 때와 동일한 어셈블리를 생성
// 따라서 push_back 을 사용하는 것이 훨씬 낫다
// emplace_back 은 예상치 못한 생성자가 호출될 위험이 있다

// ex2)
// wrapper 함수
template <typename T>
void wrapper(T u) {
  g(u);
}

class A {};

void g(A& a) { std::cout << "좌측값 레퍼런스 호출" << std::endl; }
void g(const A& a) { std::cout << "좌측값 상수 레퍼런스 호출" << std::endl; }
void g(A&& a) { std::cout << "우측값 레퍼런스 호출" << std::endl; }

int main() {
  A a;
  const A ca;

  std::cout << "원본 --------" << std::endl;
  g(a);
  g(ca);
  g(A());

  std::cout << "Wrapper -----" << std::endl;
  wrapper(a);
  wrapper(ca);
  wrapper(A());

// 결과:
// 원본 --------
// 좌측값 레퍼런스 호출
// 좌측값 상수 레퍼런스 호출
// 우측값 레퍼런스 호출
// Wrapper -----
// 좌측값 레퍼런스 호출
// 좌측값 레퍼런스 호출
// 좌측값 레퍼런스 호출
}
```

*  C++ 컴파일러가 템플릿 타입을 추론할 때 템플릿 인자 T 가 레퍼런스가 아닌 일반적인 타입이라면 const 를 무시하기 때문

```c++
// 아래 함수를 추가한다 하더라도 A()는 우측값으로 전달되기 때문에
// 여전히 컴파일 에러를 발생
template <typename T>
void wrapper(T& u) {
  g(u);
}

// 따라서 아래와 같이 2개의 함수를 모두 정의해 주면
// 정상적인 컴파일이 진행됨
template <typename T>
void wrapper(T& u) {
  std::cout << "T& 로 추론됨" << std::endl;
  g(u);
}

template <typename T>
void wrapper(const T& u) {
  std::cout << "const T& 로 추론됨" << std::endl;
  g(u);
}

// ...

wrapper(a);
wrapper(ca);
wrapper(A());

// 원본 --------
// 좌측값 레퍼런스 호출
// 좌측값 상수 레퍼런스 호출
// 우측값 레퍼런스 호출
// Wrapper -----
// T& 로 추론됨
// 좌측값 레퍼런스 호출
// const T& 로 추론됨
// 좌측값 상수 레퍼런스 호출
// const T& 로 추론됨
// 좌측값 상수 레퍼런스 호출

// A() 의 경우 const T& 로 추론되면서 g(const T&) 함수를 호출
// wrapper 안에 u는 항상 좌측값
// 언제나 좌측값 레퍼런스를 받는 함수들이 오버로딩
```

* 함수 인자가 늘어나면 모든 조합의 함수를 정의해줘야 함
  * 이는 대단히 비효율적
  * 일반적인 레퍼런스가 우측값을 받을 수 없기 때문에, 상수 레퍼런스의 조합도 정의해줘야 함
  * 디폴트로 상수 레퍼런스를 받게 한다면, 상수가 아닌 레퍼런스도 상수로 받게되는 문제점 발생

## 보편적 레퍼런스 Universal reference
* 템플릿 인자 T 에 대해서 우측값 레퍼런스를 받는 형태
  * 그저 우측값만 받는 레퍼런스와는 다름
  * 탬플릿 타입의 우측값 레퍼런스는 좌측값 역시 받을 수 있다

```c++

// 함수는 인자로 T && 를 받음
template <typename T>
void wrapper(T&& u) {

  // 여기에 forward 함수 추가!
  g(std::forward<T>(u));
}

class A {};

void g(A& a) { std::cout << "좌측값 레퍼런스 호출" << std::endl; }
void g(const A& a) { std::cout << "좌측값 상수 레퍼런스 호출" << std::endl; }
void g(A&& a) { std::cout << "우측값 레퍼런스 호출" << std::endl; }

int main() {
  A a;
  const A ca;

  std::cout << "원본 --------" << std::endl;
  g(a);
  g(ca);
  g(A());

  std::cout << "Wrapper -----" << std::endl;
  wrapper(a);
  wrapper(ca);
  wrapper(A());

// 원본 --------
// 좌측값 레퍼런스 호출
// 좌측값 상수 레퍼런스 호출
// 우측값 레퍼런스 호출
// Wrapper -----
// 좌측값 레퍼런스 호출
// 좌측값 상수 레퍼런스 호출
// 우측값 레퍼런스 호출
}
```

## 레퍼런스 겹침 규칙 reference collapsing rule
* 탬플릿 타입에서 우측값 인자를 받는 경우, 이 규칙에 따라 T 의 타입을 추론

```c++
// & 는 1 이고 && 은 0 이라 둔 뒤에, OR 연산
typedef int& T;
T& r1;   // int& &;   r1 은 int&
T&& r2;  // int& &&;  r2 는 int&

typedef int&& U;
U& r3;   // int&& &;  r3 는 int&
U&& r4;  // int&& &&; r4 는 int&&
```

* Wrapper에서 받은 인자가 우측값이고 이를 내부 함수에도 우측값으로 변환해 전달하려면
  * move 함수를 호출해야 함
  * 받은 인자가 우측값 레퍼런스 일때에만 move 함수를 호출해야 함
  * 이 문제를 forward 함수를 이용해 해결 가능

```c++
// forward 함수의 내부 모습
// remove_reference는 모든 &를 소거
template <class S>
S&& forward(typename std::remove_reference<S>::type& a) noexcept {
  return static_cast<S&&>(a);
}

// S = A& 일 때
A&&& forward(typename std::remove_reference<A&>::type& a) noexcept {
  return static_cast<A&&&>(a);
}

A& forward(A& a) noexcept { return static_cast<A&>(a); }

// S = A&& 일 때
A&&&& forward(typename std::remove_reference<A&&>::type& a) noexcept {
  return static_cast<A&&&&>(a);
}

A&& forward(A& a) noexcept { return static_cast<A&&>(a); }
```


# 출처  
* <https://modoocode.com/228#page-heading-0>