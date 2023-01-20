---
title: "Navigation Theory"
classes: wide
categories: 
  - post
  - Unreal
  - A.I.
sidebar:
  nav: "main"
author_profile: true
---
   
## Navigation with AI
길찾기를 통해 주변 환경을 헤쳐나가는 건 AI의 기본이지만 단순히 A 지점에서 B 지점으로 이동하는 것은 마냥 쉬운 일은 아니다. 길찾기는 경로 탐색과 장애물 회피로 2 단계로 나눌 수 있다. 여기서 장애물이란 고정된 상태의 물체로 정의한다. 이런 장애물을 회피하기 위해 Navigation Mesh가 필요하다.

![post_thumbnail](/assets/images/2c02ec98-841d-478f-973b-8a911f7163cb.png)

### The Navigation Mesh
Navigation Mesh는 길찾기를 위해 사용된다. 이 Mesh는 AI가 접근할 수 있는 표면적을 나타내며, 여러 Convex Polygon의 집합체로 구성되어 있다.

### Precalculated Data
게임 시작 전 미리 Baked된 Navigation Mesh는, 3D의 복잡한 충돌 정보를 하나의 2D 폴리곤 메쉬로 잘 옮겨 놓은 번역본이라고 할 수 있다. 이는 Navigation 사용에 있어 비용 부담을 줄이고 특히 실시간 시뮬레이션에서 다수의 AI Agent들이 무리 없이 작동하는 데 기여한다.

AI가 전처리된 Navigation Mesh를 사용하기 위해서는 아래 과정이 필요하다

1. **Adding the Navigation Mesh**

![post_thumbnail](/assets/images/440b9e19-4704-4f19-b11a-78691024f088.png)

* NavMeshBoundVolume을 레벨에 배치한다

2. **Define the mesh size**

![post_thumbnail](/assets/images/2dcd5547-bd5a-4685-a3fb-f49967752d62.png)

* 레벨에 배치한 NavMeshBoundVolume의 사이즈를 조정한다.
* NavMeshBoundVolume의 크기는 레벨 안에서 AI가 이동할 수 있는 모든 구간을 커버할 수 있도록 설정해야 한다.


3. **Baking the Navigation**

![post_thumbnail](/assets/images/6fe224a6-757b-43d6-9e5d-884e0b77e739.png)

* NavMesh를 배치하면 자동으로 빌드 된다.
* P키를 눌러 에디터 상태에서 어느 부분에 NavMesh가 세팅되었는지 볼 수 있다.

![post_thumbnail](/assets/images/12b29839-cb17-4335-bd96-210804604282.png)

* 만약 에디터에서 NavMesh를 자동 빌드하는 기능이 꺼져 있다면 위의 방법으로 수동 빌드를 할 수 있다.


4. **RecastNavMesh**

![post_thumbnail](/assets/images/af519506-730b-46c9-ab2e-52fbb28a7022.png)

* NavMesh를 레벨에 생성하면서 자동으로 추가된 Recast NavMesh를 선택하고 Draw Offset 값을 조절하면, 오브젝트에 가려진 NavMesh도 어디에 배치되었는지 확인할 수 있다.
* Agent Height, Agent Radius 등의 값을 입력 받아 NavMesh를 돌아다닐 AI의 크기를 측정하고 레벨의 NavMesh를 재정의 한다.


5. **NavModifier Volume**

![post_thumbnail](/assets/images/ca8d72a5-f615-411b-82d6-06ab34a41b76.png)

* **NavArea_Null**
  * 통과 불가능한 지역
* **NavArea_Obstacle**
  * 통과 비용이 높은 지역
  * 우선 경로가 이용 불가능일 때 사용하는 차선 경로
* **NavArea_LowHeight**
  * 천장이 낮은 지역
  * 웅크리거나 기어가야 통과할 수 있는 지역
* **NavArea_Default**
  * 기본 설정과 동일


6. **Supported Agents**

![post_thumbnail](/assets/images/f31c7fe5-5a3b-447c-9ed9-4896eb979d5f.png)

* 다양한 타입의 Agent와 NavMesh를 동시에 한 레벨에서 운용할 수도 있다.
* 타입에 따라 사용하는 NavMesh를 다르게 할 수 있다.

## Strengths and Weaknesses of Baked Navigation
### 장점
* 전처리된 Navigation은 빠르고 예상 가능한 결과를 도출한다
* Static Object에 대한 장애물 회피 연산 비용이 런타임에서 미미하다
* 모든 AI에 대해 한번에 공통적으로 적용된다.

### 단점
* Navigation Mesh는 실시간 변경을 할 수 없다
* Dynamic 객체인 플레이어나 다른 AI에 대한 회피는 제공하지 않는다
* 길찾기 자체는 Navigation Mesh 내부가 아닌 다른 시스템에 의해 처리된다.

## 출처
* <https://dev.epicgames.com/community/learning/courses/67R/unreal-engine-introduction-to-ai-with-blueprints/DYXe/navigation-theory>