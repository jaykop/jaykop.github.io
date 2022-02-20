---
title: "스마트 포인터 - unique_ptr"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## 자원 관리를 못하는 순간

```c++
class A {
  int *data;

 public:
  A() {
    data = new int[100];
    std::cout << "자원을 획득함!" << std::endl;
  }

  ~A() {
    std::cout << "자원을 해제함!" << std::endl;
    delete[] data;
  }
};

void thrower() {
  // 예외를 발생시킴!
  throw 1;
}

void do_something() {
  A *pa = new A();
  thrower();

  // 발생된 예외로 인해 delete pa 가 호출되지 않는다!
  delete pa;
}

int main() {
  try {
    do_something();
  } catch (int i) {
    std::cout << "예외 발생!" << std::endl;
    // 예외 처리
  }
}
```
* 잘못된 메모리 관리로 인한 문제점
  1. 예외는 정상적으로 처리되었으나, 소멸자가 호출되지 않아 **메모리 누수**가 발생
    * 프로그램이 필요하지 않은 메모리를 계속 점유하고 있는 현상
    * 사용 후 반환되지 않는 메모리가 누적되면 메모리가 낭비
  2. 이미 해제된 메모리를 다시 참조하는 경우 (double free)

  ```c++
  // 같은 메모리 주소를 2개의 포인터가 공유
  // 객체의 소유권이 명확하지 않은 경우
  Data* data = new Data();
  Date* data2 = data;

  // data 의 입장 : 사용 다 했으니 소멸시켜야지.
  delete data;

  // ...

  // data2 의 입장 : 나도 사용 다 했으니 소멸시켜야지
  delete data2;
  ```

## RAII
* Managed Language 는 가비지 컬렉터가 기본적으로 내장
  * 프로그램 상에서 더 이상 쓰이지 않는 자원을 자동으로 해제
  * 프로그래머들이 자원을 해제하는 일로부터 자유로움
* Unmanaged Language인 C++는 다름
* ***Resource Acquisition Is Initialization***
  * **자원 관리는 초기화이다**
  * 자원 관리를 스택에 할당한 객체를 통해 수행
  * **stack unwinding**을 통해 예외가 발생하더라도, stack frame을 빠져나갈 때 소멸자를 호출하는 원리를 이용
    * 스택의 항상성 유지를 위함
    * 예외 발생시, 함수 내부에 catch 구문이 없다면 호출원을 거슬러 올라가여 스택을 정리
  * 일반적인 포인터가 아닌, 객체로서의 포인터를 정의
    * auto_ptr을 보완하는 새로운 스마트 포인터

## unique_ptr
* 객체에 대한 유일한 소유권을 보장
  * **복사 금지**
* Memory leak과 double free를 방지
* std::move를 이용해 소유권 이전은 가능
  * 이동 전의 dangling pointer를 다시 사용하지 않는다는 확신하에 사용

```c++
// unique_ptr 을 사용한 포인터 할당
std::unique_ptr<A> pa(new A);

// 위 구문은 아래와 동일
A* pa = new A();

// 아래의 구문은 컴파일 에러를 발생
// unique_ptr는 복사 생성자를 명시적으로 삭제
// unique_ptr는 어떤 객체를 유일하게 소유하고 있어야 하기 때문
// -> 삭제된 함수를 사용하려는 시도
std::unique_ptr<A> pb = pa;

// 소유권 이전은 가능
// pa의 주솟값은 0 (NULL)로 변환
std::unique_ptr<A> pc = std::move(pa);
```

* 함수 인자로 전달할 때는 주솟값을 그대로 전달
* 함수 인자 타입을 unique_prt<A>&로 전달하는 방법?

```c++
// 올바르지 않은 전달 방식:
// pa로서 선언된 유일한 소유권의 의미가
// 함수 인자 ptr을 통해서도 행사가 가능해짐으로써
// 단순한 Wrapper로 전락함
void do_something(std::unique_ptr<A>& ptr) 
{ 
  ptr->do_sth(3); 
}

// 올바른 전달 방식:
// 주솟값을 전달
void do_something(A* ptr) 
{ 
  ptr->do_sth(3); 
}

int main() {
  std::unique_ptr<A> pa(new A());
  
  // 올바르지 않은 전달 방식:
  do_something(pa);

  // 올바른 전달 방식:
  // get 함수는 실제 객체의 주소값을 전달
  // 소유권이라는 의미를 떠나, 
  // do_something 함수 내부에서 객체에 접근할 수 있는 권한을 획득
  do_something(pa.get());
}
```

## C++14부터 make_unique 함수 지원

```c++
class Foo {
  int a, b;

 public:
  Foo(int a, int b) : a(a), b(b) { std::cout << "생성자 호출!" << std::endl; }
  void print() { std::cout << "a : " << a << ", b : " << b << std::endl; }
  ~Foo() { std::cout << "소멸자 호출!" << std::endl; }
};

int main() {
  
  // 이 구문은 아래의 구문과 동일
  std::unique_ptr<Foo> ptr(new Foo(3, 5));

  // 이 구문은 위 구문과 동일
  auto ptr = std::make_unique<Foo>(3, 5);

  ptr->print();
}
```

## unique_ptr의 컨테이너

```c++
int main() {
  std::vector<std::unique_ptr<A>> vec;
  std::unique_ptr<A> pa(new A());

  // case 1
  // 컴파일 오류:
  // 삭제된 복사 생성자에 접근하기 때문
  vec.push_back(pa); 

  // case 2
  // 정상적인 컴파일:
  // push_back이 우측값 레퍼런스를 받는 버전으로 오버로딩
  vec.push_back(std::move(pa)); 

  // case 3
  // 정상적인 컴파일:
  // vec.push_back(std::unique_ptr<A>(new A())); 과 동일
  // perfect forwarding
  // 불필요한 이동 연산 없음
  vec.emplace_back(new A());
}
```

## 출처
* <https://modoocode.com/229>
* <https://ko.wikipedia.org/wiki/%EB%A9%94%EB%AA%A8%EB%A6%AC_%EB%88%84%EC%88%98>
* <https://banaba.tistory.com/42>