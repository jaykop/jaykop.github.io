---
title: "interface vs. abstract"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---

## C# interface vs. abstract
  
|인터페이스| |추상|  
|:---:|:---:|:---:|  
|C# class가 multiple interface 상속 가능| |C# class가 하나의 abstract만 상속 가능|  
|constructor 없음| |constructor 있음|  
|메서드만 지원| |필드 안에 변수 선언 가능|  
|선언만 가능| |구현 제공|  
||둘 다 객체로 선언 불가능||  
|비추상 메소드 선언 불가| |비추상 메소드 선언 가능|  
|접근 지정자는 public(변경 불가)| |함수 접근 지정자 설정 가능|  
| |상대적으로 abstract가 더 빠르게 작동| |  

## 출처
* <https://holjjack.tistory.com/41>