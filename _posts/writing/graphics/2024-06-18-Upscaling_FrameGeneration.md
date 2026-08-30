---
title: "[3D Graphics] Upscaling과 Frame Generation"
classes: wide
categories:
  - writing
  - graphics
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## Upscaling

사진이나 동영상의 픽셀과 픽셀 사이에 새로운 픽셀을 끼워 넣어 해상도를 높여주는 기술.

### Spatial Upscaling

* 각 프레임의 개별 픽셀 데이터를 사용하여 업스케일링을 수행
* 모든 프레임을 독립적으로 처리

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/01.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
 <figcaption style="text-align: center;">Nearest Interpolation</figcaption>
</div>

<br>
<br>

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/02.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
 <figcaption style="text-align: center;">Bilinear Interpolation</figcaption>
</div>

<br>
<br>

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/03.png" width="25%" alt="post_thumbnail" style="display: inline-block;">
 <figcaption style="text-align: center;">12 * 2/3 + 9 * 1/3 = 11</figcaption>
</div>

* 다른 방법들 - Lanczos, 쌍곡선, …
  * [Comparison gallery of image scaling algorithms - Wikipedia](https://en.wikipedia.org/wiki/Comparison_gallery_of_image_scaling_algorithms)

### Temporal Upscaling

* 사진 여러 장이 있을 때, 사진에 보이는 물체들이 얼마나 빨리, 어느 방향으로 이동하고 있는지 추정하여 선명도를 높인다

**FSR 예시**

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/04.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
</div>

* 지난 프레임 히스토리 수집
  * Camera Jitter로 동일한 프레임 내의 픽셀들의 위치를 미세하게 움직인 결과 포함
    * 정적인 화면에서도 Temporal Data 생성
    * 업스케일링에 필요한 샘플 다양화

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/05.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
</div>

* 여러 프레임에 걸쳐서 픽셀 기여도(Contribution/Weight) 수집
  * 중앙에 가까울수록 높은 기여도 + 최근 프레임일수록 높은 기여도
* 픽셀 기여도에 따른 최종 픽셀을 선별에 저해상도 프레임 생성
* 란초스 알고리즘(공간 업스케일링)으로 업스케일링
  * [Lanczos algorithm - Wikipedia](https://en.wikipedia.org/wiki/Lanczos_algorithm)

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/06.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
</div>

* 업스케일링된 프레임에 모션 벡터 적용
  * 물체가 어느 방향으로 이동하고 있는지 벡터를 기록한 맵
  * 히스토리 누적 프레임의 각 픽셀을 대응하는 모션 벡터만큼 이동
* 현재 프레임과 보간
* 이후 고스팅 완화 및 보정 작업

### 렌더링 비용 줄이기

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/07.png" width="50%" alt="post_thumbnail" style="display: inline-block;">
</div>

* 게임 프레임을 작은 스케일로 렌더링 후 업스케일링
* 렌더링 비용 감소 → 퍼포먼스 증가 → 게임이 빠릿빠릿해짐

## Frame Generation

두 개의 연속적인 렌더링 프레임 사이의 가상의 프레임을 생성하는 기술
즉, 프레임을 2배 가까이 늘리는 기술

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/08.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
</div>

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/09.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
</div>

### 광학 흐름 방정식
* [Optical flow - Wikipedia](https://en.wikipedia.org/wiki/Optical_flow)
* [광학 흐름 - 나무위키 (namu.wiki)](https://namu.wiki/w/%EA%B4%91%ED%95%99%20%ED%9D%90%EB%A6%84)

### 인풋랙 이슈
* n 프레임 + n-1 프레임 → n - 0.5 프레임 생성
  * 보간 프레임이 생성되는 시점에, 그 다음 프레임은 이미 생성되어 있다
* 프레임이 기존의 실제 출력 시간보다 느리게 출력 된다
  * 인풋랙 발생

### 일반적으로, 최소 50 fps 이상 나오는 상태에서 효과적으로 작동
* AMD FSR은 60 fps 이상을 권장
  * [AMD FidelityFX™ Super Resolution 3 (FSR 3) - AMD GPUOpen](https://gpuopen.com/fidelityfx-super-resolution-3/#:~:text=Minimum%20frame%20rate,prominent%20at%20lower%20frame%20rates.)
* [DLSS 3.0 및 FSR 3.0은 장단점을 잘 알고서 사용해야 합니다. > 그래픽카드 (coolenjoy.net)](https://coolenjoy.net/bbs/28/4813758)

### 낮은 프레임 사이에서 보간된 프레임은 부자연스럽게 보이고, 지연 시간이 더 커진다
* 프레임 사이의 시간이 길수록, 연산의 복잡도가 상승한다
* 객체 움직임과 변화는 더 커지는데, 프레임이 낮아서 Temporal Data는 부족하다. 

## DLSS (Deep Learning Super Sampling)

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/10.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
</div>

* NVIDIA 개발
* RTX 시리즈에서만 지원
* 게임 화면 수 천만 장을 DNN으로 학습시킨 알고리즘 사용
* RTX 그래픽카드의 텐서 코어를 사용해 저해상도의 이미지를 알고리즘으로 추론하여 목표 해상도로 업스케일링하는 방식
  * DLSS 업스케일링 프리셋 - [NVIDIA DLSS Updates for Super Resolution and Unreal Engine](https://developer.nvidia.com/blog/nvidia-dlss-updates-for-super-resolution-and-unreal-engine/)
* DLSS 3.0부터 프레임 제너레이션(FG) 기술 및 인풋 랙 보정 기술인 Reflex 기능 포함
* FG는 RTX 40번대만 지원
  * 40번대에 탑재된 Optical Flow 가속기 연산 필수적
  * [RTX 40 뭐가 좋아졌지? Ada GPU 아키텍처 살펴보기 > 기획기사](https://quasarzone.com/bbs/qc_plan/views/30380#p5)
* 나머지 두 기술은 RTX GPU에서 지원
  * [DLSS - Download and Get Started](https://developer.nvidia.com/rtx/dlss/get-started)

## FSR (Fidelity Super Resolution)

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/11.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
</div>

* AMD 개발
* FidelityFX 이미지 툴킷 중 하나
  * [AMD FidelityFX™](https://www.amd.com/en/products/graphics/technologies/fidelityfx.html#tabs-7e15027970-item-090aaaa054-tab)
* FSR 3.0
  * 프레임 보간 기술을 AFMF(AMD Fluid Motion Frames)으로부터 적용
    * AFMF와 FSR-FG의 차이 - [FSR 3 FG and FSR 3 (?) AMFM : r/Amd (reddit.com)](https://www.reddit.com/r/Amd/comments/172uow2/fsr_3_fg_and_fsr_3_amfm/)
  * Reflex에 대응하는 AMD Radeon Anti-Lag 포함
  * DLAA 대응하는 NATIVE-AA 모드 포함
    * 지원 목록 - [AMD FidelityFX™ Super Resolution](https://www.amd.com/en/products/graphics/technologies/fidelityfx/super-resolution.html#requirements)

## XeSS (Xe Super Sampling)

<div style="text-align:center;">
 <img src="/assets/images/Upscaling_FrameGeneration/12.png" width="100%" alt="post_thumbnail" style="display: inline-block;">
</div>

* Intel 개발
* FSR보다 더 뛰어나고 DLSS와 견줄만하다는 평가
  * DLSS처럼 선행 학습된 AI를 이용한 업스케일러
* Shader Model 6.4 이상을 지원하고 DP4a 명령어를 사용하는 GPU를 권장
  * [Will Intel® XeSS Work with Graphics Cards from Other Vendors?](https://www.intel.com/content/www/us/en/support/articles/000090041/graphics/intel-arc-dedicated-graphics-family.html)
  * 자회사 제품은 XMX 명령어 사용

## 기타

### FSR은 AI 미사용
* [AMD 임원진, 'AI(인공지능)' 기반 '인게임 업스케일링(FidelityFX Super Resolution)'을 진행 중인 힌트를 공개 > 하드웨어 뉴스](https://quasarzone.com/bbs/qn_hardware/views/1619606)

### Xe는 Frame Generation 미지원
* [XeSS를 위한 Intel 프레임 생성 기술이 곧 출시될 수 있습니다: 게임 FPS를 향상하기 위한 프레임 추정 기능을 갖춘 ExtraSS > 뉴스/신제품](https://coolenjoy.net/bbs/38/5170391)

### DLSS / FSR / XeSS 지원 게임 목록
* [List of games that support high-fidelity upscaling - PCGamingWiki PCGW - bugs, fixes, crashes, mods, guides and improvements for every PC game](https://www.pcgamingwiki.com/wiki/List_of_games_that_support_high-fidelity_upscaling)

### DLSS / FSR / XeSS 비교 (스타필드)
* [Starfield: FSR 3 vs DLSS 3 vs XeSS Comparison Review](https://www.techpowerup.com/review/starfield-xess-1-2-vs-dlss-3-vs-fsr-3-comparison/)

### Apple의 MetalFX
* [MetalFX - 나무위키 (namu.wiki)](https://namu.wiki/w/MetalFX)

### FSR 적용 시 화면 좌우가 반짝거리는 이슈
* [FSR 3 edge of screen artifacts - Development / Rendering - Epic Developer Community Forums (unrealengine.com)](https://forums.unrealengine.com/t/fsr-3-edge-of-screen-artifacts/1527174/3)

### 각 플러그인 다운로드 링크
* DLSS - [Download and Get Started](https://developer.nvidia.com/rtx/dlss/get-started)
* FSR - [AMD FidelityFX Super Resolution 3 Unreal Engine plugin guide - AMD GPUOpen](https://gpuopen.com/learn/ue-fsr3/)
* XeSS - [Releases · GameTechDev/XeSSUnrealPlugin (github.com)](https://github.com/GameTechDev/XeSSUnrealPlugin)