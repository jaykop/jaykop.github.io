---
title: "async와 await 키워드"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## 동기와 비동기
* **동기**
  - 어떤 operation을 실행시켰을 때 결과값이 도출될 때까지 프로그램은 멈춰서 기다려야 함
* **비동기**
  - 언제 값이 도출될 지 보장할 수 없고, 그 동안 프로그램은 다른 프로세스를 진행할 수 있음
* async / await는 위 중 비동기 프로그래밍을 위해 사용될 키워드

## 아침 준비하기

```csharp
using System;
using System.Threading.Tasks;

namespace AsyncBreakfast
{
    // 아래 클래스는 예시를 위한 더미 클래스
    internal class Bacon { }
    internal class Coffee { }
    internal class Egg { }
    internal class Juice { }
    internal class Toast { }

    class Program
    {
        static void Main(string[] args)
        {
            Coffee cup = PourCoffee();
            Console.WriteLine("coffee is ready");

            Egg eggs = FryEggs(2);
            Console.WriteLine("eggs are ready");

            Bacon bacon = FryBacon(3);
            Console.WriteLine("bacon is ready");

            Toast toast = ToastBread(2);
            ApplyButter(toast);
            ApplyJam(toast);
            Console.WriteLine("toast is ready");

            Juice oj = PourOJ();
            Console.WriteLine("oj is ready");
            Console.WriteLine("Breakfast is ready!");
        }

        // 오렌지 주스 따르기
        private static Juice PourOJ()
        {
            Console.WriteLine("Pouring orange juice");
            return new Juice();
        }

        // 잼 바르기
        private static void ApplyJam(Toast toast) =>
            Console.WriteLine("Putting jam on the toast");

        // 버터 바르기
        private static void ApplyButter(Toast toast) =>
            Console.WriteLine("Putting butter on the toast");

        // 빵 굽기
        private static Toast ToastBread(int slices)
        {
            for (int slice = 0; slice < slices; slice++)
            {
                Console.WriteLine("Putting a slice of bread in the toaster");
            }
            Console.WriteLine("Start toasting...");
            Task.Delay(3000).Wait();
            Console.WriteLine("Remove toast from toaster");

            return new Toast();
        }

        // 베이컨 굽기
        private static Bacon FryBacon(int slices)
        {
            Console.WriteLine($"putting {slices} slices of bacon in the pan");
            Console.WriteLine("cooking first side of bacon...");
            Task.Delay(3000).Wait();
            for (int slice = 0; slice < slices; slice++)
            {
                Console.WriteLine("flipping a slice of bacon");
            }
            Console.WriteLine("cooking the second side of bacon...");
            Task.Delay(3000).Wait();
            Console.WriteLine("Put bacon on plate");

            return new Bacon();
        }

        // 계란 프라이 굽기
        private static Egg FryEggs(int howMany)
        {
            Console.WriteLine("Warming the egg pan...");
            Task.Delay(3000).Wait();
            Console.WriteLine($"cracking {howMany} eggs");
            Console.WriteLine("cooking the eggs ...");
            Task.Delay(3000).Wait();
            Console.WriteLine("Put eggs on plate");

            return new Egg();
        }

        // 커피 따르기
        private static Coffee PourCoffee()
        {
            Console.WriteLine("Pouring coffee");
            return new Coffee();
        }
    }
}
```
  
![post_thumbnail](/assets/images/synchronous-breakfast.png)

* 위의 코드대로라면, 아침 식사를 동기적으로 수행했고 총 30붕이 소요됐다
* 하나의 작업이 완료되기 전까지는 다른 작업을 실행할 수 없다
  * 위의 작업을 비동기로 실행하려면, 코드를 비동기로 작성해야 한다
* 위의 코드는, 실행되는 스레드에서 다른 스레드의 작업을 수행하지 못하도록 차단해버린다
  * 작업이 진행되는 동안에는 중단되지 않는다

### 차단하는 대신 대기하기

```csharp
internal class Bacon { }
internal class Coffee { }
internal class Egg { }
internal class Juice { }
internal class Toast { }

static async Task Main(string[] args)
{
    Coffee cup = PourCoffee();
    Console.WriteLine("coffee is ready");

    Egg eggs = await FryEggsAsync(2);
    Console.WriteLine("eggs are ready");

    Bacon bacon = await FryBaconAsync(3);
    Console.WriteLine("bacon is ready");

    Toast toast = await ToastBreadAsync(2);
    ApplyButter(toast);
    ApplyJam(toast);
    Console.WriteLine("toast is ready");

    Juice oj = PourOJ();
    Console.WriteLine("oj is ready");
    Console.WriteLine("Breakfast is ready!");
}
```

* 위 코드도 소요시간은 동기 코드와 거의 동일하다
* 그러나 위 코드에서는, 적어도 한 스레드가 다른 스레드의 작업을 강제로 차단하지는 않는다
  * 계란 프라이를 하면서 빵이 다 구워졌나 쳐다보는 것 정도는 가능하다

### 동시에 시작하기

```csharp
Coffee cup = PourCoffee();
Console.WriteLine("Coffee is ready");

Task<Egg> eggsTask = FryEggsAsync(2);
Task<Bacon> baconTask = FryBaconAsync(3);
Task<Toast> toastTask = ToastBreadAsync(2);

Toast toast = await toastTask;
ApplyButter(toast);
ApplyJam(toast);
Console.WriteLine("Toast is ready");
Juice oj = PourOJ();
Console.WriteLine("Oj is ready");

Egg eggs = await eggsTask;
Console.WriteLine("Eggs are ready");
Bacon bacon = await baconTask;
Console.WriteLine("Bacon is ready");

Console.WriteLine("Breakfast is ready!");
```

![post_thumbnail](/assets/images/asynchronous-breakfast.png)

* 기존 작업이 완료되기까지 기다리지 않고 다음 작업을 시작할 때, 진행하던 작업을 저장할 수 있다
  * Task 키워드를 사용한다
* 위의 코드는 20여분이 소요됐다
  * 일부 작업이 동시에 실행되었기 때문
* 또한, 위의 코드가 하나의 메서드 일때, 메서드는 비동기로 실행하기 위한 async 키워드를 붙여야 한다

```csharp
internal class Bacon { }
internal class Coffee { }
internal class Egg { }
internal class Juice { }
internal class Toast { }

static async Task<Toast> MakeToastWithButterAndJamAsync(int number)
{
    var toast = await ToastBreadAsync(number);
    ApplyButter(toast);
    ApplyJam(toast);

    return toast;
}

static async Task Main(string[] args)
{
    Coffee cup = PourCoffee();
    Console.WriteLine("coffee is ready");

    var eggsTask = FryEggsAsync(2);
    var baconTask = FryBaconAsync(3);
    var toastTask = MakeToastWithButterAndJamAsync(2);

    var eggs = await eggsTask;
    Console.WriteLine("eggs are ready");

    var bacon = await baconTask;
    Console.WriteLine("bacon is ready");

    var toast = await toastTask;
    Console.WriteLine("toast is ready");

    Juice oj = PourOJ();
    Console.WriteLine("oj is ready");
    Console.WriteLine("Breakfast is ready!");
}
```

### async 메서드
* async는 await 키워드를 메서드 내에서 사용할 수 있게 해준다
* void, Task, 혹은 Task<T>를 반환해야 한다
* void를 반환하면 메서드를 호출하는 쪽에서 비동기 제어를 할 수 없다
  * UI 버튼을 클릭하면 일어나는 작업들을 비동기로 처리할 때 void를 사용한다고 한다

### await
* void도 반환하지만 Task 또는 Task<T> 역시 반환한다

## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/concepts/async/>
* <https://private.tistory.com/24>
* <https://kangworld.tistory.com/25>