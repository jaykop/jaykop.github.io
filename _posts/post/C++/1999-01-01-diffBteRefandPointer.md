---
title: "Reference와 Pointer의 차이"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## 초기화 (Initialization)
- **Reference**
```c++
// Must initialize the reference at the first
int& ra; // Wrong
int& ra = a; // Correct

// Pointer can do this
int *a; 
```

## Reference는 한 번 초기화 이후 다른 변수를 가리킬 수 없음
```c++	
int a = 10;   
int &ra = a;  // ra가 a를 참조
int b = 3;    
ra = b;       // ra에 b의 값을 대입 (재지정 X)
b = 10; // a == ra == 3, b == 10

int *pa = &a; // pa는 최초로 a를 지정
pa = &b;      // b로 재지정 가능
```

## Reference는 메모리에 존재할 수도, 하지 않을 수도 있음
```c++
// 이미 존재하는 변수의 다른 이름
int a = 10;
int &ra = a; // Not exist in memory space

// 클래스 안에서 메모리를 차지
class A
{
public:
	int a;
	int& b = a;
}; // sizeof(A) = 4+4 = 8; // Takes memory

// 스택 프레임에서 매개변수로 메모리를 차지
void func(int &a, int &b); // Arguments are stored in stack frame memory 
```

## 레퍼런스의 배열(Array of references)? 
* **아래 식들은 모두 불가능 illegal**
	- &&a: references to references
	- & a[]: arrays of references
	- &*a: pointers to references

  ```c++  
  // 임읭의 두 변수가 선언되어(연속된 메모리에 배치되어 있지 않은)
  // 이 변수를 레퍼런스의 배열로 선언하는 것은 불가능
  int a, b; // Random location in stack
  int& arr[2] = {a , b}; // Illegal: Impossible to reference the non-adjacent variables

  // 연속된 메모리에 선언된 변수들을
  // 배열로서 레퍼선스로 선언하는 것은 가능
  int arr[3] = {1, 2, 3}; // adjacent memory locations
  int (&ref)[3] = arr; // Legal: Variables are adjacent
  ```

## 출처
* <https://modoocode.com/141>