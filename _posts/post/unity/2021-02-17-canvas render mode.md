---
title: "Canvas"
classes: wide
categories: 
  - blog
  - unity
sidebar:
  nav: "main"
author_profile: true
---
   
## Canvas
* Unity에서 모든 UI 객체를 렌더링 하기 위한 루트 컴포넌트
* 기본적으로 4개의 컴포넌트를 포함
  1. RectTransform
  2. Canvas
  3. Canvas Scaler
  4. Graphic Raycaster

## RectTransform 
* Anchor가 기준점
* 다양한 프리셋을 제공해 부모 UI에 어떻게 종속될 것인가를 결정 가능
* transform 정보를 컨트롤할 때, ahchor가 prefix된 데이터를 이용하는 것을 권장

## Graphic Raycaster
* Overlap 되는 Object(Graphics)가 있을 때, 이를 통과해서 picking 될지 말지를 체크하는 toggle

## DrawMode
1. **Screen Space - Overlay**  
![post_thumbnail](/assets/images/CanvasOverlay.png)
  * 씬 / 카메라 뷰에 상관없이 스크린 사이즈를 기준으로 스케일링
  * 스크린 해상도가 변경되면 UI는 자동으로 리스케일링
  * UI는 다른 DrawMode의 그래픽스보다 후순위에 렌더링(화면 제일 앞에 위치)
2. **Screen Space - Camera**  
![post_thumbnail](/assets/images/CanvasCamera.png)
  * 카메라 뷰를 기준으로 일정 거리를 유지하면서 렌더링
  * 거리에 따라 스케일링 되는 것이 아니라, 카메라의 Frustum을 기준으로 스케일링
  * 스크린 해상도 혹은 카메라 frustum이 변경되면 리스케일링
  * 월드 오브젝트 / UI 오브젝트 구분없이 순수하게 거리 순으로 렌더링
3. **World Space**   
![post_thumbnail](/assets/images/CanvasWorldSpace.png)
  * UI를 월드 오브젝트와 동일하게 처리
  * RectTransform으로 여전히 컨트롤할 수 있음
  
## 출처
* <https://sunghojang.tistory.com/13>
* <https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/class-Canvas.html?>
* <https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=pxkey&logNo=221558646854>
* <https://wergia.tistory.com/223>
