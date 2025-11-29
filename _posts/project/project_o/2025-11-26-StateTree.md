---
title: "[DevNote] State Tree"
classes: wide
categories: 
  - project
  - project_o
sidebar:
  nav: "main"
author_profile: true
---

## StateTree를 쓰면서 명심해야 할 점

1. StateTree 쓰지 마라
2. 뭐가 안되면 엔진을 껐다 켜라
3. 뭐가 안되면 지웠다 다시 세팅해봐라
4. 1, 2, 3 다 아니라면 로직 이슈 혹은 세팅 문제다

### 적용 사례와 소감

Behavior Tree를 대체한다고 호들갑을 떨며 홍보해대는 StateTree를 써봤다.
마우스 클릭으로 적 캐릭터를 클릭하거나 지표면을 클릭하면 플레이어 캐릭터가 공격/이동해야 했다.
Behavior Tree를 쓸까 고민했는데, 지금 아니면 언제 StateTree 써보겠냐는 생각에 그냥 내 맘대로 결정하고 적용해봤다.

StartLogic, StopLogic, PauseLogic, ResumeLogic 등 헬퍼 함수도 있어 StateTree Execution 컨트롤은 용이했다.
플로우가 한눈에 들어오는 편이며, 전용 디버거도 있고, 특정 조건이나 State를 Disable 시킬 수도 있어서 BT보다는 디버깅하기 훨씬 좋았다.
다만 조건문 확인이나 작동 플로우를 이해하는 데 직관성이 조금 떨어졌고, 이전 데이터 캐싱 또는 Live Coding 후 리프레시가 안되는 버그가 있어서 꽤 불편했다.
Break Enter 혹은 End도 있던데 이건 작동을 안하는 거 같았다.

### 버그

처음에는 튜토리얼을 따라서 BlueprintBase의 Task와 Condition, Evaluator를 만들어서 적용해보았다.
그런데 Tick에 트리거가 되지 않았다.
"BleurprintBase는 Tick 타이밍이 약간 다른가?" 라는 생각에 Unreal 기본으로 제공하는 StateTree Task를 보고 태스크를 만들어 테스트하니 Tick이 돌았다. 그래서 Condition과 Evaluator를 모두 struct로 다시 만들었다.

그런데 이렇게 만든 것들도 의도대로 작동하지 않았다.
구글링도 해보고 AI한테도 물어보고 코드도 뜯어보고 했는데도 이유를 못 찾았다가, 실수로 State에 할당한 Task를 지워버려서 다시 만들어 세팅해 돌렸더니 그제서야 제대로 작동했다.
내 워크데이 하루가 그렇게 통째로 날아갔다...
또는 엔진을 겄다 켜면 작동하는 경우도 있었다.

이 외의 내 의도대로 작동하지 않았던 경우는 전부 로직 이슈거나 세팅 이슈였다.
로직을 짤 때 염두에 두어야 할 것이 내 로직 자체의 오류뿐만이 아닌 다른 변수가 있다는 건 굉장히 피곤한 일이다.
그래서 이 시점에 StateTree를 굳이 써야 하나? 라고 누가 묻는다면 나는 아니라고 답할 것이다.
