---
title: "Memory Hierarchy"
classes: wide
categories: 
  - post
  - os
sidebar:
  nav: "main"
author_profile: true
---
   
## 저장장치 Storage
* 최소 단위는 bit
  * 8 bits = 1 byte
  * 컴퓨터 구조상 native unit of data는 word = one or more of bytes
    * 32 bit or 64 bit
* 구조
  * 주 메모리
    * CPU가 직접 access할 수 있는 유일한 대용량 저장장치
    * Random Access (RAM) 
    * 대부분 휘발성
  * 2차 메모리
    * 주 메모리를 보완하는 비휘발성의 큰 저장 공간
    * Hard-Disk and Solid-State-Disks
* 계급
  * 상부에 있을 수록 빠르고, 비싸며, 휘발성
  * 하부에 있을 수록 느리고, 싸며, 비휘발성
  * 레지스터 -> 캐시 -> 주 메모리(램) -> SSD -> 마그네틱 디스크 -> optical disk -> 마그네틱 테이프

## 레지스터 Register
* CPU 구조의 일부
* CPU 에서 연산(계산)에 사용하는 데이터를 기억하는 소규모 기억장치
* 컴퓨터는 캐시로부터 데이터를 읽어들여 레지스터에 저장한 다음 레지스터 사이로 데이터를 전달하면서 연산을 수행

## 캐시 Cache
* 데이터나 값을 미리 복사해 놓는 임시 장소
* 캐시의 접근 시간에 비해 원래 데이터를 접근하는 시간이 오래 걸리는 경우나 값을 다시 계산하는 시간을 절약하고 싶은 경우에 사용
* 컴퓨터에는 각 계층이 있고, 사용 중인 정보는 느린 저장장치에서 빠른 저장장치로 복사되어 임시로 저장된다
* 캐시를 확인하고 거기에 찾는 정보가 있으면 사용하고,
* 없으면 하부 저장장치까지 내려가 데이터를 복사해온 뒤 사용한다 (캐시 미스)

## Direct Memory Access <-> Programmed I/O
* 고속 I/O 장치들이 주 메모리 급의 속도
* CPU를 거치지 않고 data block을 local buffer에서 곧바로 메인 메모리로 전송