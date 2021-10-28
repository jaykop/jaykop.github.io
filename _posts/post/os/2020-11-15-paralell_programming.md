---
title: "Paralell Programming"
classes: wide
categories: 
  - post
  - os
sidebar:
  nav: "main"
author_profile: true
---
   
## Synchronization 동기화
* 복수 이벤트의 유연한 실행 및 조화를 위해 조정을 가하는 것
* 구속 조건은 아래와 같다
  * **Serialization**: 하나의 이벤트가 끝난 다음에 다른 이벤트가 발생
  * **Mutual Exclusion**: 두 개의 이벤트가 한 시점에 동시에 발생하고 있지 않음

## Shared variables

![post_thumbnail](/assets/images/{7F0D7DB1-A481-4D6D-BEBF-291796F5FFE8}.png)
* 위 두 스레드의 실행 결과는 매번 다르다
  * 5일 수도, 7일 수도 있다
* **Race condition**: 복수의 이벤트가 발생하고 타이밍에 의해 결과값이 의존되어 달라지는 현상
  
![post_thumbnail](/assets/images/{75A2D9B6-F1AC-4856-83C3-4B1221439B2D}.png)
* 위 두 스레드의 실행 결과 역시 매번 다르다
  * 원래 값을 0이라고 할 때, 1일 수도, 2일 수도 있다
  * 한 구문이 완벽하게 끝날 때까지 침범받지 않는 구문이 필요
* **Atomic**: Interrupt 되지 않는 operation

## Mutex
* Mutex의 성질
  
  |성질|내용|
  |:---:|:---|
  |<strong>Mutual Exclusion<strong/>|여러 개의 프로세스/스레드가 임계 구역에 함께 진입할 수 없음|
  |<strong>Progress<strong/>|하나의 스레드가 임계구역을 벗어나면 다음 임계구역에 들어갈 스레드는 아직 임계구역에 들어가지 못한 스레드 중 하나여야 한다|
  |<strong>Bounded waiting<strong/>|다른 프로세스의 기아(Starvation)를 방지하기 위해, 한 번 임계 구역에 들어간 프로세스는 다음 번 임계 구역에 들어갈 때 제한을 두어야 한다|
  
* 한번에 하나의 스레드만 Critical Section(임계구역)에 진입하며, 이를 벗어난 스레드가 바로 다시 임계구역으로 들어가서는 안된다

```c++
// Dekker’s algorithm

threadAwantsin = 0
threadBwantsin = 0
favored = A

// Thread A
while ( 1 ) do {
  threadAwantsin = 1
  // 양 쓰레드에서 동시 진입하더라도,
  while ( threadBwantsin == 1 ) do {
    if ( favored == B ) do {
      // 상대방이 진입하도록 토글을 바꾼다
      threadAwantsin = 0
      // 토글을 바꿔준 뒤 이 스레드는 계속 멈춰있다
      while ( favored == B ) do {}
        threadAwantsin = 1
    }
  }
  // while문을 벗어난 스레드는 임계구역으로 진입한다
  critical section code
  // 진행 토글을 상대방으로 전환한다
  favored = B
  threadAwantsin = 0
  non critical code
}

// Thread B
while ( 1 ) do {
  threadBwantsin = 1
  // 양 쓰레드에서 동시 진입하더라도,
  while ( threadBwantsin == 1 ) do {
    if ( favored == A ) do {
      // 상대방이 진입하도록 토글을 바꾼다
      threadBwantsin = 0
      // 토글을 바꿔준 뒤 이 스레드는 계속 멈춰있다
      while ( favored == A ) do {}
        threadBwantsin = 1
    }
  }
  // while문을 벗어난 스레드는 임계구역으로 진입한다
  critical section code
  // 진행 토글을 상대방으로 전환한다
  favored = A
  threadAwantsin = 0
  non critical code
}
```

## Amdahl의 법칙

![post_thumbnail](/assets/images/{BF98C5E3-5B76-4639-AB08-FFE2FEBEF806}.png)

|문자|내용|
|:---:|:---|
|<strong>r<strong/>|최대 성능 향상|
|<strong>p<strong/>|시스템 전체 작업 중 개선된 부분|
|<strong>s<strong/>|성능 향상 정도|

* 컴퓨터 시스템의 일부를 개선할 때 전체적으로 얼마만큼의 최대 성능 향상이 있는지 계산하는 데 사용
  * 어떤 작업의 40%에 해당하는 부분의 속도를 2배로 늘릴 수 있다면, P는 0.4이고 S는 2이고 최대 성능 향상은 1.25

## Semaphore
* 다익스트라에 의해 고안
* Count가 있는 Mutex, **Mutex의 일반형**
  * Mutex는 Count가 1인 Semaphore
* **Initialization/Wait/Signal**
* Semaphore의 Count가 n으로 설정되어 있다면, 임계구역의 진입할 수 있는 스레드의 수는 n이다
* **Multiplex**
  * 복수의 스레드가 임계구역에 진입하도록 하는 것

## Basic Syncronization Patterns

![post_thumbnail](/assets/images/{57C2F452-895C-4816-A44C-8B1D2A9A4DDE}.png)

* 위 코드는
  * b2가 a1을 기다리는 것을 보장
  * a2가 b1을 기다리는 것을 보장
* 두 스레드가 만나는 지점을 **랑데부(Rendezvous)**
* 3개 이상의 스레드의 랑데부를 **Barrier**

```c++

count = 0
mutex = Semaphore(1)
barrier = Semaphore(0)
barrier2 = Semaphore(1) // noticed the value

while (1) {
  //rendezvous
  
  // mutex로 count 연산을 atomic으로 보장
  mutex.wait()
  count = count + 1
  if ( count == n ) {
    barrier2.wait() 
    barrier.signal()
  }
  mutex.signal()

  // turnstile (개찰구)
  // n 번째 스레드가 들어올 때
  // if ( count == n ) 문 안으로 들어갈 수 없으므로
  // 데드락 현상을 방지하고자 개찰구를 만듦
  barrier.wait()
  barrier.signal()

  // critical point ...
  
  // mutex로 count 연산을 atomic으로 보장
  // 재사용 가능한 barrier 디자인을 위해
  // count를 감소하는 구문 추가
  mutex.wait()
  count = count - 1
  if ( count == 0 ) {
    barrier.wait()
    barrier2.signal()
  }
  mutex.signal()

  barrier2.wait()
  barrier2.signal()
}
```

## Dead lock
  * 서로 원하는 리소스가 상대방에게 할당되어 있거나 진행 조건이 상호간에 진행되지 않아 두 프로세스가 무한정 기다리게 되는 상태

  ```c++  
  // 아래 두 스레드는 각기 진입을 원하는 신호를 서로에게 교환한다
  // 그러나 양쪽 모두 값을 1로 바꾼 다음 while 문 안으로 들어가게 되면,
  // 프로그레스를 더 이상 진행할 수 없다
  threadAwantsin = 0
  threadBwantsin = 0

  // Thread A
  while (1) do {
    threadAwantsin = 1
    while ( threadBwantsin == 1 ) do {}
    // critical section code...
    threadAwantsin = 0
    // non critical code...
  }

  // Thread B
  while (1) do {
    threadBwantsin = 1
    while ( threadBwantsin == 1 ) do {}
    // critical section code...
    threadBwantsin = 0
    // non critical code...
  }
  ```

