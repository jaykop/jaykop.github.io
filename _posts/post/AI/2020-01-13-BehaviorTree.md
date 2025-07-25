---
title: "행동트리(Behavior Tree)"
classes: wide
categories: 
  - post
  - A.I.
sidebar:
  nav: "main"
author_profile: true
---

## 행동트리(Behavior Tree)
* 도식화했을 때 직관적이고 쉽게 디자인할 수 있음  
* 런타임에서 테스트 또는 디버깅하기가 까다로움  
* 행동 패턴을 계획한 대로 시행하는 모델(model of plan execution)  
* FSM, HFSM을 구현할 때 상태가 많아지면 유지보수 및 가독성 면에서 사용성이 떨어지게 되는 단점을 보완했다고 한다
  * ...잘 모르겠는데?

## 노드의 종류
### Control Flow 
- 여러 개의 노드를 가지고 있는 컨테이너
- Selector 
  - 노드 중 하나만 참이어도 return true
- Sequence 
  - 모든 노드가 참이어야 return true

### Decorator (condition)
- 액션 노드들을 꾸며주는 노드
- Repeater
   - 해당 노드의 실행을 반복
- Succeeder
   - 항상 return true
- Inverter
   - 값의 역을 return

### Action (leaf)
- Behavior tree 노드 중 리프 노드
- 실행 결과에 따라 success, failure, running 중 하나를 결과로 리턴
  - running인 경우에는 실행 중인 Action이 종료하지 않았다는 뜻