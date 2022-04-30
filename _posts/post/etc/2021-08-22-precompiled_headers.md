---
title: "Precompiled Header"
classes: wide
categories: 
  - post
  - etc.
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## Precompiled Header(미리 컴파일된 헤더)
* 헤더를 미리 컴파일 해두는 것
* 자주 변경되지 않는 긴소스를 미리 컴파일하여 컴파일 결과를 별도의 파일에 저장
* 다시 똑같은 헤더를 컴파일할 경우 해당 파일을 처음부터 컴파일하지 않고, 미리 컴파일된 헤더 파일을 사용해 컴파일 속도를 월등히 향상

## 사용법

![post_thumbnail](/assets/images/stdafx.jfif)
* **Standard Application Frameworks (stdafx)**
* 각 stdafx.h와 stdafx.cpp에 대해 위 그림과 같이 설정

```c++
// stdafx.h
#pragma once 
#include "something_big_and_long.h"

// stdafx.cpp
#include "stdafx.h" // precompiled header를 사용하는 모든 cpp 파일에 추가
```

## 출처
* <https://noirstar.tistory.com/12>
* <https://en.wikipedia.org/wiki/Precompiled_header>
* <https://docs.microsoft.com/ko-kr/cpp/build/creating-precompiled-header-files?view=msvc-160>