---
title: "Class의 사이즈"
classes: wide
categories: 
  - blog
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## Class의 사이즈

```c++
// 1 byte
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

// 8+8 = 16(64bit) bytes: 
// size of pointers(to vtable)
class A
{
	virtual void function1();
	virtual void function2();
} 

// 8+8 = 16 bytes: 
// size of pointers(to vtable)
class B: public A
{
	void function1();
	void function2();
} 
```