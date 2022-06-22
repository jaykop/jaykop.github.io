---
title: "SpriteRenderer vs. UI Image"
classes: wide
categories: 
  - post
  - Unity
sidebar:
  nav: "main"
author_profile: true
---

## SpriteRenderer 
* 어떤 hierarchy에도 배치할 수 있다
* Transform으로 조정한다
* transparent geometry queue를 통해서 render된다
  * default material을 사용하는 경우
* 자동으로 최적 메쉬를 생성한다
* draw call을 줄이기 위해 sprite atlas를 사용할 수 있다

## UI Image (CanvasRenderer)
* owner인 gameobject가 canvas 컴포넌트를 가지고 있어야 한다
* RectTransform으로 세팅한다
  * Interface 시스템 상에서의 위치 조정을 용이하게 한다
* transparent geometry queue를 통해서 render된다
  * canvas가 overlay rendering mode인 경우
* 직사각형 모양의 메쉬를 생성한다
* draw call을 줄이기 위해 sprite atlas를 사용할 수 있다

### SpriteRenderer vs. UI Image 메쉬 생성
![image](/assets/images/sprite-example.webp)
![image](/assets/images/sprite-example-2.webp)
* sprite renderer는 최적의 메쉬를 생성
* UI Image는 직사각형의 메쉬를 생성

![image](/assets/images/sprite-meshes.webp)
* island(이미지가 붙어있지 않고 떨어진)인 경우, 별도의 메쉬를 생성한 sprite renderer
* UI Image는 그런 거 없음

## Performance
* 위와 같은 차이는 다수 객체를 렌더링할 때 심화된다
  * terrain 혹은 particle 등
* texture를 render하기 위해 GPU driver에 명령구문을 보낸다.
  * vertices, indices, uv corrdinates, texture data, shader param 등
  * 이 정보를 취합해 draw call을 생성한다
* 스크린에 이미지가 최종적으로 그려지기 전까지의 pipeline은 아래와 같다
* **Simplified Rendering Pipeline**
  1. CPU가 GPU에 Draw command 날림
  2. GPU가 VRAM에 texture 정보를 복사하는 등 draw를 위한 정보를 취합
  3. geometries 정보는 vertex shader와 rasterizer 등을 거쳐 pixel 단위로 transform
  4. fragment shader를 거쳐 1회 혹은 그 이상 framebuffer로 transform
  5. 한 번의 frame이 완료되면서 image가 screen에 노출

* 위의 설명만 보면 sprite renderer가 geometry 정보가 더 많으므로 rendering cost가 더 높을 것으로 보인다
* 하지만 **vertex operation이 fragment operation 보다 cost가 더 낮고, mobile과 semi-transparent material에서 특히 그 차이가 크다면?**
* Unity를 비록한 대부분의 엔진에서 semi-transparent(반투명) materials는 back-to-front 순서로 render된다
  * 카메라로부터 먼 object부터 순서대로 그려져오는 것
  * opaque(불투명) material들은 카메라로부터 가까운 순서부터, 즉 위와 반대로 rendering 하면서 culling을 한다
* Pixel shader는 screen에 보이는 모든 sprite의 pixel 단위 하나하나마다 실행될 것이며, 이는 거대한 sprite를 그릴 때도 마찬가지다
  * transparent object들은 camera frstum 안에 있더라도 효율적으로 cull할 수 없다
  * screen에 노출되지 않는 semi-transparent sprite들에도 pixel shader가 불필요하게 실행된다
  * 같은 픽셀에 반복적으로 rendering하는 overdraw 문제, memory bandwidth 문제, pixel fillrate limit에 도달하는 문제 등이 발생한다
  * 위와 같은 문제로 인해 mobile 같은 저사양 기기를 지원하지 못할 수도 있다
* **SpriteRenderer 캄포넌트는 transparent pixel을 제외한 최적의 메쉬를 생성한다**
  * 불필요한 pixel shader 작동을 하지 않고, overdraw를 줄일 수 있다
* 이에 반해 UI Image는 간단한 메쉬를 생성하지만, overdraw의 위험에 노출되어 있다

### UI Image는 언제 사용?
* UI 포지셔닝이나 특정 포맷을 위한 기능들이 필요할 때 쓰면된다

## 참고
* transparent material - 텍스쳐 전체가 투명
* semi-transparent material - 텍스쳐가 투명/불투명 혼재
* opaque material - 텍스쳐 전체가 불투명

## 출처
* <https://thegamedev.guru/unity-ui/sprite-vs-image/>