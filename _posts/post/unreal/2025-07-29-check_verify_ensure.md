---
title: "check, verify, ensure"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## check 사용 케이스
* DO_CHECK = 1인 경우 
  * 매크로 내부를 실행
  * 데스트 실패 시 중단점 체크 + 크래시 리포터
* DO_CHECK = 0인 경우 
  * 매크로를 무시한다

### 1. 필수적인 내용의 코드 실행 시

```c++
UGameInstance* GameInstance = GetGameInstance();
check(GameInstance);
```

* 위의 경우 GameInstance가 없으면 코드 진행이 불가능
* 코드 플로우 상 GameInstance가 nullptr일 수 없는 경우

### 2. 레퍼런스를 반환하는 xxxChecked() 함수

```c++
FORCEINLINE UObject& GetValueChecked(int32 Index) const
{
  const UObject* Found = Data[Index];
  checkf(Found, TEXT("Tried to get a Value"));
  return *Found;
}
```

## verify 사용 케이스
* DO_CHECK = 1인 경우 
  * 매크로 내부를 실행
  * 데스트 실패 시 중단점 체크 + 크래시 리포터
* DO_CHECK = 0인 경우 
  * 매크로를 실행한다
  * 테스트 실패 시에는 아무것도 하지 않는다

### 1. 변수 할당과 검사를 동시에 할 때

```c++
verify(UGameInstance* GameInstance = GetGameInstance());
```

### 2. 함수 실행과 검사를 동시에 할 때

```c++
verify(WorldContext && CheckCondition(WorldContext));
```

## ensure 사용 케이스
* DO_CHECK = 1인 경우 
  * 매크로 내부를 실행
  * 데스트 실패 시 중단점 체크
* DO_CHECK = 0인 경우 
  * 매크로를 실행한다
  * 테스트 실패 시에는 아무것도 하지 않는다

### 1. 함수 실행과 검사를 동시에 할 때

```c++
ensure(CheckCondition(WorldContext));
```

* 위의 사례는 verify와 겹치지만, 테스트 실패 시 크래시 리포턱를 실행하지 않는다는 차이가 있다
* **비정상 종료를 시키지 않는 경우**에, ensure를 사용한다

### 2. robust if statement

```c++
if (ensure(condition))
{
  // always execute this code
}
else
{
  // must not happen
  // and cover this case
}
```

* 테스트가 실패할 일이 없어야 하지만, 혹시 모를 상황을 체크하기 위한 목적