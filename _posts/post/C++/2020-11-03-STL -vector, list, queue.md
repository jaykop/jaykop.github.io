---
title: "STL - Vector, List, Queue"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## 컨테이너의 종류
* Sequence Container
  * 객체를 순사적으로 보관
  * ex) vector, list, queue, ...
* Associative Container
  * 키를 바탕으로 대응되는 값 함께 보관
  * 키로 탐색하여 값을 반환
  * ex) map, set, unordered_map, ...

## 벡터 vector
* 후입선출(LIFO)
* back이 아닌 다른 포지션에 삽입하거나 제거할 때 불리
* 메모리 접근할 때 subscription operator를 사용하기 때문에 O(1) 소요
* capacity가 더 필요한 경우, 기존 메모리보다 더 큰 사이즈로 할당 후 복사 실행
  * capacity: 메모리만 할당 받고 초기화 되지 않은 용량까지 반환([]로 접근 불가능)
  * size: 메모리를 할당 받고 초기화도 된 용량만 반환([]로 접근 가능)

  ```c++
  vector<int> a = { 1,2,3,4,5 };

  // case 1
  // c = 11
  // s = 11
  a.resize(11);

  // case 2
  // c = 5
  // s = 2
  a.resize(2);

  // case 3
  // c = 11
  // s = 5
  a.reserve(11);

  // case 4
  // c = 5
  // s = 5
  a.reserve(2);

  // 이미 할당한 메모리를 반환하지 않는다
  // reize를 통해 가용 가능한 메모리 사이즈는 조절힌다
  int c = a.capacity();
  int s = a.size();
  ```

* **amortized O(1)**
  * amortized는 분할상환이라는 뜻
  * capacity가 다 차면 기존 사이즈의 2배를 할당 후 복사 이동
    * 비용은 O(n)
    * 자주 발생하는 케이스는 아님
  * 평균적으로 벡터에 새로운 객체를 맨 뒤에 추가할 때 비용은 O(1)

### push_back
* 작돋원리
  1. push_back 함수의 인자에 넣을 객체 A를 생성
  2. A를 인자로 받고 push_back 함수 내에서 A를 복사해 B를 생성
  3. B를 벡터에 추가
  4. push_back 스코프를 벗어난 후 A를 소멸
* 암시적인 생성자를 호출한다

### emplace_back
* 작동원리
  1. 객체를 생성하기 위해 필요한 인자들이 emplac_back 함수 안으로 전달
  2. 전달받은 인수로 객체를 생성
  3. 생성한 객체를 벡터에 추가
* 모든 유형의 생성자를 호출한다

### push_back vs. emplace_back
* 상단의 원리로 인해 일반적으로 emplace_back이 더 빠르다
* emplace_back은 모든 유형의 생성자를 호출함으로써 런타임에서의 문제를 야기할 수 있다

```c++
// addressof 함수는 & 연산자가 오버로딩 되어있는 경우를 대비해
// 그 객체의 실제 주소를 가져오는 역할을 한다
std::vector<std::unique_ptr<T>> v;
T a;

// a는 포인터 형식이 아니기 때문에 삽입할 수 없음!!
// T*와 unique_ptr<T>는 호환이 되지 않는다
v.push_back(std::addressof(a)); 

// ok, 컴파일할때는 에러가 발생하지 않음.
// 모든 유형의 생성자를 호출해서 unique_ptr<T*> 명시적 생성자를 호출
v.emplace_back(std::addressof(a)); 
```

## 반복자 iterator
* 반복자는 각 컨테이너의 멤머 변수로 정의
* *it와 같은 표현식으로 반복자가 가리키는 컨테이너 내의 값을 확인 가능
  * *는 포인터가 아니라 operator

![post_thumbnail](/assets/images/2165E44C595A970A1676B5.webp)

* begin()은 컨테이너의 맨 첫 객체
* end()는 컨테이너의 마지막 객체의 뒤
* **begin() == end()**로 컨테이너가 비어있음을 표현 가능
* 상수로 표현하는 const iterator, 역반복자인 rbegin()과 rend()도 있음
* **벡터의 index는 unsigned 상수**

## 리스트 List
* 어느 위치로든 삽입/삭제가 가능
  * 전후 Node의 prev와 next로 연결된 링크만 수정하면 됨
* 메모리에 접근할 때 순차적으로 접근
  * O(n)의 시간이 소요
  * [] operator나 at 함수가 없음
* 반복자의 연산 중 prefix와 postfix만 수행 가능

```c++
auto itr = list.begin();

itr++  // itr ++
itr--  // --itr 도 가능!

itr + 5  // 불가능!
```
* 위 코드에서 맨 마지막 구문이 불가능한 이유
  * 할당이 연속된 메모리로 이뤄져 있지 않기 때문
  * itr + 5의 주소값에 해당하는 레퍼런스는 list가 아닐 수 있음
* fragmentation을 유발

## 덱 deque & 큐 queue
### 덱
![post_thumbnail](/assets/images/245FC94C595B5F9B133E4E.webp)

* **deque의 각 블록은 실제 값이 아닌 그 값(블록)의 주소를 저장**
  * **원소들이 메모리 속에 연속되어 저장되어 있지 않음**
  * 속도를 위해 메모리를 희생하는 구조
* 벡터보다 삽입이 빠름
  * 벡터는 기존보다 큰 메모리를 새로 할당받아 값을 전체 복사
  * 덱은 새로운 블록을 만들어서 원소를 삽입
* LIFO FIFO 모두 가능
  * 중간 위치의 삽입과 삭제는 어려움
* iteration 가능
  * index로 값 접근도 가능

### 큐
* FIFO (선입선출)
  * 고정 배열을 사용했을 때 enqueue, dequeue 할 때마다 데이터를 이동해야하는 문제 발생
  * Linkedlist를 이용한 원형 큐 구조를 사용
    * 데이터 변경이 발생할 때마다 front와 rear를 초기화
    * 사이즈가 꽉 찾을 경우를 표기하기 위해서는 front와 rear가 동일한 노드를 가리키도록 함
      * 이 노드는 평소에는 비어있음
* iteration 불가

## 스택 stack
* LAST IN FIRST OUT
* 벡터와 사실상 같으나 가독성 면에서 쓰임의 목적이 다름
* iteration 불가

## 출처
* <https://modoocode.com/223>
* <https://openmynotepad.tistory.com/10>