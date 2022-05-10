---
title: "CAS Algorithm & ABA problem"
classes: wide
categories: 
  - post
  - OS
sidebar:
  nav: "main"
author_profile: true
---
   
## lock-base 코드의 몇가지 문제점
* lock 순서를 제대로 관리하지 않으면 데드락의 가능성
* priority inversion - 낮은 우선 순위의 스레드가 진행되기 위해 높은 순위의 스레드 락을 요구하는 경우
* atomic한 operation이 오래 걸리는 경우, 다른 스레드들은 기다려야 함

## CAS Algorithm (Compare and Swap)
* 논블로킹으로 atomic한 operation의 지연을 보완하기 위한 방법
* 주소값을 확인해서 tick마다 같은 스레드가 계속 사용 중인지, 다른 스레드로 변환이 발생했는지 확인
* **이 방법은 atomic한 작업임을 전제로 함**

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

## CAS의 한계?
* location의 값 자체가 바뀌지 않았더라도, 사용됐을 가능성
  * ABA Problem
* 같은 메모리 주소가 반환되었다가 재할당되어 사용되는 경우
* Banker Algorithm 과 같이 가용 가능한 메모리 큐로부터 순서대로 메모리를 할당받아 사용하면 상대적으로 더 안전하게 사용 가능

## ABA problem
### 과정
1. 프로세스 P_1이 shared memory로 부터 value A를 읽음
2. P_1 정지, 프로세스 P_2 가 실행
3. P_2 가 shared memory 값 A를 B로 변경했다가, 다시 A로 변경하고 정지, 
4. P_1 는 shared memory 값이 변경된 적이 없다고 판단하고 실행을 다시 시작
* P_1 이 다시 실행하지만, shared memory에 숨겨진 변경사항이 결과값을 다르게 만들어내거나 다른 behavior가 발생할 수 있음

### Solutions
1. 기존 노드를 지우지 않는다(재사용하지 않는다)
  * 메모리 릭이 발생할 수 있음
  * 삭제가 거의 일어나지 않은 상황이나 프로그램 종료시에만 이 방법을 사용
2. 삭제된 노드를 queue로 보내고 일정 시간 동안 기다린 후 반환한다
  * ABA 문제가 발생할 확률은 최소화 시킬 수 있음. 
  * 지워지자마자 재사용되는 것이 아니기 때문에 새로운 노드가 생성되거나 삽입될 때 이 노드를 사용하지 않을 것