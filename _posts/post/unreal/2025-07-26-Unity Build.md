---
title: "FORCEINLINE"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---
   
## FORCEINLINE과 inline
* 일반적인 inline 키워드를 사용했을 때, 컴파일러는 해당 구문을 inline화 할지 여부를 스스로 결정한다
* 하지만 __forceline 키워드는 컴파일러의 판단여부와 무관하게 무조건 inline화 하도록 강제한다
  * __forceinline은 VS 컴파일러에서 제공하는 non-standard 매크로이며, 언리얼의 FORCEINLINE과 유사하게 작동한다

## UFUNCTION과 FORCEINLINE 동시 사용?
* UFUNCTION 매크로를 사용하는 이유는 BP에서 함수를 호출하기 위해서이다
* 그러나 C++로 작성한 함수를 BP에서 사용하기 위해서는 FORCEINLINE 매크로가 있으면 안된다

## 출처
* <https://forums.unrealengine.com/t/what-is-forceinline-macro/438373>
* <https://koreanfoodie.me/969>