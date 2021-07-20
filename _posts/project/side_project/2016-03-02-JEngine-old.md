---
title: "JEngine-old"
excerpt: "커스텀 3D 프레임워크"
classes: wide
categories: 
  - project
  - side
header:
  teaser: "assets/images/jengine_thumbnail.png"
sidebar:
  nav: "main"
author_profile: true
---

<figure class="half">
    <a href="/assets/images/jengine_page1.png"><img src="/assets/images/jengine_page1.png"></a>
    <a href="/assets/images/jengine_page2.png"><img src="/assets/images/jengine_page2.png"></a>
</figure>
<figure class="half">
    <a href="/assets/images/jengine_page3.png"><img src="/assets/images/jengine_page3.png"></a>
    <a href="/assets/images/jengine_page4.png"><img src="/assets/images/jengine_page4.png"></a>
</figure>
<div style="text-align: center" markdown="1">
***새 브런치에서 새로 작업 중***  
***이하 설명은 과거 엔진에 대한 설명***
</div>

## 개요
* 개인 사이드 프로젝트로 시작한 게임 엔진 프로젝트
* 3D 그래픽스와 A.I. 테크 데모 구현과 새로운 C++ syntax 적용을 위해 개발
  
## 사용 언어 및 라이브러리
* C++ 
* OpenGL 
* GLSL 
* SDL 
* IMGUI 

## 구현된 게임 엔진 기능
- 전체 화면 / 창 모드와 해상도 조정
- 게임 레벨을 불러오는 ***JSON 포맷을 이용한 파서***
- 게임 레벨 전환을 지원하는 GUI
- 엔진 자체 컴포넌트가 아닌 ***사용자가 직접 게임 로직 디자인하도록 지원***
- 텍스쳐 및 사운드 에셋 로드 기능

## 구현된 3D 그래픽스 기능
- OBJ 포맷 파일을 불러와 ***3D 모델 렌더링***
- 눈/비, 폭발, 노멀 업데이트의 ***파티클 이펙트***
- 2D 텍스쳐 애니메이션
- Directional light, Point Light, Spotlight 타입의 ***라이팅 이펙트***
- Unicode 지원하는 텍스트 렌더링

## 구현된 A.I. 테크
- ***Finite State Machine***
  - 각 에이전트끼리 메세지를 주고 받으며 상호작용
- ***Steering behavior***
  - Flee, Arrival, Evade, Seek, Wander, Pursuit등의 행동 구현

## Git Repository
[Github](https://github.com/jaykop/JEngine-old/){: .btn .btn--dark}`