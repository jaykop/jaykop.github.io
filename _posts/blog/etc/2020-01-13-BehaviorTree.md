---
title: "행동트리(Behavior Tree)"
classes: wide
categories: 
  - blog
  - etc
---
   

행동트리 Behavior tree
도식화했을 때 직관적이고 쉽게 디자인할 수 있음
런타임에서 테스트 또는 디버깅하기가 까다로움
model of plan execution 행동 패턴을 계획한 대로 시행하는 모델
노드의 종류
Control Flow 
여러 개의 노드를 가지고 있는 컨테이너
selector - 노드 중 하나만 참이어도 return true
sequence - 모든 노드가 참이어야 return true
Decorator (condition) 
액션 노드들을 꾸며주는 노드
repeater - 해당 노드의 실행을 반복
succeeder - 항상 return true
inverter - 값의 역을 return
Action 
Behavior tree 노드 중 리프 노드
실행 결과에 따라 success, failure, running 중 하나를 리턴

  
---  
출처:   
* https://quinoa.tistory.com/31
