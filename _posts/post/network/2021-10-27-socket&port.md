---
title: "Socket & Port"
classes: wide
categories: 
  - post
  - Network
sidebar:
  nav: "main"
author_profile: true
---

## Host
* **네트워크에 연결된 모든 종류의 장치를 Node**
* **노드 중 IP 주소(네트워크 주소)가 할당된 것들을 Host**
  * Host들끼리 데이터를 송수신한다
  * 데이터의 송수신은 Host가 실행하는 Process가 수행

## Port
* 따라서, 데이터는 Host가 아닌 데이터를 받아 수행할 Process에게까지 전달되어야 한다
* Port는 호스트 내부적으로 프로세스가 할당받는 고유의 값
  * 이 값을 통해 네트워크를 통해 주고받는 프로세스를 식별
  * Port Number라고 한다
* 데이터를 요청할 때, Request를 보내는 호스트가 어디로 되돌려 받을지 Port Number를 기재

## Socket
* 프로세스가 데이터 송수신을 위해 열어놓는 창구
* 보내는 쪽, 받는 쪽 모두 Socket이 열려 있어야 함
* Socket을 열기 위해 다음 3가지를 정의
  1. IP 주소
  2. Port Number
  3. 프로토콜

## Socket & Port
* 프로세스가 통신을 위해 포트를 할당받는데, 서버는 보통 1개만 할당 받음
  * **하나의 포트에서 여러 소켓을 열 수 있다**
  * 같은 프로토콜, 같은 IP, 같은 Port Number의 소켓을 복수 정의 가능
    * 따라서, 위의 3가지 정보로 소켓을 식별하는 것을 불가능
  * 이에 따라 하나의 프로세스는 여러개의 프로세스 요청을 처리 가능

## 출처
* <https://blog.naver.com/myca11/221389847130>