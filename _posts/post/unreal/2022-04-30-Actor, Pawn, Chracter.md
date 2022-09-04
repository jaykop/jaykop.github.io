---
title: "Unreal Framework"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---
  
## Unreal vs. Unity

|카테코리|유니티|언리얼|
|:--|:--|:--|
|게임 오브젝트|Component<br>Game Object<br>Prefab|Component<br>Actor/Pawn<br>Blueprint class|
|메시|Mesh<br>Skinned Mesh|Static Mesh<br>Skeletal Mesh|
|머테리얼|Shader<br>Material|Material/Material Editor<br>Material Instance|
|이펙트|Particel Effect<br>Shuriken|Effect/Particle/Cascade<br>Cascade|
|UI|UI|UMG()|
|언어|C#|C++|
|물리|Raycast<br>Rigid Body|Line Tracing/Shape Trace<br>Collision/Physics|

### Unity Component System
![post_thumbnail](/assets/images/{107C035B-1B4D-4646-883B-4D2F363FF60E}.png)
* Unity에서의 GameObject는 Component의 집합이다
* Empty GameObject가 Transform Component를 가진 채로 존재하며, 사용자는 여기에 Component를 추가 및 제거하며 직접 디자인할 수 있다
* 사용자 정의의 코드는 Monobehavior에서 상속하여 커스텀 Component로서 GameObject에 추가된다

### Unreal Component System
![post_thumbnail](/assets/images/{8F8A3F52-0B85-4DFE-BEA8-4E51E94D0D8B}.png)
* Unreal은 Actor 클래스를 베이스로 상속을 거치며 사용자의 코드를 추가하는 식으로 디자인한다
* Actor 클래스에서 상속된 커스텀 GameObject 클래스에 필요한 Component들이 멤버 변수로서 정의된다
* Actor 클래스는 Unity의 Transform과 유사한 SceneComponent를 기본적으로 가진다
  * SceneComponent는 RootComponent라는 이름으로 정의되어 있다
* 접두사 A를 가진 클래스는 월드에 스폰할 수 있다
* 접두사 U를 가진 클래스는 스폰할 수 없는 컴포넌트로서 Actor에 포함되어야 한다

## 주요 클래스

### Actor
* Actor란 언리엘 엔진의 레벨에서 배치할 수 있는 게임 오브젝트
* 레벨에 배치할 수 있는 모든 오브젝트
* AActor
  * Actor
* Component를 추가해 액터를 디자인할 수 있다

### Pawn
* 플레이어 혹은 A.I.에 의해 제어되는 액터
* Pawn을 생성하면 APawn 클래스로부터 상속되고, APawn은 Actor의 Base Class인 AActor로부터 상속된다.
  * AActor
    * Actor
    * APawn
      * Pawn

### Chatacter
* 플레이어 컨트롤에 의해 제어되는 Pawn
* 스켈레탈 메시를 포함한 휴머노이드 형, 캡슐 콜리전, CharacterMovementComponennt 등을 포함
* AActor
    * Actor
    * APawn
      * Pawn
      * Character

### Controller
* Player Controller
  * 플레이어의 입력값을 Pawn으로 전달
* AI Controller
* 캐릭터의 Movement를 Wrapping해서 컨트롤하기 쉽도록 해주는 컴포넌트

### Game Mode
* 게임의 규칙들을 정의
* 게임 전반에 걸친 데이터를 저장

## 출처
* <https://orcacode.tistory.com/entry/%EC%96%B8%EB%A6%AC%EC%96%BC-%EC%97%94-Actor%EC%99%80-Pawn%EA%B3%BC-Character%EC%9D%98-%EC%B0%A8%EC%9D%B4%EC%A0%90>
* <https://www.reddit.com/r/gamedev/comments/8r43ko/unity_component_system_vs_unreal_engine_component/>
* <https://www.koreascience.or.kr/article/JAKO201926151347005.pdf>
