---
title: "컴포넌트 베이스 게임 엔진"
classes: wide
categories: 
  - blog
  - etc
sidebar:
  nav: "main"
author_profile: true
---

## 왜 컴포넌트를 사용하는가?
- **확장성** - 기존의 컴포넌트를 기반으로 새로운 행동으로 확장하기에 용이
- **재활용성** - 다양한, 다른 상황들에 대해 재사용이 가능
- **독립성** − 컴포넌트는 최대한 상호 독립적으로 작동하도록 디자인 됨
- **교체성**− 컴포넌트는 쉽게 다른 컴포넌트로 대체가 가능
- **고유 시스템에 의존적** − 컴포넌트들은 종속되어 있는 각 시스템에 의해서만 업데이트됨
  
## 작동 원리
- 각 컴포넌트는 게임 스테이트에 관련된 데이터를 가지고 있음
- 엔티티(게임 오브젝트)는 여러 컴포넌트를 가지고 있음
- 시스템은 각자 업데이트/작동시킬 컴포넌트를 가지고 있고 이를 실행
   

## 출처
* <https://www.tutorialspoint.com/software_architecture_design/component_based_architecture.htm>
