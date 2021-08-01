---
title: "C/C++ Memory Layout"
classes: wide
categories: 
  - blog
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## C/C++ 메모리 레이아웃
![post_thumbnail](/assets/images/memoryLayoutC.jpg)
1. **Text segment**
    * 기계어로 변환된 실행코드가 메모리 or obj에 저장
2. **Data segment**
    * 초기화된 전역변수(global) 및 정적변수(static)
3. **Block Started by Symbol(BSS) segment**
    * 비초기화된 전역변수 및 정적변수
    * OS 커널에서 산술적 값 0으로 초기화 혹은 explicit 초기화 없이 유지 
4. **Stack**
    * 지역변수 및 매개변수
    * 스코프 벗어나면 해제
5. **Heap**
    * 동적할당 메모리

## 출처
* <https://www.geeksforgeeks.org/memory-layout-of-c-program/>