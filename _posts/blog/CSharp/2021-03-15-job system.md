---
title: "Job System"
classes: wide
categories: 
  - blog
  - CSharp
---
   

**delegate(대리자) 키워드**  
  
delegate는 메서드를 다른 메서드에 인수로 전달하는 데 사용된다. 형식이 일치하는 구조의 모든 메서드는 대리자에 할당할 수 있다. 메서드는 정적/인스턴스일 수 있다. 
  
**delegate 속성**  
  
* 함수 포인터와 유사하지만, 객체 지향적으로 인스턴스 및 메서드를 캡슐화한다.
* 메서드를 매개 변수로 전달할 수 있다.
* 콜백 메서드를 정의할 수 있다.
  
**delegate 가변성 사용**  
  
* Covariance(공변성)
  - 메서드가 대리자에 정의된 것보다 더 많은 수의 파생된 형식을 반환하도록 허용  
  - 기존에 정의된 반환 타입의 파생 클래스를 반환하는 것을 허용

```cs
  class Mammals {}  
  class Dogs : Mammals {}  
    
  class Program  
  {  
      
      //Define the delegate.
      public delegate Mammals HandlerMethod();  
    
      public static Mammals MammalsHandler()  
      {  
          return null;  
      }  
    
      public static Dogs DogsHandler()  
      {  
          return null;  
      }  
    
      static void Test()  
      {  
          HandlerMethod handlerMammals = MammalsHandler;  
    
          // Covariance enables this assignment.  
          HandlerMethod handlerDogs = DogsHandler;  
      }  
  }
```  
  
* Contravariance(반공변성)
  - 메서드가 대리자 형식보다 더 적은 수의 파생된 매개 변수 형식을 갖도록 허용  
  - 부모 클래스를 매개 변수를 사용하는 메서드를 정의하고, 파생 클래스를 매개 변수로 하는 대리자를 통해 이를 처리

```cs  
public delegate void KeyEventHandler(object sender, KeyEventArgs e);

public delegate void MouseEventHandler(object sender, MouseEventArgs e);

// Event handler that accepts a parameter of the EventArgs type.  
private void MultiHandler(object sender, System.EventArgs e)  
{  
    label1.Text = System.DateTime.Now.ToString();  
}  
  
public Form1()  
{  
    InitializeComponent();  
  
    // You can use a method that has an EventArgs parameter,  
    // although the event expects the KeyEventArgs parameter.  
    this.button1.KeyDown += this.MultiHandler;  
  
    // You can use the same method
    // for an event that expects the MouseEventArgs parameter.  
    this.button1.MouseClick += this.MultiHandler;  
  
}  

```  
  
---  
출처:   
<https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/delegates/>  
<https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/concepts/covariance-contravariance/using-variance-in-delegates>
