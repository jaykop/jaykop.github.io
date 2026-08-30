---
title: "[Game A.I.] Path-Finding"
classes: wide
categories:
  - archive
  - game-ai-theory
author_profile: true
sidebar:
  nav: "main"
author_profile: true
---

## 공간 분할의 타입
### Grid
![post_thumbnail](/assets/images/PathFinding/01.png)
### QuadTree/OctTree
![post_thumbnail](/assets/images/PathFinding/02.png)
![post_thumbnail](/assets/images/PathFinding/03.png)
### Waypoint graphs
![post_thumbnail](/assets/images/PathFinding/04.png)
### Coner graphs
![post_thumbnail](/assets/images/PathFinding/05.png)
### Circle-based waypoint graphs
![post_thumbnail](/assets/images/PathFinding/06.png)
### Navigation meshess
![post_thumbnail](/assets/images/PathFinding/07.png)

## Path-Finding Search Algorithm
* Random Bounce
* Robust Trace
* [BFS & DFS]()
* [Dijkstra](https://jaykop.github.io/archive/game-ai-theory/A_star/#%EB%8B%A4%EC%9D%B5%EC%8A%A4%ED%8A%B8%EB%9D%BC-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-dijkstra-algorithm)
* Greedy Best-First
* [A*](https://jaykop.github.io/archive/game-ai-theory/A_star/)
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
![post_thumbnail](/assets/images/PathFinding/08.png)
* xDiff + yDiff = 9 + 3 = 12
* 체스에서 거리를 정의할 때 이동

### Chebyshev distance
![post_thumbnail](/assets/images/PathFinding/09.png)
* max(xDiff, yDiff) = max(9, 3) = 9
* **두 지점 사이의 벡터 값 중 가장 큰 값**
* 체스에서 킹의 움직임을 정의할 때 이용
  * 킹은 대각선 이동도 가능하므로, 이 경우를 커버하기 위함

### Euclidean distance
![post_thumbnail](/assets/images/PathFinding/10.png)
* sqrt(xDiff2 + yDiff2) = sqrt(92 + 32) = 9.48
* 두 지점 사이의 최단 거리를 측정
* **Most optimal**

### Octile distance
![post_thumbnail](/assets/images/PathFinding/11.png)
* min(xDiff, yDiff) * sqrt(2) + (max(xDiff, yDiff) – min(xDiff, yDiff))
* min(9, 3) * 1.41 + (max(9, 3) – min(9, 3)) = 10.24
* **경로 상의 Grid를 명확히 지정할 수 있음**

## 출처
* <https://en.wikipedia.org/wiki/Chebyshev_distance>
* <https://datascience.stackexchange.com/questions/20075/when-would-one-use-manhattan-distance-as-opposed-to-euclidean-distance>
* <https://discuss.analyticsvidhya.com/t/when-manhattan-distance-is-preffered-over-euclidean-distance/80112>