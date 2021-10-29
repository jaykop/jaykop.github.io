---
title: "Lighting Effect"
classes: wide
categories: 
  - post
  - Graphics
sidebar:
  nav: "main"
author_profile: true
---
   
## Light Source Type    
* **Point light**

  ![post_thumbnail](/assets/images/pointlight.png)
  - 광원 지점에서 전 방향으로 빛을 발사
  - 광원으로부터 멀어질수록 attenuation 공식에 따라 밝기 조정
    - lighting position에 의존적
  - constant, linear, quadratic, distance에 따라 연산
  - ex) 전구

* **Directional light**

  ![post_thumbnail](/assets/images/directionallight.png)
  - 빛의 방향성과 색만을 가지고 연산
    - 광원과의 거리가 무한정으로 멀다는 가정
    - 물체 표면에 도달하는 빛의 방향은 모두 평행
    - attenuation은 고려하지 않음
  - ex) 태양광

* **Spotlight**

  ![post_thumbnail](/assets/images/spotlight.png)
  - 광원지점에서 특정 방향으로만 빛을 발사
    - **cut off angle**
    - 빛의 진행 모형은 cone과 유사
  - point light와 마찬가지로 attenuation 공식에 따라 밝기 조정
  - 특정 방향/각도에서의 라이팅 이펙트가 강조되도록 spotlightEffect 연산
  - **innerAngle**
     - 강조되는 내부 원뿔 영역 
     - 빛의 intensity가 일정
  - outerAngle 
    - 점점 흐려지는 외부 원뿔 영역
    - outerAngle의 외부 빛의 intensity = 0
  - 빛 강도를 0 - 1사이로 clamp

## Lighting and Material
* 각 lighting map을 모두 합산한 결과 값으로 빛 효과 연산

* **Ambient**

  ![post_thumbnail](/assets/images/ambient.png)
  - 주변광, 광원이 불분명한 빛
    - Lighting Direction을 정의할 수 없음
  - 일정한 밝기와 색으로 표현 가능
  - **I_ambient = I_a * K_a**
    - **I_a**: ambient lighting의 세기
    - **K_a**: ambient lighting이 최종 표면에 도착하기 까지 몇 번의 반사를 거쳤는지의 coefficient

* **Diffuse**

  ![post_thumbnail](/assets/images/diffuse.png)
  - 빛으로부터 곧장 들어와 물체 표면에 뿌려짐
    - 물체의 표면에서 분산되어 눈으로 들어오는 빛
  - 각도에 따라 밝기가 다름
  - **I_diffuse = I_d * K_d * cosθ = I_d * K_d * (N*L)**
    - **I_d**: diffuse lighting의 세기
    - **K_d**: 물체 표면 반사에 대한 coefficient
    - **N**: face normal unit vector
    - **L**: 물체 표면에서 광원 방향으로의 unit vector
    - **θ**: face normal과 L의 사이각
  - N과 L의 사이각이 90보다 커지면 diffuse 의 값은 0
    - I_diffuse = I_d * K_d * max(N*L, 0) 과 같이 조정
  - diffuse 값의 연산은 viewer를 고려하지 않고 연산하기 때문에 viewer의 위치 및 각도로부터 독립

* **Specular**

  ![post_thumbnail](/assets/images/specular.png)    
  - diffuse와 동일하게 광원에서 직접 들어오는 빛
    - 그러나 특정한 방향으로 완전히 반사되는 빛
    - viewer의 위치에 따라 달라짐
  - 흰색의 광으로 표현

  ![post_thumbnail](/assets/images/spec_vectors.png)    
  - **I_specular = I_s * K_s * (R*L)^ns**
    - **I_s**: specular lighting의 세기
    - **K_s**: 물체 표면 반사에 대한 coefficient
    - **R**: reflection unit vector
    - **V**: 물체 표면에서 viweer 방향으로의 unit vector
    - **ns**: 표면 질감에 따라 반사되는 광량이나 범위를 조절하는 index

  ![post_thumbnail](/assets/images/emissive.png)
* **Emissive**
  * 오브젝트가 스스로 발산하는 빛
    * 다른 빛에 의해 영향을 받지 않음
    * Material의 속성일 뿐, 광원이 발산하는 빛이 아님

## Shading
* **Phong lighting**
  * 라이팅 이펙트를 픽셀이 아닌 버텍스 단위로 연산
* **Phong shading** 
  * 라이팅 이펙트를 픽셀 단위로 연산
* **Blinn shading** 

  ![post_thumbnail](/assets/images/phong1.png)
  ![post_thumbnail](/assets/images/phong2.png)
  * 퐁 쉐이딩에서 리플렉션 벡터를 이용하는 대신 하프 벡터를 이용
    * **Half Vector = Lighting Vector + Viewer Vector**
  * 더 광범위하고 평평한 표면에 대해 연산이 표율적
    * Reflection Vector(R)를 일일이 연산할 필요 없음
    * 광원과 viewer가 물체로부터 어느 정도 멀더라도, V와 L은 상수
  * specular 값의 왜곡을 방지
* **Lighting Direction** = -(Lighting Vector)
  * 광원에서 fragments로 향하는 벡터
  
## 출처
* <https://learnopengl.com/Lighting/Lighting-maps>
* <https://learnopengl.com/Lighting/Light-casters>  
* <https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=edgerider&logNo=110147438518>