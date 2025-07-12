---
title: "Framebuffers"
classes: wide
categories: 
  - post
  - Graphics
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## 버퍼란? Buffer
* 데이터를 한 곳에서 다른 곳으로 전송하는 동안 일시적으로 그 데이터를 보관하는 메모리 영역

### 버퍼링 Buffering
* 버퍼를 활용하는 방식 혹은 버퍼를 채우는 동작
* 큐 Queue 라고도 한다

## 프레임버퍼란? Framebuffer
* 화면에 나타날 영상 정보를 일시적으로 저장하는 기억 장치
  * GPU가 CPU로부터 도형을 표현하는 리스트를 받아 변환하여 버퍼에 기록
  * 프레임버퍼의 각 기억 단위는 픽셀
  * 각 픽셀의 On/Off 상태와 색 정보를 비트맵으로 저장

### OpenGL에서의 프레임버퍼
* 기본 프레임버퍼는 어플리케이션이 실행되고 윈도우 창을 생성할 때 함께 생성된다
* 프레임버퍼는 실제로 버퍼가 아니라, 여러 attachment 정보를 가진 하나의 집합체
  * 각 버퍼로의 포인터를 가진 일종의 구조체다
  * 프레임버퍼에 attached 된 버퍼는 Renderbuffer 이거나 Texture일 수 있다
* 프레임버퍼 객체 Framebuffer Object (FBO)로 선언되어 사용

### 렌더버퍼 Renderbuffer
* 실제 바이트 혹은 픽셀 정보를 담는 버퍼
* 렌더버퍼가 Offscreen rendering에 더 최적화되어 있어, 텍스쳐에 그리는 것보다 더 빠르다
* 하지만 네이티브, 개발 의존적 포맷이기 때문에 읽어들이는 것은 텍스쳐에 비해 더 느리다

## 출처
* <https://iskim3068.tistory.com/21>
* <https://learnopengl.com/Advanced-OpenGL/Framebuffers>
* <https://stackoverflow.com/questions/2213030/whats-the-concept-of-and-differences-between-framebuffer-and-renderbuffer-in-op>
* <https://stackoverflow.com/questions/46384007/what-is-the-meaning-of-attachment-when-speaking-about-the-vulkan-api>