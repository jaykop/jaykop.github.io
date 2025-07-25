---
title: "Forward Rendering & Deferred Rendering"
classes: wide
categories: 
  - post
  - Graphics
sidebar:
  nav: "main"
author_profile: true
---

## 포워드 렌더링(Forward Rendering)
![post_thumbnail](/assets/images/forward-v2.png)
* 가장 보편적이고 일반적인 렌더링 방법
* 픽셀 당 쉐이딩과 라이팅 연산 값을 추가하는 방식
* 각 fragment shader에서 연산
  * 빛의 개수 만큼 함
* 투명도 처리, 안티얼라이징 가능
* 라이팅 및 쉐이딩 연산 오버헤드

## 디퍼드 렌더링(Deferred Rendering)
![post_thumbnail](/assets/images/deferred-v2.png)
* multiple render target에 대해 1번만 라이팅 및 쉐이딩 연산
  * 각 프레그먼트 쉐이더에서 따로 하지 않음
* 다수 라이팅 이펙트를 구현하는 데 용이
* 투명도 처리, 안티 얼라이징 불가능

## 렌더타겟이란? Render Target
* 렌더링하고자 하는 최종적인 목적지 / 타겟
  * 텍스쳐일수도 있고, 버퍼일수도 있다

## 출처
* <https://m.blog.naver.com/blue9954/220296252565>  
* <https://gamedevelopment.tutsplus.com/articles/forward-rendering-vs-deferred-rendering--gamedev-12342>
* <https://stackoverflow.com/questions/27186038/what-is-a-render-target-in-opengl>