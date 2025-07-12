---
title: "Command Pattern"
classes: wide
categories: 
  - post
  - design_pattern
sidebar:
  nav: "main"
author_profile: true
---
   
### 정의
* 흔히 ***실체화*** 또는 ***일급***이라고 하면 어떤 개념을 변수에 저장하거나 함수에 전달할 수 있도록 객체로 바꿀 수 있다는 의미이다
  * 이 개념은 값일 수도, 함수와 같은 로직일 수도 있다
* 즉 메서드 호출을 실체화한 것이며, 함수 호출을 객체로 감쌌다는 의미이다
  * 콜백, 일급 함수, 함수 포인터, 클로저 등의 용어가 이에 해당한다

### 예시

![image](/assets/images/스크린샷 2024-11-17 124713.png)

* 위와 같은 매핑으로 키 바인딩이 되어있다고 하자

```c++
// 게임 입력 버튼을 세팅
void InputHandler：：handlelnput() 
{
  if (isPressed(BUTTON_X)) jump()；
  else if (isPressed(BUTTON.Y)) fireGun()；
  else if (isPressed(BUTTON_A)) swapWeapon()；
  else if (isPressed(BUTTON_B)) lurchlneffectively()；
}
```
* 위 코드에서는 입력키 변경이 불가하다

```c++
// 상위 클래스릃 만들고 하위에서 정으한다
class Command
{
  public :
    virtual ~Command() {}
    virtual void execute() = 0;
}

// 커맨드 별 하위 클래스
// Jump 하는 클래스
class JumpCommand : public Command
{
  public :
    virtual void execute()
    {
      jump();
    }
}

// Move하는 클래스
class MoveCommand : public Command
{
  public :
    virtual void execute()
    {
      move();
    }
}
```

```c++
// 키 별로 커맨드를 가진다
class InputHandler {
public:
void handlelnput();

// 각각의 Command에 실행할 Command 클래스를 할당한다
private:
  Command* buttonX ;
  Command* buttonY_;
  Command* buttonA ;
  Command* buttonB_;
}；

void InputHandler::handlelnput() {
  if (isPressed(BUTTON_X)) buttonX_->execute()；
  else if (isPressed(BUTTON_Y)) buttonY_->execute()；
  else if (isPressed(BUTTON_A)) buttonA_->execute()；
  else if (isPressed(BUTTON_B)) buttonB_->execute()；
}
```
* 위의 클래스는 액터를 인자로 받지 않는다
* 하나의 게임 객체(보통 플레이어)의 동작만을 제어하는 한계가 있다

```c++
// Actor를 인자로 받도록 수정
class Command
{
  public :
    virtual ~Command() {}
    virtual void execute(Actor& actor) = 0;
}

class JumpCommand : public Command
{
  public :
    virtual void execute(Actor& actor)
    {
      actor.jump();
    }
}

// 기존의 InputHandler::handlelnput는 인자를 받을 줄 모른다
// 따라서 handlelnput함수는 Command를 반환하는 식으로 수정한다
Command* InputHandler::handlelnput() {
  if (isPressed(BUTTON_X)) return buttonX_；
  else if (isPressed(BUTTON_Y)) return buttonY_；
  else if (isPressed(BUTTON_A)) return buttonA_；
  else if (isPressed(BUTTON_B)) return buttonB_；

  return nullptr;
}

// X, Y, A, B 중 하나의 버튼을 누르면 command가 할당될 것이고,
// 아니라면 계속 nullptr이 할당될 것이다.
Command* command = inputHandler.handlelnput();

// 할당된 command가 valid하다면, 액터를 받아 실행한다
if (command) command->execute(actor);
```
* 위의 코드에서 게임 내 모든 액터를 제어할 수 있다
  * AI 코드에서 액터를 Command로 제어하는 것이 가능하다
* 이외에도 상태 변수를 추가하여 redo / undo 명령을 디자인할 수도 있다