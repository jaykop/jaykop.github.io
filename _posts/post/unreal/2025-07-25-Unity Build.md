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
   
## Unity Build
* C / C++의 프로젝트를 컴파일 할 때, 여러 translation unit을 하나로 뭉쳐서 빌드하는 방식
  * Unity 엔진과는 전혀 무관하다

```c
// file_a.cc
#include "header.h"

// content of source file A ...
```

```c
// file_b.cc
#include "header.h"

// content of source file B ...
```

* 위의 두 유닛이 같은 프로젝트에 있다면, 컴파일러에 의해 header.h 한번의 빌드 시에 2번 처리 된다

```c
// jumbo_file.cc
#include "file_a.cc"
#include "file_b.cc"
```

* 위와 같이 묶어놓으면 jumbo_file.cc를 컴파일할 때, header.h는 1번만 처리된다

### 장점
* 이 방법을 통해 컴파일 시, 중복된 헤더 파일의 파싱을 줄일 수 있다
* 묶음으로 처리하기 때문에 생성되는 오브젝트 파일의 수도 줄일 수 있다
* 또한, 다른 소스 파일에 여러 번 정의된 심볼의 재정의를 식별하고 경고 또는 오류를 뱉을 수 있다

### 단점
* Translation Unit의 사이즈가 커지기 때문에, 메모리 사용량이 증가한다
  *  이는 병렬 빌드 구조에서 더 크게 작용한다
* 변경된 일부 부분만 다시 빌드하기 어렵다
* 단일 유닛에서 사용할 것으로 전제하고 선언한, 그러나 동일 이름의 정적 심볼 및 익명 네임스페이스 등의 충돌이 발생할 수 있다
  * 언리얼에서는 묶음 단위가 변경되는지, 잘 작동하던 코드가 에러가 발생하는 이유가 이것이 아닐까 싶다

### cpp / cxx / cc
* 관습적인 차이만 있다고 한다
* h / hpp의 차이도 마찬가지 ㅋㅋ

## 출처
* <https://en.wikipedia.org/wiki/Unity_build>
* <https://www.slideshare.net/slideshow/ndc2010-unity-build/4335591>