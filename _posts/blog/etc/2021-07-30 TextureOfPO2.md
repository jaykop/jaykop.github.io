---
title: "Texture 사이즈"
classes: wide
categories: 
  - blog
  - etc
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## Texture 사이즈를 2의 제곱수로 세팅하는 이유

ETC와 PVRTC가 지향
유니티 아틀라스를 사용하면 별도로 세팅하지 않아도 된다
오늘날 대부분의 GPU는 이러한 제약으로부터 자유롭다 (NPOT)
RAM을 사용할 때 NPOT 이미지는 그보다 큰 사이즈의 POT로 확장된다
이 과정에서 메모리는 낭비된다
확장된 사이즈만큼 가장자리에 edging artifact가 발생할 수 있다
NPOT 텍스쳐는 상대적으로 POT보다 느리게 처리된다
구형 GPU는 NPOT 지원하더라도 느린 경우가 많다
NPOT Texture를 지원하지 않는 경우도 있다
사이즈가 2의 제곱수가 아닌 Texture의 장점?
저장장치에서 차지하는 Texture 용량이 작다
NPOT -> POT로 변환하지 않으니 시간 절약

## 출처
* <https://gamedev.stackexchange.com/questions/7927/should-i-use-textures-not-sized-to-a-power-of-2>