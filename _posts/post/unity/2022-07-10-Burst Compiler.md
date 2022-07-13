---
title: "Burst"
classes: wide
categories: 
  - post
  - Unity
sidebar:
  nav: "main"
author_profile: true
---

## 개요
* LLVM을 사용하여 IL을 고도로 최적화된 네이티브 코드로 변환하는 컴파일러

### LLVM 
![image](/assets/images/다운로드 (7).png)
* Low Level Virual Machine 저수준 가상 머신
* 모듈화된, 재사용 가능한 컴파일러, 툴체인 기술의 집합체라고 한다
  * 가상 머신과는 상관이 없다
* **Intermediate / Binary 코드를 생성 및 최적화하는 데 사용되는 라이브러리**
* SIMD 기능 사용
* 프론트 엔드와 백엔드로 구분

#### SIMD Single Instruction Multiple Data 
* 하나의 명령어로 여러 개의 데이터를 한번에 처리
  * Vertorization
* 일반적으로는 SISD 
  * Single Instruction Single Data
* 한번에 실행할 수 있는 대역폭이 정해져 있음

#### 프론트엔드

![image](/assets/images/다운로드 (1).jfif)

* 앱을 만들기 위해 사용하는 언어로 작성된 부분을 읽고 파싱
* Intermediate Representation을 생성
  * IL이라고 생각하면 될 듯?
* Clang 클랭을 이용

#### 백엔드
* 앱을 컴퓨터 코드로 변환
* 생성된 IR을 LLVM 컴파일러를 통해 타겟에 맞는 기계어로 변환
  * x86, ARM 등

### Mono
* 여러 플랫폼에서 C# 코드를 컴파일하고 .Net 프로그램을 실행하도록 지원
  * 유니티가 멀티 플랫폼을 지원하며 모바일 시장에서 성장할 수 있었던 이유
* C# 스크립트를 CLRVM이 실행하고 관리할 수 있도록 컴파일
* 네이티브에 CLR이 포함되면서 실행 속도 저하
* 이를 타개하기 위한 새로운 컴파일러가 버스트

## 다른 기능들
* ECS - 메모리 설계 최적화를 위한 기능
* Job System - 멀티 스레틷ㅇ을 극한으로 사용하기 위한 기능
* IL2CPP - 성능개선의 여지를 주면서 시작한 것이 버스트

## 출처
* <https://docs.unity3d.com/kr/2019.4/Manual/com.unity.burst.html>
* <https://zeddios.tistory.com/1175>
* <https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=canny708&logNo=221557851696>
* <https://everyday-devup.tistory.com/70>