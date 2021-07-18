---
title: "Coroutine"
classes: wide
categories: 
  - blog
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   

코루틴(Coroutine) 이란? https://happysalmon.tistory.com/4
C언어 등에서 일반적으로 사용하는 함수는 시작할 때 진입하는 지점이 하나 존재하고 함수가 모두 실행되거나, return 구문에 의해 종료되는 지점을 설정할 수 있습니다.
이러한 함수를 Subroutine( 서브루틴 )이라 부르는데, 코루틴은 이를 더 일반화한 개념으로 진입하는 시점을 여러 개를 가질 수 있는 함수를 의미합니다. 개념적으로만 본다면 코루틴도 서브루틴의 한 종류라고 볼 수 있겠죠.
함수가 실행되고 return 으로 종료되는 대신에 Yield 하면 Yield 한 부분을 기억했다가 나중에 Yield 된 지점부터 실행을 이어 갈 수 있습니다.

coroutine - https://www.slideshare.net/QooJuice/coroutine-119750550
함수가 실행되어 진행되다가 멈추고 다시 실행될 때 멈춘 시점에서 다시 시작
쓰레드가 아니라 함수
서브루틴은 시작점과 종료점이 1개인 코루틴에 포함
일반 함수는 코루틴에 포함
스레드와의 차이?
스레드 실행 도중 다른 스레드가 간섭하여 실행될 수 있다
실행 중인 코루틴이 종료되어야 다음 코루틴이 실행된다
스레드는 OS가 스케줄링
코루틴은 유저가 스케줄링
yield
코루틴이 종료되고 다시 시작할 지점을 지정하는 키워드


  
---  
출처:   
<https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/delegates/>  
<https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/concepts/covariance-contravariance/using-variance-in-delegates>
