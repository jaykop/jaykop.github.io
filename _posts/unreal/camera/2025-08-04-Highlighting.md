---
title: "[DevNote] 장애물 너머의 오브젝트 하이라이트"
classes: wide
categories:
  - unreal
  - camera
sidebar:
  nav: "main"
author_profile: true
---

## Custom Depth Pass

![post_thumbnail](/assets/images/Highlighting/01.png)

* Custom Stencil을 사용하지 않는 Actor들에 대해, Depth를 비교해 해당 Actor보다 하이라이트할 대상이 더 뒤에 있으면 Stencil 값을 체크해 Actor 표면에 그려서 Highlight 효과를 부여하는 방식으로 적용

### 이미 Stencil 값을 가진 다른 Object에 가려진 경우라면...?
* 같은 Render Target를 사용하므로 Draw 순서대로 Stencil 값이 덮어씌워져 버린다
* BitMask를 사용

### Foliage 제외
* 표면에 하이라이트할 장애물 카테고리 중에서 Foliage는 제외하기로 결정
1. Custom Depth Pass에 렌더하도록 토글을 On하는 방법
  * 동일한 Custom Depth Pass에 렌더하니 Foliage를 하이라이트 대상보다 나중에 그리면서 덮어씌울 것으로 기대
  * 하지만 모든 Foliage StaticMesh 객체에 이 옵션을 켜는 것은 번거롭다
2. 하이라이트 Material BP에서 Shading Nodel ID를 확인하고 하이라이트할지 말지 결정하는 로직을 추가
  * Shading Mpoel은 Enum이고, 이 중 Two Sided Folaige(6)이면 하이라이트 하지 않도록 추가

### 아군 플레이어 하이라이트 조건
* 아군 캐릭터가 내가 로컬로 조종하는 플레이어에 가려지면 하이라이트 되어야 했다
  * 단, 둘 사이에 장애물이 있는 경우에만
  * 카메라 / 내 캐릭터 / 장애물 / 아군 캐릭터 -> 하이라이트 처리
  * 카메라 / 내 캐릭터 / 아군 캐릭터 -> 하이라이트 처리 안 함
* 이 케이스를 위해 별도의 로직 처리가 없으면 단순히 내 캐릭터가 아군 캐릭터를 가릴 때도 하이라이트 되는 현상이 발생했다
* 그래서 카메라 위치를 기준으로, 아군 캐릭터들을 향해 Ray를 쏴서 장애물이 있는지 없는지 검사해 하이라이트 여부를 결졍했다
  * 매 Tick 하지 않고 일정 Interval을 주었다

## 아웃라이너 추가
* 기존 아군 캐릭터의 하이라이트 기능을 폐기했다
* 대형 몬스터에 아군 캐릭터가 가려지는 등 특정 상황에 아웃라이너가 보이는 기능을 추가해야 했다

## 문제 상황
* 몬스터 등 장애물로 판정될 대상들이 이미 Custom Depth & Stencil을 사용하는 경우가 있다
* Stencil로 겹침 여부는 알 수 있어도, 어느 것이 앞에 있는지는 판단이 불가했다

## 해결 방법
* **추가 커스텀 뎁스 버퍼 사용**
* 커스텀 렌더 패스 추가로 엔진 수정이 불가피
* **GBuffer에 마스크값 기록**
* 캐릭터 Material에서 GBuffer를 기록하는 MP 중 남는 채널을 활용해 PC/Monster를 구분하여 값을 기록
* PP Material에서 이 값 기반으로 누가 앞에 있는지 판단 가능
  1. PC의 CustomDepth 여부 판단 
    - PC의 CustomDepth의 값이 있다면, 무언가가 가리고 있다는 의미
  2. G Buffer의 값 확인 
    - 몬스터의 값이라면, 몬스터에 가려진 것
  3. 위 두 조건이 만족할 시, 아웃라이너 로직 실행
  
## G Buffer란?
* 렌더링 엔진이 디퍼드 렌더링 시 사용하는, 픽셀 단위로 필요한 정보를 저장하는 버퍼
  * 위치, 색상, 밝기, 그림자 등 정보 저장
  * Geometry Pass에서 여러 정보를 각 렌더 타겟에 저장
    * 표면 정보 텍스처 세트'가 바로 G-Buffer
  * 이렇게 저장한 정보로 Lighting Pass에서 광원 계산 수행
* **즉, 표면 재질을 구성하는 정보 버퍼**

# 출처
* <https://eastroot1590.tistory.com/entry/UE4-Advenced-%EB%B2%BD-%EB%92%A4%EC%97%90%EC%9E%88%EB%8A%94-%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8-%EA%B7%B8%EB%A6%AC%EA%B8%B0-feat-Custom-Depth>