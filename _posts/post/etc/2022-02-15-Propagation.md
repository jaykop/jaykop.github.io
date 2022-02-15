---
title: "Propagation"
classes: wide
categories: 
  - post
  - etc
sidebar:
  nav: "main"
author_profile: true
---
   
## Influence Mapping 영향도 알고리즘
* 수치를 2d grid에 분산시켜 놓은 추상 디자인

## Generalized Grid Terrain Analysis
* 다중 레이어가 가진 수치의 총합으로 맵 구성
* **레이어의 종류**
  1. **Visibility**: 현재 위치에서 보이는지
  ![image](/assets/images/{82FC1D20-F5F6-41F6-B6F3-B2FF7B6BD9CD}.png)  
  2. **Openness layer**: static obstacle에 얼마나 근접하는지
  3. **Cover layer**: 현재 위치에서 영향력을 행사할 수 있는지
    * 무기 범위, 인지 범위 등
  ![image](/assets/images/{DEEBBCCB-EC5A-4731-8BBD-C6FF3976620C}.png)  
  4. **Area occupancy layer**: 한 위치에 얼마나 많은 오브젝트가 있는지
  ![image](/assets/images/{F7C5C822-8043-4136-AB82-4B93DFA5B619}.png)  
  5. **Line-of-fire layer**: 에임했을 때 데미지 받는 방향과 범위 안인지
  6. **Light level layer**: 빛이 도달하는지
  7. **Area search layer**: 탐색 과정에서 이미 방문한 곳인지
  8. **Occupancy map**: 탐색 대상이 있을 확률

## Combine Layers
* 위의 각 레이어를 하나로 합쳐서 수치의 총계를 산출
![image](/assets/images/{47A2D7E7-368D-413B-A61B-C645DA05C37F}.png)  
* 이때 최종 수치 산출하는 방법은
  1. multiplied
  2. mean
  3. geometric mean

## 출처
* <https://drehzr.tistory.com/249>