---
title: "Path-Finding"
classes: wide
categories: 
  - post
  - etc
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## 공간 분할의 타입
### Grid
![post_thumbnail](/assets/images/{5A275299-4B06-4925-8821-A4745827DDD7}.png)
### QuadTree/OctTree
![post_thumbnail](/assets/images/{FF9AF87A-BF67-48D1-9AEB-DC682B303246}.png)
![post_thumbnail](/assets/images/{C64ECF75-C726-47DB-9840-AFD3592839D7}.png)
### Waypoint graphs
![post_thumbnail](/assets/images/{30674D68-35CF-4969-B957-F0D8F79B63A6}.png)
### Coner graphs
![post_thumbnail](/assets/images/{851E96E9-7AB4-46B2-972B-3FA450700EDD}.png)
### Circle-based waypoint graphs
![post_thumbnail](/assets/images/{BBB94392-3B82-4EEF-B71F-18D51D909096}.png)
### Navigation meshess
![post_thumbnail](/assets/images/{B2E60B62-EB19-44C0-94EA-20465A4B1BD8}.png)

## Path-Finding Search Algorithm
* Random Bounce
* Robust Trace
* [BFS & DFS]()
* [Dijkstra](https://jaykop.github.io/post/etc/A-star/#%EB%8B%A4%EC%9D%B5%EC%8A%A4%ED%8A%B8%EB%9D%BC-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98dijkstra-algorithm)
* Greedy Best-First
* [A*](https://jaykop.github.io/post/etc/A-star/#a-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98a-algorithm)
* Jump Point Search
* Roy-Floyd-Warshall

## 탐색 알고리즘의 구조

### OpenedList
방문한 적이 없는 노드 셋
### ClosedList
이미 방문한 노드 셋
### 노드의 구조

```c++
struct Node
{
  Node* parent;
  float cost;
} 
```

1. 시작 노드를 OpenList에 추가
2. While (OpenList not empty)
  - OpenList에서 노드를 버퍼에 저장한 뒤 삭제
  - 버퍼의 노드가 목적지라면 while 문 종료
  - 아닌 경우 노드의 이웃들에 대한 이동 cost 측정
  - 조건부로 OpenList에 이웃 노드를 추가
  - 현재 노드를 ClosedList에 추가

## Heuristics Calculation
### Manhattan distance
![post_thumbnail](/assets/images/{293326BC-E385-49F7-B1E5-ED067CC24061}.png)
* xDiff + yDiff = 9 + 3 = 12
* 체스에서 거리를 정의할 때 이동
### Chebyshev distance
![post_thumbnail](/assets/images/{FDB81158-1C49-4FFC-BD56-075161EA63C5}.png)
* max(xDiff, yDiff) = max(9, 3) = 9
* **두 지점 사이의 벡터 값 중 가장 큰 값**
* 체스에서 킹의 움직임을 정의할 때 이용
  * 킹은 대각선 이동도 가능하므로, 이 경우를 커버하기 위함
### Euclidean distance
![post_thumbnail](/assets/images/{83040582-7CEB-49E8-A44C-B8F34E173DFB}.png)
* sqrt(xDiff2 + yDiff2) = sqrt(92 + 32) = 9.48
* 두 지점 사이의 최단 거리를 측정
* **Most optimal**
### Octile distance
![post_thumbnail](/assets/images/{1BD82934-0A8F-4A8C-A715-2061E86688BE}.png)
* min(xDiff, yDiff) * sqrt(2) + (max(xDiff, yDiff) – min(xDiff, yDiff))
* min(9, 3) * 1.41 + (max(9, 3) – min(9, 3)) = 10.24
* **경로 상의 Grid를 명확히 지정할 수 있음**

## 출처
* <https://en.wikipedia.org/wiki/Chebyshev_distance>
* <https://datascience.stackexchange.com/questions/20075/when-would-one-use-manhattan-distance-as-opposed-to-euclidean-distance>
* <https://discuss.analyticsvidhya.com/t/when-manhattan-distance-is-preffered-over-euclidean-distance/80112>