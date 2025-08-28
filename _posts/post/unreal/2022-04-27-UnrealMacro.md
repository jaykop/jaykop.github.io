---
title: "Unreal 매크로"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## 언리얼에 매크로를 사용하는 이유
* 언리얼 C++ 코드는 [Unreal Header Tool](https://www.unrealengine.com/ko/blog/unreal-property-system-reflection), UHT Preprocessor라 불리는 커스텀 [RTTI](https://jaykop.github.io/post/c++/rtti/)를 사용한다
* 이런 매크로가 달린 코드는 일반적인 C++ 매크로와 달리 더 낮은 레벨에서 작동하며 관리된다
* 이 매크로들은 RTTI, Reflection 등 작동을 위해 메타 데이터를 생성한다

## 출처
* <https://stackoverflow.com/questions/34404277/unreal-engine-calls-these-macros-is-this-normal-in-c-now>
