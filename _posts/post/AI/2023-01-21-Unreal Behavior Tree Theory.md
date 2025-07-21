---
title: "Behavior Tree Theory"
classes: wide
categories: 
  - post
  - Unreal
  - A.I.
sidebar:
  nav: "main"
author_profile: true
---
   
## Behavior Tree
행동 트리는 AI가 현재 환경에서 어떤 행동을 할 지 결정하는 분기를 도식화한 것이다. 이는 각 개별 노드의 실제 작동 원리를 이해할 필요 없이, AI의 행동 플로우를 시각적으로 제공한다.

![post_thumbnail](/assets/images/e6774420-5725-409e-a68f-9ad5b757f241.png)

### Behavior Tree의 작동 플로우?
각 노드의 위치는 BT가 진행하는 순서를 내포한다. 위에서 아래로 내려오고 왼쪽에서 오른쪽으로 진행한다. 

## Tasks
### Task Nodes
Task는 더 이상 하위 노드를 가질 수 없는 최하위 노드다. 

### Task Statuses
각 Task Node는 Succeeded, Failed, InProgress의 3개 상태 중 하나를 반드시 반환한다. 

Suceeded와 Failed는 다음 노드로 이동하여 진행하도록 하지만, InProgress는 BT의 진행을 이 노드에서 멈추게 한다. 이 경우 다른 방법으로 노드의 Status를 변경해 BT가 다시 진행할 수 있도록 풀어줘야 한다. 

## Composites
일반적인 BT 구조상 Root Node는 Composite이다.  여러 Task Node를 순서대로 실행할 수 있는 분기점 역할을 한다. Task Node처럼 특정 Action을 수행하지는 않는다. 다만 하위 Task Node의 Status에 따라 BT 흐름을 통제한다.

### Selector
하위 Task Node 중 Succeeded를 반환하면 그 즉시 Succeeded를 반환하고, 그 이후에 Task Node가 있더라도 더 이상 진행하지 않는다. 즉, 여러 하위 Task Node를 거치면서 Failed면 진행하고, Succeeded면 멈춘다.

여러 선택지 중 하나를 실행할 때 사용한다.

### Sequence
하위 Task Node 중 Failed를 반환하면 그 즉시 Failed를 반환하고, 그 이후에 Task Node가 있더라도 더 이상 진행하지 않는다. 즉, 여러 하위 Task Node를 거치면서 Succeeded면 진행하고, Failed면 멈춘다.

일련의 Action이 모두 성공해야 할 때 사용한다.

### Simple Parallel

![post_thumbnail](/assets/images/bef0432b-a85e-4cc7-87f5-9eb80b79cda7.png)
![post_thumbnail](/assets/images/94d461ce-0fe3-4410-b276-82c11db10c1a.png)

메인 Task Node 하나를 서브트리와 병행 실행시킬 수 있다.  좌측 메인 Task Node가 실행을 완료하면 Config에 따라 우측의 서브 트리도 강제로 종료할 지, 아니면 완료할 때까지 대기할 지를 결정한다.

### 왜 단순 반복 Composite은 없을까?

![post_thumbnail](/assets/images/7a18cdcc-cfac-465c-bd94-e9f14c8df2b9.png)

Decorator 중 Force Success 노드를 하위 Task Node의 Decorator로 추가하고 상위 Composite을 Sequence로 하면 가능할 것 같긴 하다.

## 출처
* <https://dev.epicgames.com/community/learning/courses/67R/unreal-engine-introduction-to-ai-with-blueprints/qzZ2/behavior-tree-theory>
* <https://docs.unrealengine.com/5.1/ko/unreal-engine-behavior-tree-node-reference-composites/>