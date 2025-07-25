---
title: "FString, FText, FName"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---
   
## FName
* 텍스트에 대소문자 구분을 하지 않는다

```c++
FName MyActor = FName(FString("MyActor"));
FName myActor = FName(FString("myActor"));

// return true
bool bCompare = MyActor == myActor;
```

### Name Table
* 엔진 초기화 시점 또는 새로운 문자열을 생성할 때마다 문자열을 전역 저장소에 저장한다
    * 한 번만 추가한다
    * 해시 테이블 구조

* FName 자체도 실제 문자열 데이터를 포함하지 않고, Name Table을 참조하는 index와 instance number를 가진다
    * index: Name Table에 저장된 위치
    * instance number:  동일한 문자열이라도 다른 목적으로 쓰일 수 있기에 Instance Number로 맥락을 구분한다

```c++
// 예시 코드 (실제 언리얼 엔진 코드와는 다를 수 있으나 개념 설명을 위함)
FName MyFName = FName(TEXT("PlayerCharacter"));

// MyFName 객체는 "PlayerCharacter" 문자열의 인덱스와 인스턴스 넘버를 가짐
// *MyFName을 통해 이름 테이블에서 "PlayerCharacter" 실제 문자열을 가져옴
UE_LOG(LogTemp, Warning, TEXT("My FName: %s"), *MyFName);
```

* 추가된 문자열은 엔진이 종료될 때까지 메모리에서 해제되지 않는다
    * 한 번 생성되면 값을 변경하지 않는다 (immutable)

### 언제 쓰나?
* 성능이 중요한 비교할 때 
* 고유 식별자로서 사용할 때

## FText
* 사용자에게 노출할 텍스트 표기 및 지역화 필요 시

```c++
// NSLOCTEXT(NamespaceName, KeyName, DefaultValue);
FText testText = NSLOCTEXT("A", "B", "C");
```

* 위 코드의 의미는 아래와 같다
    * **A**라는 Namespace에서 **B**라는 Key를 가진 FText 값을 찾아 사용한다
    * 해당하는 Value가 없으면 DefaultValue로 **C**를 사용한다

```c++
#define LOCTEXT_NAMESPACE "A"
FText testText1 = LOCTEXT("B", "C");
FText testText2 = LOCTEXT("D", "E");
#undef
```

* 사용할때마다 일일이 Namespace를 지정하지 않고, 위와 같이 사용할 수도 있다.

### Namespace 정의는 어떻게 하는가?
* 이건 좀 더 공부해봐야 할듯...
* ()[https://openmynotepad.tistory.com/133]

## FString
* C++에서의 std::string과 유사한 가변 문자열
    * 사용자 입력, 경로, 로그 메시지 등

```c++
// L"TestString"로 변환
FString TestString = FString(TEXT("TestString"));
```

### TEXT 매크로의 역할
* PC, 콘솔, 모바일 등에서 기본 문자 인코딩 방식이 다를 수 있다
* 이를 하나의 인코딩 방식으로 변환해주는 역할
    * UTF_16

## 출처
* <https://moonbug4.tistory.com/156>
* <https://velog.io/@dnjswns98/UE5-C-FName-FText-FString>