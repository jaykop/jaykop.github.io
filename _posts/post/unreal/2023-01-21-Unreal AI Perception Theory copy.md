---
title: "AI Perception Theory"
classes: wide
categories: 
  - post
  - Unreal
  - A.I.
sidebar:
  nav: "main"
author_profile: true
---

## Parts of the AI Perception System
Unreal은 AI Perception System을 통해 Actor가 무엇을 감지하는지, World의 어떤 부분을 감지할 수 있는지를 제어하게 해준다. 수집한 정보는 Event-driven system이 처리하면서 간단해지며 가벼운 비용만을 소모한다. 결과적으로 블루프린트 안에서 전범위에 걸쳐 사용할 수 있으며 다양한 상황에서 핸들링이 가능하다.

### The Components
대표적인 2개의 Component는 AI Percpetion Component와 AI Perception Stimuli Source다. AI Perception Stimuli Source는 다른 AI들이 이 Actor의 어떤 요소를 인지할 수 있는지 결정한다. AI Perception Component는 반대로 이 Actor가 어떤 감지 능력을 사용할 수 있는지를 결정한다.

### AI Perception Component

![post_thumbnail](/assets/images/26c1b126-6e2b-484e-8e02-056a8a33569c.png)

이 Component에는 Perception System에서 사용할 감각을 설정할 수 있다. 복수의 감각을 하나의 컴포넌트에 추가할 수 있다. Dominant Sense를 지정해 특정 감각이 다른 감각보다 높은 우선순위를 유지하게 할 수 있다.
* 이 컴포넌트를 소유한 Actor가 감지하는 주체 

### AI Perception Stimuli Source Component

![post_thumbnail](/assets/images/1b1735c4-4604-4b1d-a1f3-a87d14dfac22.png)

이 Component를 Actor에 추가함으로써 어떤 감각이 AI Perception System에 등록할 것인지를 결정하게 한다. 이를테면, 이 자극 소스 컴포넌트를 시각 자극으로 세팅하면 다른 AI가 이 Actor를 시각적으로 볼 수 있다.
* 이 컴포넌트를 소유한 Actor가 감지되는 객체

위의 Component들로 수집한 정보는 OnTargetPerceptionUpdated 이벤트를 통해 Stimulus 구조체로 수집된다. 

![post_thumbnail](/assets/images/e5a217b7-d833-4f93-9855-83bb7d0d88a2.png)

## How AI Sense
### Source and Stimuli

![post_thumbnail](/assets/images/42f013b6-8978-4ffd-a78c-d9737d4c9000.png)

AI 캐릭터가 어떤 자극을 감지할 수 있도록 하기 위해서는 AI Perception Component가 필요하다. 또 어떤 Actor가 자극을 만들어서 다른 AI에게 감지되게 하고 싶다면, AI Perception Stimuli Source Component가 필요하다.

### Sensing Stimuli

![post_thumbnail](/assets/images/daa1a4ba-f2ee-4155-907b-a2dd8f70d169.png)

플레이어의 AI Perception Stimuli Source Component에 Sight 를 추가하고 AI가 플레이어를 맞닥뜨렸다고 가정해보자. AI는 플레이어의 AI Perception Stimuli Source Component를 확인하고 유효한 자극이 있을 때 OnTargetPerceptionEvent를 실행한다.

## 출처
* <https://dev.epicgames.com/community/learning/courses/67R/unreal-engine-introduction-to-ai-with-blueprints/586p/ai-perception-theory>