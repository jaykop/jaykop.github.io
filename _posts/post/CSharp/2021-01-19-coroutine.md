---
title: "Coroutine"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## 코루틴(Coroutine) 이란?

* 서브루틴(Subroutine)
   - C언어 등에서 일반적으로 사용하는 함수
   - 시작할 때 진입하는 지점이 하나 존재하고, 종료되는 지점을 설정할 수 있다.
   - 서브루틴은 시작점과 종료점이 1개인 코루틴에 포함

* 코루틴
  - 서브루틴의 일반화 버전
  - 진입하는 시점을 여러 개를 가질 수 있는 함수
  - 함수가 실행되고 return 으로 종료되는 대신, yield 키워드로 종료 지점을 기억했다가 나중에 그 지점부터 재개
  - 쓰레드가 아니라 **함수**

## 스레드와의 차이?

![post_thumbnail](/assets/images/코루틴.png)

* 스레드 실행 도중 다른 스레드가 간섭하여 실행될 수 있다
* 실행 중인 코루틴이 종료되어야 다음 코루틴이 실행된다
* 스레드는 OS가 스케줄링
* 코루틴은 유저가 스케줄링
* 코루틴은 실제로 병렬 처리를 하는 것은 아니지만 스레드보다 가볍기 때문에 성능 면에서는 더 좋다

## yield
* 코루틴이 종료되고 다시 시작할 지점을 지정하는 키워드
* 루프 안에서 현재 상태를 기억하고, 값을 하나씩 반환
* 특정 상황에 따라 부하를 줄일 수 있다

  ```csharp
  yield break;
  // method를 iterator로서 사용하고 있음을 의미
  // 코루틴을 중지할 때 사용
  // == return;
  // https://riptutorial.com/csharp/example/29811/the-difference-between-break-and-yield-break

  yield return <expression>;
  // yield return 문을 사용하여 각 요소를 따로따로 반환할 수 있습니다.
  // http://davidgiard.com/CommentView,guid,ec46ef9d-9cae-4629-9cf9-e10c20d795ef.aspx
  yield return null;
  // 다음 프레임에 이 분기를 마무리 할 수 있도록 기다림

  yield return new;
  // == yield return null;
  // 새로운 코루틴을 호출할 때 사용
  ```

## IEnumerator & IEnumerable

* **IEnumerator**
  - C#에서 컬렉션을 반복하기 위한 인터페이스
  - yield 문을 만날 때까지 코루틴 내부에 있는 코드를 실행

    ```csharp
    public interface IEnumerator
    {
        object Current { get; }
        bool MoveNext();
        void Reset();
    }
    ```
* **IEnumerable**
  - IEnumerator GetEnumerator() 함수를 구현하도록 요구하는 인터페이스
  - foreach 키워드를 사용하기 위해서는 IEnumerable 인터페이스에서 상속되어야 함

    ```csharp
    public interface IEnumerable
    {
        IEnumerator GetEnumerator();
    }
    ```

## 출처
* <https://happysalmon.tistory.com/4>  
* <https://www.slideshare.net/QooJuice/coroutine-119750550>
* <https://aaronryu.github.io/2019/05/27/coroutine-and-thread/>
* <https://teraphonia.tistory.com/723>
* <https://ansohxxn.github.io/c%20sharp/enumerate/>
* <https://angangmoddi.tistory.com/224#:~:text=%EA%B7%B8%EB%9F%B0%EB%8D%B0%2C%20%EC%8A%A4%EB%A0%88%EB%93%9C%EC%99%80%20%EC%BD%94%EB%A3%A8%ED%8B%B4,%EB%B9%84%EB%8F%99%EA%B8%B0%EC%A0%81%EC%9C%BC%EB%A1%9C%20%EC%9E%91%EB%8F%99%ED%95%9C%EB%8B%A4.&text=%EC%BD%94%EB%A3%A8%ED%8B%B4%EC%9D%80%20%ED%95%9C%20%EB%AA%85%EC%9D%98,%EB%90%98%EB%8A%94%20%EA%B2%83%EC%B2%98%EB%9F%BC%20%EB%B3%B4%EC%9D%B4%EA%B2%8C%20%ED%95%98%EB%8A%94%20%EA%B2%83%EC%9D%B4%EB%8B%A4.>