---
title: "OpenGL 파이프라인"
classes: wide
categories: 
  - post
  - Graphics
sidebar:
  nav: "main"
author_profile: true
---

## View에 따른 OpenGL Pipeline 분류

|View|Purpose|
|:---:|:---|
|**Functional**|매 단계에서의 결과값의 연속|
|**Transform**|수학적 변형(Transform)의 연속|
|**System**|하드웨어 설계|
|**Programmable**|데이터 흐름에 따른, 유저가 정의한 구현|

## Functional View

  ![post_thumbnail](/assets/images/{65CBADF9-7FA6-4ED2-90E8-9631CF0A279B}.png)
* OpenGL 구현은 항상 다음을 지원
  1. Vertices 들은 transform 되었거나 lit한 상태 
  2. 프로세싱된 Vertices들은 geometry, color, texture를 이용해 이미지를 생성하기 위해 Rasterizer로 단계도 이동
  3. Pixels은 frame buffer에 저장돼 디스플레이에 다음 사이클에 업데이트 되기를 기다린다

## Transform View

  ![post_thumbnail](/assets/images/{8B1EB8E6-196C-4ED5-8C0B-1534DAB4F98A}.png)
* ModelView transformation
  * model space에서 view space로 vertices 이동
* Projection transformation 
  * view space에서 normalized projection space로 vertices 이동
* Viewport transformation 
  * NDC에서 viewport (screen) space로 vertices 이동

## Programmable View

  ![post_thumbnail](/assets/images/{59CC0FF3-098C-41CC-A04D-3E109D6B64BE}.png)

1. **Vertex Specification**
  * 정렬된 버틱스 리스트를 나열
  * 이를 이용해 primitive boundaries를 정의해 텍스처 좌표와 색깔을 정의할 수 있음
  * 파이프라인 첫 단계
  * Vertex Puller가 필요한 vertex data를 수집해 VS로 보냄

2. **Vertex shader**
  * 파이프라인 상 Programmable한 첫 단계
  * 버텍스 데이터를 처리
  * GPU가 모든 각 버텍스의 최종 위치를 연산 
  * Shader Stage 중 유일한 필수 단계

3. **Tessellation(optional)**
  * 일정한 형태의 도형들로 평면을 빈틈없이 채우는 것
  * 더 작고 단순한 여러 개의 프리미티브로 분할하는 작업
    * 메쉬 트라이앵글로 테셀레이션

4. **Geometry shader(optional)** 
  * 추가 연산을 통해 최종 버텍스의 수를 유지하거나 증가 시킴
  * primitive의 타입을 변환

5. **Primitive Assembly**
  * 삼각형, 선, 점 등의 도형들을 정렬 

6. **Vertex Post-processing**
  * 클리핑 
    * 오브젝트 및 메쉬 중 버릴 것과 다음 스테이지로 넘어갈 것을 정하는 단계

7. **Rasterization**
  * 선별된 오브젝트들을 픽셀로 변경
  * 프라그먼트들을 출력
  * 픽셀 interpolation 수행

8. **Fragment Shader**
  * 각 프래그먼트의 최종 색깔을 정의

9. **Per-sample Operation**
    * scissor, stencil, depth 등의 테스트를 실행
