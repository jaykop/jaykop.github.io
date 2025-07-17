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