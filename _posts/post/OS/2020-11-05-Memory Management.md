---
title: "Memory Management"
classes: wide
categories: 
  - post
  - OS
sidebar:
  nav: "main"
author_profile: true
---

## 메모리 관리
* 프로그램을 실행하기 위해 모든(또는 일부) 실행 구문과 데이터의 전부(또는 일부)은 **메모리 안에 있어야 함**
* CPU가 유저 작업에 반응하고 최적화하기 위해 **어떤 데이터를 메모리 안에 넣을지를 정하는 작업**
* Activities: 
  * 어떤 메모리가 쓰이는지, 누구에 의해 사용되는 지를 트래킹
  * 어떤 프로세스, 데이터가 메모리에 진입하고 방출될지를 결정
  * 필요한 만큼의 메모리를 할당 또는 반환

## 메모리 보호
* **OS를 변조하려는 유저 태스크를 막는 것**
* OS는 유저 태스크에 일정 메모리를 할당
* 유저 모드에서 태스크는 할당받은 메모리 범주 내에만 접근 가능
* 접근 확인은 하드웨어에서 이뤄짐
* 만약 유저 태스크가 할당된 메모리 범주를 벗어나는 시도를 하면 segmentation fault가 발생
  * **세그멘테이션 결함(Segmentation Fault)**, 세그멘테이션 위반, 세그멘테이션 실패, 세그폴트(Segfault)
  * 프로그램이 허용되지 않은 메모리 영역에 접근을 시도하거나, 허용되지 않은 방법으로 메모리 영역에 접근을 시도할 경우 발생

## 가상 기억 장치 (가상 메모리)
![post_thumbnail](/assets/images/MMU_principle_updated.png)
* 메모리 자원을 이상적으로 추상화하여 물리 기억 장치의 크기보다 더 큰 메모리를 제공
* 활성 RAM과 디스크의 비활성 메모리로 결합
* 가상 주소와 물리 주소로 구분되며, Memory Management Unit에 의해 가상 주소에서 물리 주소로 변환
* 페이징을 하는 방법

## MMU Memory Management Unit
* CPU가 메모리에 접근하는 것을 관리하는 하드웨어
* CPU에게서 가상 메모리 주소를 받으면 뒤쪽 N비트는 바꾸지 않고 앞쪽 나머지 비트를 실제 메모리 주소로 변환

## 저장매체 관리
* OS는 정보 저장에 있어 동일하고 논리적인 UI를 제공
  * 물리 요소를 논리 저장 단위로 추상화 -> 파일
  * 각 파일은 기기에 의해 관리됨
    * 접근 속도, 크기, 데이터 이동률, 접근 방법 등 요소가 내재
* 파일 시스템 관리
  * 파일은 보통 디렉터리 안에 저장
  * 대부분의 시스템에서의 접근 관리는 누가 어디에 접근할 수 있는지를 관리
  * OS는
    * 파일과 디렉터리를 생성하거나 삭제
    * 파일과 디렉터리의 요소를 변경
    * 파일을 다른 저장장치에 이동
    * 파일을 비휘발성 저장장치에 백업

## 디스크에서 레지스터까지의 데이터 마이그레이션
![post_thumbnail](/assets/images/image (1).png)
* 멀티태스킹 환경에서 모든 CPU가 가장 최근의, 동일한 데이터를 제공해주는 역할은 매우 중요
* 이 데이터가 본래 어디에 저장되어 있든 상관없이 안정적으로 전달되어야 한다
* 디스크 -> 주 메모리 -> 캐시 -> 레지스터

## I/O 서브시스템
* OS의 역할 중 하나는 하드웨어 기기의 기묘함을 숨기는 역할

|I/O 서브시스템|내용|
|:---:|:---|
|<strong>버퍼링 Buffering<strong/>|* 버퍼 메모리 영역에 데이터를 모았다가 사용<br/>* 자료의 생산자와 소비자 사이에 속도가 다른 것에 대처<br/>* 서로 다른 장치들 사이에 사용되는 자료 전송의 사이즈가 다른 것을 극복<br/>* 데이터 입출력의 의미를 명확하게 하기 위함
|<strong>캐싱 Caching<strong/>|* 좀 더 빠른 메모리 단계로 데이터를 저장해 놓고 사용|
|<strong>스풀링 Spooling<strong/>|* 디바이스를 독점적으로 사용해 프로세스가 작업을 수행하는 동안 다른 요청을 처리할 수 없는 경우<br/>* 교차해서 동작될 수 없는 프린터 같은 장치를 위해 출력 자료를 보관하는 버퍼<br/>* 프린팅 작업을 대기시켜야 함|

  * 일반적인 기기 - 드라이브 인터페이스 제공
  * 특정 하드웨어 기기를 위한 드라이버

## System Call
* 컴퓨터 프로그램이 실행할 때 커널이나 OS에 서비스를 요청하는 방법
* OS 서비스가 제공되기 위한 프로그래밍 인터페이스
* 주로 C나 C++로 작성됨
* 프로그램이 직접 시스템 콜을 하기보다 API를 거쳐 접근 

## 출처
* <https://ko.wikipedia.org/wiki/%EB%A9%94%EB%AA%A8%EB%A6%AC_%EA%B4%80%EB%A6%AC_%EC%9E%A5%EC%B9%98>
* <https://m.blog.naver.com/complusblog/221204759836>