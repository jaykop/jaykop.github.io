---
title: "Return Value Optimization"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## 임시 값 할당 인자
* C++ 에서는 임시값을 const reference와 rvalue reference, 그리고 값으로서의 함수 인자로 받도록 허용한다
* non-const reference 인자를 받는 함수는 함수 실행 중 인자를 수정하고서 변경된 상태로 다시 caller로 돌아가는 것을 허용한다

```c++
vector<double> emptyvec()
{
    vector<double> v;    // no elements
    return v;
}

grade(midterm, final, emptyvec());
```

* 위 예시에서 emptyvec()은 임시 객체를 반환한다
* grade 함수는 emptyvec()를 const reference로 받는다고 가정한다
* 이 과정에서 grade의 인자로 받은 emptyvec()는 **복사된다**
  * 그러나 이 과정은 **프로그램(사용자가 작성한 코드)에 의해서가 아니라 컴파일러에 의한 복사다**

## Return Value Optimization 반환값 최적화 기법

### 일반적인 함수의 반환 방식
![post_thumbnail](/assets/images/{8210C0C8-B87F-4BCF-A07F-FB9E1167AE2B}.png)
* 반환할 값만큼의 스택 메모리가 있고, 그 값을 연산할 함수 실행을 위한 메모리가 할당된다

![post_thumbnail](/assets/images/{0ACF247A-A4B3-4F0A-8000-058AEE943938}.png)
* 함수 실행을 위해 stack frame 2가 생성되었다
* 함수의 local variable과 이를 이용한 최종 return 값을 할당할 메모리가 추가적으로 잡힌다
* RVO가 작동하지 않으면, 이 최종 return 값을 stack frame 1의 return value로 복사한다

![post_thumbnail](/assets/images/{8994A648-641F-4433-ACD4-D0FAAF4DDF01}.png)
* 그러나 RVO가 작동한다면, 반환할 값을 처음부터 stack frame 1에 위치한 return value 메모리에 할당한다

### RVO이 작동하지 않는 경우

```c++
class A
{
  int a = 0;
public:
  A() {}
  ~A() {}
  A(const A&) {}

  A& operator +=(int i)
  {
    a += i;
    return *this;
  }
  
  // case 1
  // 조건에 의해 반환 값이 달라질 수 있는 경우
  A case1()
  {
    A a;
    if (condition) return a;
    else return a;
  }
  
  // case 2
  // 반환되는 값에 대해 단항식이 아닌 경우
  A case2()
  {
    A a;
    return a += 10;
  }
  
  // case 3
  // **이레 식에서는 이름 없는 반환 값에 대한 RVO가 작동한다
  A case3()
  {
    return A(a + 10);
  }
}
```

## Name Return Value Optimization
* 함수 안에서 생성된 local variable의 type과 함수의 return type이 동일하고 반환 식이 name이라면 NRVO 할 수 있다

```c++
// 아래 함수는 이름이 있는 식 a를 반환한다
// NRVO로 작동한다
A func1()
{
  A a;
  return a;
}

// 아래 함수는 이름이 없는 식을 반환한다
// RVO로 작동한다
A func2()
{
  return A();
}
```

# 출처  
* <https://quick-adviser.com/can-a-temporary-object-be-passed-to-a-const-reference/>
* <https://stackoverflow.com/questions/42201135/about-passing-a-temporary-object-to-a-const-reference>
* <https://m.post.naver.com/viewer/postView.nhn?volumeNo=9735713&memberNo=559061>
