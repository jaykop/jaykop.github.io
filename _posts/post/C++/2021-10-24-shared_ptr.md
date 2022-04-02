---
title: "스마트 포인터 - shared_ptr"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## shared_ptr
* 여러 개의 스마트 포인터가 하나의 객체를 같이 소유해야하는 상황
* 하나의 자원을 몇개의 포인터가 가리키는지 추적하는 포인터
* **control block**을 할당하여 복사를 허용
  * 각 shared_ptr 객체에 저장되는 것이 아니라 실제 객체를 가리키는 control block을 할당
  * 객체를 가리키는 모든 스마트 포인터들이 소멸되어야만 객체를 파괴
  * **reference count**가 0이 되면 자원을 해제

```c++
// ex 1)
std::shared_ptr<A> p1(new A());
std::shared_ptr<A> p2(p1);  // p2 역시 생성된 객체 A 를 가리킨다.

// reference count를 확인
std::cout << p1.use_count();  // 2
std::cout << p2.use_count();  // 2

// 반면에 unique_ptr 의 경우
std::unique_ptr<A> p1(new A());
std::unique_ptr<A> p2(p1);  // 컴파일 오류!

// ex 2)
// 결괴:
// 자원을 획득함!
// 첫 번째 소멸!
// 다음 원소 소멸!
// 마지막 원소 소멸!
// 소멸자 호출!
// 프로그램 종료!
int main() {
  std::vector<std::shared_ptr<A>> vec;

  vec.push_back(std::shared_ptr<A>(new A()));
  vec.push_back(std::shared_ptr<A>(vec[0]));
  vec.push_back(std::shared_ptr<A>(vec[1]));

  // 벡터의 첫번째 원소를 소멸 시킨다.
  std::cout << "첫 번째 소멸!" << std::endl;
  vec.erase(vec.begin());

  // 그 다음 원소를 소멸 시킨다.
  std::cout << "다음 원소 소멸!" << std::endl;
  vec.erase(vec.begin());

  // 마지막 원소 소멸
  std::cout << "마지막 원소 소멸!" << std::endl;
  vec.erase(vec.begin());

  std::cout << "프로그램 종료!" << std::endl;
}
```

## make_shared 

```c++
// 이 방법은 비효율적인 방법이다
// 1. new A를 동적 할당
// 2. 이에 해당하는 control block를 또 할당해야 한다
// 즉, 동적 할당이 2번이나 일어난다
std::shared_ptr<A> p1(new A());

// 아래 방법이 더 효율적이다
// 객체 A와 control block이 할당될 메모리를 한번에 동적 할당받는다
std::shared_ptr<A> p1 = std::make_shared<A>();
```

## shared_ptr 생성 시 주의할 점
* shared_ptr 를 주소값을 통해서 생성하는 것을 **지양**

```c++
int main() {
  A* a = new A();

  // 아래와 같이 할당하는 경우, 
  // control block이 각 pa1과 pa2에 하나 씩
  // 총 2개가 생성된다
  std::shared_ptr<A> pa1(a);
  std::shared_ptr<A> pa2(a);

  std::cout << pa1.use_count() << std::endl; // 1
  std::cout << pa2.use_count() << std::endl; // 1

  // 메모리가 해제될 때 소멸자를 2번 호출함으로써
  // 에러가 발생한다
}
```

* shared_ptr을 주소값을 통해서 생성해야하는 경우
  * 반드시 해당 객체의 shared_ptr를 먼저 정의
  * 객체를 enable_shared_from_this로부터 상속
  * **shared_from_this**는 control block을 확인할 뿐, 생성하지 않음

```c++
class A : public std::enable_shared_from_this<A> {
  int *data;

 public:
  // ...

  std::shared_ptr<A> get_shared_ptr() { return shared_from_this(); }
};

int main() {
  
  // 올바르지 않은 구문:
  // 해당 객체의 shared_ptr가 정의되어 있지 않음
  A* a = new A();
  std::shared_ptr<A> pa1 = a->get_shared_ptr();
  
  // 올바른 구문:
  // 해당 객체의 shared_ptr가 pa1으로 정의되어 있음
  std::shared_ptr<A> pa1 = std::make_shared<A>();
  std::shared_ptr<A> pa2 = pa1->get_shared_ptr();
}
```

## 출처  
* <https://modoocode.com/252>