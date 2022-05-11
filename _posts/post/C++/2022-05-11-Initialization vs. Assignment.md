---
title: "Initialization vs. Assignment"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## Initialization 
* 어떤 객체든 객체의 데이터 멤버는 생성자의 본문이 실행되기 전 초기화되어야 한다

### 잘못된 Initialization

```c++
class ABEntry
{
  public:
  ABEntry(const std::string& name, const std::string& address, 
    const std::list<PhoneNumber>& phones);
    
  private:
  std::string& theName;
  std::string& theAddress;
  std::list<PhoneNumber>& thePhones;
  int numTimesConsulted;
}

ABEntry(const std::string& name, const std::string& address, 
  const std::list<PhoneNumber>& phones)
  {
      theName = name;
      theAddress = address;
      thePhones = phones;
      numTimesConsulted = 0;
  }
```

* 위의 생성자에서는 모두 대입, 즉 할당을 하고 있을뿐 초기화가 아니다
* 생성자의 본문이 실행되기 전에 초기화가 끝나야 하는데, 위는 그렇지 않다

### 올바른 Initialization

```c++
ABEntry(const std::string& name, const std::string& address, 
  const std::list<PhoneNumber>& phones)
    : theName(name), theAddress(address), thePhones(phones), numTimesConsulted(0), 
  { }
```

* 위는 초기화 리스트를 사용한 코드
* 기본 제공 타입이 아닌 멤버 변수의 경우에는 복사 생성자에 의해 초기화된다
  * 대부분은 기본 생성자 호출 후 복사 대입 연산자를 호출하므로, 먼저 번의 할당을 하는 생성자보다 더 효율적
* 다만 기본 제공 타입의 객체는 초기화와 대입의 비용 차이가 없다
  * 위의 코드의 경우에는 int numTimesConsulted
  * 굳이 어떤 데이터는 대입, 어떤 데이터는 초기화 리스트에 올리면서 나눌 이유는 없다
  * 그러나 상수이거나 참조자 데이터 멤버인 경우에는 반드시 초기화되어야 한다

## 출처
* https://stackoverflow.com/questions/15679977/constructor-initialization-vs-assignment>
