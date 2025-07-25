---
title: "Transient"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---
   
## Transient
* 언리얼 오브젝트는 직렬화 기능으로 오브젝트의 UPROPERTY 매크로로 속성을 저장 및 로딩할 수 있다
  * 이를 테면, CurrentHP와 같은 값은 게임을 시작할 때마다 변경되므로 이 값을 저장 또는 로딩하는 것은 디스크 낭비다
  * 이런 속성에 Transient 키워드를 추가해 직렬화 대상에서 제외할 수 있다

### Transient 플래그는 Instance에만 해당한다
* CDO에서는 Transient 플래그가 있더라도 Serialize 된다
  * Instance들은 로드할 때마다 CDO의 값을 참조해 초기화한다
  * EditAnywhere 플래그를 동반하더라도, Instance에서의 값들은 휘발되고 CDO의 값들만 저장된다

## 출처
* <https://en.wikipedia.org/wiki/Unity_build>
* <https://www.slideshare.net/slideshow/ndc2010-unity-build/4335591>