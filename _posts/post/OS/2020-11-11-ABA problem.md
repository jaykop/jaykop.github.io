---
title: "ABA problem"
classes: wide
categories: 
  - post
  - OS
sidebar:
  nav: "main"
author_profile: true
---
   
## ABA problem
### 과정
1. 프로세스 P_1이 shared memory로 부터 value A를 읽음
2. P_1 정지, 프로세스 P_2 가 실행
3. P_2 가 shared memory 값 A를 B로 변경했다가, 다시 A로 변경하고 정지, 
4. P_1 는 shared memory 값이 변경된 적이 없다고 판단하고 실행을 다시 시작
* P_1 이 다시 실행하지만, shared memory에 숨겨진 변경사항이 결과값을 다르게 만들어내거나 다른 behavior가 발생할 수 있음

### Solutions
* 기존 노드를 지우지 않는다(재사용하지 않는다). 
  * 메모리 릭이 발생할 수 있음
  * 삭제가 거의 일어나지 않은 상황이나 프로그램 종료시에만 이 방법을 사용
* 삭제된 노드들이 queue로 보내져 일정 시간 동안 기다린다. 
  * ABA 문제가 발생할 확률은 최소화 시킬 수 있음. 
  * 지워지자마자 재사용되는 것이 아니기 때문에 새로운 노드가 생성되거나 삽입될 때 이 노드를 사용하지 않을 것
