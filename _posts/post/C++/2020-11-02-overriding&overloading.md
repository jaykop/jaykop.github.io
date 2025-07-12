---
title: "Overriding & Overloading"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## Overloading 
* 같은 이름의 메서드를 여러 개 정의 
* 매개변수의 타입이 다르거나, 갯수가 다름 
* 리턴 타입이나 접근 제어자는 영향을 주지 않음

```c++
int add(int a, int b);
float add(float a, float b);
int add(int a, int b, int c);
// ...
```

## Overriding 
* 상위 클래스의 메소드를 하위 클래스에서 재정의

```c++
// 베이스 클래스
class A
{
  // 오버라이딩할 메서드
  virtual void do_something(int a, int b);
}

// 파생 클래스
class B : A
{
  // 파생 클래스에서 재정의(오버라이딩)된 메서드
  void do_something(int a, int b) override;
}
```

## 굳이 override를 쓰는 이유?
* 부모 클래스에서 virtual keyword를 사용한 function이 있고, 이를 파생 클래스에서 overriding 할 때 명시적으로 이를 표시해주는 역할
* 필수적이지 않으나 코드 리딩에 도움을 줌
* 파생 클래스 메서드에서 override를 사용했는데 부모 클래스로부터 override할 함수가 없다면 컴파일 에러를 출력

```c++
class Base {

  // 오버라이딩을 허용한 부모 클래스의 메서드
  virtual void what() { std::cout << "기반 클래스의 what()" << std::endl; }
};

class Derived : public Base {

  // 파생 클래스에서는 명시적으로 overriding 했는지 나타내는 키워드 없음
  // 또한 const 한정자로 실제로 부모 클래스의 what과 다른 함수
  void what() const { std::cout << "파생 클래스의 what()" << std::endl; }
};

int main()
{
  Derived c;
  Base* p_c = &c;

  // 부모 클래스의 what() 출력!
  p_c->what();    
}
```

## 출처
* <https://modoocode.com/210>