---
title: "Actor Lifecyle"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## 기본적인 Actor의 라이프 사이클
### PreInitializeComponents
* 컴포넌트 초기화 이전 
### InitializeComponents
* 액터에 정의된 각 컴포넌트 생성용 헬퍼 함수
### PostInitializeComponents
* 액터에 속한 모든 컴포넌트의 초기화가 완료
### BeginePlay
* 플레이 시작, 레벨이 시작되면 호출
* 액터가 게임에 참여할 때 호출
### Tick
* 매 프레임 호출
### EndPlay
* 액터가 게임에서 퇴장할 때 호출
* Destory, Level Transition, 액터가 존재하는 Level Streaming이 Unload 되면 발동

## 각 라이프 사이클의 시점들
### 디스크에서 로드
* 최초 액터를 생성하는 시점
  * 로드할 레벨에 이미 존재하고 있는(세팅되어 있는) 액터에 대한 생명주기 단계
* LoadMap - 최초 레벨과 함께 로드
* AddToWorld - World Partition에서 Steaming 할 때 레벨과 함께 로드

### 에디터에서 플레이
* 디스크에서 로드하지 않고, 에디터에 이미 초기화되어 있는 액터를 복사

### 위 두 과정에서 차이와 공통점?
* 디스크에서 로드는 최초에 액터 정보를 디스크로부터 읽어와 생성
  * PostLoad 함수 호출
* 에디터에서 플레이는 에디터에 이미 불러온 정보를 바탕으로 액터를 생성
  * PostDuplicate 함수 호출
* 이후 과정은
  * InitializeActosForPlay - 플레이할 액터를 초기화
  * 아직 초기화 되지 않은 액터들은 RouteActorInitialize 함수 호출
    * PreInitializeComponents, InitializeComponents, PostInitializeComponents
  * 그리고 BeginPlay

### 스폰
* 액터를 인스턴싱하는 단계
* SpawnActor -> PostSpawnInitialize -> PostActorCreated -> ExecuteConstruction -> PostActorConstruction 
* PostActorCreated
  * 에디터나 게임 플레이 도중 생성되었ㅇ르 때 호출
  * 레벨에 의해 로드된 경우는 안 불림
* ExecuteConstruction -> OnConstruction
  * ExecuteConstruction은 블루프린트 생성
  * OnConstruction은 모든 블루프린트가 생성된 뒤, ExecuteConstruction 끝에 호출
  * 게임 플레이 중 스폰된 액터에서만 호출
* OnActorSpawned 
  * 액터 스폰이 완전히 종료되면 World에 Broadcast한다

## 디퍼드 스폰
* 유예 생성을 시킬 액터들을 나중에 한번에 몰아서 스폰시킬 때 사용하는 플로우

## 액터의 소멸
### 게임플레이 도중 
* Destroy
  * 게임 플레이 중 수동으로 액터를 제거
  * 킬 대기 상태로 액터를 마킹
  * 레벨 액터 배열에서 제거
* EndPlay
  * 액터의 수명이 끝남을 컨펌
  * Destroy, 에디터 플레이 종료, Level Transition, 스트리밍 레벨 언로드, 어플리케이션 종료 등의 상황에서 호출
* OnDestroy
  * 액터가 소멸하면서 호출
  * Legacy이므로 이 코드 내용은 가급적 Level Transition이나 EndPlay로 옮기자

### 가비지 컬렉션
* 소멸 예정으로 마킹된 이후, 액터가 실제 제거되는 시점은 가비지 컬렉션을 통해 리소스가 해제될 때
* BeginDestroy
  * 오브젝트 메모리 해제
* IsReadyForFinishDestory
  * 가비지 컬렉션 프로세스가 이 액터 메모리를 영구 해제해도 되는지 확인
  * false면 다음 프로세스로 유예
* FinishDestory
  * 메모리 해제 직전 호출

## 수명 주기 분해도
![post_thumbnail](/assets/images/ActorLifeCycle1.webp)

## 출처
* <https://docs.unrealengine.com/4.27/ko/ProgrammingAndScripting/ProgrammingWithCPP/UnrealArchitecture/Actors/ActorLifecycle/>
* <https://woo-dev.tistory.com/267>
* <https://narakit.tistory.com/185>