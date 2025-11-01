---
title: "[C++] string_view"
classes: wide
categories: 
  - post
  - CPP
sidebar:
  nav: "main"
author_profile: true
---

## string_view
* C++17부터 추가된 타입
* 문자열의 길이와 문자열에 대한 포인터만 가지고 있다
  * string 보다 훬씬 가볍다
* null 종료 문자를 가지지 않는다

> [!NOTE]
> string_view가 문자열을 소유하고 있지 않기 때문에, 읽을 문자열이 소멸된 상태인지 아닌지 주의해야한다

### 위험한 참조 케이스

```c++
// 힙 메모리의 동적 할당 문자열
std::string* ptr = new std::string("world");
std::string_view sv = *ptr;              // 힙의 string을 참조
delete ptr;                              // ptr 삭제 후 sv는 dangling

// 5. ???
std::string_view get_view() {
    std::string local = "temporary";
    return local;                        // 위험! local이 곳 소멸됨
}
```

* 이 중 지역 변수를 참조하거나 임시 객체 참조, 해제된 동적 할당된 메모리 접근 등의 경우가 위험하다 할 수 있다

### substr
* string_view의 연산은 원본 문자열을 수정하지 않는다
  * substr 같은 경우는 포인터의 이동 및 길이의 재조정 이후 새로운 string_view를 생성하는 것이 전부이다

## 문자열 메모리 위치

```c++
std::string str = "hello world";
```

1. "hello world" 리터럴은 데이터 세그먼트에 존재
2. string 생성자가 호출됨
3. 문자열이 SSO 한계를 초과하면:
    * 힙에 새 메모리 할당 (new char[12] 같은 동작)
    * 데이터 세그먼트의 리터럴을 힙으로 복사
4. str.data()는 이제 힙의 주소를 가리킴

### Short String Optimization
* std::string은 보통 리터럴 문자열을 복사해 힙에 저장한다
* 일정 길이 이하의 작은 배열의 경우에는 오버헤드를 줄이기 위해 작은 배열을 만들어 스택에 저장한다

## 출처
* <https://modoocode.com/292>
* <https://m.blog.naver.com/dorergiverny/223032930096>
* <https://del4u.tistory.com/135>