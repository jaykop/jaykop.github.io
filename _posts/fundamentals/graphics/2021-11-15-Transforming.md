---
title: "[3D Graphics] Transforming - World"
classes: wide
categories:
  - fundamentals
  - graphics
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## Translation
![post_thumbnail](/assets/images/Transforming/01.png)
* 어떤 P1 (x, y)를 P2(x', y')로 이동
* 두 점 사이의 거리는 (Tx, Ty)
  * x’ = x + Tx
  * y’ = y + Ty

## Rotation
![post_thumbnail](/assets/images/Transforming/02.png)
* 각 a의 크기에 따라 방향이 달라진다
![post_thumbnail](/assets/images/Transforming/03.png)
* 각 a에 의해 회전한 점의 공식
![post_thumbnail](/assets/images/Transforming/04.png)

## Scale
![post_thumbnail](/assets/images/Transforming/05.png)

## Homogeneous Coordinates
* Transform 연산은 vector와 matrix로 수행
* pre-multiplication을 하기 위함
* 마지막 원소인 w로 Point와 Vector를 구분
  * w = 1 : Point
  * w = 0 : Vector