---
title: "Multiple Inheritance"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## 다중 상속 Multiple Inheritance
* C++에서는 C#과 다르게, 다중 상속을 허용
* 기반 클래스의 멤버 또는 메서드의 이름이 동일한 경우 주의해야 한다

![post_thumbnail](/assets/images/다운로드1.png)

```c++
struct A 
{ 
  int a; 
}; 

struct B 
{ 
  int a; 
}; 

// 다중 상속 
struct C : public A, public B 
{ 
  int c; 
}; 

int main() 
{ 
  C c; 
  // c.a = 10; 2개의 기반클래스에서 같은 멤버 이름을 사용하고 있으므로 ambiguous error 
  c.A::a = 10; // 상속 받은 A 클래스의 a 멤버에 대입 
  c.B::a = 20; // 상속 받은 B 클래스의 a 멤버에 대입 
}
```

## 가상 상속 Virtual Inheritance
* 위의 예시에서 나타난 다이아몬드 다중 상속의 경우에 사용
* 이중 상속을 방지

```c++
// 다이아몬드 상속의 예시
struct X { 
  int x; 
}; 
struct A : public X // X의 멤버 x를 상속 
{ 
  int a; 
}; 
struct B : public X // X의 멤버 x를 상속 
{ 
  int b; 
}; 
struct C : public A, public B // 다중 상속 
{ 
  int c; 
}; 
int main() 
{ 
  C c; 
  c.x = 10; // 에러 X의 멤버인 x를 A, B 클래스가 상속받은 상태로 접근이 모호 
}

// 가상 상속 
// ...
struct A : public X // X의 멤버 x를 상속 
{ 
  int a; 
}; 
struct B : public X // X의 멤버 x를 상속 
{ 
  int b; 
}; 
// ...

int main() 
{ 
  C c; 
  c.x = 10; // A, B를 가상 상속으로 바꿔주면 한곳에서 상속만 보장 되므로 해결
}
```

## 가상 상속 처리 방식

![post_thumbnail](/assets/images/997279425AA73DCC0E.png)
* 가상 상속을 하지 않는 경우
* class D는 class A를 한번만 호출했지만, 2개의 class A가 불려온다
* ambiguous compile error가 발생

![post_thumbnail](/assets/images/99E87B465AA73F4004.png)
* class B와 class C가 가상으로 class A를 상속받는다
* 가상 상속은 2개의 class A를 1개로 처리하도록 한다

![post_thumbnail](/assets/images/9926DA3D5AA77FFA1A.png)
* 더 엄밀히 말하면, class D에서는 class A를 몇개나 상속받았는지 알 수 없다
* 이런 경우, class A를 한 개로 인식한다

## 출처  
* <https://www.devoops.kr/60>
* <https://jerryjerryjerry.tistory.com/12>