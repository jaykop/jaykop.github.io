---
title: "UFUNCTION Overload"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## UFUNCTION Overload
* UFUNCTION 함수는 Overload 할 수 없다
	* 만약 Overload 필요하다면 UFUNCTION 키워드를 제거하고 사용해야 한다
* UHT가 Unreal Function을 등록하기 위해서 Iterate 할 때, 헤더 파서가 확인하는 것은 함수의 이름 뿐
	* 인자의 타입이나 개수는 체크하지 않는다

## BlueprintNativeEvent
### BlueprintCallable
* C++로 작성된 함수를 블루프린트 그래프에서 호출 가능하도록 하는 키워드
* 당연히 정의된 함수는 블루프린트 그래프에서 덮어씌우거나 변형이 불가능

### BlueprintImplementableEvent
* 함수 선언만 C++ 헤더파일에서 하고 구현부는 블루프린트 그래프에서 한다

### BlueprintNativeEvent
* 기본 로직은 C++ 상에서 정의할 수 있으나, 블루프린트에서 이 구현부 로직을 재정의할 수 있다
* C++ 코드에서 뒷 부분에 _Implementation이라는 postfix가 붙는다

## 출처
* <https://forums.unrealengine.com/t/why-does-function-declaration-with-the-same-name-with-different-number-of-argument-cause-a-build-error/283730>
* <https://forums.unrealengine.com/t/overloading-a-ufunction/337808>