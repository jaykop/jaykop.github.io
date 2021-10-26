---
title: "exception"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---
  
## 예외란?
* 정상적인 상황에서 벗어난 모든 예외적인 상황들

```c++
// 인덱스 범위를 벗어난 배열으로의 접근
std::vector<int> v(3);  // 크기가 3 인 벡터 만듦
std::cout << v.at(4);   // ??

// 시스템에서 감당할 수 없는 과도한 메모리의 할당
std::vector<int> v(1000000000); // ??
```

## 기존 예외 처리 방식
* C 언어 차원에서 제공하는 예외 처리 방식 없음
* 결과 값을 확인하는 방식
* 이는 결과값을 일일이 확인해야하는 번거로움을 야기

```c++

bool func1(int *addr) {
  if (func2(addr)) {
    // Do something
  }
  return false;
}

bool func2(int *addr) {
  if (func3(addr)) {
    // Do something
  }
  return false;
}

bool func3(int *addr) {
    // if array is not null, then you have an array with 1,000,000 ints.
    char *c = (char *)malloc(1000000000);

    // c가 정상적으로 할당됐으면 true
    return c != NULL;
  }

// 각 func1과 func2 에서 별도의 메모리 프로세스 과정을 거친다면,
// 함수별로 다시 결과 값이 정상적인지 확인하는 코드를 추가해야 함
int main() {
  int *addr;
  if (func1(addr)) {
    // 잘 처리됨
  } else {
    // 오류 발생
  }
}
```

## throw

```c++
template <typename T>
class Vector {

  // 사이즈를 할당하는 생성자
  Vector (size_t size) : size_(size){
    data_ = new T[size_];
    for (int i =0 ;i < size_; ++i)
    {
      data_[i] = 3;
    }
  }

  // 해당 인덱스의 값을 반환하는 함수
  const T& at(size_t index) const {
    if (index >= size_) {

      // 예외를 발생시킨다!
      throw out_of_range("vector 의 index 가 범위를 초과하였습니다.");
    }
    return data_[index];
  }

  // 소멸자
  ~Vector() { delete[] data_; }
}
```

* **C++ 에는 예외를 던지고 싶다면, throw 로 예외로 전달하고 싶은 객체를 써주면 된다**
  * 기본적으로 예외로 아무 객체나 던져도 상관없다
  * C++가 기본적으로 제공하는 여러 종류의 객체가 있으니 이를 활용하는 것이 좋다
* **throw 위치에서 모든 함수가 종료된다**
  * 예외를 처리하는 부분으로 점프하여 실행한다
  * stack에 쌓인 메모리는 모두 해제된다
    * stack unwinding
  
## try & catch

```c++
template <typename T>
class Vector {

  // 위 클래스와 동일...

  const T& at(size_t index) const {
    if (index >= size_) {
      throw std::out_of_range("vector 의 index 가 범위를 초과하였습니다.");
    }
    return data_[index];
  }

  // 위 클래스와 동일...
}

int main() {
  Vector<int> vec(3);

  // 기존 data 초기화
  int index, data = 0;
  std::cin >> index;

  try {
    data = vec.at(index);
  } catch (std::out_of_range& e) {
    std::cout << "예외 발생 ! " << e.what() << std::endl;
  }

  // 예외가 발생하지 않았다면 3이 출력되고, 
  // 예외가 발생하였다면 원래 data 에 들어가 있던 0이 출력된다.
  std::cout << "읽은 데이터 : " << data << std::endl;
}
```

* **try** 안에서 예외가 발생할만한 코드가 실행
* 예외가 발생하지 않으면, try 안의 코드만 실행하고 catch의 부분은 무시됨
* 예외가 발생하면 stack의 모든 객체 소멸자들을 호출하고, **가장 가까운 catch 구문으로 이동**

```c++
// 이 구문에서 예외 발생
// out_of_range를 throw
if (index >= size_) {
  throw std::out_of_range("vector 의 index 가 범위를 초과하였습니다.");
}

// ...

// 이 구문으로 이동
// catch가 out_of_range를 받음
catch (std::out_of_range& e) {
  std::cout << "예외 발생 ! " << e.what() << std::endl;
}
```

## Stack Unwinding
* catch 로 점프 하면서 스택 상에서 정의된 객체들을 소멸시키는 과정

```c++
#include <iostream>
#include <stdexcept>

class Resource {
 public:
  Resource(int id) : id_(id) {}
  ~Resource() { std::cout << "리소스 해제 : " << id_ << std::endl; }

 private:
  int id_;
};

int func3() {
  Resource r(3);
  throw std::runtime_error("Exception from 3!\n");
}
int func2() {
  Resource r(2);
  func3();
  std::cout << "실행!" << std::endl;
  return 0;
}
int func1() {
  Resource r(1);
  func2();
  std::cout << "실행!" << std::endl;
  return 0;
}

// 예외 발생 시 가장 가까운 catch 구문인
// main으로 이동
int main() {
  try {
    func1();
  } catch (std::exception& e) {
    std::cout << "Exception : " << e.what();
  }
}

// 예외 발생 결과 
// 리소스 해제 : 3
// 리소스 해제 : 2
// 리소스 해제 : 1
// Exception : Exception from 3!

// throw std::runtime_error("Exception from 3!\n")
// 없었다면 (예외 처리 없었다면)
// 리소스 해제 : 3
// 실행!          (func2)
// 리소스 해제 : 2
// 실행!          (func1)
// 리소스 해제 : 1
```

## 여러 종류의 예외
* catch는 여러 종류의 예외를 받아들일 수 있다

```c++
#include <iostream>
#include <string>

int func(int c) {
  if (c == 1) {
    throw 10;
  } else if (c == 2) {
    throw std::string("hi!");
  } else if (c == 3) {
    throw 'a';
  } else if (c == 4) {
    throw "hello!";
  }
  return 0;
}

int main() {
  
  // 인풋에 따라 다른 예외 처리
  int c;
  std::cin >> c;

  try {
    func(c);
  } catch (char x) {
    std::cout << "Char : " << x << std::endl; // Char : a
  } catch (int x) {
    std::cout << "Int : " << x << std::endl;  // Int : 10
  } catch (std::string& s) {
    std::cout << "String : " << s << std::endl; // String : hi!
  } catch (const char* s) {
    std::cout << "String Literal : " << s << std::endl; // String Literal : hello!
  }
}
```

```c++
// 부모 클래스와 파생 클래스의 예외처리
#include <exception>
#include <iostream>

class Parent : public std::exception {
 public:
   virtual const char* what() const noexcept override { return "Parent!\n"; }
};

class Child : public Parent {
 public:
 // 부모 클래스의 what overriding
  const char* what() const noexcept override { return "Child!\n"; }
};

int func(int c) {
  if (c == 1) {
    throw Parent();
  } else if (c == 2) {
    throw Child();
  }
  return 0;
}

int main() {
  int c;
  std::cin >> c;

  try {
    func(c);
  } catch (Parent& p) {
    std::cout << "Parent Catch!" << std::endl;
    std::cout << p.what();
  } catch (Child& c) {
    std::cout << "Child Catch!" << std::endl;
    std::cout << c.what();
  }
}

// 결과
// Parent Catch!
// Parent!
// Parent Catch!
// Child!
```

* catch문이 여러 개일 경우, 가장 먼저 대입할 수 있는 객체를 받는다
  * 첫 번째 구문인 catch (Parent& p)의 인자에 Child()를 대입할 수 있다
  * 이 같은 경우를 방지하고자, **파생 클래스를 받는 catch 구문을 먼저 쓰는 것이 좋다**

```c++
// ...

try {
  func(c);
} catch (Child& c) { // 파생 클래스의 예외 처리를 먼저 받음
  std::cout << "Child Catch!" << std::endl;
  std::cout << c.what();
} catch (Parent& p) { // 부모 클래스의 예외 처리를 나중에 받음
  std::cout << "Parent Catch!" << std::endl;
  std::cout << p.what();
}

// ...
```

## 기타 예외를 처리하는 방법

```c++
// func에서는 runtime_error를 throw 하지만,
// 가장 가까운 catch 에서는 이를 받아주는 구문이 없다.
// 이 코드는 예외를 발생시키며 비정상적으로 종료된다.
#include <iostream>
#include <stdexcept>

int func() { throw std::runtime_error("error"); }

int main() {
  try {
    func();
  } catch (int i) {
    std::cout << "Catch int : " << i;
  }
}

// 이를 지원하는 catch 구문 처리는 아래와 같다
try {
  func(c);
} catch (int e) {
  std::cout << "Catch int : " << e << std::endl;
} catch (...) { // try에서 발생한 모든 예외를 방을 수 있다
  std::cout << "Default Catch!" << std::endl;
}
```

## noexcept - 예외를 발생시키지 않는 함수
* 함수가 예외를 발생시키지 않는다는 것을 명시적으로 표현하는 키워드
* 하지만 이는 함수 안에서 throw 구문이 없음을 보장하지 않는다
* noexcept 처리된 함수가 예외를 발생시키면 프로그램은 비정상적으로 종료된다
  * 예외 처리 역시 정상적으로 이뤄지지 않는다
* noexcept는 프로그래머가 컴파일러에게 주는 힌트에 지나지 않는다
  * 함수가 throw 하지 않을 거라는 신뢰를 컴파일러에게 주는 것
  * 컴파일러는 이로써 최적화를 진행할 수 있다
* **C++11부터 소멸자들은 기본적으로 noexcept이다**
  * 절대로 소멸자에서 예외를 던지면 안된다

```c++
int foo() noexcept {}
int bar(int x) noexcept { throw 1; }

// case 1
// 이 코드는 경고와 함께 정상적으로 컴파일된다
int main() { foo(); }

// case 2
// 이 코드는 실행 중 비정상적으로 종료된다
int main() {
  foo();
  try {
    bar();
  } catch (int x) {
    std::cout << "Error : " << x << std::endl;
  }
}
```

## 출처
* <https://modoocode.com/230>