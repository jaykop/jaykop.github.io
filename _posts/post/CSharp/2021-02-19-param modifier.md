---
title: "C# parameter modifier"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   

## in 키워드
* in 매개변수로 전달되는 변수는 메서드로 전달되기 전 반드시 초기화
* 인수가 참조로 전달되지만, 수정되지 않음
* C++에서의 const Type&과 유사
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

## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/language-reference/keywords/ref>
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/language-reference/keywords/in-parameter-modifier>
* <https://docs.microsoft.com/ko-kr/dotnet/csharp/language-reference/keywords/out-parameter-modifier>
* <https://dobby-the-house-elf.tistory.com/159>
