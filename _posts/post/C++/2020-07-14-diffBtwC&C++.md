---
title: "C와 C++ 차이 몇 가지"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## C의 malloc과 C++ new의 차이
* **malloc**
  * malloc은 함수(function)
  * 할당할 메모리의 사이즈를 매개변수로 받음size as input
  * header file을 포함시켜야 함
  * 실 사용할 타입으로 casting 필요
      * 메모리 청크만 heap에서 받아 옴
  * 자동으로 constructor를 호출하지 않음

* **new**
  * new는 연산자(operator)
  * C++ 빌트인 키워드이기 때문에 별도로 헤더파일 필요 없음
  * 실 사용할 타입으로 바로 메모리 할당 받아올 수 있음
      * 자동으로 constructor를 호출

## class와 struct
* **class**
  * 기본적으로 다 프라이빗
  * class는 object 역할 (관습적인 차이)
* **struct**
  * 기본적으로 다 퍼블릭
  * struct는 데이터의 묶음 (관습적인 차이)
  * **C에서의 struct는….**
    * 안에 함수를 직접 만들 수 없음
      * function pointer를 할당하여 사용
    * 다형성,  상속성이 없음
    * constructor, destructor가 없음

```c++
// 클래스에서 스트럭트 파생 가능
class Base {
public:
    int x;
};
 
 // 이 경우
 // struct Derived : public Base {}
struct Derived : Base { }; 
 
int main()
{
  Derived d;
  d.x = 20; // 멤버 변수에 접근 가능
  getchar();
  return 0;
}
```

## 컴파일러에 의해 자동 생성되는 class 생성자 및 연산자 
* default constructor
* default destructor
* copy constructor

### copy constructor
* **사용자가 직접 copy constructor를 작성하지 않으면, 컴파일러는 shallow copy를 하는 copy constructor를 생성**
* **copy constructor의 인자는 항상 레퍼런스로 넘겨줘야 한다**
* 동일한 타입의 인자를 받는 생성자를 작성할 때, 인자를 &로 받지 않고 값으로 받으면 컴파일 에러 발생
* copy constructor는 오브젝트가 값으로서 인자를 받을 때 호출된다. 
* 따라서 레퍼런스가 아닌 값으로서 인자를 받게 된다면, 그 값을 복사하기 위해 또 copy constructor 호출하면서 무한반복한다

```c++
// ex 1)
class Point {
    int x;
public:
    Point(int x) { this->x = x; }
    Point(Point p) { x = p.x;}        // 에러 발생
    Point(const Point p) { x = p.x;}  // 에러 발생
    Point(Point& p) { x = p.x;}       // ok
    Point(const Point& p) { x = p.x;} // ok
    int getX() { return x; }
};
 
int main()
{
   Point p1(10);
   Point p2 = p1;
   cout << p2.getX();
   return 0;
}

// ex 2)
class Test
{
public:
    Test(Test& t) { }
    Test() { }
};

Test fun()
{
    cout << "fun() Calledn";
    Test t;
    return t;
}

int main()
{
    Test t1;

    // 1. fun()을 통해 반환된 임시 객체는 값으로서 전달된다 // 고유 주소가 없다
    // 2. 이 값을 copy constrcutro를 사용해 t2로 전달한다
    // 3. 이 임시 객체는 non-const references 인자로 받아들여질 수 없음
    // 4. 따라서 아래 코드는 컴파일 에러를 발생
    Test t2 = fun();
    return 0;
}

// 위의 코드를 작동하도록 바꾸는 방법은 2가지이다
// sol 1
// copy constructor 앞에 const 인자를 추가하는 것
// 임시 객체의 값을 변환할 수 없게 됨
Test(const Test &t) { cout << "Copy Constructor Called\n"; }

// sol 2
// copy constructor를 호출하지 않는 것
Test t2;
t2 = fun();
```

* assignment operator
* move constructor
  ```c++
  A (A&& rhs) { ... };
  ```
* move assignment operator
  ```c++
  A& operator=(A&& rhs) { ... };
  ```
* **사용자가 어떤 생성자를 작성해주면, 컴파일러는 default constructor를 생성하지 않음**

## 패러다임의 차이

### C
* 절차지향적
  * 순차적인 처리가 중요
  * 프로그램이 함수화
  * 함수의 유기적인 연결로 프로그램이 구성
* 하향식 접근
  * 순차적인 실행이 가능하도록 단계적 세분화 작업을 거침
  * 수행되는 함수들끼리의 연결을 중요시

### C++
* 객체지향적
  * 유사한 데이터나 함수를 클래스라는 하나의 그룹으로 묶음
  * 그룹의 객체에 의해서 프로그램이 구동되게 한다
* 상향식 접근
  * 추상 객체를 디자인하고 이들을 조합하는 방식
* **언어는 언어일 뿐 개발 방식 및 개발 패러다임은 개발자가 정하는 것**
  * C++가 객체지향적이라면 friend 같은 키워드는 만들지 않았을 것

## 객체지향 프로그래밍이란?

### 캡슐화
* 데이터와 메서드를 하나의 클래스라는 단위로 묶음
* 클래스 내부 정의에 대해 외부에서 볼 수 없음
* methods + data = object(class)

### 추상화/상속성
* base (추상,일반) -----------> derived (고유,구체)
* 객체의 공통적이고 일반적인 특징을 상위클래스에 디자인
* 파생된 하위클래스는 고유의 성질
* 기존의 클래스를 바탕으로 특징을 추가해 새로운 클래스를 만들 수 있음
* ex) 동물 -> **상위 클래스**
  * 개/호랑이/닭/…. -> **하위 클래스**

### 다형성
* virtual function description
* 같은 함수여도, 클래스에 따라 다르게 작동할 수 있음

```c++
class Vehicle {
  virtual void move_forward()
}
class Train: public Vehicle {
  virtual void move_forward();
}
class Bus: public Vehicle {
  virtual void move_forward();
}
class KTX: public Train {
  virtual void move_forward();
}
```

### C언어에서의 다형성 구현

```c++
#include <stdio.h>
#include <stdlib.h>

//  "C-style" virtual function
struct B 
{
  // p points to the first element of array of pointers
  // this array is the pointer to the virtual table
  int (**p)(void*);
};    

// virtual "methods" for B
int B_foo(struct B* p) { return 1; }
int B_bar(struct B* p) { return 2; } 
int (*b_a[2])(void*) = { (int (*)(void*))B_foo, (int (*)(void*))B_bar }; // global VMT
void makeB (struct B* this) { this->p = b_a; } // ctor

struct D  
{
  // p points to the first element of array of pointers
  // this array is the pointer to the virtual table
  int (**p)(void*);    
};    

// virtual "methods" for D
int D_foo(struct D* p) { return 3; }
int D_bar(struct D* p) { return 4; } 
int (*d_a[2])(void*) = { (int (*)(void*))D_foo, (int (*)(void*))D_bar };
void makeD (struct D* this) { this->p = d_a; } // ctor

int call( void* p_obj, int i ) {
    return ((struct B*)p_obj)->p[i]( p_obj );
    //            1     0      2 3    4

}

int main() {
    struct B* p = (struct B*)malloc( sizeof( struct B ) );
    makeB(p);
    printf("%i\n", call( p, 0 ) );
    free ( p );

    struct D* p2 = (struct D*)malloc( sizeof(  struct D ) );
    makeD(p2);
    printf("%i\n", call( p2, 1 ) );
    free ( p2 );
```

## 출처
* <https://geekhub.tistory.com/68>
* <https://www.geeksforgeeks.org/structure-vs-class-in-cpp/>
* <https://www.geeksforgeeks.org/copy-constructor-argument-const/>
* <https://www.geeksforgeeks.org/copy-constructor-in-cpp/>
* <https://stackoverflow.com/questions/2685854/why-should-the-copy-constructor-accept-its-parameter-by-reference-in-c>