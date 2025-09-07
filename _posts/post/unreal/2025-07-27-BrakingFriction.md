---
title: "[Unreal] Braking Friction"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## Braking Friction 

![post_thumbnail](/assets/images/BrakingFriction/BrakingFriction.png)

* 캐릭터의 Deceleration을 처리할 때, 즉 목적지를 향해 거의 다다른 캐릭터의 속도가 자연스럽게 감소하도록 하는 인자
* CharacterMovement Component 안에 이와 관련된 여러 요소가 있습니다.

### Braking Friction Factor
* 적용하고 있는 Braking Friction 값에 multiplier로 사용하는 값

### Braking Friction
* Use Separated Braking Friction가 true인 경우에 활성화
* 이 Braking Friction을 사용하면, 실제 적용되고 있는 외부 환경 기반의 Firction이 아닌 독립적인 Braking Friction을 사용하는 것입니다.

### Braking Sub Step Timer
* Braking Friction을 적용할 Interval을 의미합니다

### Braking Deceleration Walking
* Walking 상태에서 가속하지 않을 때 적용하는 Deceleration 상수입니다.
* 위의 조건에서, 현재 Velocity에 저 값만큼의 힘을 적용해 Deceleraete 합니다

### Fixed Path Braking Distance
* Use Fixed Braking Distance for Paths가 true인 경우에 활성화 됩니다.
* 이 특정 거리를 기준으로 Braking을 시작하게 합니다.