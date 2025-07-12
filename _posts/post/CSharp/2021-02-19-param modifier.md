---
title: "C# parameter modifier"
classes: wide
categories: 
  - post
  - CSharp
  - Unity
sidebar:
  nav: "main"
author_profile: true
---
   

## in 키워드
* in 매개변수로 전달되는 변수는 메서드로 전달되기 전 반드시 초기화
* 인수가 참조로 전달되지만, 수정되지 않음
* **오버로딩 규칙**
  ```csharp
  class InOverloads
  {
      // 오버로딩 허용
      public void SampleMethod(in int i) { }
      public void SampleMethod(int i) { }
  }

  class CS0663_Example
  {
      // 오버로딩 미허용
      // Compiler error CS0663: "Cannot define overloaded
      // methods that differ only on in, ref and out".
      public void SampleMethod(in int i) { }
      public void SampleMethod(ref int i) { }
  }
  ```

## out 키워드
* out 매개변수로 전달되는 변수는 메서드로 전달되기 초기화할 필요 없음
* 그러나 메서드가 반환되기 전, 반드시 값을 할당
* **오버로딩 규칙**
  ```csharp
  class OutOverloadExample
  {
      // 오버로딩 허용
      public void SampleMethod(int i) { }
      public void SampleMethod(out int i) => i = 5;
  }

  class CS0663_Example
  {
      // 오버로딩 미허용
      // Compiler error CS0663: "Cannot define overloaded
      // methods that differ only on ref and out".
      public void SampleMethod(out int i) { }
      public void SampleMethod(ref int i) { }
  }
  ```

## ref 키워드  
* 참조로 메서드에 인수 전달
* 메서드 정의와 호출 메서드가 모두 ref 키워드를 명시적으로 사용
  ```csharp
  void Method(ref int refArgument)
  {
      refArgument = refArgument + 44;
  }

  int number = 1;
  Method(ref number);
  Console.WriteLine(number);
  // Output: 45
  ```
* **오버로딩 규칙**
  ```csharp
  class RefOverloadExample
  {
      // 오버로딩 허용
      public void SampleMethod(int i) { }
      public void SampleMethod(ref int i) { }
  }
  ```

## 테이블

|키워드|읽기|쓰기|
|:---:|:---:|:---:|
|ref|가능|가능|
|in|가능|불가능|
|out|가능|필수|

## params 키워드
* 가변 개수의 인수를 사용하는 메서드 매개 변수를 지정
* params 키워드 뒤에 다른 매개 변수를 추가할 수 없음
* 선언 형식은 1차원 array
* **사용 예시**

```csharp
public void UseParams(params int[] list) 
{
  // do something withe the list...
}

int Main()
{
  // 지정된 형식의 쉼표로 구분된 인수 목록으로 호출
  UseParams(1,2,3,4);

  // 지정된 형식의 array로 호출
  int [] a = {1,2,3,4,5};
  UseParams(a);
}
```

## 참초 타입 인자
### 값으로 인자 넘기기

```csharp
class PassingRefByVal
{
    static void Change(int[] pArray)
    {
        pArray[0] = 888;  // 이 할당은 원래 arr 데이터에 영향을 준다
        pArray = new int[5] {-3, -1, -2, -3, -4};   // 이 할당은 로컬에 한정된다
        System.Console.WriteLine("Inside the method, the first element is: {0}", pArray[0]);
    }

    static void Main()
    {
        int[] arr = {1, 4, 5};
        System.Console.WriteLine("Inside Main, before calling the method, the first element is: {0}", arr [0]);

        Change(arr);
        System.Console.WriteLine("Inside Main, after calling the method, the first element is: {0}", arr [0]);
    }
}
/* 결과:
    Inside Main, before calling the method, the first element is: 1
    Inside the method, the first element is: -3
    Inside Main, after calling the method, the first element is: 888
*/
```

* 지역 변수로 새롭게 할당하려한 주소값은 스코프(Change 함수) 내에서만 유효하고, 그 밖에서는 그렇지 못했다
  * 다만 직접 메모리에 접근해 값을 수정한 **pArray[0] = 888;**는 유효했다

### 참조로 인자 넘기기

```csharp
class PassingRefByRef
{
    static void Change(ref int[] pArray)
    {
        // 아래 할당은 모두 arr 데이터에 영향을 준다
        pArray[0] = 888;
        pArray = new int[5] {-3, -1, -2, -3, -4};
        System.Console.WriteLine("Inside the method, the first element is: {0}", pArray[0]);
    }

    static void Main()
    {
        int[] arr = {1, 4, 5};
        System.Console.WriteLine("Inside Main, before calling the method, the first element is: {0}", arr[0]);

        Change(ref arr);
        System.Console.WriteLine("Inside Main, after calling the method, the first element is: {0}", arr[0]);
    }
}
/* Output:
    Inside Main, before calling the method, the first element is: 1
    Inside the method, the first element is: -3
    Inside Main, after calling the method, the first element is: -3
*/
```

* ref로 넘긴 참조형의 인자는 스코프 내에서도 모두 값이 변화한다

## Unity에서 Vector3의 값 변경하기

```csharp
transform.position.x = 10f; // 안 바뀜
transform.position.SetX(10f); // 안 바뀜

transform.posiiton = new Vector3(10f, 0f, 0f); // 바뀜

// ????
```

* 위와 같은 일이 많았다
* 우선, transform.position은 gettor, 즉 read-only다
  * 아무리 값을 변경하려고 해도 그 copy에 값을 할당하고 있을 뿐이다.
  * ~~직접 접근하고 싶다면, position[0], position[1], position[2]로 접근할 수 있다~~안 되던데???
* 그럼 transform.position의 Set은?
  * 역시 gettor가 불려왔기 때문
* 그럼 다른 방법은?

```csharp
// 값을 복사해서 다시 할당하거나
var pos = transform.position;
pos.y = 1f;
transform.position = pos;

// 아예 새로 할당하거나
transform.position = new Vector3(1f, 1f, 1f);
```

* 위의 방법으로 먹히는 이유는?

```csharp
Vector3 position { get; set; }
```

* =operator에 의해 set이 발동했기 때문

## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/language-reference/keywords/ref>
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/language-reference/keywords/in-parameter-modifier>
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/language-reference/keywords/out-parameter-modifier>
* <https://dobby-the-house-elf.tistory.com/159>
* <https://forum.unity.com/threads/why-can-i-modify-transform-position-but-not-transform-position-y.504494/>
* <https://docs.unity3d.com/ScriptReference/Vector3.Index_operator.html>