---
title: "Stack Overflow"
classes: wide
categories: 
  - post
  - etc
sidebar:
  nav: "main"
author_profile: true
---

## 발생 이유
* **Stack 메모리의 크기는 스레드가 초기화될 때 고정된 크기로 결정**
  * 사용량을 초과하여 사용한다면 소프트웨어는 undefined behavior 야기
* Stack 영역의 메모리가 지정된 범위를 넘어갈 때 발생
  * 한 함수에서 너무 큰 지역 변수를 선언
  * 함수를 재귀적으로 무한정 호출하게 되면 발생

## 해결 방법
* 컴파일러 옵션에서 stack의 영역을 늘려줌
* 함수에서 사용하는 지역 변수의 크기를 줄임
* 지역 변수를 전역변수로 수정
* 재귀함수가 안정적으로 종료할 수 있도록 함

# 출처  
* <https://gammabeta.tistory.com/736>
* <https://keepdev.tistory.com/21>
* <https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=neos_rtos&logNo=220096325801>