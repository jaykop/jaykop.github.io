---
title: "Replication"
classes: wide
categories: 
  - post
  - Unreal
  - Network
sidebar:
  nav: "main"
author_profile: true
---
   
## 멀티플레이어 게임
* 멀티플레이어 게임 동일한 게임이 여러 인스턴스에서 동시에 실행되어야 한다.
    * 공유된 세계에 대해 일관된, 동일한 그림을 그려내야 한다

![post_thumbnail](/assets/images/Replication/Replication_1.png)

* Server는 각 Game Instance에 대해 Authority()를 가진다
* Server에서 무언가 변경되면 해당 변경 사항은 각 Game Instance에 전파되는데, 이 프로세스가 바로 **Replication(복제)**이다

### Replication
* Unreal 자체에 내장된 first class 기능
* 소켓이나 패킷, 직렬화, 인코딩 등을 관리하지 않아도 된다.
* 특정 Property를 ***복제하겠다***고 선언하면 된다.

## NetMode

```c++
// World가 가지는 속성
ENetMode UWorld::GetNetMode() const;
```

![post_thumbnail](/assets/images/Replication/Replication_2.png)

* Playable? - 플레이 가능한가?
    * GameInstance에 LocalPlayer가 있는가?
    * Player의 Input을 처리하는가?
    * Viewport를 Rendering 하는가?
* Authority? - Server인가?
    * GameMode Actor가 포함된 World인가?
    * GameMode는 게임 플레이 전반의 핵심 로직을 정의하는 non-visual class이다
    * 이 Actor가 World에 있다는 것은 해당 World가 게임의 핵심 로직을 실행하고 관리하는 주체라는 의미이다
        * 즉, 이 World는 서버(Authority) 역할을 수행하고 있다는 뜻이다
* Open to Client? - Client의 참여가 가능한가?
    * 연결 시도에 대해 열려 있는가?
    * 다른 플레이어가 클라이언트로서 참여할 수 있는가?

![post_thumbnail](/assets/images/Replication/NetMode_1.png)

* Game이 실행되면 프로세스 수명을 가지는 GameInstance와 연결되어 URL(서버 주소 혹은 Map 이름)를 통해 Map을 로드한다
    * 그리고 World를 반환 받는다

### NM_Client

![post_thumbnail](/assets/images/Replication/NetMode_2.png)

* GameInstance가 원격 서버에 연결되었다면, 해당 World는 NM_Client가 된다
    * 서버의 요청에 따라 월드가 업데이트된다

### NM_Standalone

![post_thumbnail](/assets/images/Replication/NetMode_3.png)

* GameInstance가 로컬로 Map을 로드한 경우에는 NM_Standalone
    * Server이자 Client 역할을 모두 수행한다
    * 단일 플레이어 구성으로, Client가 연결할 수 없다

### NM_ListenServer

![post_thumbnail](/assets/images/Replication/NetMode_4.png)

* 로컬에서 Map을 로드하면서 **?Listen** 옵션과 함께 실행
    * Standalone과 동일하지만 Client가 연결할 수 있다

### NM_DedicatedServer

![post_thumbnail](/assets/images/Replication/NetMode_5.png)

* ServerOnly 콘솔 어플리케이션이다
    * Viewport도 Local Player도 없다

## Unreal Replication System
* 멀티플레이 게임을 실행하면 Background에서는 Replication System이 작동해 Sync를 맞춘다
* 각 GameInstance의 World를 구성하고, Replication System은 World에서 일어나는 일에 대해 검토 후 동시 실행을 처리한다
* 이 때 사용되는 class가 UNetDriver, UNetConnection, UNetChannel이다

![post_thumbnail](/assets/images/Replication/Replication_4.png)

### UNetDriver
* 서버와 클라이언트는 각각 UGameEngine 객체를 갖는다
* 일단 서버가 부팅하면, NetDriver가 생성된다
    * 원격 프로세스의 메시지 수신을 시작한다
* 클라이언트가 부팅하면, 역시 NetDriver가 생성된다
    * 서버 연결 요청을 전송한다

### UNetConnection
* 서버와 클라이언트의 연결에 성공하면 NetConnection이 설정된다
* 서버는 각 원격 프로세스마다 개별 NetConnection을 가진다
* 각 클라이언트는 서버와 연결된 하나의 NetConnection을 가진다

### UNetChannel
* 각 NetConnection에는 Channel이 포함된다
    * 일반적으로 VoiceChannel, ControlChannel, ActorChannel 등이 있다

* 이제 어떤 Actor가 Replication 되기를 원한다면, 이 Actor가 Replication 되도록 세팅하면 된다

```c++
// IsNetRelevantFor(P0) => true;
bReplicates = true;
```
* 이 Actor에 대해 업데이트가 필요하다고 간주되면, 서버와 클라이언트는 이 Actor Channel을 열고 해당 Actor에 대한 정보를 교환한다

## Actor Replication

![post_thumbnail](/assets/images/Replication/ActorReplication.png)

* Actor가 Replication 될 때, 아래 3요소가 동기화 된다

### Lifetime
* 서버가 Replicated Actor를 생성 또는 파괴하면, 클라이언트에서도 자체 사본을 생성 또는 파괴한다

### Property Replication
* Actor의 Property 중 Replicated 속성을 가지고 있으면 이 값의 업데이트는 서버에서 클라이언트로 전파된다

### Remote Procedure Call
* 함수가 Multicast RPC라면, 서버가 해당 함수를 처리할 때 클라이언트에서도 해당 함수를 호출해야 한다고 전한다
* Server RPC 또는 Client RPC로 단일 클라이언트와 서버 간의 통신을 할 수도 있다

### Ownership
* 각 Actor는 다른 Actor를 Owner로 설정할 수 있다
    * 보통은 Actor 생성 시에 정의된다
    * SetOwner 함수로 Runtime에 변경도 가능하다

* NetConnection은 PlayerController를 나타내며, Player가 게임에 정상적으로 로그인하면 NetConnection은 PlayerController와 연결된다
* 서버 관점에서, 이 NetConnection은 PlayerController를 **소유**하는 것이며, 즉 PlayerController가 소유한 Actor까지 소유한다
    * 즉, PlayerController가 소유하는 모든 Actor는 NetConnection이 소유하는 것이다
    * 이로써 서버가 클라이언트에 연결된 Actor를 판별할 수 있다

### Relevancy

```c++
// 모든 클라이언트에 대해서 서버는 항상 Actor의 변경점을 전파한다
bAlwaysRelevant = true;
```

* 어떤 Replicated 된 Actor의 변경점을 다른 클라이언트에 전파하는지 여부
    * 몇몇 Actor는 모든 클라이언트에 대해 Relevant 할 수도 있다
    * PlayerController와 같은 Actor는 자신을 소유한 Client에 대해서만 Relevant 하다
* 이 Relevancy는 Actor의 Owner를 inherit하도록 세팅할 수도 있다

```c++
// 특정 거리 이내의 Actor에 대해서만 업데이트하도록 세팅할 수도 있다
NetCullDistanceSquared = FMath::Sqaure(3000.f);

// 요 함수를 override 해서 조건을 커스터마이즈할 수 있다
bool AActor::IsNetRelevantFor(...)
{
    // ...
}
```

![post_thumbnail](/assets/images/Replication/ActorReplication_2.png)

* 그외에도 NetUpdateFrequency 및 NetPriority 등으로 업데이트 주기와 우선 순위를 할당할 수 있다
    * NetPriority 에서 후순위로 할당된 경우, Transfer Byte 용량이 넘어서면 업데이트 전파가 안될 수 있다
    * Skip 처리된 Actor와 플레이어에 가까운 Actor들은 높은 우선순위 보정을 받기 때문에 결국은 모두 업데이트가 되긴 한다
* 그러나 위와 같은 설정은 즉시 클라이언트로의 업데이트를 보장하지 않는다

## RPC in Detail

```c++
UFUNCTION(Client)
void Client_DoSomething();

UFUNCTION(Server)
void Server_DoSomething();

UFUNCTION(Multicast)
void Multicast_DoSomething();
```

### Client RPC

![post_thumbnail](/assets/images/Replication/RPC_1.png)

* 서버에서 Client RPC를 호출하면, 함수의 실제 구현부는 해당 함수를 호출한 Actor의 OwningClient 쪽에서만 실행된다

### Server RPC

![post_thumbnail](/assets/images/Replication/RPC_2.png)

* 클라이언트에서 Server RPC를 호출하면, 함수의 실제 구현부는 Server에서만 실행된다
* 서버가 클라이언트로부터 데이터를 수집하는 방법

### Multicast RPC

![post_thumbnail](/assets/images/Replication/RPC_3.png)

* 서버에서 Multicast RPC를 호출하면, 서버 그리고 서버와 연결된 모든 클라이언트에서 실행된다

![post_thumbnail](/assets/images/Replication/RPC_4.png)

* 이 경우에는 Relevancy 세팅에 의해 호출 여부가 결정된다

### Reliable / Unreliable

```c++
UFUNCTION(Server, Reliable)
void Server_DoSomething();

UFUNCTION(Server, Unreliable)
void Server_DoSomething();
```

* Reliable: RPC 전파와 그 순서를 보장한다
    * 과용할 경우 보틀넥 현상 혹은 패킷 자체가 loss 될 수 있다
* Unreliable: RPC 전파를 보장하지 않는다

### WithValidation

```c++
// Server_DoSomething2가 Server RPC라 가정하자

// 이 함수는 Client 사이드에서 실행한다
void ASomeActor::DoSomething1()
{
    // ...
    Server_DoSomething2();)
}

// 이 함수는 Server 사이드에서 실행한다
void ASomeActor::Server_DoSomething2_Implementation()
{
    // ...
}

// UFUNCTION(..., WithValidation)
bool ASomeActor::Server_DoSomething3_Validation()
{
    // 이 Server RPC가 fail을 반환하면, client는 그 즉시 게임에서 퇴장당한다
    return bCheated == false;
}
```

## Replicated Property in Detail

```c++
UFUNCTIONN(ReplicatedUsing=OnRep_OnUpdate)
int32 Property;

// Property 값이 업데이트 될때마다 Client 사이드에서 호출한다
UFUNCTION()
void OnRep_OnUpdate();

// Blueprint에서는 서버에서의 갑 변경 시 서버사이드에서도 호출하지만, C++ 구현 시에는 직접 호출해줘야 한다
{
    //...
    if (HasAuthority())
    {
        Property = 32;
        OnRep_OnUpdate();
    }
}
```

## Authority

```c++
enum ENetRole
{
    ROLE_None,
    ROLE_SimulatedProxy,
    ROLE_AutonomousProxy,
    ROLE_Authority
}

//
{
    // 이 GameInstance가 NM_Standalone 이거나
    // NM_DedicatedServer 혹은 NM_ListenServer 이거나
    // NM_Client이고 이 Actor가 이 Client에서 스폰되었거나 (이 Client에만 존재하거나)
    if (HasAuthority())
    {
        // 업데이트 가능
    }
    // 이 GameInstance가 NM_Client 이거나
    // 이 Actor가 Server에서 스폰되었거나
    else
    {
    
    }
}
```

### ROLE_None
* 네트워크 상에서 아무런 의미 있는 역할도 하지 않는다

### ROLE_SimulatedProxy
* 서버로부터 복제된 데이터를 수신해 자신의 상태를 업데이트한다
* 제어권은 서버에 있고, 현재 GameInstance(Client)에서는 모방해 보여주는 역할

```c++
HasAuthority() == false
IsLocallyControlled() == false
```

### ROLE_AutonomousProxy 
* 로컬 플레이어가 직접 조종한다
    * 자신의 입력을 서버에 보내고, 서버에서 받은 데이터로 업데이트 한다
* 제어권 자체는 여전히 서버에 있지만, 서버에 요청을 보내거나 Local Predict로 서버에 요청 전송 및 응답 전에 움직임을 처리하기도 한다
    * 후에 서버로부터 받은 데이터로 보정도 한다

```c++
HasAuthority() == false
IsLocallyControlled() == true
```

### ROLE_Authority  
* 모든 상태 변경의 최종적인 결정 권한을 가지고 있으며, 다른 클라이언트들에게 이 액터의 상태를 전파하는 역할

```c++
HasAuthority() == true

// 1. 서버가 Dedicdated이고 Player가 접속하지 않은 경우
IsLocallyControlled() == false

// 2. 서버가 Listen이고 서버 사이드의 플레이어가 해당 액터를 조종하는 경우
IsLocallyControlled() == true
```

![post_thumbnail](/assets/images/Replication/Authority_1.png)

## 출처
* https://www.youtube.com/watch?v=JOJP0CvpB8w