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
   
## 병렬 프로그래밍
* Serialization: 하나의 이벤트가 끝난 다음에 다른 이벤트가 발생
* Mutual Exclusion: 두 개의 이벤트가 한 시점에 동시에 발생하고 있지 않음
* Race condition: 복수의 이벤트가 발생하고 타이밍에 의해 결과값이 의존되어 달라지는 현상
* Atomic: Interrupt 되지 않는 operation
* Mutex
  * Mutual Exclusion - 2개의 프로세스/스레드가 임계 구역에 함께 진입할 수 없음
  * Progress - 하나의 스레드가 임계구역을 벗어나면 다음 임계구역에 들어갈 스레드는 아직 임계구역에  들어가지 못한 스레드 중 하나여야 한다.
  * Bounded waiting - 다른 프로세스의 기아(Starvation)를 방지하기 위해, 한 번 임계 구역에 들어간 프로세스는 다음 번 임계 구역에 들어갈 때 제한을 두어야 한다.
  * 임계구역을 벗어난 스레드가 바로 다시 임계구역으로 들어가서는 안된다
* Semaphore:
  * Count가 있는 Mutex, Mutex의 일반형
  * Initialization
  * Wait
  * Signal
* Multiplex
  * 복수의 스레드가 임계구역에 진입하도록 하는 것
* Dead lock
  * 서로 원하는 리소스가 상대방에게 할당되어 있기 때문에 이 두 프로세스는 무한정 기다리게 되는 상태

