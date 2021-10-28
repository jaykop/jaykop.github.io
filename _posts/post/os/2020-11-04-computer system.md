---
title: "Computer System"
classes: wide
categories: 
  - post
  - os
sidebar:
  nav: "main"
author_profile: true
---
   
## 컴퓨터 시스템 구조 Four Components of a Computer System

|시스템|내용|
|:---:|:---:|
|<strong>하드웨어<strong/>|CPU, I/O,. memory 등 기본 연산 자원을 제공|
|<strong>OS<strong/>|사용자와 application에 따른 하드웨어의 사용을 제어하고 관리|
|<strong>Application<strong/>|사용자의 연산 문제를 풀기 위해 어떤 시스템 자원을 어떤 방식으로 사용할지 정의|
|<strong>사용자<strong/>| - |

## 컴퓨터 시작
1. 컴퓨터 전원 작동 혹은 reboot를 할 때 bootstrap이 작동
  * **bootstrap** - 한 번 시작되면 알아서 진행되는 일련의 과정
2. ROM or EPROM에 저장되어 있음
  * 전원을 꺼도 데이터가 저장되는 비휘발성
  * BIOS나 OS, 펌웨어를 저장하는 데 쓰임
  * 최근에는 일부가 플래시 드라이브로 대체
3. 시스템 전 방면에 대하여 초기화
4. OS 커널을 불러오고 실행

## 커널 Kernel
* **모든 하드웨어와 자원을 관리하는 가장 낮은 수준의 프로그램**
* 보안 
  - 컴퓨터 하드웨어와 프로그램의 보호
* 자원관리
   - 효율적인 자원 분배, 스케줄링으로 프로그램을 실행
* 추상화
   - 하드웨어의 복잡한 명령어들을 추상화하여 간편한 인터페이스 제공

## 버스 Bus
* 컴퓨터 안의 부품들 간에, 또는 컴퓨터 간에 **데이터와 정보를 전송하는 통로**
* 현대 PC들은 대량의 정보 처리를 위해 복수의 bus를 탑재

## 프로세서 Processor
* 컴퓨터 운영을 위해 기본적인 명령어들을 처리하고 반응하기 위한 논리회로
* **제어장치 Control Unit**
   - 소프트웨어로부터 신호를 받아 하드웨어로 전송
* **연산장치 Arithmetic Logic Unit**
   - 사칙연산과 논리연산을 처리

## CPU Central Processing Unit
* 디바이스가 해야할 일을 총지휘하는 프로세서
  * **보조 프로세서 Coprocessor**
    - CPU를 보조하며 연산, 제어의 핵심부분을 담당
* 기억, 연산, 제어 컴퓨터의 논리적 사고를 처리 
* 코어, 캐시 메모리, 컨트롤러 등을 포함

  |구분|역할|
  |:---:|:---:|
  |<strong>RAM<strong/>|단기 기억|
  |<strong>Disk<strong/>|장기 기억|
  |<strong>CPU<strong/>|사고|

## 코어 Core
  * CPU의 각종 연산을 수행 핵심 요소 중 하나
  * 프로세서가 하는 일을 분담

## 컴퓨터 시스템 조직
* 컴퓨터 시스템의 작동

![post_thumbnail](/assets/images/1319300_orig.png)
  * 하나 이상의 CPU와 Device Controller 들이 common bus 를 통해 연결
  * common bus는 shared memory에 access를 제공
  * 각 메모리의 사이클을 두고 CPU와 기기들이 실행을 위해 경쟁
* Computer System Organization
  * CPU와 I/O device는 동시에 실행 가능
  * 각 device controller는 특정 device type을 소관하며, 들어오고 나가는 데이터 정보를 임시로 저장하기 위한 local buffer를 가짐
  * CPU가 main memory와 local buffers 사이의 data를 전송
  * 목적을 달성하기 위해 CPU/메모리와 외부 장치간에 정보를 주고 받는 것을 I/O라 지칭
  * Device controller는 interrupt 에 의해 작동이 중지됨을 CPU에 알린다

## 배치 처리 시스템
  * Queue 구조로, 하나의 태스크가 종료될 때까지 다음 태스크를 시작하지 않음
  * 이를 보완하기 위한 시스템이 시분할 시스템

## 멀티프로세싱 vs. 멀티프로그래밍 vs. 멀티태스킹 vs. 멀티스레드
* **멀티프로세싱** 

![post_thumbnail](/assets/images/multiPROCESSINGjpg.jpg)
  * 여러 프로세서가 협력하여 일을 처리 (= 멀티코어 시스템)
  * 병렬 구조의 프로세서 처리방식
    * 처리량 증대
    * 규모의 경제 - 많은 인풋에 따른 아웃풋 증대로 효율성 증가
    * 신뢰도 상승
  * 비대칭 멀티프로세싱 - 특정 프로세서가 특정 태스크만을 처리
  * 대칭 멀티프로세싱 - 모든 프로세서가 모든 태스크를 처리 

* **멀티프로그래밍 Multiprogramming (Batch system)**

  ![post_thumbnail](/assets/images/multiprogramming.jpg)
  * 단일 프로세스 상에서 여러 프로그램이 실행되도록 하는 것
    * 프로세서가 입출력 작업(I/O)의 종료를 대기할 동안 다른 프로그램을 수행
    * 자원의 낭비를 막기 위한 목적
  * 태스크를 조직화 하여 **CPU가 항상 하나의 일을 하도록 해준다**
  * 태스크의 서브셋은 항상 메모리에 저장되어 있다
  * 스케줄링에 의해 하나의 태스크가 선택되고 실행된다
  * **태스크가 정지되어야 하면 OS는 다른 태스크로 이동한다**
    * 하나의 태스크가 I/O되면, CPU는 해당 태스크에 대한 작업을 정지하고 다른 태스크를 Pool에서 받아와 실행
    * 태스크의 I/O가 완료되면 다시 그 일을 수행

* **멀티태스킹 Multitasking (Time Sharing)**

  ![post_thumbnail](/assets/images/multitasking.jpg)
  * CPU가 태스크를 변경함에 있어 사용자가 각 태스크가 작동하는 동안 반응하고, 상호작용할 수 있도록 하는 논리적 확장
    * 반응 시간은 최대 1초
    * **실행되고 있는 프로세스들이 일정 시간을 분할 받아 돌아가며 실행**
  * 각 사용자(프로그램)는 적어도 하나의 프로세스를 메모리에서 실행 중이어야 한다 (process)
  * 여러 태스크가 동시에 실행될 준비가 되어 있어야 한다(CPU scheduling)
  * 프로세스가 메모리에 맞지 않으면, 스와핑을 이용해서 가상메모리에 저장
  * OS가 태스크마다 일정 시간을 분배하여 여러 태스크를 번갈아가며 수행
  * 정해진 시간동안 각각의 task를 번갈아가며 수행하기 위한 목적

* **멀티스레드** 

![post_thumbnail](/assets/images/vlc.jpg)
  * **하나의 프로세스 안에서 여러 스레드들이 자원을 공유하며 병렬 구조로 작업을 수행**
    * 하나의 Context 안에서 동시에 여러 Code Segment를 수행
  * 한 유저에 대해 프로그램의 복수 실행(또는 복사)없이 여러 Request를 받아 수행 가능
    * 예시) 위 VLC 그림을 기준으로,
      1. t1은 VLC를 실행
      2. t2는 음악을 재생
      3. t3는 새 음악을 추가

## 출처
* <https://donghoson.tistory.com/14>
* <https://www.geeksforgeeks.org/difference-between-multitasking-multithreading-and-multiprocessing/>