---
title: "BlueprintPure와 const"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---
   
## BlueprintPure
* **함수를 블루프린트에 노출시킬 때, 이 함수가 OwnerObject에 아무 영향을 주지 않는 것을 보장하는 키워드**
* Gettor의 성격을 가진다 

```c++
UFUNCTION(BlueprintPure)
void Func();

UFUNCTION(BlueprintCallable)
void Func() const;
```

* 즉, BlueprintPure로 함수를 선언한다는 것은 이미 이 함수를 상수화했다는 것
  * UTH의 판단에 **const 키워드가 redundant**하면 붙일 필요가 없다

### Conflating BlueprintPure and C++'s const keyword is a little dubious because C++ const does not imply purity. const functions may modify mutable members and global state

* C++에서 mutable로 선언된 변수는 const 함수라도 변경될 수 있으므로 단순 대입할 수 잇는 관계는 아니라고 한다

## 출처
* <https://en.wikipedia.org/wiki/Unity_build>
* <https://www.slideshare.net/slideshow/ndc2010-unity-build/4335591>