---
title: "Memory Layout"
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

## C/C++ 프로그램이 작동하는 순서
1. 코드 작성
    * 프로그램이 수행할 코드를 텍스트로 개발자가 작성
2. 컴파일
    * 텍스트 파일인 소스 코드가 바이너리/오브젝트 파일로 변환
    * .o 파일로 저장
    * 기계어로 변환되는 과정
        1. Lexical analysis (Scanning) 
            * 코드가 token 단위로 분리되는 과정
        2. Syntax analysis (Parsing) 언어 규칙 체크
            * 토큰이 언어 규칙에 따라 트리를 형성
            * expression이 valid한지를 체크
        3. Semantic analysis (Analyzing) 코드 체크
            * 선언된 함수나 변수를 체크
            * 호출된 함수의 파라미터 수와 return type을 체크
    * 신택스 분석과 시맨틱 분석이 실패하면 컴파일 에러를 생성
3. 링크
    * 각 모듈별로 생성된 오브젝트 파일을 연결
    * .a나 .exe 파일을 최종적으로 생성
    * Linking takes separate object files or libraries and converts them to an executable or library
4. 코드 생성
5. 실행

## 출처
* <https://www.geeksforgeeks.org/memory-layout-of-c-program/>