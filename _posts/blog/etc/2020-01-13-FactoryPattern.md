---
title: "팩토리 패턴(Factory Pattern)"
classes: wide
categories: 
  - blog
  - etc
---
   

팩토리 패턴
	팩토리는 부모 클래스에서 상속된 여러 자식 클래스 중 하나를 리턴하는 디자인 패턴
사전 정의되지 않은, 또는 인터페이스로서 제공되거나 동적으로 정의된 컴포넌트를 가진 클래스를 생성 
EX) 
탈것 클래스에서 모터 컴포넌트가 존재하지만, 모터의 구체적인 타입은 정의되지 않은 상태. 
추후 탈것 생성자에서 전기모터/가솔린모터 등으로 구체화 가능.
탈 것 생성자 내부에서 모터 팩토리를 콜함
사전 정의되지 않은 컴포넌트의 부모 클래스에서 의해 (동적 선언되는 또는 인터페이스만 제공되는 하위 클래스를 생성할 수 있도록 허용.  
EX) 
탈것 클래스는 전기비행선과 구형차량 따위의 하위클래스로 선언될 수 있고, 멤버로  동적할당될 타입의 모터를 가지고 있음. 하위 클래스가 생성되는 시점에 모터도 어떤 타입이 선언될 지 결정됨.
모터 타입이 히든으로 제공된다는 전제로 탈 것 팩토리를 이용해 하위 클래스를 선언하는 것이 가능
여러 개의 생성자가 존재하더라도, 코드 가독성을 보장
EX) 
Vehicle(make:string, motor:number)와 Vehicle(make:string, owner:string, license:number, purchased:date) 보다는
Vehicle.CreateOwnership(make:string, owner:string, license:number, purchased: date) 와 Vehicle.Create(make:string, motor:number)가 더 이해하기 쉬움
상위 클래스의 접근을 차단하고 바로 하부 클래스의 객체화를 하도록 디자인 
EX) 
탈 것 클래스에 대한 생성자 접근을 외부로부터 차단
오직 하위클래스에 대한 접근만을 허용하여 팩토리 메서드를 통해 생성되도록 허용
  
  
---  
출처:   
* https://quinoa.tistory.com/31
