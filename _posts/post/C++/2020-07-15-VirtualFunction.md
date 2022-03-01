---
title: "Virtual Function"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## 함수의 작동

### Stack segment(Call stack)
  - 현재 실행 중인 서브루틴의 실행이 끝났을 때, 제어를 반환할 지점을 보관

### Stack Frame
- 스택에 할당/해제되는 데이터 덩어리
* 모든 활성함수를 추적, 함수 매개변수와 지역변수의 할당 처리
* CPU Stack Pointer - 최상위 스택 프레임 pointing
	1. 프로그램에 함수 호출
	2. 스택 프레임이 생성되고 콜 스택에 푸시
    * **스택 프레임**
      * 함수가 종료되면 복귀할 주소
			* 함수의 모든 매개 변수
			* 지역 변수
			* 함수가 반환할 때 복원해야 하는 수정된 레지스터의 복사본
	3. CPU가 함수의 시작점으로 점프한다.
	4. 함수 내부의 명령어를 실행한다.
* 함수가 종료 이후
	- 레지스터가 콜 스택에서 복원
	- 스택 프레임이 콜 스택에서 해제
    - 모든 지역 변수와 매개 변수에 대한 메모리 해제
	- 반환 값이 처리
	- CPU는 반환 주소에서 실행을 재개

## 가상 함수의 작동

### 일반 함수
  * 정적 바인딩(Static binding)
  * 컴파일러가 함수의 주소를 알고 있음

### 가상 함수(Virtual Functions)
  * 동적 바인딩(Dynamic binding)
  * 각 객체 별이 아닌, 클래스마다 vtable을 가지고 있음
    * 각 객체는 vtable의 주소값을 가리키는 포인터를 저장
  * 객체가 가진 vtable에 대한 포인터를 통해 프로그램이 가상 함수를 호출할 때 vtable로 엑세스하여 적절한 함수를 호출

### 순수 가상 함수(Pure virtual function)
  * 순수 가상 함수를 가진 클래스는 객체 생성 불가능
  * 파생 클래스는 베이스 클래스에서 선언된 순수 가상 함수를 반드시 구현해야 함
    * 하위 클래스에서의 method 정의를 강제함으로서 interface를 제공하는 방법
    * **절대 사용되지 않을 dummy method를 정의할 필요 없음**
    * **절대 사용되지 않을 dummy class의 생성을 방지**
    * **재정의된 하위 클래스에서의 메서드들을 필수적으로 override**

  ```c++
  // 베이스 클래스
  class A {
    public:
      // 베이스 클래스의 순수 가상 함수
    	virtual void function(void) = 0; 
  };

  // 파생 클래스
  class B: public A {
    public:
      // 아래와 같은 형식으로 필히 구현되어야 함
      void function(void) override {  };
      virtual void function(void) {  };
  };

  // 베이스 클래스의 객체 생성은 불가
  A a; 
  ```

## Virtual Table이란?
* 클래스 안에 가상함수가 포함되어 있을 시, 객체를 생성할 때 가상함수를 가리키는 포인터가 생성
* 이 포인터는 가상테이블의 시작주소를 가리키는 포인터이고, 각 클래스마다 하나의 고유 가상테이블이 생성
* 고유의 가상테이블은 가상함수를 가리키는 함수 포인터 배열로 되어있다.
  * 가상 함수를 실행하려면 vptr-> vtable -> func() 를 호출하게 되는 것
* VTable은 컴파일 타임에 생성된다
  * 컴파일 타임에 정의가 가능하기 때문
  * 특정 타입의 객체가 런타임에 생성된다면, vptr는 생성되면서 정적 vtable을 가리키고 있다

## Derived Class를 위해 Base Destructor에 virtual을 붙이는 이유
```c++
Base *b =  new Derived;
delete b;
```

* 이 같은 경우에 virtual 키워드를 붙이지 않으면 derived class의 destructor가 override 되지 않움

```c++
// 베이스 클래스의 destructor에 virtual 키워드 없는 경우
class Base
{
  Base();
  ~Base();
}

class Derived : public Base
{
  Derived();
  ~Derived();  
}

// 호출 순서
Base constructor
Derived constructor
Base destructor
```

* 오버로딩 하도록 base 소멸자에 virtual 키워드를 붙이면 정상작동

```c++
// 베이스 클래스의 destructor에 virtual 키워드 있는 경우
class Base
{
  Base();
  virtual ~Base();
}

class Derived : public Base
{
  Derived();
  ~Derived();  
}

// 호출 순서
Base constructor
Derived constructor
Derived destructor
Base destructor
```

## 출처
* <https://boycoding.tistory.com/235>
* <https://stackoverflow.com/questions/3849498/when-is-vtable-in-c-created>
* <https://stackoverflow.com/questions/39898126/why-we-need-interface-or-pure-virtual-function-in-c>