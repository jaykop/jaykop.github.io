---
title: "interface vs. abstract"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---

## C# interface vs. abstract
  
|인터페이스| |추상|  
|:---:|:---:|:---:|  
|C# class가 multiple interface 상속 가능| |C# class가 하나의 abstract만 상속 가능|  
|constructor 없음| |constructor 있음|  
|메서드만 지원| |필드 안에 변수 선언 가능|  
|선언만 가능| |구현 제공|  
||둘 다 객체로 선언 불가능||  
|비추상 메소드 선언 불가| |비추상 메소드 선언 가능|  
|접근 지정자는 public(변경 불가)| |함수 접근 지정자 설정 가능|  
| |상대적으로 abstract가 더 빠르게 작동| |  
  

## 용법 예시

* interface 
  * 특정 메서드들의 조합을 고려

  ```csharp

  // 움직일 수 있는 오브젝트에 필요한 메서드 조합
  interface IMovable{

    void Walk();
    void Stop();
    void Run();
    void Jump();

  }

  // 전투 가능한 오브젝트에 필요한 메서드 조합
  interface IAttackable{

    void Attack();
    void Defend();

  }

  // 비행 가능한 오브젝트에 필요한 메서드 조합
  interface IFlyable{

    void Fly();
    void Land();

  }

  // 메서드들의 기능은 
  // 아래의 각 클래스에서 실제로 구현되며.
  // 동일한 조합의 interface를 제공하지만
  // 실제 구현은 다르게 작동

  // 유저 클래스 디자인
  public class User : IMovable, IAttackable
  {
    // ...
  }

  // Dragon 클래스 디자인
  public class Dragon : IMovable, IAttackable, IFlyable
  {
    // ...
  }

  // Eagle 클래스 디자인
  public class Eagle : IMovable, IAttackable, IFlyable
  {
    // ...
  }

  // NPC 클래스 디자인
  public class NPC : IMovable
  {
    // ...
  }

  ```

* abstract 
  * 하나의 class를 전체적으로 상속해 사용해야 하는 경우

  ```csharp

  // 몬스터의 기본 정의가 내려진 클래스
  public abstract class HumanTypeMonster
  {
    // ...
  }

  // 드래곤 클래스는 몬스터의 모든 메서드와 데이터를 이용
  public class Urk : Monster
  {
    // ...
  }

  // 오크 클래스는 몬스터의 모든 메서드와 데이터를 이용
  public class Orc : Monster
  {
    // ...
  }
  ```

## 출처
* <https://holjjack.tistory.com/41>