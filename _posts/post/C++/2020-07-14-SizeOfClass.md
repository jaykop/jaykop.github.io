---
title: "Class의 사이즈"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## Class의 사이즈

```c++
// 1 byte
// 이 객체의 크기가 1 byte인 이유는 
// 이 클래스가 여러 객체로 선언되었을 때, 
// 그 객체들 간의 주소값이 구분되도록 하기 위함
class A{}; 

// 1 byte
class A{
	char a;
} 

// 4+4+4 = 12 bytes: a000 bbbb c000
// 0 = padding
class A{
	char a; // 1
  int b; // 4
  char c; // 1
}; 

// / 4+2+2 = 8 bytes: bbbb ac00
class A
{
  int b; // 4
  char a; // 1
  char c; // 1

  // stored in Data segment, 
  //not included in the class size
  static int d; 
} 

// 1 bytes
// Methods don’t affect the size of the class
class A
{
	void function(); 
} 

// size of class A: 8(64bit) bytes: 
// size of class B: 8(64bit) bytes: 
// size of class C: 8+8 = 16(64bit) bytes: 
// size of pointers(to vtable)
class A
{
public:
    virtual void foo()
    {
        cout << "class A foo\n";
    }

    virtual void bar()
    {
        cout << "class A bar\n";
    }
};

class B
{
public:
    virtual void foo()
    {
        cout << "class B foo\n";
    }

    virtual void bar()
    {
        cout << "class B bar\n";
    }
};

class C : public A, public B
{
    void foo() override
    {
        cout << "class C foo\n";
    }

    void bar() override
    {
        cout << "class C bar\n";
    }
};

// what if this?
// size of class C: 8+8+8 = 24(64bit) bytes: 
class C : virtual public A, virtual public B
{
    void foo() override
    {
        cout << "class C foo\n";
    }

    void bar() override
    {
        cout << "class C bar\n";
    }
};

// 8+8 = 16 bytes: 
// size of pointers(to vtable)
class B: public A
{
	void function1();
	void function2();
} 
```

## 출처:
* <https://www.geeksforgeeks.org/why-is-the-size-of-an-empty-class-not-zero-in-c/>