---
title: "Linear Transformation (2)"
classes: wide
categories: 
  - post
  - Math
sidebar:
  nav: "main"
author_profile: true
---

## 크기 변환
![image](/assets/images/{D8DFD133-C6B2-4BEB-9A61-22821624A595}.png)
* 벡터의 크기와 방향 중 크기만 변경하는 것
* 각 성분에 각 계수만큼의 크기를 곱해 양을 바꿈

![image](/assets/images/{21776676-9CA6-4F38-8A24-4AAD9EDAF4DD}.png)
* 각 기저벡터에 대해 주대각성분 a, b, c 만큼의 양을 곱한 변환행렬

![image](/assets/images/{4494BB41-4CFF-4EE8-9225-524B9CC22A19}.png)
* 행렬 곱셈은 위와 같다
* a, b, c가 모두 값이 같으면 모든 축에 대해 동일 비율로 크기를 변환하는 것이다
    * 이를 균등 크기 변환 uniform scaling 혹은 isotropic scaling 이라 한다
    * 크기가 다른 변환은 비균등 크기 변환 non-uniform scaling 혹은 anisotropic scaling이라 한다

### 크기 변환 역행렬
![image](/assets/images/{6886A339-6069-4F51-BE99-CC74628E525C}.png)
* a만큼 크기를 변환했으면, 1/a만큼 다시 변환시킨다

## 회전 변환
* 얼마나 회전할지, **회전의 양**
* 무엇을 기준으로 회전할지, **회전의 축**

![image](/assets/images/{04104D4B-401B-48E1-BABA-03FC61D89DC6}.png)
* 반시계, 시계 방향으로 회전할지의 결정 여부는 좌표계

### 좌표 축 기준 (z축 기준)
<figure class="half">
    <a href="/assets/images/{61675859-06D6-482F-9A49-2A5F8BFB1021}.png"><img src="/assets/images/{61675859-06D6-482F-9A49-2A5F8BFB1021}.png"></a>
    <a href="/assets/images/{CB4E07F5-8343-4B15-84B3-017D4E62398D}.png"><img src="/assets/images/{CB4E07F5-8343-4B15-84B3-017D4E62398D}.png"></a>
</figure>

![image](/assets/images/{4E0BBEAC-CA15-4245-AB2F-EAFC6359CB06}.png)
* 회전 축인 z축 성분에는 변화가 없다
* 극좌표계 polar coordinate를 통해 위와 같은 연관 식이 성립한다

<figure class="half">
    <a href="/assets/images/{E19CF922-EC5C-4D1B-BF35-D31D150BE626}.png"><img src="/assets/images/{E19CF922-EC5C-4D1B-BF35-D31D150BE626}.png"></a>
    <a href="/assets/images/{10EFBCFC-A8CF-4714-BA6C-C91C36317CEF}.png"><img src="/assets/images/{10EFBCFC-A8CF-4714-BA6C-C91C36317CEF}.png"></a>
</figure>

![image](/assets/images/{E7FFDA22-041E-44C3-B6BE-59B10199EB91}.png)
* 벡터의 극좌표계 표현식과 삼각함수의 성질을 이용해 회전 변환 T를 구할 수 있다

![image](/assets/images/{2CF817F5-5991-4801-A9FB-1C6E128C5036}.png)
![image](/assets/images/{DC97822F-C0C6-44D7-9FD4-6FBA8305716D}.png)
![image](/assets/images/{5158B116-B461-4875-9E57-8DE53959E86A}.png)
* 기저벡터 i,j,k를 두고 식을 간소화한 뒤 변환행렬을 위와 같이 구할 수 있다
* 같은 받법으로 x, y축에 대한 회전 행렬도 구할 수 있다

### 축 회전 변환 역행렬
![image](/assets/images/{7D9B8878-9907-435F-874F-7106D6C4C9DE}.png)
* x축에 대한 회전 행렬의 역행렬
    * a만큼 회전했으면, 다시 -a만큼 회전시킨다

* 회전 변환 행렬이 **직교 행렬**이라는 점을 이용할 수도 있다
* 직교 행렬 - 행렬의 각 열/행벡터들이 서로 정규 직교
    * 길이가 모두 1
    * [상호 수직인 경우](https://jaykop.github.io/post/math/Vector/#%EB%82%B4%EC%A0%81%EC%9D%98-%EC%82%AC%EC%9A%A9-%EC%98%88%EC%8B%9C)
* **직교 행렬의 역행렬은 그 행렬의 전치행렬과 같다**
    * 어떤 행렬의 행과 열을 뒤바꾸면 전치 행렬 transpose matrix라 한다

### 임의의 축 기준
![image](/assets/images/{3291487E-0D15-420C-AF46-AD80D797E9F6}.png)
* 벡터 v를 축 a에 대해 degree a만큼 회전변환
* 벡터 a가 단위벡터인 경우의 위의 식이 성립

![image](/assets/images/{D21DBCAB-D89D-42F9-A9F3-7E4F23F399D6}.png)
* 변환된 벡터 R_a(v)는 축의 단위벡터인 v_proj와 v_perp를 회전시킨 R_a(v_perp)의 합

![image](/assets/images/{53F4F68D-AEA7-4CD3-A71C-ADD8CEE32C6C}.png)
* 위의 그림을 통해서 벡터 w를 표현할 수 있다

![image](/assets/images/{8037B35B-4F9C-46D4-9B23-B3812CE0B000}.png)
* w와 v_perp 두 축을 기준으로 평면 좌표를 새로 생성하면 위와 같이 표한할 수 있다
* r1과 r2 두 벡터를 구해보자

![image](/assets/images/{6ECF636B-4FE7-4B73-8FE0-A2F92F7171E3}.png)
* r1의 길이는 위와 같이 표현가능하다
* R_a(v_perp)가 아닌 v_perp가 쓰인 이유는, 두 벡터는 상호 회전 변환만을 거쳤기 때문
    * 즉, 길이가 같기 때문
    * 그림 4-6 참조

![image](/assets/images/{20C09059-99E0-4638-97A5-01590AE0CAFC}.png)
![image](/assets/images/{28B3B3B5-383E-452C-BD80-9FF32E1205F9}.png)
* r2 역시 위와 같이 구할 수 있다
* 벡터 w의 길이는 마찬가지의 이유로 v_perp와 그 길이가 같다
    * 위의 식 표현은 그냥 역순으로 이해하는 게 속이 편하다
    * 그림 4-7 참조
* R_a(v_perp)가 아닌 v_perp가 쓰인 이유는, 두 벡터는 상호 회전 변환만을 거쳤기 때문
    * 마찬가지로 길이가 같기 때문
    * v_perp 역시 w를 회전만 했으므로, 길이는 같다

![image](/assets/images/{8CF4A8E8-37A5-4D1F-91C9-E3AF632C6006}.png)
* 이제 R_a(v_perp)를 위와 같이 표현할 수 있다

![image](/assets/images/{E1241DDE-5308-4403-977C-23F5279C2222}.png)
![image](/assets/images/{966CCDA8-C38F-4B91-9FAD-07E44CEC3C81}.png)
* 그리고 위의 푀종 식이 로드리게스 회전 공식 Rodrigues' rotation formula라고 한다
* 아래 행렬은 임의의 축에 대한 회전 변환 행렬이다
* 여기는 나도 잘 모르겠다
    * 선형 변환의 조합과 행렬곱셈도...