---
title: "const & volatile 키워드"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## Read-Only
* 변수의 값을 변경할 수 없다
* 메서드에서 클래스의 멤버 변수를 변경할 수 없다

## const 표현식
```c++
// 1) read-only integer
const int a; 
int const a; 

// 2) pointer to const integer
int main() {
  int a;
  int b;

  // 꼭 const int를 가리킬 필요는 없다
  // a의 값이 변하지 않으면 될 뿐
  // const int* 의 의미는 const int 형 변수를 가리킨다는 것이 아니다
  // 값을 절대로 바꾸지 말라는 뜻이다
  // 하지만 a는 변수이기 때문에, a = 3 등과 같이 값을 바꿔도 상관없다
  const int* pa = &a;

  // 올바르지 않은 문장
  // *pa는 const int 이기 때문
  *pa = 3;  

  // 올바른 문장
  pa = &b;  
  return 0;
}

// 3) const pointer to integer
int main() {
  int a;
  int b;

  // pa 의 값(주소값)이 바뀐 안된다
  int* const pa = &a;

  // 올바른 문장
  // 변수의 값을 바꾸려는 시도
  *pa = 3;  

  // 올바르지 않은 문장
  // 주소값을 바꾸려는 시도
  pa = &b;  

  return 0;
}

// 4) const pointer to const integer
int main() {
  int a;
  int b;

  // 값도 못 바꾸고, 주소값도 못 바꿈
  const int* const pa = &a;

  *pa = 3;  // 올바르지 않은 문장
  pa = &b;  // 올바르지 않은 문장

  return 0;
}
```

## volatile
* 컴파일러가 자동으로 최적화하는 것을 방지
* interruption 핸들링 또는 멀티스레딩에서 공유되는 변수에 사용

## volatile const
* 컴파일러 최적화 불가능
* 프로그래머의 쓰기/변경 불가능
* ex)
  * 하드웨어마다 레지스터 주소값이 다른데 컴파일러의 임의 변환을 막기 위해 volatile
  * 또한 하드웨어 주소값은 사용자가 지멋대로 바꾸면 안됨, 그래서 const

## 출처
* <https://geekhub.tistory.com/68>
