---
title: "Process Management"
classes: wide
categories: 
  - post
  - os
sidebar:
  nav: "main"
author_profile: true
---
   
## 개요
* **프로세스란 메모리 상에 실행되고 있는 프로그램**
  * 프로그램 - 작업을 위해 실행할 수 있는 파일

  |상태|내용|
  |:---:|:---|
  |<strong>프로그램<strong/>|* 실행가능한 코드<br/>* 일반적으로 파일로서 디스크에 저장|
  |<strong>프로세스<strong/>|* 메모리에 할당되어 실행 중인 프로그램|

* **Process State**
  * 할당된 메모리, 레지스터에서 사용 중, 실행 기간 등의 정보
  * State는 한번에 하나의 State로 정의
  * new, readay, running, suspended, blocked, terminated

  |State|내용|
  |:---:|:---|
  |<strong>New (Created)<strong/>|프로세스 실행 (생성)|
  |<strong>Running<strong/>|CPU 및 다른 자원들을 이용해 실행|
  |<strong>Blocked<strong/>|프로세스가 타 이벤트 혹은 I/O로 인하여 정지되어 있음 |
  |<strong>Ready<strong/>|프로세스가 Ready queue에 있고 CPU가 할당될 때까지 기다리는 중|
  |<strong>Terminated<strong/>|프로세스가 일을 끝내서 종료되거나, 시스템 혹은 유저가 강제로 종료|

* **Thread** - 서브 프로세스로서 한 개의 프로세스는 여러 개의 스레드를 가질 수 있음
* **CPU Burst** - 인터럽트가 없는 CPU 사이클 시간
* **I/O Burst** - I/O 작업이 완료되는 시간

## 프로세스 관리 Process Management
* 작업을 수행하기 위해
  * CPU, Memory, I/O, files Initialization Data 등의 자원이 필요
* 프로세스를 파괴할 때 재사용 가능한 메모리 구역을 요청
* 싱글 스레드 프로세스는 하나의 프로그램 카운터를 보유
* 멀티 스레드 프로세스는 스레드 당 프로그램 카운터를 보유
* **프로그램 카운터 Program Counter (명령어 포인터)**
  - CPU 내부에 있는 레지스터 중의 하나
  - 다음에 실행될 명령어의 주소를 가지고 있어 실행할 기계어 코드의 위치를 지정

## Process Control Block (PCB)
* OS가 프로세스를 관리하기 위해 장보를 저장하는 곳
  * 프로세스의 상태 정보를 저장
  * 프로세스가 생성될 때 만들어지며, RAM에 유지
* 모든 프로세스는 C 구조체 타입의 정보를 담는 메모리를 가짐
* CPU, Disk 상에서 링크리스트 형태로 보존되며 큐로 표현됨
* PCB의 구조

|구조|내용|
|:---:|:---|
|<strong>Process Id (PID<strong/>)|프로세스 고유번호|
|<strong>Process State<strong/>|준비, 대기, 실행 등의 상태|
|<strong>Program counter (명령어 포인터)<strong/>|프로세스가 다시 실행될 때 실행할 명령어 (복귀 지점)|
|<strong>CPU registers<strong/>|명령어 포인터를 포함하며, 추후에 reload 하기 위해 저장|
|<strong>Open files<strong/>|열린 파일 또는 I/O는 PCB에 기록|
|<strong>Scheduling info<strong/>|우선순위, 시간, etc.|

## Context Switch
* OS가 인터럽트 요청을 받고 진행중이던 프로세스를 변경
  * I/O request (입출력 요청할 때)
  * time slice expired (CPU 사용시간이 만료 되었을 때)
  * fork a child (자식 프로세스를 만들 때)
  * wait for an interrupt (인터럽트 처리를 기다릴 때) 
* 라운드로빈 스케줄링에서 OS는 주기적으로 프로세스를 스위치해야함
![post_thumbnail](/assets/images/다운로드.jfif)
* 과정
  1. 프로세스 정보는 PCB로부터 읽어옴
  2. 타이머를 초기화
  3. 프로세스를 실행(혹은 재실행)
  4. 타이머가 끝나기 전 프로세스가 종료되면
    1. 스케줄링 리스트에서 해당 PCB를 삭제
    2. 아니면 타이머가 끝나고 난 뒤 현재 현재 프로세스의 정보를 PCB에 저장
  5. 리스트에 있는 다음 프로세스로 스위치
  * 위 과정을 반복
  * **Context Switching 때 해당 CPU는 아무런 일을 하지 못 함**
    * 컨텍스트 스위칭이 잦아지면 오버헤드가 발생해 효율(성능)이 저하

## 프로세스 생성
* 새 프로그램을 실행
  * unique process ID (PID) 할당
  * 프로세스의 우선순위 할당
  * PCB 생성
  * 디스크에서 프로그램을 메모리로 로드해옴
  * 프로세스가 스케줄 리스트에 입력 
* 기존 실행 중인 프로세스가 새 프로세스를 실행 가능
  * Parent: existing process  
  * Child: created process 
  * fork 펑션을 이용해 Child process를 생성
    * return value가 0이면 child 
    * PID면 parent
  * child는 항상 exit function을 사용해서 종료
  * parent는 일반적으로 child가 종료될 때까지 wait

## 프로세스 종료
* 프로세스가 종료될 때, 사용 중이던 자원을 OS에 return 해야 함
* 물리 및 가상 메모리 반환
* 열린 파일들 종료
* I/O buffers 해제
* OS에 의해 기타 모든 자원들을 해제
* 프로세스의 종료 방법은 voluntary 아니면 involuntary.  
  * Normal exit (voluntary)  
    * 프로세스가 마지막 단계에 이르러 실행을 종료하게 되면 OS에 확정을 받음
  * Error exit (voluntary)  
    * 프로세스가 강제 종료를 요구하는 fatal error를 발견
  * Killed by another process (involuntary) 
    * 프로그램 자체의 버그로 인하여 종료
      * 프로세스가 할당받은 메모리를 초과
      * 프로세스가 비정상적인 실행을 시도
      * 프로세스가 존재하지 않는, 또는 비정상적인 메모리를 참조
      * 0으로 나눔  
    * (일반적으로 부모)프로세스가 다른 프로세스를 종료
      * 해당 프로세스가 더 이상 필요하지 않을 때
      * 다른 프로세스가 종료되고, OS가 종료된 프로세스 없이 기존 프로세스의 실행을 허락하지 않을 때
      * OS가 종료되어 실행중인 모든 프로세스를 종료

## Interprocess Communication (IPC)
* 프로세스들 사이에 서로 데이터를 주고받는 행위 또는 그에 대한 방법이나 경로
* Shared memory 공유 메모리 
  * 메모리 중 common block에 접근할 수 있음
  * 공유 메모리에 읽고 쓰기가 가능
  * 빠르지만 synchronization 이슈가 있음
* Message passing 
  * 커널을 통한 프로세스 간의 정보 이동
  * 메시지 프로토콜 필요
  * 안정적이지만 느림
* POSIX pipes 
  * 두 프로세스가 읽고 쓰는 펑션을 이용해 커뮤니케이션 가능

## 프로세스 vs. 쓰레드
* 프로세스
  * 실행되고 있는 한 개의 프로그램
  * CPU는 프로세스를 실행하기 위해 적절한 양의 자원을 할당하고, 운영체제의 성능에 좌우
* 쓰레드
  * 프로세스 내부에서 자원을 할당받아 실행되는 독립적인 작업 단위
  * 스레드는 각자의 스택 메모리 영역을 가짐
  * 동일한 프로세스 내의 다른 스레드들과 전역 메모리를 공유
  * CPU로부터 새로운 자원을 할당받지 않아도 되기 때문에 프로세스보다 실행 속도가 빠름

## 출처
* <https://jhnyang.tistory.com/33>