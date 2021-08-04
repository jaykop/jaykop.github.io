---
title: "friend keyword"
classes: wide
categories: 
  - blog
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## friend class
* 한 class에서 다른 class의 field를 public으로 참조하도록 허용

```c++
class A
{
  // class B를 friend로 허용
  friend class B;
  
  // id는 private 제어자로
  // 외부에서 접근 제한된 멤버 변수
  private int id;

  // ...
}

class B
{
  private int copied_id;

  // A의 id를 복사
  void copy_id(const A& a)
  {
    copied_id = a.id;
  }

  // A의 id를 출력
  void print_id(const A& a)
  {
    printf("%d", a.id);
  }
}
```

## friend member function
* 한 class의 특정 함수에서 class의 field를 public으로 참조하도록 허용

```c++
class A
{
  // class B의 메서드 copy_id를 friend로 허용
  friend class B::copy_id;
  
  // id는 private 제어자로
  // 외부에서 접근 제한된 멤버 변수
  private int id;

  // ...
}

class B
{
  private int copied_id;

  // A의 id를 복사
  // class A에서 이 함수에 대한 접근을 
  // friend로 허용
  void copy_id(const A& a)
  {
    copied_id = a.id;
  }

  // A의 id를 출력
  // 이 함수는 a.id에 접근할 수 없음
  void print_id(const A& a)
  {
    printf("%d", a.id);
  }
}
```

## friend global function
* 전역 함수가 class의 field를 public으로 접근하도록 허용

```c++
//forward declaration
class B; 
class A
{
    int x;
    public:
         void setdata (int i)
           {
              x=i;
           }
    friend void max (A, B); //friend function
} ;

class B
{
     int y;
     public:
          void setdata (int i)
            {
               y=i;
            }
     friend void max (A, B);//friend function
};

// 함수 구현
void max (A a, B b)
{
   if (a.x >= b.y)
         std:: cout<< a.x << std::endl;
   else
         std::cout<< b.y << std::endl;
}

int main ()
{
  A a;
  B b;
  a. setdata (10);
  b. setdata (20);
  max (a, b);
  // max 함수는 클래스 A,B 모두에게 friend이고, 
  // max는 이 두 함수의 field에 접근 가능

  return 0;
}
```
* 이 같은 형태가 필요한 예시
  * 바이너리 연산자 오버로딩

  ```c++
  class X
  {
  public:
      // 이 연산자는 기본 적으로 전역 함수이나,
      // class X의 멤버 변수에 접근해 출력하기 위해 friend 키워드를 사용
      friend std::ostream& operator<<(std::ostream& os, const X& x); 

  private:
      // ...
  };

  std::ostream& operator<<(std::ostream& os, const X& x)
  {
      return os << x.a << x.b << x.c << '\n';
  }
  ```
  * constructor가 복잡할 때

  ```c++
  class X
  {
  public:
      friend X makeX(/* something easier */);
  protected:
      X(/* something complex */);
  };

  X makeX(/* something easier */)
  {
      // some logic
      // ...

      return X(...);
  }
  ```

## 출처
* <https://genesis8.tistory.com/98>
* <https://www.mygreatlearning.com/blog/friend-functions-in-cpp/>
* <https://www.reddit.com/r/AskProgramming/comments/7znw4i/c_what_is_the_point_of_a_global_friend_function/>