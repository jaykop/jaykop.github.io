---
title: "Terrain Analysis & Propagation"
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

## Propagation
![image](/assets/images/{E945C464-D0F6-4844-BCF5-30B523268A2F}.png)  
1. Influence Layer와 Temp Layer 2개의 Layer 세팅
2. Decay 후의 값을 Temp Layer에 저장
3. Temp Layer의 값을 Influence Layer에 다시 복사

### Decay Factor 
* 얼마나 빠르게 distance에 따라 decay가 전파되는지
* 얼마나 빠르게 influence가 사라지는지
* **decay factor가 높을수록 influence는 빠르게 낮아진다**

### Growing Factor 
![image](/assets/images/{7284492B-4DE8-48BA-9E05-6BDA145C4EB2}.png)  
* influence value를 업데이트 하면서 기존 값과 새 값 중 어느 값에 더 편중할지

### How to propagate?
![image](/assets/images/{2E88141D-105C-4CD2-8A2C-0859B3A39B4A}.png)  
* decay factor와 growing factor 세팅
* 현재 노드 (Red)에 대해 이웃 노드들 (Right, Bottom, Right-Bottom)에 대해 Decay formula로 influence value 연산
* 최대값 확인 (Right-Bottom = 0.75)

![image](/assets/images/{9B5099CE-E6EE-4E7D-B462-579B4CA97F8B}.png)  
* 보간 공식에 따라 값 연산
* 해당 값을 TempLayer에 저장

![image](/assets/images/{9E963912-5A69-4CEA-BACA-441F962A3CBE}.png)  
* 최종 연산한 값들이 저장된 TempLayer의 값을 Original Layer에 복사

### Why using double bufferubg?
![image](/assets/images/{0A530AEB-3A3E-4632-B75B-8944D9B20E55}.png)  
* TempLayer가 필요한 이유는 하나의 Layer에서 Influence 값을 연산하면서 후순위로 연산되는 값들이 앞에 이미 연산된 값들에 영향을 받아 오류가 발생하기 때문

## 출처
* <https://drehzr.tistory.com/249>