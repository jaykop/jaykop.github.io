---
title: "[DevNote] OnlineSubsystem 세션 탐색 및 접속 Troubleshooting"
classes: wide
categories:
  - unreal
  - framework
sidebar:
  nav: "main"
author_profile: true
---

## Session Search 안되는 현상

세션을 검색하는 세팅 구조체 FOnlineSearchSettings를 정의할 때 아래와 같이 한다.

```c++
FOnlineSearchSettings SearchSettings;
//	SearchSettings.Set(SEARCH_PRESENCE, true, EOnlineComparisonOp::Equals); DEPRECATED 됨. 사용 안함.
SearchSettings.Set(SEARCH_EMPTY_SERVERS_ONLY, false, EOnlineComparisonOp::Equals);
SearchSettings.Set(SEARCH_NONEMPTY_SERVERS_ONLY, false, EOnlineComparisonOp::Equals);
SearchSettings.Set(SEARCH_SECURE_SERVERS_ONLY, false, EOnlineComparisonOp::Equals);
SearchSettings.Set(SEARCH_MINSLOTSAVAILABLE, 1, EOnlineComparisonOp::GreaterThanEquals);
SearchSettings.Set(SEARCH_LOBBIES, true, EOnlineComparisonOp::Equals);
```

이 설정을 유지한 상태로 엔진 업데이트 후 세션 검색이 되지 않는 현상이 발생했다.

```c++
/** Search for a match with min player availability (value is int) */
#define SEARCH_MINSLOTSAVAILABLE FName(TEXT("MINSLOTSAVAILABLE"))
```

주석 설명은 참가 가능한 자리(Slot)의 개수가 SEARCH_MINSLOTSAVAILABLE보다 높으면 반환 결과에 포함시킨다는 것인데, 기존 코드는 최소 1자리 이상인, 그러니까 참여할 수 있는 Slot이 있는 Session만 검색하기를 바랐다.

겉보기엔 이것이 문제가 아니었기에 다른 부분만 열심히 찾아보다가 결국 SEARCH_MINSLOTSAVAILABLE 값을 0으로 바쿼 테스트했고, 그랬더니 모든 세션을 검색해서 반환 결과가 표시되었다.

```c++
SearchSettings.Set(SEARCH_MINSLOTSAVAILABLE, 0, EOnlineComparisonOp::GreaterThanEquals);
```

Slot이 없어 참가할 수 없는 세션도 검색되어 나온 결과를 보니 SEARCH_MINSLOTSAVAILABLE의 의도 자체는 참가할 수 있는 인원(슬롯)의 최소값이 맞기는 한 거 같은데...
엔진 버그인지 뭔지 알수가 없었다.
Unreal Forum을 좀 더 찾아보니 답변 중에 이와 관련된 내용이 있긴 했다.

## Session Join 안되는 현상

이후 세션 검색 결과는 표시되지만 Slot이 있는 세션에 접속이 안되는 현상이 발생했다.

```c++
// FindSession에서 찾은 Session의 SessionSetting을 JoinSession 전에 다시 설정
auto NewSessionToJoin = InSessionToJoin;
/** Whether to prefer lobbies APIs if the platform supports them */
NewSessionToJoin.Session.SessionSettings.bUseLobbiesIfAvailable = true;
/** Whether to display user presence information or not */
NewSessionToJoin.Session.SessionSettings.bUsesPresence = true;

bIsJoiningSessionInProgress = true;
const TSharedPtr<const FUniqueNetId> UniqueNetId = LocalPlayer->GetPreferredUniqueNetId().GetUniqueNetId();
GetSessionInterface()->JoinSession(*UniqueNetId, InSessionName, NewSessionToJoin);
```

다행히 동일한 버그 해결 방법이 있어 그대로 적용했더니 해결 되었다.
Sesstion Settings가 FindSession 실행 후 변경되는 현상이 있었고, 변수 2개 값을 다시 초기화해 테스트하니 세션 접속에 성공했다.

## 출처
* <https://forums.unrealengine.com/t/isten-server-steamlobby-not-listed-advanced-sessions/488267/2>
* <https://velog.io/@ryan_ur/Multiplayer%EC%9A%A9-Session-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EB%A7%8C%EB%93%A4%EC%96%B4-%EB%B3%B4%EA%B8%B0-2>
