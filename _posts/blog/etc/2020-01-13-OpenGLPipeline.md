---
title: "OpenGL 파이프라인 개요"
classes: wide
categories: 
  - blog
  - etc
---
---

1. vertex specification
* 정렬된 버틱스 리스트를 나열
* 이를 이용해 primitive boundaries를 정의해 텍스처 좌표와 색깔을 정의할 수 있음 / 파이프라인 첫 단계

2. vertex shader
* 버텍스 데이터를 처리
* GPU가 모든 각 버텍스의 최종 위치를 연산 

3. tessellation - optional, 
* 테셀레이션 과정을 통해 메쉬 트라이앵글을 처리

4. geometry shader - optional, 
* 추가 연산을 통해 최종 버텍스의 수를 유지하거나 증가 시킴 primitive의 타입을 변환

5. vertex post-processing
* 클리핑 - 오브젝트 및 메쉬 중 버릴 것과 다음 스테이지로 넘어갈 것을 정하는 단계

6. primitive assembly
* 도형들을 정렬 / 삼각형, 선, 점 등

7. rasterization
* 프라그먼트들을 출력

8. fragment shader
* 이론적으로 필수적이지 않은 단계
* 각 프래그먼트의 최종 색깔을 정의

9. per-sample operation
* scissor, stencil, depth 등의 테스트를 실행
  
  
---  
출처:   
* https://quinoa.tistory.com/31
