---
title: "Singleton 패턴"
classes: wide
categories: 
  - post
  - etc
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## Singleton
* 오직 한 개의 instance만을 갖도록 보장
  * 전역 상태를 관리하는 클래스에게 필요

```c++
class FileSystem 
{
  public :
    static FileSystem& instance() 
    {
      // 게으른 초기화
      if (instance == NULL) 
      {
        instance = new FileSystem();
      }
      return *instance;
    }

    // 또는
    static FileSystem& instance() 
    {
      // 정적 지역 변수 초기화 코드가 한번만 실행
      static FileSystem *instance  = new FileSystem();
      return *instance;
    }

  private :
    // 생성자를 private으로 제한해 
    // 외부에서 객체 생성이 불가
    FileSystem() {}
    static FileSystem*  instance;
}；
```

## 싱글턴 사용하는 이유?
* 사용하지 않으면 생성하지 않는다
* 런타임에 초기화
  * 정적 멤버 변수는 자동 초기화의 문제가 발생
    * 컴파일러는 main 함수를 호출하기 전에 정적 변수를 초기화
  * 클래스가 필요한 정보를 미리 사용할 수 없음
    * 싱글턴 패턴은 최대한 늦게 초기화됨
* 상속이 가능

## 기피되는 이유?
* 싱글턴은 결국 전역변수이다
  * 전역 변수는 코드 가독성을 저하시킨다
  * 함수 코드와 매개변수만으로 구성된 코드를 보는 것이 좋다
* 커플링을 조장한다
  * 참조 헤더파일만 추가하면 어디에서나 접근 가능한 기능이 되어버린다
  * 모듈 간의 상호 의존성을 증가시킨다
* 멀리스레딩에 맞지 않다
  * Deadlock이나 Race condition을 유발할 수 있다
* 사용빈도가 높아짐에 따라 추후에 코드 수정이 어렵다
* 게으른 초기화는 초기화 시점을 명확히 하는 데 방해가 된다

## 대안?
1. 객체를 총괄하는 클래스 필요성에 대한 의문
  * 어줍잖은 싱글턴은 다른 클래스의 Helper에 그치는 경우가 많다
  * 객체가 스스로를 챙기도록 하는 것이 진정한 OOP

```c++
class Bullet {
  public:
    int getX() const { return x_; } 
    int getY() const { return y_; } 
    void setX(int x) { x_ = x; } 
    void setY(int y) { y_ = y; }
  private:
    int x_;
    int y_;
};

// 굳이 BulletManager가 필요한가?
class BuUetManager {
  public :
  Bullet*  create(int x, int y) 
  {
    Bullet*  bullet = new BulletQ;
    bullet->setX(x); 
    bullet->setY(y); 
    return bullet;
  }
  
  bool isOnScreen(BuUet& bullet) 
  {
    return bullet.getX() >= 0 && 
    bullet.getY() >= 0 && 
    bullet.getX() < SCREEN.WIDTH && 
    bullet.getY() < SCREEN-HEIGHT;
  }
  
  void move(Builet& bullet) 
  {
    bullet.setX(bullet.getX() + 5);
  }
};

// Manager의 기능을 Bullet이 가지게 디자인
class Bullet {
  public:
  Bullet(int x, int y) : x_(x), y_(y) {}
  
  bool isOnScreen() {
    return x_ >= 0 && x_ < SCREEN_WIDTH && 
    y_ >= 0 && y_ < SCREEN_HEIGHT;
  }
  
  void move() { x_ += 5; }
  
  private:
    int x_; 
    inr y_;
};
```

2. 하나의 객체만을 보장하는 방법
  * 필요한 정보를 상위 클래스로부터 상속받거나 매개변수로 받기
  * 이미 전역인 객체로부터 받기
