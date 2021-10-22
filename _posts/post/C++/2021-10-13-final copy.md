---
title: "final 키워드"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

# final

```c++
class A final
{
  public:
    A();
    virtual ~A();
    virtual void Func(String InParam);
};

// Error!!
class B : public A
{
  public:
    B();
    virtual ~B();
    void Func(String InParam) override;
}

class C
{
	C();

  // Error!!!
   void Func(String InParam) final; 
};

class D : public C
{
	D();

  // Error!!!
  virtual void Func(String InParam) override; 
};

// - A는 final로 선언되었기 때문에 상속 불가
// - B의 Func 멤버 함수는 final로 선언되었기 때문에 C에서  overriding이 불가능
```
* 더 이상의 상속을 차단하는 키워드
  * 클래스, 메서드에 사용 가능
* C#의 sealed와 유사

## 출처   
* <https://award09130.tistory.com/9>
* <https://docs.microsoft.com/ko-kr/cpp/cpp/final-specifier?view=msvc-160>