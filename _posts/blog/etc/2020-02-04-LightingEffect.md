---
title: "Lighting Effect"
classes: wide
categories: 
  - blog
  - etc
---
   

Lighting effect
Phong lighting - 라이팅 이펙트를 픽셀이 아닌 버텍스 단위로 연산
Phong shading - 라이팅 이펙트를 픽셀 단위로 연산
Blinn shading - 퐁 쉐이딩에서 리플렉션 벡터를 이용하는 대신 하프 벡터를 이용해 스페큘러 값의 왜곡을 방지
lighting direction = from lighting source towards the fragments
각 lighting map을 모두 합산한 결과 값으로 빛 효과 연산
specular
완전히 반사되는 빛
흰색의 광으로 표현
diffuse
물체의 표면에서 분산되어 눈으로 들어오는 빛
각도에 따라 밝기가 다름
ambient
주변광, 광원이 불분명한 빛
일정한 밝기와 색으로 표현 가능
Point light
광원 지점에서 전 방향으로 빛을 발사
광원으로부터 멀어질수록 attenuation 공식에 따라 밝기 조정
constant, linear, quadratic, distance에 따라 연산
Directional light
태양광, 빛의 방향성만을 가지고 연산
Spotlight
광원지점에서 특정 방향으로만 빛을 발사
point light와 마찬가지로 attenuation 공식에 따라 밝기 조정
특정 방향/각도에서의 라이팅 이펙트가 강조되도록 spotlightEffect 연산
innerAngle - 강조되는 내부 원뿔 영역
outerAngle - 점점 흐려지는 외부 원뿔 영역
빛 강도를 0 - 1사이로 clamp

  
---  
출처:   
<https://m.blog.naver.com/PostView.nhn?blogId=shakey7&logNo=221435517430&proxyReferer=https:%2F%2Fwww.google.com%2F>  
