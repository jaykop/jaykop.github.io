---
title: "Observer Pattern"
classes: wide
categories: 
  - post
  - design_pattern
sidebar:
  nav: "main"
author_profile: true
---

### 관찰자 패턴의 사례
* [MVC 패턴](https://jaykop.github.io/post/etc/MVC/#mvc-%ED%8C%A8%ED%84%B4)
* C#의 event
* java의 라이브러리

### 예제
* 특정 기능을 담당하는 코드는 한 데 모아두는 것이 좋다. 하지만...
* 어떤 조건을 만족하는지 체크 하기 위한 코드를 여기저기에 써야하는 상황에서는?
  * 충돌 검사 코드에도 넣어야 한다면?
* 관찰자 패턴을 통해 조건을 만족하는지 여부를 알림을 통해 알 수 있다

```c++
// 어떤 게임 오브젝트의 상태를 업데이트 하는 Physcis 클래스의 함수
void Physics::updateEntity(Entity& entity)
{
  bool wasOnSurface = entity.isOnSurface();
  
  // 물리 엔진 코드는 침범하지 않는다
  entity.accelerate(GRAVITY);
  entity.update();

  // 유저의 다리에서 떨어지기 업적을 체크하는 코드
  // 리시버가 있든 없든 계속 알림을 보낸다
  if (wasOnSurface && !entity.isOnSurface())
  {
    // 어떤 알림을 보내야하는지는 알아야 한다
    // 완전한 디커플링은 아니다
    // **실제로는 이렇게 작성하지 않을 것이다...**
    notify(entity, ENVET_START_fALL);
  }
}
```

* 위의 방법으로 물리엔진의 작동 코드 자체는 건드리지 않는다
* entity를 업데이트하면서 observer가 subject의 status를 업데이트 하도록 요청한다
  * 어떤 observer가 이를 수행할지는 Physics도 entity도 모른다

## 작동 원리
### 관찰자

```c++
class Observer
{
  public: 
    virtual ~Observer() {};
    // entity - Invoker: 누가, 어떤 대상Subject 이 함수를 실행시켰는가?
    // event - message: Observer 함수 쪽에서 norify 함수를 받아서 실행시킬 때 필요한 정보
    virtual void onNotify(const Entity& entity, Event event) = 0;
}
```
* 어떤 클래스든 Observer가 되면 관찰자가 된다

```c++
class Achievements : public Observer
{
  public:
    virtual void onNotify(const Entity& entity,  Event event)
    {
      switch (event)
      {
        case EVENT_ENTITY_FALL:
          // 해당 객체가 플레이어인지,
          // 플레이어가 다리위에 있는 것인지...
          if (entity.isHero() && heroIsOnBridge_)
          {
            unlock(ACHIEVEMENT_FELL_OFF_BRIDGE);
          }
          break;
          // heroIsOnBridge_ 값 업데이트
          // 그 외...
      }
    }

  private:
    void unlcok(Achievement achievement)
    {
      // 아직 업적이 남아있다면 해제
    }
    bool heroIsOnBridge_;
}
```

### 대상 Subject
* 관찰당하는 객체가 알림 메서드를 호출
* 대상은 알림을 기다리는 관찰자 목록을 보유
  * 하나의 관찰자에만 반응하게 된다면 복수의 시스템과 동시에 상호작용할 수 없다
  * 후에 알림을 넣은 관찰자가 먼저 알림을 넣은 관찰자를 방해할 수도 있다
    * 물론 이런 구조로 짜면 안된다
  * 관찰자는 다른 관찰자를 신경쓰지 않는다

```c++
class Subject
{
  // Observer 목록을 갱신할 수 있도록 메서도 공개
  public:
    void addObservers() { /*.Observer 추가..*/ }
    void removeObservers() { /*Observer 제거...*/ }
    // ...

  private: 
    Observer* observers_[MAX_OBSERVERS];
    int numObservers_;
}
```
* 관찰자와 대상은 상호작용한다
  * 그러나 서로 커플링되어 있지 않다

```c++
// 아래 코드는 observers_의 size가 고정되어 있다는 전제로 작성
class Subject
{
  // 상속하는 클래스를 위해 protected
  protected:
    void notify(const Entity& entity, Event event)
    {
      for (int i = 0; i < numObservers_; ++i>)
        observers_[i]->onNotify(entity, event);
    }
}
```
* 대상은 관찰자에게 알림을 보낸다
  * 대상은 관찰자 목록을 가지고 있고, 사실은 이 관찰자 포인터를 통해 직접 함수를 실행시켜버리는 구조
  * 관찰자 목록에 add, remove를 통해 목록을 업데이트 할 수 있다

## 문제점과 해결방안
### 속도
* 관찰자 패턴을 사용하는 시스템이 Queuing이나 동적할당을 하기 때문에 실제로 느릴 수 있다
  * **솔직히 여느 게임이라면 속도 문제는 제기될 일이 없다**
  * 성능에 민감하지 않다면 [동적 디스패치](https://jaykop.github.io/post/pattern/Observer-Pattern/#%EB%8F%99%EC%A0%81-%ED%95%A0%EB%8B%B9)를 사용해도 된다
* 정적 호출보다 느리지만 가상함수를 통해 필요한 알림을 보내면 된다

### 동기적
* 대상이 notify를 통해 관찰자의 메서드를 실행시키고, 이 작업이 완료되기 전까지는 다음 작업을 진행할 수 없다
  * 죽, 블록 상태의 우려가 있을 수는 있다
* 그러나 인지하고 있으면 큰 문제는 아니다
  * 오히려 멀티스레드나 락을 사용하는 것이 더 불안할 수 있다
  * 경우에 따라 queue를 사용하거나 비동기 상호작용 방식으로 풀 수 있을 것이다

### 동적 할당
* 위의 예제에서는 고정 할당된 관찰자 목록을 사용했다
  * 하지만 이를 동적으로 사용할 수도 있다
* 새로운 관찰자가 추가될 때만 동적할당이 일어난다
  * 알림 메서드를 날릴 때마다 동적할당되는 게 아니다
* 굳이 신경이 쓰인다면...

```c++
// Subject가 목록을 들고 있는 대신,
// Observer끼리 next 포인터를 통해 연결되어 있도록 하는 구조를 사용했다
void Subject::addObserver(Observer* observer)
{
  observer->next = head;
  head = observer;
}
```

![image](/assets/images/{08408586-56CF-492B-B9B1-9EF1C030D921}.png)  
  * Observer를 linked list로 구현한다
    * 이 경우, Observer는 한 번에 하나의 대상만 관찰할 수 있다
    * 왜나하면, observer->next가 하나로만 정의되니까..
    * 반면에 대상마다 Observer 목록이 있다면 Observer를 여러 대상에 등록할 수 있다
      * 

![image](/assets/images/{D5BFE3BA-CECB-4401-B0A2-4C54F216E8DB}.png)  
  * Obsever Pool의 노드들이 Observer를 포인터로 가리키게 한다
    * 같은 관찰자를 여러 노드가 가리킬 수 있다
    * 같은 관찰자를 여러 대상에 추가할 수 있다

### 대상과 관찰자 제거
* 관찰자가 삭제될 수 있다면, dangling pointer 문제가 발생할 수 있다
  * Observer객체는 삭제되었지만 Subject의 목록에는 아직 남아있는 경우, 괜히 notify 함수를 계속 날리려는 것이다
* 보통은 관찰자가 대상을 참조하지 않기 때문에 대상을 지우는 것이 더 쉽다
  * 그러나 삭제된 대상의 알림을 관찰자가 계속 기다릴 수도 있다
    * 관찰자 객체의 존재 목적이 특정 1개 대상의 알림을 기다리는 것이라면, 그 대상과 함께 삭제되어야 한다
    * 아무것도 하지 않는 메모리로 계속 남아있게 된다...
  * 대상이 삭제될 때, 목록에 보유한 모든 관찰자들에게 **사망** 알림을 보내면 된다
* 관찰자를 제거할 때 스스로 등록을 취소하게 할 수도 있다
  * 모든 대상으로부터 등록을 취소할 수도 있다
  * **물론 이 경우, 상호 참조를 해야하기 때문에 더 복잡해진다**

### 사라진 리스너 문제
  * 캐릭터가 상태창을 열면 UI 객체를 생성한다
  * 상태창을 닫으면 GC가 알아서 정리하게 한다
  * 캐릭터는 대상이고, UI는 캐릭터에 관찰자로 등록되어 있다
    * 캐릭터의 상태가 변하면 notify를 받아 UI에 표시되는 데이터를 업데이트 한다
  * 근데 상태창을 닫을 때 대상의 관찰자를 등록해제 하지 않는다면?
    * 대상의 관찰자 목록에 참조된 채로 투명화된 UI는 계속 남아있다
    * GC는 참조된 메모리이므로 해제하지 않는다
    * 근데 새로운 UI는 상태창을 열때마다 쌓인다
    * notify는 모든 UI에 계속 날린다...

### 항상 답은 아니다
  * 관찰자 패턴은 두 코드를 명시적으로 연결하기 애매한 경우에 차용하자
  * **긴밀한 두 코드를 연결지어야 한다면, 오히려 명시적으로 커플링 시켜버리는 게 더 낫다**
  * 하나의 기능을 구현하는 코드 덩어리 안에서는 굳이 쓸 필요가 없다
    * 더 복잡해지기만 할 뿐
  * **서로 상관없는 분야에서 연결되어야 하는 경우에 쓰자**