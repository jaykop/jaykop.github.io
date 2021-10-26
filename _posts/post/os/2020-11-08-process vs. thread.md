---
title: "Process vs. Thread"
classes: wide
categories: 
  - post
  - OS
sidebar:
  nav: "main"
author_profile: true
---
   
## 프로세스  vs. 쓰레드
* 프로세스
  * 실행되고 있는 한 개의 프로그램
  * CPU는 프로세스를 실행하기 위해 적절한 양의 자원을 할당하고, 운영체제의 성능에 좌우
* 쓰레드
  * 프로세스 내부에서 자원을 할당받아 실행되는 독립적인 작업 단위
  * 스레드는 각자의 스택 메모리 영역을 가짐
  * 동일한 프로세스 내의 다른 스레드들과 전역 메모리를 공유
  * CPU로부터 새로운 자원을 할당받지 않아도 되기 때문에 프로세스보다 실행 속도가 빠름
