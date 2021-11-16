---
title: "Transforming - World"
classes: wide
categories: 
  - post
  - Graphics
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## Translation
![post_thumbnail](/assets/images/{67402326-F4F4-490D-A187-211BDACAE424}.png)
* 어떤 P1 (x, y)를 P2(x', y')로 이동
* 두 점 사이의 거리는 (Tx, Ty)
  * x’ = x + Tx
  * y’ = y + Ty

## Rotation
![post_thumbnail](/assets/images/{10A85668-AAEB-4C0E-9358-152B69C3FE06}.png)
* 각 a의 크기에 따라 방향이 달라진다
![post_thumbnail](/assets/images/{8CD19AC0-53FE-4D20-BAE7-1ACBE650255D}.png)
* 각 a에 의해 회전한 점의 공식
![post_thumbnail](/assets/images/{8157FEC8-5395-47BF-9526-1DCA78CA9A57}.png)

## Scale
![post_thumbnail](/assets/images/{AC65DFF5-A1D3-41D5-87BE-CBD0617295C9}.png)

## Homogeneous Coordinates
* Transform 연산은 vector와 matrix로 수행
* pre-multiplication을 하기 위함
* 마지막 원소인 w로 Point와 Vector를 구분
  * w = 1 : Point
  * w = 0 : Vector