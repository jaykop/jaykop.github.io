---
title: "Class Scheduler"
excerpt: "DigiPen 학생들이 학기 수강 계획을 세울 수 있도록 도와주는 웹 어플리케이션"
classes: wide
categories: 
  - project
  - academic
header:
  teaser: "assets/images/DigiPenScheduler_thumbnail.png"
sidebar:
  nav: "main"
author_profile: true
---

<figure class="half">
    <a href="/assets/images/DigiPenScheduler_page1.png"><img src="/assets/images/DigiPenScheduler_page1.png"></a>
    <a href="/assets/images/DigiPenScheduler_page2.png"><img src="/assets/images/DigiPenScheduler_page2.png"></a>
</figure>
<figure class="half">
    <a href="/assets/images/DigiPenScheduler_page3.png"><img src="/assets/images/DigiPenScheduler_page3.png"></a>
    <a href="/assets/images/DigiPenScheduler_page4.png"><img src="/assets/images/DigiPenScheduler_page4.png"></a>
</figure>
<div style="text-align: center" markdown="1">
</div>

## 개요
* 2019.09 ~ 2019.12
* By Webcake (Team of 3 programmers)
* ReactJS, Postgresql
* 브라우저 기반의 DigiPen 학생을 타켓으로 한 수강 스케줄러

## 프로젝트 설명 
<div style="text-align: justify" markdown="1">
DigiPen 학생들이 학기 수강 계획을 세울 수 있도록 도와주는 웹 어플리케이션입니다.
학생들은 자신들이 선택한 강의들이 시간대가 겹치는지의 여부를 시작적이고 보다 직관적인 강의 시간표를 통해 확인할 수 있습니다.
</div> 

## 개발 내용 
  * 역할: 알고리즘 프로그래머
  * DB에서 강의 정보를 정수형, 문자열로 변환하는 ***Parser*** 개발
	  - DB에 쿼리문을 보내 raw data 받음
	  - 받아온 데이터로 강의명, 섹션, 강의실, 요일, 교수명, 시작 시간과 종료 시간을 파싱
  * 시간 충돌 감지 기능 
	  - 파싱된 데이터를 통해 두 강의의 시간 충돌 여부를 확인하는 기능
  * 학생이 선택한 강의들을 조합하여 시간표를 생성해주는 ***시간표 생성기*** 개발
	  - 불가능한 시간표를 필터링하고 조합 가능한 강의들로만 시간표를 생성
	  - Merging operator는 기존 시간표에 새 강의를 추가하고 시간 충돌 여부를 체크한 뒤, 학생이 고를 수 있는 새로운 시간표 후보군들을 생성 
	  - Subtracting operator는 생성된 시간표 중 필터링할 강의를 포함하고 있는지 체크. 필터링할 강의를 포함한 시간표들은 후보군에서 제거
  * 기능 검수
	  - 상기된 개발 목록; 강의 정보 Parser, 시간 충돌 감지 기능, 시간표 merge/subtract operator는 jtest를 통해 검수됨
    - 검수를 통해 발견된 edge case들은 모두 수정 적용됨
  * 스플래시 화면과 크레딧 화면 디자인
    - tailwind css를 사용해 웹 어플리케이션 시작 시 DigiPen 로고 스플래시 화면과 우하단에 있는 버튼을 클릭 시 뜨는 크레딧 팝업 창을 구현
  
