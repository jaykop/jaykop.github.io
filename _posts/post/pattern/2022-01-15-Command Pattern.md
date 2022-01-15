---
title: "Command Pattern"
classes: wide
categories: 
  - post
  - Pattern
sidebar:
  nav: "main"
author_profile: true
---
   
### 정의
* 메서드 호출을 실체화한 것
* 함수 호출을 객체로 감쌌다는 의미
* 콜백을 객체지향적으로 표현한 것

### 예시

```c++
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

class JumpCommand : public Command
{
  public :
    virtual void execute()
    {
      jump();
    }
}

class MoveCommand : public Command
{
  public :
    virtual void execute()
    {
      move();
    }
}

// 키 별로 커맨드를 가진다
class InputHandler {
public:
void handlelnput();

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
// 따라서 아래와 같이 수정한다
Command* InputHandler::handlelnput() {
  if (isPressed(BUTTON_X)) return buttonX_；
  else if (isPressed(BUTTON_Y)) return buttonY_；
  else if (isPressed(BUTTON_A)) return buttonA_；
  else if (isPressed(BUTTON_B)) return buttonB_；

  return nullptr;
}
// 이외 업데이트 함수에서
Command* command = inputHandler.handlelnput();
if (command) command->execute(actor);
```
* 위의 코드에서 게임 내 모든 액터를 제어할 수 있다
* AI 코드에서 액터를 Command로 제어하는 것이 가능하다
* 이외에도 상태 변수를 추가하여 redo / undo 명령을 디자인할 수도 있다