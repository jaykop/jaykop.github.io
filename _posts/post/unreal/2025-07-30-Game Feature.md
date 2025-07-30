---
title: "Unreal Game Feature"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## Game Feature

![post_thumbnail](/assets/images/GameFeature/GameFeature_1.png)

* 모듈형 게임플레이 기능 도입
* 런타임 중에 콘텐츠 활성화 및 비활성화 가능
* 라이브 서비스 중인 게임에서도 활용 가능
	* 일회성 이벤트 전용 피쳐를 활성화 또는 비활성화하는 목적
* 플러그인 Game Feature와 Modular Gameplay를 모두 활성화해야 사용 가능

![post_thumbnail](/assets/images/GameFeature/GameFeature_2.png)
	
* 말 그대로 게임의 기능 단위로 모듈화가 가능
* 기본적으로 각 Game Feature는 상호 의존성이 없다. 즉, 서로 참조하지 않는다
	* 물론 Dependencies 세팅을 통해 참조 구조를 세팅할 수도 있다
	* 다만, 이 경우에 참조하려는 Game Feature가 Core Game으로 이전되어야 하는 게 아닐지 고민해보는 게 좋다
	* 여러 Game Feature가 특정 Game Feature를 참조한다면, 그 Game Feature는 Core Game에 있는 게 더 나을지도

![post_thumbnail](/assets/images/GameFeature/GameFeature_3.png)

### Add Data Registry / Add Data Registry Source
* **Data Registry**
	* 언리얼 엔진에서 정적이고 자주 접근되는 대량의 게임 데이터를 관리하는 캐싱 및 접근 시스템
	* 개념은 이렇다는데 이것도 실사용해본 적이 없어서 좀 더 알아봐야 할듯..

### Add Cheats
* Cheat Manager에 Extension을 추가해 사용
* 피쳐 단위로 치트를 활성화 및 비활성화 하여 관리할 수 있다
* 사용을 위해 UCheatManagerExtension 클래스를 상속한 클래스가 필요

### Add Components

![post_thumbnail](/assets/images/GameFeature/GameFeature_4.png)

* 특정 클래스인 모든 Actor에 Component를 추가할 수 있다
	* Component Manager에서 특정 클래스를 정의한다  

## Custom Game Feature Action
* UGameFeatureAction 클래스를 상속해 커스텀한 Game Feature 구현 가능
	* UGameFeatureAction_AddComponents 클래스를 BP로 상속하는 것도 한 방법

## 출처
* <https://www.youtube.com/watch?v=-DLeHXrGPrM>
* <https://dev.epicgames.com/documentation/ko-kr/unreal-engine/data-registries-in-unreal-engine#integration-with-game-features>
* <https://dev.epicgames.com/documentation/ko-kr/unreal-engine/quick-start-guide-for-unreal-engine-data-registries>