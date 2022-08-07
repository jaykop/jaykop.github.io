---
title: "Inheritance"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## Base class

```c++
class A 
{
    public:
       int x;
    protected:
       int y;
    private:
       int z;
};
```

* 위와 같은 Base class가 있다고 가정하고, 각 케이스를 살펴본다

### public inheritance

```c++
class B : public A
{
    void func_b()
    {
        x = 10;     // x is public
        y = 15;     // y is protected
        // z = 20;  // z is private, not accessible
    }
};

// ...

int main()
{
    B b;

    b.x = 10;     // x is public
    // b.y = 15;  y is protected, not accessible
    // b.z = 20;  z is private,   not accessible
}
```

* 일반적으로 가장 많이 사용하는 방식
* Base class의 public 변수에 접근이 가능하다
* Base class의 protected 변수에도 접근이 가능하다
* Base class의 private 변수에는 접근이 불가능하다

### protected inheritance

```c++
class C : protected A
{
    void func_c()
    {
        x = 10;     // x is protected
        y = 15;     // y is protected
        // z = 20;  // z is private,  not accessible
    }
};

// ...

int main()
{
    C c;

    // c.x = 10; x is protected,  not accessible
    // c.y = 15; y is protected,  not accessible
    // c.z = 20; z is private,    not accessible
}
```

* public 키워드가 붙어있던 x 변수가 protected가 된다
* y와 z는 기존의 키워드를 유지한다
* 하위 클래스에서의 접근 여부는?
  * 유지된다

### private inheritance

```c++
class D : private A    // 'private' is default for classes
{
    void func_d()
    {
        x = 10;     // x is private
        y = 15;     // y is private
        // z = 20;  // z is private, not accessible
    }
};

// ...

int main()
{
    D d;

    // d.x = 10; x is private, not accessible
    // d.y = 15; y is private, not accessible
    // d.z = 20; z is private, not accessible
}
```

* 상속 키워드를 명시하지 않는 경우의 default
* public 키워드의 x와 protected 키워드가 붙은 y가 private이 된다
* z는 기존의 키워드를 유지한다
* 하위 클래스에서의 접근 여부는?
  * 역시 유지된다

## 결론

![post_thumbnail](/assets/images/W6CJ3.jpg)

* 외부에서 접근 시 public -> protected -> private 순서로 접근 제어자가 제한된다
* 그러나 내부에서의 접근은 유지된다

## 출처
* <https://stackoverflow.com/questions/860339/what-is-the-difference-between-public-private-and-protected-inheritance-in-c>
