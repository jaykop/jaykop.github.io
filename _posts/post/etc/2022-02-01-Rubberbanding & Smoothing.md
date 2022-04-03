---
title: "Rubberbanding & Smoothing"
classes: wide
categories: 
  - post
  - etc
sidebar:
  nav: "main"
author_profile: true
---
   
## Rubberbanding
<figure class="half">
    <a href="/assets/images/{1ED93BDA-6379-4B4F-A841-A9AA03312F9B}.png"><img src="/assets/images/{1ED93BDA-6379-4B4F-A841-A9AA03312F9B}.png"></a>
    <a href="/assets/images/{66DBC664-F945-484D-A286-E4712E3162DF}.png"><img src="/assets/images/{66DBC664-F945-484D-A286-E4712E3162DF}.png"></a>
</figure>

* **그리드 기반에서 불필요한 중간 노드를 지우는 과정**
* 세 그리드 또는 지점 사이가 통과 가능한 공간인지를 확인
  * 통과 가능하면 중간 점은 리스트에서 제거

```c++
bool AStarPather::rubberbanding(
    const GridPos& first, 
    const GridPos& second,
    const GridPos& third)
{
    // 세 점이 이루는 전 영역을 대상
    int left = std::min(first.row, std::min(second.row, third.row)),
        right = std::max(first.row, std::max(second.row, third.row)),
        top = std::max(first.col, std::max(second.col, third.col)),
        bot = std::min(first.col, std::min(second.col, third.col));

    for (int i = left; i <= right; i++) {
        for (int j = bot; j <= top; j++) {

            // 해당 영역이 이동가능한지 확인
            GridPos p{i, j};
            if (terrain->is_valid_grid_position(p)
                && terrain->is_wall(p))
                return false;
        }
    }

    // otherwise,
    return true;
}
```

## Smoothing
### 곡선
![image](/assets/images/curve_formula.png)  
![image](/assets/images/img1.daumcdn.net.png)
* 두 점 A, B 사이의 점 P를 위와 같이 표현
* t에 대한 방정식
  * **1차 베지에 곡선**
  * 점 P의 집합, 즉 A와 B를 잇는 **선분**

<figure class="half">
    <a href="/assets/images/img2.daumcdn.net.png"><img src="/assets/images/img2.daumcdn.net.png"></a>
    <a href="/assets/images/img3.daumcdn.net.png"><img src="/assets/images/img3.daumcdn.net.png"></a>
    <a href="/assets/images/img4.daumcdn.net.png"><img src="/assets/images/img4.daumcdn.net.png"></a>
</figure>

* 각 점을 잇는 선분 또는 곡선 위의 점들에 대하여, 이들을 다시 서로 잇는다
* n차 베지에 곡선은 n개의 점들에 대해 밀도 t를 조절해가며 곡선을 생성할 수 있다

### 연속성
* 여러 곡선을 자연스럽게 잇는 방법
* **C0**: 전체 곡선이 연속한다
* **C1**: 곡선이 연속하고, 각 곡선이 만나는 곳의 접선 벡터가 같다
  * 0차, 1차 도함수가 연속이다
* **C2**: 곡선이 연속하고, 각 곡선이 만나는 곳의 접선 벡터가 같고, 곡률도 같다
  * 0차, 1차, 2차 도함수가 연속이다

### Spline Points
![image](/assets/images/{01A05CC8-3CA4-4FC5-A01F-A9EA746D3AF9}.png)
* 보간 스플라인의 한 종류
* 4게 제어점이 주어질 때 이들 모두를 곡선을 그리며 통과하는 선을 그린다
  * 네 개 점에서 곡선은 중간 점 2개 사이에 정의된다

### 캣멀롬 스플라인
![image](/assets/images/{3AE4B197-CA39-45D4-9060-63382DF8E7EE}.png)
* s는 밀도
* 4개 점을 대상으로 곡선을 이루는 점들을 구하는 방법

![image](/assets/images/rubberbanding_process (25).png)  
![image](/assets/images/rubberbanding_process (24).png)  
![image](/assets/images/rubberbanding_process (23).png)  
![image](/assets/images/rubberbanding_process (22).png)  
![image](/assets/images/rubberbanding_process (21).png)  
![image](/assets/images/rubberbanding_process (20).png)  
![image](/assets/images/rubberbanding_process (19).png)  
![image](/assets/images/rubberbanding_process (18).png)  
![image](/assets/images/rubberbanding_process (17).png)  
![image](/assets/images/rubberbanding_process (16).png)  
![image](/assets/images/rubberbanding_process (15).png)  
![image](/assets/images/rubberbanding_process (14).png)  
![image](/assets/images/rubberbanding_process (13).png)  
![image](/assets/images/rubberbanding_process (12).png)  
![image](/assets/images/rubberbanding_process (11).png)  
![image](/assets/images/rubberbanding_process (10).png)  
![image](/assets/images/rubberbanding_process (9).png)  
![image](/assets/images/rubberbanding_process (8).png)  
![image](/assets/images/rubberbanding_process (7).png)  
![image](/assets/images/rubberbanding_process (6).png)  
![image](/assets/images/rubberbanding_process (5).png)  
![image](/assets/images/rubberbanding_process (4).png)  
![image](/assets/images/rubberbanding_process (3).png)  
![image](/assets/images/rubberbanding_process (2).png)  
![image](/assets/images/rubberbanding_process (1).png)  

### 오류
![image](/assets/images/{3A358BB3-8D0C-4799-8E7C-3FA8728B062C}.png)  
* 그리드 간 World Distance를 1로 잡았을 때, Rubberbanding 후의 각 점 사이의 거리가 1.5배 이상이면 Smoothing 시 오류가 발생한다

![image](/assets/images/{B7E890C3-A051-4B3D-A264-5DF75D2950AF}.png)  
* 이 경우 back points를 새로 삽입해준다
  * 기존에 있던 point 들의 중간 지점을 몇 개 더 배치한다
* 그 다음 스무싱을 해준다

## 출처
* <https://tsyang.tistory.com/57>
* <https://ko.wikipedia.org/wiki/%EC%BA%A3%EB%A9%80%EB%A1%AC_%EC%8A%A4%ED%94%8C%EB%9D%BC%EC%9D%B8>