---
title: "CAS Algorithm"
classes: wide
categories: 
  - post
  - OS
sidebar:
  nav: "main"
author_profile: true
---
   
## CAS Algorithm
* lock-base 코드의 몇가지 문제점
  * lock 순서를 제대로 관리하지 않으면 데드락의 가능성
  * priority inversion - 낮은 우선 순위의 스레드가 진행되기 위해 높은 순위의 스레드 락을 요구하는 경우
  * atomic한 operation이 오래 걸리는 경우, 다른 스레드들은 기다려야 함

```c++
bool CAS( location, expected, new )
{
  // CAS is atomic and executes
  // 아무도 location의 값을 바꾸지 않았음 or 예상한 location의 값으로 유지되어 있음
  if ( location == expected )
  {
    return true;
  } 
  else 
  { 
    // 다른 스레드가 location의 값을 바꿨음, 타겟을 변경함
    expected = location;
    return false;
  }
}
```