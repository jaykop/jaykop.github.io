---
title: "Scheduling"
classes: wide
categories: 
  - post
  - os
sidebar:
  nav: "main"
author_profile: true
---
   
## 스케줄링
![post_thumbnail](/assets/images/img(2).png)
* **프로세스가 실행되기 위하여 OS 스케줄러에 의해 자원을 할당받는 것**
  * User processes 
  * System processes 

## 장기 스케줄링 Long-Term Scheduler / Job Scheduler

![post_thumbnail](/assets/images/img.png)
* 한정된 메모리를 배분하기 위하여 프로세스를 임시로 대용량 메모리에 저장
* 이 중 어느 프로세스를 Ready Queue로 보낼지 결정하는 작업
  * CPU Bound Process 
    - CPU가 처리해야 하는 비중이 높은 프로세스
    - 이 프로세스 위주로 스케줄링 되면 상호작용 효율이 떨어짐
  * I/O Bound Procses 
    - 입출력을 많이 요구하는 프로세스
    - 이 프로세스 위주로 스케줄링 되면 입출력을 기다리며 허비되는 CPU 자원 많아짐
* 프로세스의 종료 / 실행 중인 프로세스 개수에 따라 조절하므로 수행 텀이 긺
* **현대에는 Virtual Memory Management의 발달로 의미가 퇴색**

## 단기 스케줄링 Short-Term Scheduler / CPU Scheduler

![post_thumbnail](/assets/images/img(1).png)
* Ready Queue에 있는 프로세스 중 어떤 프로세스를 실행할지 결정
* 실행 / 중기되는 태스크의 교체를 매 순간 수행
  * 최소 100ms interval

## 중기 스케줄링 Medium-Term Scheduler / Swapper

![post_thumbnail](/assets/images/img(3).png)
* 중기/단기 이후에 고안된 스케줄러
* 자원 관리를 위해 CPU에서 디스크로 swapping(쫓아내는) 하는 작업 
  * 우선순위가 가장 낮거나, 일정시간 동안 활성화되지 않았던 프로세스 위주
  * 멀티프로그래밍할 개수를 줄이는 의의

## 스케줄링 조건
* CPU 효율: 노는 CPU를 허락하지 않는다
* 반응 시간: 빠른 태스크 실행
* Turnaround time: 태스크는 적정 시간을 기하여 완료되어야 함
* 우선순위: 어떤 태스크는 다른 태스크에 비해 더 중요할 수 있음

## Queueing (비선점적 스케줄링) non-preemptive
* 여러 프로세스가 CPU 자원을 획득하기 위해 경쟁
* 중도 회수할 수 없음
  * 실행 중인 프로세스가 CPU 연산이 필요 없을 때에만 운영체제가 회수 가능
* 태스크는 큐안에서 순서대로 실행
  * First In, First Out (FIFO) queue 먼저 큐에 들어온 일부터
  * Shortest Job First (SJF) queue 빨리 끝낼 수 있는 일부터 

## Round-Robin (선점적 스케줄링) preemptive
* 프로세스들 사이에 우선순위를 두지 않고, 돌아가며 시간단위(Time Quantum)로 CPU를 할당하는 방식
* OS가 타이머 등 트리거를 이용해 강제로 CPU 자원을 뺏어 프로세스를 종료 가능
* 문맥 전환의 오버헤드가 큼
* 응답시간이 짧아지는 장점이 있어 실시간 시스템에 유리
* 각 프로세스는 할당받은 time slice가 있음 (Time Sharing)
  * 그 시간 동안만 작동
  * 시간이 다 하면 다음 프로세스가 작동

## 출처
* <https://jhnyang.tistory.com/372>