---
title: "Prototype Pattern"
classes: wide
categories: 
  - post
  - Pattern
sidebar:
  nav: "main"
author_profile: true
---
   
## 프로토타입 디자인 패턴
* 여러 몬스터 타입과 각 몬스터를 소환하는 Spwaner를 디자인해보자

```c++
// 몬스터 타입
class Monster
{
  // ...
};
class Ghost : public Monster {};
class Demon : public Monster {};
class Sorcerer : public Monster {};

// 스포너 타입
class Spawner
{
  public:
  ~Spawner() {}
  virtual Monster* spawnMonster() = 0;
  // ...
};
class GhostSpawner : public Spawner {
  public: 
  Monster* spawnerMonster() override
  {
    return new Demon();
  }
};
class DemonSpawner : public Spawner { /*...*/ };
class SorcererSpawner : public Spawner { /*...*/ };
```

* 위 방식의 코드는 비효율적이다
* **어떤 객체가 자기와 비슷한 객체를 스폰할수만 있으면 된다**

```c++
class Monster
{
  public:
  virtual ~Monster() {}
  virtual Monster* clone() = 0;

  // 그 외...
}

class Ghost : public Monster
{
  public:
  Ghost(int health, int speed)
  : health_(health), speed_(speed) {}
   Monster* clone() override
  {
    return new Demon(health_, speed_);
  }

  private:
  int health_;
  int speed_;
}

// 개인적으로는 그냥 spawnerMonster 함수에 
// monster를 인자로 넣어도 되지 않을까 싶다
class Spawner
{
  public:
  Spawner(Monster* prototype) : prototype_(prototype) {}
  Monster* spawnerMonster() 
  {
    return prototype_->clone();
  }

  private:
  Monster* prototype_;
}

// 이제 아래와 같이 써먹을 수 있다
Monster* ghostPorototype = new Ghost(15, 3);
Spawner* ghostSpawner = new Spawner(ghostPorototype);
```
* 위의 clone 함수 추가로 하위 상속 객체들은 clone을 재사용할 수 있다
  * Ghost 타입 class 처럼
* 따라서 스포너도 하나만 만들면 된다
  * 스포너는 Monster의 **상태까지 그대로 복사**해 생성한다
* **하지만 clone 함수를 매 class 마다 만들어야 한다**
  * Deep copy, Shallow copy의 애매모호함도 있다
  * 요즘 엔진에서는 Monster마다 클래스를 만들지 않는다 **(?!?!)**
    * 컴포넌트 조합이나 타입 객체로 모델링한다고 한다

### 방법 1 - 스폰 함수

```c++
// 특정 타입의 Monster를 스폰하는 함수
Monster* spawnGhost()
{
  return new Ghost();
}

// 스폰 함수 포인터를 받는 스포너
typedef Monster* (*SpawnCallback)();
class Spawner
{
  public:
  Spawner(SpawnCallback spawn) : spawn_(spawn) {}
  Monster* spawnMonster() { return spawn_(); }

  private:
  SpawnCallback spawn_;
}

// ghost를 스폰하는 스포너 생성
Spawner* ghostSpawner = new Spawner(spawnGhost);
```

### 방법 2 - 탬플릿

```c++
class Spawner 
{
  virtual ~Spawner() {};
  virtual Monster* spawnMonster() = 0;
};

template <class T>
class SpawnerFor : public Spawner
{
  public:
  virtual Monster* spawnMonster() { return new T(); }
};

// ghost를 스폰하는 스포너 생성
Spawner* ghostSpawner = new SpawnerFor<Ghost>();
```
* 탬플릿 구조를 이용해 타입 T를 생성하는 스포너는 위와 같이 디자인할 수 있다
* **Spawner 클래스를 상위로 따로 두는 이유**
  1. 생성하는 몬스터 종류에 상관없이 Monster 포인터만으로 작업하는 코드를 Spawner 클래스에서 쓸 수 있기 때문
  2. 상위 클래스인 Spawner가 없다면 몬스터를 스폰하는 코드에서 매번 탬플릿 매개변수를 추가해야 한다
  => 무슨 말이지...?

### 일급자료형
* C++가 아닌 자바스크립트, 파이썬, 루비 등 클래스가 전달 가능한 일급 자료형인 동적 자료형 언어에서는 이보다 더 간단하게 작업할 수 있다고 한다
* 원하는 몬스터 클래스의 런타임 객체를 함수에 전달하면 된단다

