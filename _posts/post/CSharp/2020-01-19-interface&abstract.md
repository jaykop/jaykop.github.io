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
  
## interface 
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

### implicit implementation

```csharp
interface IFile
{
  void ReadFile();
  void WriteFile(string text);
}

class FileInfo : IFile
{
  public void ReadFile()
  {
    ...
  }
  public void WriteFile(string text)
  {
    ...
  }
}

// 아래 코드는 정상적으로 컴파일 된다
public static void Main()
{
  IFile file1 = new FileInfo();
  FileInfo file2 = new FileInfo();

  file1.ReadFile();
  file1.WriteFile("a");

  file2.ReadFile();
  file2.WriteFile("a");
}

```

### explicit implementation
* explicit으로 interface를 작성할 때는 public 키워드를 사용하지 않는다
  * 그렇지 않으면 컴파일 에러를 야기할 것

```csharp
interface IFile
{
  void ReadFile();
  void WriteFile(string text);
}

class FileInfo : IFile
{
  void IFile.ReadFile()
  {
    ...
  }
  void IFile.WriteFile(string text)
  {
    ...
  }

  public void Search()
  {
    ...
  }
}

// 아래 코드는 정상적으로 컴파일 된다
public static void Main()
{
  IFile file1 = new FileInfo();
  FileInfo file2 = new FileInfo();

  file1.ReadFile();
  file1.WriteFile("a");
  // file1.Search();        // compile error

  // file2.ReadFile();      // compile error
  // file2.WriteFile("a");  // compile error
  file2.Search();
}

```

## abstract 
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

### abstract 다중 상속이 안되는 이유
![post_thumbnail](/assets/images/{B943E995-082D-4B3E-B6C4-1ED8D525A763}.png)
* **죽음의 다이아몬드**
* 다중 상속 시 모호성이 발생

```csharp
// MyVehicle의 Ride가 어떤 Ride를 상속할 지 알수 없다
Plane plane = new MyVehicle();
Car car = new MyVehicle();
```

## C# interface vs. abstract
  
|인터페이스| |추상|  
|:---:|:---:|:---:|  
|C# class가 multiple interface 상속 가능| |C# class가 하나의 abstract만 상속 가능|  
|constructor 없음| |constructor 있음|  
|메서드만 지원| |필드 안에 변수 선언 가능|  
|선언만 가능| |구현 제공|  
||둘 다 객체로 선언 불가능||  
|추상 메소드만 선언 가능| |비추상 메소드 선언 가능|  
|접근 지정자는 public(변경 불가)| |함수 접근 지정자 설정 가능|  
| |상대적으로 abstract가 더 빠르게 작동| |  

## 출처
* <https://holjjack.tistory.com/41>
* <https://nomad-programmer.tistory.com/170>
* <https://www.tutorialsteacher.com/csharp/csharp-interface>