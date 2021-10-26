---
title: "AssetBundle"
classes: wide
categories: 
  - post
  - unity
sidebar:
  nav: "main"
author_profile: true
---
  
## 에셋번들
![post_thumbnail](/assets/images/24306D4A5837A29D28.jfif)
* 유니티 프로젝트에 사용할 리소스들을 묶은 것
  1. 유니티에서 에셋 번들 생성
  2. 외부 스토리지(서버)에 저장
  3. 프로젝트의 런타임 중 번들을 다운로드
  4. 다운로드한 번들에서 개별 에셋을 로드해 사용

## 에셋번들을 사용하는 이유
* 유니티 게임을 빌드 시 실행파일와 에셋은 별도로 수정이 불가능
* 에셋만 수정하여 게임을 다시 빌드할 필요 없이 개별로 관리가 가능
* 모바일 환경에서 작은 단위로 에셋 번들을 개별 관리하여 용량 관리에 용이

## 출처
* <https://itmining.tistory.com/54>
* <https://blogs.unity3d.com/kr/2020/04/09/learn-to-save-memory-usage-by-improving-the-way-you-use-assetbundles/>
* <https://jingonpark-gameclient.tistory.com/16>