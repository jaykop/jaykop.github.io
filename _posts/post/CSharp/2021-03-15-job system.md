---
title: "Job System"
classes: wide
categories: 
  - blog
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## Job System이란?
* 스레드를 대신해 태스크를 만들어 멀티스레드 코드를 관리
* 여러 코어에 걸쳐 워커 스레드 그룹을 관리
* 일반적으로 컨텍스트 변경을 방지하기 위해 코어당 하나의 워커 스레드가 있으나 사용할 코어 예약도 가능
* 잡 대기열에 순서대로 잡을 배치하여 실행

## 잡이란?
* 단일 작업을 수행하는 작업 단위

## 안전 시스템
* 데드락 방지를 위해 데이터의 레퍼런스가 아닌 복사본을 이용해 처리
* bittable 데이터 타입에만 엑세스 가능
* memcopy를 이용해 데이터를 복사
  
## NativeContainer 
* 네이티브 메모리에 비교적 안전한 C# Wrapper 를 제공하여 관리되는 값 형식
* NavtiveContainer를 사용하면 Job을 통해 사본으로 작업하는 대신 주 스레드와 공유 된 데이터에 접근
* 기본 제공되는 타입은 NativeArray<T>

## 유니티의 Entity Component System
* NativeList - List<T> 와 유사
* NativeHashMap - Dictinonary<K, T>와 유사
* NativeMultiHashMap - Dictinonary<K, T>와 유사하지만 동일한 Key를 등록할 수 있음
* NativeQueue - Queue<T>와 유사합니다. (FIFO 선입선출 구조)

## 출처
* <https://redforce01.tistory.com/239>
* <https://redforce01.tistory.com/240?category=721608>
* <https://zprooo915.tistory.com/66>
* <https://mrbinggrae.tistory.com/223?category=882742>