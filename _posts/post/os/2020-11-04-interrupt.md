---
title: "Interrupt"
classes: wide
categories: 
  - post
  - os
sidebar:
  nav: "main"
author_profile: true
---

## 인터럽트 (Interrupt)
* **CPU가 특정 기능을 수행하는 도중에 급하게 다른 일을 처리하고자 할 때 사용할 수 있는 기능**
* 대부분의 컴퓨터는 한 개의 CPU를 사용
 * 한 순간에는 하나의 일 밖에 처리할 수 없음
 * 어떤 일을 처리하는 도중에 우선 순위가 급한 일을 처리해야하는 경우 발생 

## 내부 인터럽트 
* 하드웨어 고장(Hardware Interrupt) 
  * 컴퓨터 고장 
  * 데이터 전달 과정에서의 비트 오류 
  * 전원이 나간 경우 
* 실행할 수 없는 명령어
  - 기억장치에서 인출한 명령어의 비트 패턴이 정의되어 있지 않은 경우 
* 명령어 실행 오류
  - 나누기 0을 하는 경우 
* 사용 권한 위배
  - 사용자가 운영체제만 사용할 수 있는 자원에 액세스하는 경우 

## 외부 인터럽트 
* 외부 인터럽트는 **주로 입출력장치에 의해 발생**
* 타이머 인터럽트
  - 타이머가 일정한 시간 간격으로 중앙처리장치에게 인터럽트를 요청 
* 입출력 인터럽트
  - 속도가 느린 입출력장치가 입출력 준비가 완료되었음을 알리기 위해 인터럽트를 요청

## 소프트웨어 인터럽트 SuperVisor Call: SVC
* 사용자가 프로그램을 실행시키거나 감시프로그램을 호출
* 소프트웨어 이용 중 다른 프로세스를 실행시키면 시분할 처리를 위해 자원 할당

## 인터럽트 우선 순위
* 전원 이상(Power fail) > 기계 착오(Machine Check) > 외부 신호(External) > 입출력(I/O) > 명령어 잘못 > 프로그램 검사(Program Check) > SVC(SuperVisor Call)
* 하드웨어 인터럽트 > 소프트웨어 인터럽트
* 외부 인터럽트 > 내부 인터럽트

## 인터럽트 동작 순서
![post_thumbnail](/assets/images/MD4NrLz.png)
1. 인터럽트 요청
2. 프로그램 실행 중단
3. 프로그램 상태 보존
  * PCB, PC를 이용
4. 인터럽트 처리 루틴 실행
  * 인터럽트 요청한 장치 식별
5. 인터럽트 서비스 루틴 실행
  * 원인을 파악하고 실질 작업 수행
  * 레지스터 상태 보존
  * 서비스 루틴 중 우선순위에 따라 1~5의 과정을 재귀적으로 수행
6. 상태 복구
  * 저장해 둔 Program Counter를 복구
7. 중단된 프로그램 실행 재개

## 인터럽트 작동 방식
* 제어권을 옮길 때, interrupt service routine 주소값이 저장된 interrupt vector에 접근
* Interrupt architecture는 반드시 interrupted된 작동 주소를 저장
* A trap or exception는 유저 리퀘스트 혹은 에러에 의해 소프트웨어적으로 생성된 interrupt이다
* OS는 간섭중심적(interrupt driven) 

## Interrupt Handling
* OS는 컴퓨터 카운터나 레지스터를 이용해 저장함으로써 CPU의 상태를 보존
  * 어떤 타입의 간섭이 일어났는지 확인
  * 간섭의 타입에 따라 어떤 action이 일어나야 할 지 segment를 구분

## Polling과의 차이?
* Polling은 대상을 주기적으로 감시하여 상황이 발생하면 해당처리 루틴을 실행해 처리
* 일정한 조건을 만족할 때 송수신 등의 자료처리를 하는 방식
* **인터럽트는 CPU에 일을 처리해 달라고 요청하는 수단**

## 듀얼 모드
* OS 스스로와 다른 컴포넌트 시스템을 지킬 수 있음
* 사용자 모드와 커널 모드로 구분
  * CPU가 제공하는 mode bit를 이용 (하드웨어 베이스)
  * 시스템이 유저 코드를 실행하는지 커널 코드를 실행하는지 구분
  * 특정 명령은 커널 모드에서만 실행
  * 커널모드에서의 콜이 종료되면 다시 사용자 모드로 회귀
  * 메모리 할당, 디바이스 I/O 상호작용 등이 모두 mode bit를 바꾸면서 실행

  |모드|내용|
  |:---:|:---|
  |<strong>사용자 모드<br/>User Mode<strong/>|* 사용자 태스크는 여기서 처리<br/>* 유저 임의로 커널 모드로 스위치 불가<br/>* OS만이 할 수 있음<br/>* 커널모드에서만 처리되는 태스크가 필요하면 사용자가 시스템에 리퀘스트해야 함(System Call)<br/>|
  |<strong>커널 모드<br/>Kernel Mode<strong/>|* 시스템 작업과 같은 것들이 OS에 의해 작동<br/>* 인터럽트는 커널 모드에서 처리<br/>* 무한 루프, 자원 낭비 등을 막기 위해 OS는 커널모드 진입시 타이머를 세팅하고 시간이 0이 되면 기존 실행하던 application을 resume할지, 아니면 terminate할지 결정|

## 출처
* <https://raisonde.tistory.com/entry/인터럽트Interrupt의-개념과-종류>
* <https://kkhipp.tistory.com/155>
* <https://jiss02.tistory.com/32>