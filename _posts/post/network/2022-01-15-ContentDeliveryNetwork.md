---
title: "Content Delivery Network"
classes: wide
categories: 
  - post
  - Network
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## Content Delivery Network
### 정의
* 지리적으로 분산된 여러 개의 서버
* 컨텐츠를 사용자와 가까운 서버에서 전송해 속도면에서 이득
* **중앙 서버에서 개별 사용자에게 컨텐츠를 전송하려면 트래픽 과부하 및 전송 속도, 시간 문제 발생**
* 파일 복사본을 캐싱하여 각 데이터 센터에 저장

### 사례
* 콘텐츠를 캐싱해 전 세계 여러 곳의 **‘PoP(Points of Presence)’**에 저장
* PoP는 자체 캐싱 서버를 갖고 있으며 각 지역 사용자에게 콘텐츠를 전송

### Points of Presence
* 상호접속지점
* 고유 IP 주소를 가지는 인터넷 엑세스 포인트 위치

### 엣지 컴퓨팅 vs. 클라우드 vs. CDN
* **엣지 컴퓨팅**
  * CDN의 확장
  * CDN 4.0 - 디바이스 가까이에서 연산을 하는 서비스
* **CDN**
  * 사용자가 요청한 콘텐츠를 오리진 서버에 저장된 다음, 필요에 따라 다른 곳에 복제되고 저장
  * 여러 서버에 걸쳐 지역적으로 부하를 분산시켜 오리진 서버에 대한 스트레스를 줄임
  * CDN 1.0 - 전송 속도 증가
  * CDN 2.0 - 동적 컨텐츠 전달 속도 증가
  * CDN 3.0 - 모바일 사용자 증가에 따른 보안 / 분산 보완
* **클라우드**
  * 컴퓨터의 하드 드라이브 대신 인터넷 서버에 정보를 저장
  * 인터넷 상의 서버를 통해 데이터를 처리
  * 

## 출처
* <https://www.akamai.com/ko/our-thinking/cdn/what-is-a-cdn>
* <https://zdnet.co.kr/view/?no=20210827110539>
* <http://www.terms.co.kr/POP.htm>
* <https://it.donga.com/31357/>