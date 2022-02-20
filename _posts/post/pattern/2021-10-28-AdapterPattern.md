---
title: "Adapter 패턴"
classes: wide
categories: 
  - post
  - Pattern
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## Adaper 패턴
* 인터페이스를 제공함으로써 호환되지 않는 원본 인터페이스를 이용할 수 있게 함
* 라이브러리의 업데이트 및 교체에 유연하게 대처할 수 있음

```c++
// 기존의 라이브러리
class Object { virtual void Draw() = 0;}
class Circle : public Object {
  void Draw() override { /*Draw Circle*/ }
}

// 새롭게 추가된 함수(또는 라이브러리)
class TextBox {
  void ViewText() {/*텍스트 상자 생성*/}
}

// 그래서 수정한 기존 함수...
void Display(Object* obj, TextBox* tb)
{
  if (obj) obj->Draw();
  else if (tb) tb->ViewText();
}
```
* 위의 방법은 obj를 사용하는 부분에 일일이 수정을 해야 함
* 그래서 아래와 같이 수정

```c++
// 기존의 라이브러리
class Object { 
  public:
    virtual void Draw() = 0;}
class Circle : public Object {
  public:
  void Draw() override { /*Draw Circle*/ }
}

// 새롭게 추가된 함수(또는 라이브러리)
class TextBox {
  public:
    void ViewText() {/*텍스트 상자 생성*/}
}

// 그래서 새로 만든 클래스 TextObject
// 1. Object Patern
// 새로운 클래스를 만들고, 거기서 필요한 객체를 생성해 사용
class TextObject : public Object
{
    // TextBox를 객체로 받아서 사용
    TextBox* pObj = nullptr;
  public:
    TextObject() {pObj = new TextBox;}
    void Draw() { pObj->ViewText(); }
}

// 2. Class Pattern
// 새로운 클래스를 만들고, 거기에 상속을 받아 사용
class TextObject : public Object, private TextBox
{
  public:
    // 필요한 함수를 다른 이름으로 Wrapping
    void Draw() { ViewText(); }
}

// 기존 함수 사용 가능
void Display(Object* obj)
{
  if (obj) obj->Draw();
}
```

## 출처
* <https://1d1cblog.tistory.com/397>
* <https://arisu1000.tistory.com/27679>