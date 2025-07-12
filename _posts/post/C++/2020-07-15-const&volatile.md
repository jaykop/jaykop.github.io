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

## constexpr
* 해당 객체나 함수의 리턴값을 컴파일 타임에 알 수 있음
  * 상수식을 만들 수 있음

```c++
// size가 정수 상수식이어야 함
constexpr int size = 3;
int arr[size];

// number가 정수 상수식이어야 함
constexpr int number = 3;
template <int N>
struct A {
  int operator()() { return N; }
};
A<number> a;

// number가 정수 상수식이어야 함
constexpr int number = 3;
enum A { a = number, b, c };
```

## const vs. constexpr
* constexpr는 항상 const
* const는 constexpr이 아님

```c++
// case 1 
int a;
// Do something...
const int b = a;

// case 2
// a가 상수식이어야 하는데, 컴파일 타임 시 무엇인지 알 수 없음
// 따라서 아래 구문은 컴파일 에러 발생
int a;
// Do something...
constexpr int b = a;

// case 3
// 아래 구문에서 i는 컴파일 타임에 초기화될 수도, 런타임에 초기화될 수도 있음
// 컴파일 타임에 확실히 사용하고 싶다면 constexpr를 사용해야 함
const int i = 3;
```

### const는 언제 runtime 상수인가?
```c++
// case 1
// 다른 변수로 초기화되는 const 변수
std::cout << "Enter your age: ";
int age;
std::cin >> age;
const int usersAge { age }; // usersAge can not be changed

// case 2
// 함수의 파라미터
void printInteger(const int myValue)
{
    std::cout << myValue;
}
```

## constexpr 함수
* 컴파일 타임 상수인 객체를 만드는 함수를 정의

```c++
int factorial(int N) {
  int total = 1;
  for (int i = 1; i <= N; i++) {
    total *= i;
  }
  return total;
}

template <int N>
struct A {
  int operator()() { return N; }
};

// 의도: A<factorial(5)> = A<120>
// 그러나 컴파일 에러 발생
// factorial(5)가 컴파일타임 상수가 아니기 때문
int main() { A<factorial(5)> a; }

// 위와 같은 상황을 타개하기 위해서
// 템플릿 메타 프로그래밍의 방식을 사용
template <int N>
struct Factorial {
  static const int value = N * Factorial<N - 1>::value;
};

template <>
struct Factorial<0> {
  static const int value = 1;
};

template <int N>
struct A {
  int operator()() { return N; }
};

int main() {
  // 컴파일 타임에 값이 결정되므로 템플릿 인자로 사용 가능!
  // 의도: A<3628800> a
  A<Factorial<10>::value> a;

  std::cout << a() << std::endl;
}
```

* 위와 같은 경우 TMP는 조건문들이 탬프릿 특수화를 통해 구현
* 반복문은 재귀함수를 사용
  * 가독성 떨어짐

```c++
// constexpr를 사용해 3628800를 컴파일 타임에 계산
constexpr int Factorial(int n) {
  int total = 1;
  for (int i = 1; i <= n; i++) {
    total *= i;
  }
  return total;
}

template <int N>
struct A {
  int operator()() { return N; }
};

int main() {
  A<Factorial(10)> a;

  std::cout << a() << std::endl;
}
```

* **constexpr 함수의 제약 조건**
  1. goto 문 사용
  2. 예외 처리 (try 문; C++ 20 부터 가능)
  3. 리터럴 타입이 아닌 변수의 정의
  4. 초기화 되지 않는 변수의 정의
  5. 실행 중간에 constexpr 이 아닌 함수를 호출
* constexpr 함수는 컴파일 타임 상수가 아닌 인자도 받아서 동작 가능

```c++
constexpr int Factorial(int n) {
  int total = 1;
  for (int i = 1; i <= n; i++) {
    total *= i;
  }
  return total;
}

int main() {
  // 일반 정수
  int num;
  std::cin >> num;

  // 잘 동작한다
  std::cout << Factorial(num) << std::endl;
}
```

## 리터럴 타입
* 컴파일러가 컴파일 타임에 정의할 수 있는 타입
* 아래 타입들은 constexpr 로 선언 또는 constexpr 함수 내부에서 사용 가능
  1. void 형
  2. 스칼라 타입
    * int, char, bool, long, float, double, ...
  3. 레퍼런스 타입
  4. 리터럴 타입의 배열
  5. 아래 조건을 만족하는 타입
    * default 소멸자
    * 다음 중 하나를 만족
      * 람다 함수
      * arggregate 타입
        * 사용자 정의 생성자 및 소멸자가 없으며 모든 멤버가 public
        * ex) pair
      * constexpr 생성자를 가지며 복사 생성자나 이동 생성자가 없음

## constexpr 생성자

```c++
// Default 소멸자 & constexpr 생성자 & 복사 및 이동 생성자가 없음
// Vector는 리터럴 타입
class Vector {
 public:
  constexpr Vector(int x, int y) : x_(x), y_(y) {}

  constexpr int x() const { return x_; }
  constexpr int y() const { return y_; }

 private:
  int x_;
  int y_;
};

constexpr Vector AddVec(const Vector& v1, const Vector& v2) {
  return {v1.x() + v2.x(), v1.y() + v2.y()};
}

template <int N>
struct A {
  int operator()() { return N; }
};

int main() {
  constexpr Vector v1{1, 2};
  constexpr Vector v2{2, 3};

  // constexpr 객체의 constexpr 멤버 함수는 역시 constexpr!
  A<v1.x()> a;
  std::cout << a() << std::endl;

  // AddVec 역시 constexpr 을 리턴한다.
  // AddVec이 constexpr 함수
  // v1, v2가 constexpr
  // 함수 x()가 constexpr 이기 때문
  A<AddVec(v1, v2).x()> b;
  std::cout << b() << std::endl;
}
```

## if constexpr

```c++
// 아래 함수는 t가 포인터인 경우
// *t로 값을 리턴하고,
// 아닌 경우는 t로 값을 리턴한다
// 하지만 컴파일 되지 않는다
template <typename T>
void show_value(T t) {
  if (std::is_pointer<T>::value) {
    std::cout << "포인터 이다 : " << *t << std::endl;
  } else {
    std::cout << "포인터가 아니다 : " << t << std::endl;
  }
}

int main() {
  int x = 3;
  show_value(x);

  int* p = &x;
  show_value(p);
}

// 위 구문대로 탬플릿이 인스턴스화 되면서 아래 함수가 정의된다
// if 구문에서 *t 때문에 컴파일에러가 발생한다
void show_value(int t) {
  if (std::is_pointer<int>::value) {
    std::cout << "포인터 이다 : " << *t << std::endl;
  } else {
    std::cout << "포인터가 아니다 : " << t << std::endl;
  }
}

// 위 함수에서 constexpr를 추가한다
// 조건이 반드시 bool로 타입 변환될 수 있는 컴파일 타입 상수식이어야만 한다
// 참인 경우, else에 해당하는 문장은 컴파일 되지 않는다
// 거짓인 경우, else에 해당하는 부분만 컴파일 된다
template <typename T>
void show_value(T t) {
  if constexpr (std::is_pointer<T>::value) {
    std::cout << "포인터 이다 : " << *t << std::endl;
  } else {
    std::cout << "포인터가 아니다 : " << t << std::endl;
  }
}
```

## 출처
* <https://geekhub.tistory.com/68>
* <https://modoocode.com/293>
* <https://heroine-day.tistory.com/m/60>