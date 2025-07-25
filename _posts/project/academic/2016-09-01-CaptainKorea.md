---
title: "Captain Korea"
excerpt: "2D 탑다운 시점의 강력한 타격감을 제공하는 액션 잠입 게임"
classes: wide
categories: 
  - project
  - academic
header:
  teaser: "assets/images/CaptainKorea_thumbnail.png"
sidebar:
  nav: "main"
author_profile: true
---

<figure class="half">
    <a href="/assets/images/CaptainKorea_tech_hires.jpg"><img src="/assets/images/CaptainKorea_tech_hires.jpg"></a>
    <a href="/assets/images/CaptainKorea_3_hires.jpg"><img src="/assets/images/CaptainKorea_3_hires.jpg"></a>
</figure>
<figure class="half">
    <a href="/assets/images/CaptainKorea_2_hires.jpg"><img src="/assets/images/CaptainKorea_2_hires.jpg"></a>
    <a href="/assets/images/CaptainKorea_1_hires.jpg"><img src="/assets/images/CaptainKorea_1_hires.jpg"></a>
</figure>

## 개요
* 2016.09 ~ 2017.05
* By HOW (Team of 2 programmers)
* C++, 스크래치 엔진
* 2D 탑다운 시점의 강력한 타격감을 제공하는 액션 잠입 게임

## 게임 설명
플레이어는 위기에 빠진 대한민국을 구하기 위해 적진에 침투해 다음 레벨로 나아가야 합니다.  
특공대 출신의 플레이어는 강력한 펀치만으로 적을 궤멸시킬 수 있지만, 잔상을 만드는 능력, 적의 위치를 파악하는 능력, 발소리를 숨기는 능력, 보다 강력한 펀치를 날리는 능력 역시 사용할 수 있습니다.  
적과 마주해 공격적으로 대응할 지, 아니면 최소한의 움직임으로 잠입할 지는 플레이어의 선택입니다.  
  
## 개발 내용
  * ***Component-based 게임 엔진*** 개발
  * 게임 씬의 정지, 재생, 전환, 종료 등을 지원하는 ***게임 스테이트 매니저*** 구현
  * ***JSON 포맷 파서***를 구현해 레벨 정보를 불러오는 기능 추가
  * A* 알고리즘을 이용하여 ***적의 플레이어 추격 패턴***을 디자인
  * GLSL을 이용해 ***물결 이펙트, 파티클 이펙트*** 구현
  * 2D 물리 시스템 및 FMOD 라이브러리를 이용해 사운드 시스템 구현
  
## 프로젝트 설명
본 게임은 스크래치 엔진 개발 이후 게임 개발까지 총 1년의 시간이 소요된 프로젝트입니다.  
총 개발 인원은 2명이었으며 OpenGL, GLSL, C++, JSON, SDL 등을 이용하여 개발했습니다.  
제가 맡은 파트는 전반적인 엔진 개발, 게임플레이 프로그래밍 및 비주얼 이펙트 디자인이었습니다.  

인력확보를 하지 못한 탓에 다른 팀들보다 상대적으로 많은 태스크를 수행해야 한다는 부담감이 있었지만, 적은 인원으로 인해 의견 수렴과 디자인 합의에 빨리 도달할 수 있어 개발에 투자할 시간이 많았습니다.  
또 이전보다 다양한 분야와 많은 태스크를 수행했기에 새로운 지식과 경험을 쌓을 수 있었으며, 게임 디자인도 마음에 들어 동기부여를 증대시켰고 개발 자체가 즐거웠던 프로젝트였습니다.  
</div>
---