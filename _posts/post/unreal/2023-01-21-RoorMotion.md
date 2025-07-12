---
title: "Root Motion"
classes: wide
categories: 
  - post
  - Unreal
  - Animation
sidebar:
  nav: "main"
author_profile: true
---
   
## 루트 모션 사용 여부에 따른 차이

### 루트 모션을 사용하지 않는 Animation
* 애니메이션을 출력하더라도 제자리에서 걷는다
* Game-Driven motion
  * 게임에서 연산된 데이터를 받아 적절한 애니메이션을 출력할 수 있다
  * **게임에 의해 캐릭터가 이동하게 하고 애니메이션은 그 위에 얹는 느낌**
* TPS 게임에서 주로 사용하는 애니메이션
  * **게임 캐릭터의 속도에 따라 걷거나 뛰는 애니메이션을 출력한다**
* 캐릭터의 속도와 발 움직임이 맞지 않을 수 있다
  * 발 미끄러지는 현상

### 루트 모션을 사용하는 Animation
* 애니메이션의 매 프레임마다 캐릭터가 얼마나 이동할지 결정한다
  * 애니메이션이 출력되면 실제로 캐릭터가 이동해버린다
  * Root Node가 캐릭터가 얼마나 이동해야 할 지에 대한 정보를 갖는다
* Animation-Driven motion
  * **애니메이션에 의해 캐릭터가 이동한다**
* 캐릭터의 속도와 발 움직임이 동일하다
  * 발 미끄러지는 현상이 없다

## 루트 모션 네트워킹
### 네트워킹 게임에서의 루트 모션 사용?
* Animation이 Replicated 되지 않았다면 Root Motion은 Animation Montage를 사용해야 한다
* RootMotioMode = Root Motion from Montages Only로 설정해야 한다
* Blend Space를 사용하는 Animation은 네트워크 동기화하기가 매우 어렵다
  * 가능하다는 포스트도 있지만...

## 출처
* <https://docs.unrealengine.com/5.1/ko/root-motion-in-unreal-engine/>
* <https://docs.unrealengine.com/4.27/ko/AnimatingObjects/SkeletalMeshAnimation/Blendspaces/>
* <https://forums.unrealengine.com/t/what-is-the-difference-between-using-root-motion-and-not-when-should-we-use-it/470594/2>
* <https://forums.unrealengine.com/t/root-motion-over-network-how-its-done/75059>
* <https://forums.unrealengine.com/t/root-motion-for-multiplayer-and-montage-state-machines/78042>