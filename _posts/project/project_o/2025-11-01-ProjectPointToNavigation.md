---
title: "[DevNote] ProjectPointToNavigation"
classes: wide
categories: 
  - project
  - project_o
sidebar:
  nav: "main"
author_profile: true
---

## 가장 가까운 NavMesh 위치 탐색
*  ProjectPointToNavigation을 많이 사용한다

```c++
UNavigationSystemV1* NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());
NavSys->ProjectPointToNavigation(MoveRequest.GetGoalLocation(), ProjectedLocation, INVALID_NAVEXTENT, &AgentProps);
```

* 위 함수를 사용해 보통은 Z축 기준으로 하방에 있는 NavMesh 위의 Position을 탐색한다

### Extent의 의미
*  Extent 박스와 교차하는 폴리곤들 중에서만 가장 가까운 점을 찾기 때문에, 실제로 더 가까운 폴리곤이 Extent 범위 밖에 있으면 찾지 못합니다.

```c++
// NavigationSystem.h
bool ProjectPointToNavigation(const FVector& Point, FNavLocation& OutLocation, const FVector& Extent = INVALID_NAVEXTENT, const FNavAgentProperties* AgentProperties = NULL, FSharedConstNavQueryFilter QueryFilter = NULL)
	{
		return ProjectPointToNavigation(Point, OutLocation, Extent, AgentProperties != NULL ? GetNavDataForProps(*AgentProperties, Point) : GetDefaultNavDataInstance(FNavigationSystem::DontCreate), QueryFilter);
	}

// NavigationType.h
#define INVALID_NAVEXTENT (FVector::ZeroVector)
```

* EXTENT 범위를 충분히 넓게 가져가지 않으면 아무 검사도 하지 않을 수 있다

```c++
bool UNavigationSystemV1::ProjectPointToNavigation(const FVector& Point, FNavLocation& OutLocation, const FVector& Extent, const ANavigationData* NavData, FSharedConstNavQueryFilter QueryFilter) const
{
	SCOPE_CYCLE_COUNTER(STAT_Navigation_QueriesTimeSync);

	if (NavData == nullptr)
	{
		NavData = GetDefaultNavDataInstance();
	}

	return NavData != nullptr && NavData->ProjectPoint(Point, OutLocation
											, UE::Navigation::Private::IsValidExtent(Extent) ? Extent : NavData->GetConfig().DefaultQueryExtent
											, QueryFilter);
}
```

* 이 경우, NavData의 Config에 접근해 Default Extent 값을 가져와 적용한다
* 즉, 이 함수를 사용한다면 매번 분명히 의도한 Extent값을 넣어주거나 DefaultQueryExtent에 프로젝트에 통용될 만한 유의미한 값을 세팅해줘야 한다

### 진짜 가까운 NavMesh를 탐색하는가?
* Extent와 겹치는 NavMesh를 검사하고, findNearestPoly2D와 closestPointOnPoly를 통해 실제 NavMesh 상의 가장 가까운 Point를 반환하는 건 맞는 것으로 보인다

```c++
dtStatus dtNavMeshQuery::closestPointOnPoly(dtPolyRef ref, const float* pos, float* closest) const
{
    // ...
    closestPointOnPolyInTile(tile, poly, pos, closest);
    return DT_SUCCESS;
}

void dtNavMeshQuery::closestPointOnPolyInTile(const dtMeshTile* tile, const dtPoly* poly, const float* pos, float* closest) const
{
    // ...
    
    // Clamp point to be inside the polygon.
    dtVcopy(closest, pos);
    if (!dtDistancePtPolyEdgesSqr(pos, verts, nv, edged, edget))
    {
        // Point is outside the polygon, clamp to nearest edge.
        float dmin = FLT_MAX;
        int imin = -1;
        for (int i = 0; i < nv; ++i)
        {
            if (edged[i] < dmin)
            {
                dmin = edged[i];
                imin = i;
            }
        }
        const float* va = &verts[imin*3];
        const float* vb = &verts[((imin+1)%nv)*3];
        dtVlerp(closest, va, vb, edget[imin]); // 가장 가까운 edge 위의 점
    }

    // Find height at the location using detail mesh
    // ...
}
```

* 다만 Extent 체크를 Sphere가 아닌 육면체로 하기 때문에, 항상 가장 가까운 Point를 반환하지는 못할 수도 있다
  * 따라서 충분한 Extent 수치를 항상 고려하고 인자에 넣어야 한다