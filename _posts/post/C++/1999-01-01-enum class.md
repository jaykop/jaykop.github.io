---
title: "enum과 enum class"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## enum과 enum class의 차이
* 값 중복 에러 여부

```c++
// enum
// Error 발생
enum shaderType {model, text, partyicle, light, end}
enum someType {model, text, partyicle, light, end} 

// enum class
// Error 없음
enum class people {none, white, black, yellow}
enum class color {none, white, red, black, yellow}

// enum class는 값 호출 시 class::까지 표기
enum class people {none, white, black, yellow}
enum class color {none, white, red, black, yellow}
people p = white; // 에러 
people p = people::white; // 가능
```

* implicit 정수 치환 가능 여부

```c++
// enum
// implicit conversion to int
// 루프 가능 (enum class는 불가능)
for (int i = 0; i < shaderType ::end; ++i) 
{ 
  // ...
}
```

* 기타

```c++
// enum의 값 범위를 아래와 같이 정의 가능
enum COLOR : int {WHITE, RED, BLUE, BLACK, YELLOW, END};
enum PEOPLE : unsigned int {WHITE, BLACK, YELLOW, END};

// enum 값 범위를 bool로 두었을 때
// 0, 1, 1, 1, 1, …..
enum A : bool { ONE , TWO  , THREE,  FOUR, ... };
A a = THREE; // 1

// enum 값 할당 
enum A : char { ONE = 4, TWO = 3, THREE };
A a = THREE; // 4
```