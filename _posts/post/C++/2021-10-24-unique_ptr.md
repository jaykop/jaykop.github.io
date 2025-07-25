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

### raw pointer over than smart pointer
* 소유권 개념이 없는 모든 경우
* legacy 코드를 고려해야 하는 경우

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
// unique_ptr& 인자로 받으면서 
// 유일한 소유권의 의미가 함수 인자 ptr을 통해서도 행사가 가능해짐
// => 단순한 Wrapper
void do_something(std::unique_ptr<A>& ptr) 
{ 
  ptr->do_sth(3); 
}

// 올바른 전달 방식:
// 실제 객체의 주솟값을 전달
// 함수 내부에서 객체의 주소를 통해 직접 접근할 수 있는 권한 획득
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
* 위와 같은 경우는 컨테이너의 인덱싱을 통한 접근으로만 사용할 목적이어야 한다
* unique_ptr을 사용한 객체에 대한 소유권은 단 하나이기 때문에, 컨테이너에 넣기 전 외부에서 생성한 pa로는 더 이상 접근할 수 없다
* 만약 컨테이너 인덱싱으로도, 외부에서 생성한 객체로도 모두 주소값에 접근하고 싶다면 unique_ptr을 사용하면 안된다
  
## uniqure_ptr 을 리턴하는 함수
* uniqure_ptr은 복사 혹은 대입이 불가능
  
```c++
std::unique_ptr<int> func()
{
  std::unique_ptr<int> ptr(new int [10]);
  return ptr;  
}
```
* 그러나 위와 같은 함수를 만들 수 있다
* **함수가 반환하는 값은 rvalue이기 때문**
  * move contructor 호출
* 따라서 위의 함수는 실제로 아래 함수처럼 작동한다
  
```c++
std::unique_ptr<int> func()
{
  std::unique_ptr<int> ptr(new int [10]);
  return std::move(ptr);  // 이동생성자 unique_ptr(unique_ptr&&) 호출
}
```
  
* 그러나 위의 방법은 실제 반환하는 값의 타입과 함수의 리턴 타입이 다른 경우에 사용하는 걸 권장한다
* move를 사용하지 않으면 컴파일러가 move contructor를 호출하지 않고 RVO 최적화를 실행할 수 있다.

```c++
std::unique_ptr<Base> func()
{
  std::unique_ptr<Derived> ptr(new int [10]);
  return std::move(ptr);  
}
```
  
## 멤버 변수로서의 unique_ptr

```c++
class A {
private:
   std::unique_ptr<MyType> mt;
public:
   void initStuff() {
      mt = StaticFuncSomewhereElese::generateMyType();
   } 
};

std::unique_ptr<MyType> StaticFuncSomewhereElese::generateMyType() {
    auto temp = std::make_unique<MyType>(…);
    // `make_unique` is C++14 (although trivially implementable in C++11).
    // Here's an alternative without `make_unique`:
    // std::unique_ptr<MyType> temp(new MyType(…));

    //do stuff to temp (read file or something...)
    return temp;
}
```
  
* 멤버 변수 unique_ptr은 최대한 빠르게 할당해주는 것이 좋다

```c++
class Square
{
public:
    ...

    // 소유권을 가져오지 않기 위해 raw pointer로 반환
    const Piece* getPiece() const;

    std::unique_ptr<Piece> setPiece(std::unique_ptr<Piece> piece);

    ...

protected:
    std::unique_ptr<Piece> piece;
    ...
};
  
const Piece* Square::getPiece() const
{
    return piece.get();
}

std::unique_ptr<Piece> Square::setPiece(std::unique_ptr<Piece> piece)
{
    // 기존에 가지고 있던 포인터를 old에 할당
    std::unique_ptr<Piece> old = std::move(this->piece);
  
    // 받은 인자를 move를 통해 멤버 변수로 이동
    this->piece = std::move(piece);
  
    // 사용하던 포인터를 반환 (삭제 혹은 사용하지 않도록 하기 위함)
    return std::move(old);
}
```
  
## 출처
* <https://modoocode.com/229>
* <https://ko.wikipedia.org/wiki/%EB%A9%94%EB%AA%A8%EB%A6%AC_%EB%88%84%EC%88%98>
* <https://banaba.tistory.com/42>
* <https://2pound2pound.tistory.com/82>
* <https://stackoverflow.com/questions/9827183/why-am-i-allowed-to-copy-unique-ptr?noredirect=1&lq=1>
* <https://stackoverflow.com/questions/42595473/correct-usage-of-unique-ptr-in-class-member>
* <https://stackoverflow.com/questions/54543496/how-to-pass-a-unique-ptr-to-set-the-member-variable-of-my-object>
* <https://stackoverflow.com/questions/6675651/when-should-i-use-raw-pointers-over-smart-pointers/6676183#6676183>
* <https://stackoverflow.com/questions/8706192/which-kind-of-pointer-do-i-use-when>
