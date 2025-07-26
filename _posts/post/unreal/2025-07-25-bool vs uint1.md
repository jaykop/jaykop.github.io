---
title: "Unity Build"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---
   
## Bit field 선언

```c++
uint8 bBlockInput:1;
uint8 bCollideWhenPlacing:1;
uint8 bFindCameraComponentWhenViewTarget:1;
uint8 bGenerateOverlapEventsDuringLevelStreaming:1;
uint8 bIgnoresOriginShifting:1;
uint8 bEnableAutoLODGeneration:1;
uint8 bIsEditorOnlyActor:1;
uint8 bActorSeamlessTraveled:1;
```

* 위와 같이 선언하고서 bool과 같은 로직으로 사용하는 경우가 있다
  * 이를 피트 필드 선언이라고 한다
* 위의 코드를 bool 타입으로 8개를 선언하면 1byte * 8 = 8 bytes (64 bit)의 용량이 필요
  * 비트 필드로 선언하면, 공간을 연속하는 비트 필드가 공유하여 사용 가능
  * **1 byte 안에 8개의 bool 변수를 모두 담을 수 있다**
* 즉, 위의 코드에서 선언된 변수의 크기는 각각 1bit이며, 모두 합해 1byte(8bit)이다

## 특징
* 위와 같이 메모리 공유를 통해 사용 영역을 줄이는 데 장점이 있다
* 열거형을 포함한 정수 형식의 타입으로 선언이 가능하다
  * 열거형의 경우는, 멤버 개수에 따라 비트 수를 다르게 세팅해야 한다
* **비트 필드의 주소는 탐색할 수 없다**
* **선언과 동시에 초기화하는 것이 불가능하다**
* non const 참조 변수를 비트 필드로 초기화하는 것은 불가능

## 출처
* <https://velog.io/@hon454/bool-%EB%8C%80%EC%8B%A0%EC%97%90-uint8uint16uint32-%EB%B3%80%EC%88%98%EB%AA%851%EC%9D%84-%EC%93%B0%EB%8A%94-%EC%9D%B4%EC%9C%A0>
* <https://learn.microsoft.com/ko-kr/cpp/cpp/cpp-bit-fields?view=msvc-160>