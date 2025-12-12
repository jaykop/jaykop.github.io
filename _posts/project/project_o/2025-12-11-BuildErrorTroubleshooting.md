---
title: "[DevNote] Build Error Troubleshooting"
classes: wide
categories: 
  - project
  - project_o
sidebar:
  nav: "main"
author_profile: true
---

### NU1902: 보안 취약성에 대한 패키지 종속성 감사
* 딱히 영향을 줄만한 변경점이 없었는데 갑자기 nuGet쪽 취약성으로 인해 빌드 머신에서 빌드가 안되는 현상이 발생했다
  * 어처구니 없는 건, 문제가 되는 패키지들이 전부 최신 버전이라는 것...
  * 근본적인 해결 방법은 찾지 못했지만, 일단은 취약성 경고를 에러로 처리하는 옵션을 해제하기로 했다
* 영향을 받는 XXXX.csproj 파일에 아래 옵션을 추가했다

```cs
<Property>
  <NuGetAudit>false</NuGetAudit>
  <WarningsNotAsErrors>NU1901;NU1902;NU1903;NU1904</WarningsNotAsErrors>
  
  // 기존 Property ...
</Property>
```

### C4003: windows.h 선언으로 인한 std::min, std::max 함수 컴파일 에러
* 특정 헤더 파일이 windows.h 파일을 선언하면 min max 함수 메서드가 겹치면서 컴파일 에러를 일으켰다
* 인터넷에서 경험자들이 권장하는 방법은 문제가 일어나는 파일에 #define NOMINMAX을 선언하라는 것이었다
  * 하지만 내 경우에는 엔진 코드에서 이 에러가 발생했다
* claude에게 물어보니, Project.Build.cs에 추가하기를 권했다
  * windows.h 선언이 된 파일이 여러 개일 수도 있고, 우선순위 이슈도 있어 이게 가장 나은 방법인 듯하다

```cs
public class YourProject : ModuleRules
{
    public YourProject(ReadOnlyTargetRules Target) : base(Target)
    {
        // ...

        // NOMINMAX 정의 추가
        PublicDefinitions.Add("NOMINMAX=1");
    }
}
```


