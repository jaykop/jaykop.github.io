---
title: "Flyweight Pattern"
classes: wide
categories: 
  - post
  - Pattern
sidebar:
  nav: "main"
author_profile: true
---
   
### 첫번째 예제
* 공유할 수 있는 데이터를 하나의 객체, 즉 공유 객체로 통합해서 관리
* 각 인스턴스는 공유 객체를 참조하기만 하고 상태 값은 인스턴스에 저장

```c++
// 수 많은 나무를 렌더링 하기 위해 나무의 클래스를 정의

// 공유 객체를 통해 중복 데이터를 참조하도록 한다
class TreeModel
{
  private:
  Mesh mesh_;
  Texture bark_;
  Texture leaves_;
}

// 각 인스턴스
class Tree
{
  private: 
  TreeModel* model_;

  Vector position_;
  double height_;
  double thickness_;
  Color barkTint_;
  Color leafTint_;
}
```
### 인스턴스

![image](/assets/images/{D5F2B8D0-DEF7-496F-B38C-224A5384A8A3}.png)  
* 주메모리에 객체를 저장하기 위해 위의 패턴은 충분
* 그러나 GPU가 렌더링 하기 위해 사용할 버스는 여전히 부담
  * **Instance Rendering**을 통해 그래픽카드나 API가 공유 데이터 사용하도록 지원
  * 공유 데이터를 딱 한 번만 CPU에서 GPU로 전송
  * 두 개의 데이터 스트림을 통해 각각 공유 객체와 인스턴스 목록 + 매개변수들이 전송
* 이 예제는 메모리 크기보다는 전송 시간이 더 중요
  * 그러나 이 문제를 해결하기 위한 방법이 경량 패턴과 동일

## 경량 패턴
* 어떤 객체의 수가 너무 많아 이를 가볍게 만들고 싶을 때 사용
* 공유 데이터를 **고유 상태 intrinsic state**나 **자유문맥 context-free**라 한다
* 나머지 데이터를 인스턴스 별로 값이 다른 **외부 상태 extrinsic state**라 한다

### 두번째 예제
* 그리드 기반의 World와 이를 구성하는 Terrain을 만들고자 한다
* 2x2 array를 모두 Terrain 객체 데이터로 채우는 짓은 하지 않는다

```c++
// 지형 클래스
class Terrain
{
  public:
  Terrain (int movementConst, bool isWater, Texture tex)
  : movementConst_(movementConst),
  isWater_(isWater_),
  tex_(tex)

  int getMovementConst() const { return movementConst_;}
  bool isWater() const { return isWater_; }
  const Texture& getTexture() const { return tex; }

  private:
  int movementConst_;
  bool isWater_;
  Texture tex_;
}

// World 클래스
class World
{
  public:
  World()
  : grassTerrain_(1, false, GRASS_TEXTURE),
  grassTerrain_(1, false, GRASS_TEXTURE),
  grassTerrain_(1, false, GRASS_TEXTURE) {}

  private:
  Terrain* terrain_[WDITH][HEIGHT];
  Terrain grassTerrain_;
  Terrain hillTerrain_;
  Terrain riverTerrain_;

  // 지향을 생성하는 함수
  void generateTerrain()
  {
    // ...
  }
  // ...
}
```

![image](/assets/images/{5D8CC3FD-262C-4534-B084-5A5F9AE57B3F}.png)  
* 이로써 World의 Terrain은 3개의 공유 데이터를 Terrain 인스턴스 포인터가 가리키면서 이루어진다
* Life cycle 관리를 위해 3개의 공유 데이터는 World에 저장한다

### 성능
* 포인터를 통한 접근은 캐시 미스를 유발할 수 있어 성능 면에서 조금 부족한 건 사실이다
  * 간접 조회 indirect lookup
* 메모리에 객체가 배치되는 구조에 따라 퍼포먼스는 달라질 수 있다
  * 애매하면 두 방법 모두 측정한 뒤 결정하라
  * 프로파일링을 해본 뒤 하드코딩을 해도 늦지 않다
* 객체 복사를 줄이면서도 객체 지향 방식을 추구할 수 있다