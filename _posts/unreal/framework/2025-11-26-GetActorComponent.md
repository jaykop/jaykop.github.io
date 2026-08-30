---
title: "[DevNote] 커스텀 GetActorComponent"
classes: wide
categories:
  - unreal
  - framework
sidebar:
  nav: "main"
author_profile: true
---

### 갑자기 든 의문

오늘날의 게임 개발 분야에서 Entity 혹은 GameObject라는 것은, 여러 개의 Component를 하나로 묶은 단위이다.<br>
그러나 대부분은 그에 그치지 않고, 그 GameObject의 고유 기능이 클래스 멤버 함수 또는 변수로 포함되기도 한다.<br>
만약 그런 경우에는, 그런 고유 기능도 Component로 분리되어야 할까?<br>
GameObject는 단순히 복수의 Component를 담는 Wrapper 혹은 Holder의 역할이어야 할까?<br>
<br>

### 상황 예시

여러 기능들이 각 Component로 구현되어 있고, 어떤 기능을 추가하기 위한 방법이 Actor에 특정 Component 하나만 추가하는 것이라면 이는 모듈화가 잘된 것이겠다.<br>
반대로 어떤 기능을 사용하지 않겠다면, 그 기능을 수행하는 Component만 제거하면 그만이다.<br>
커플링 혹은 디커플링은 차치하고라도, 이렇게 함으로써 불필요한 상속을 막을 수 있다.<br>
<br>
ACharacter -> AMonster<br>
ACharacter -> APlayer<br>
<br>
위와 같은 상속구조가 있다고 하자.<br>
그런데 기획이 추가되어, 게임 기능에 탈 것을 구현해야 한다.<br>
흔히 탈 것 구현은 Player 캐릭터에서 다른 탈 것 캐릭터로 Possess하는 방법이 쓰인다.<br>
그렇다면 이 탈 것 캐릭터는 Player를 상속한 클래스여야 하는가?<br>
- 다른 탈것을 구현하는 방법은 잠시 접어두고, 이런 문제 상황이 일어난 이유에 대해 생각해보자.<br>

### Blueprint로 정의하는 Class

언리얼이라는 엔진을 사용하면서, 클래스는 C++로도 정의할 수 있지만, Blueprint를 사용하는 방법도 있다.<br>
ACharacter가 APlayer가 되기 위해서, 굳이 C++ 클래스로 정의하지 않고, Blueprint로 ACharacter를 상속해 필요한 Component를 거기에서 붙여도 된다.<br>
이는 클래스 정의에 유연성을 더하는 방법이며, 경우에 따라 이 Blueprint를 상속하지 않아도 된다.<br>
그냥 ACharacter를 Blueprint로 상속해 AVehicle이라는 새로운 클래스를 정의할 수도 있다. 탈 것 구현에 필요한 Component만 추가해서 말이다.<br>

### GetActorComponent

물론 이런 구조도 단점은 있다.<br>
* 코드로 멤버 변수에 접근하기 쉽지 않다
  * FindCOmponentByClass는 모두가 알다시피 불필요한 코스트를 발생시키며, 애초에 C++ 클래스로 정의되었다면 멤버 변수로 정의해서 직접 접근하거나 Getter 함수로 접근하는 방법도 있는데, Blueprint로는 그럴 방도가 없다.
그래서 아래와 같은 함수가 있었다<br>

```c++
template<typename T>
T* GetActorComponent(AActor* Actor)
{
  if (!Actor)
  {
    return nullptr;
  }

  UClass* ComponentClass = T::StaticClass();

  // 캐싱 인터페이스 확인
  if (IComponentCacheInterface* CacheInterface = Cast<IComponentCacheInterface>(Actor))
  {
    // 캐시에서 먼저 조회
    if (UActorComponent* CachedComponent = CacheInterface->GetCachedComponent(ComponentClass))
    {
      return Cast<T>(CachedComponent);
    }

    // 캐시에 없으면 찾아서 캐싱
    if (T* FoundComponent = Actor->FindComponentByClass<T>())
    {
      CacheInterface->CacheComponent(ComponentClass, FoundComponent);
      return FoundComponent;
    }
  }
  else
  {
    // 캐싱 미지원 Actor는 일반 검색
    return Actor->FindComponentByClass<T>();
  }

  return nullptr;
}
```

```c++
class UComponentCacheInterface : public UInterface
{
  GENERATED_BODY()
};

class IComponentCacheInterface
{
  GENERATED_BODY()

public:
  /**
   * 캐시에서 컴포넌트 조회
   * @param ComponentClass - 찾을 컴포넌트 클래스
   * @return 캐시된 컴포넌트 (없으면 nullptr)
   */
  virtual UActorComponent* GetCachedComponent(UClass* ComponentClass) const
  {
    if (!ComponentClass)
    {
      return nullptr;
    }

    if (const TObjectPtr<UActorComponent>* FoundComponent = CachedComponents.Find(ComponentClass))
    {
      return *FoundComponent;
    }

    return nullptr;
  }

  /**
   * 컴포넌트를 캐시에 저장
   * @param ComponentClass - 컴포넌트 클래스
   * @param Component - 저장할 컴포넌트
   */
  virtual void CacheComponent(UClass* ComponentClass, UActorComponent* Component)
  {
    if (ComponentClass && Component)
    {
      CachedComponents.Add(ComponentClass, Component);
    }
  }

  /**
   * 캐시 초기화
   */
  virtual void ClearComponentCache()
  {
    CachedComponents.Empty();
  }

protected:
  /**
   * 캐싱된 컴포넌트 맵
   * 주의: UClass를 키로 사용하므로 동일한 타입의 컴포넌트가 여러 개인 경우,
   * 첫 번째로 찾은 컴포넌트만 캐싱됩니다.
   */
  TMap<UClass*, TObjectPtr<UActorComponent>> CachedComponents;
};
```

인터페이스는 Component 타입을 Key로 가지고 Component Instance를 Value로 가지는 Map을 가진다.<br>
그리고 GetComponent를 호출하면, 최초 호출 시에는 FindComponentByClass, 그 이후에는 캐싱한 Component를 반환한다.<br>
꽤 사용하기 까다로운 조건을 동반하는 함수다.<br>
* Type별로 1개의 Instance만 저장할 수 있고, 그것이 잘못된 Component Instance일 수도 있다. 
  * 또 이런 위험성이 있기에 Blueprint에 단 1개만 존재하는 타입의 Component에 접근하는 방법으로 써야한다는 규약을 지켜야 한다.
  * 오히려 C++ 클래스로 직접 멤버함수에 접근할 수 잇는 Getter는 더 명시적이고 직관적이며, 안전하다.
- 캐싱을 하기 때문에 비효율적이라는 의견도 있는데, 사실 Class에 멤버 변수로 Component를 정의해두는 것도 캐싱이다
  - 오히려 이쪽이 호출하지 않는 경우에는 아예 캐싱하지 않는다

### 그냥 내 생각

경험에 비추어봤을 때, 나는 상속을 별로 좋아하지 않고, 위의 경우에 GetComponent 함수를 만들어 사용하는 것을 더 선호한다<br>
이 함수는 단순히 Component를 감싸기 위해 C++ 클래스를 정의하는 수고를 덜어주며, 그렇게 함으로써 상속 구조를 덜 만들게 한다<br>
그렇게 상속 구조를 줄이면 로직 하나를 수정하기 위해 이 BP 저 BP 돌아다니며 복사되어 있는 데이터나 로직을 바꿀 필요가 없다.<br>