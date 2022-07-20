---
title: "Garbage Collector"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---

## GC 기본사항
* CLR에서 자동 메모리 관리 역할을 하기 위해 GC를 둔다
  * 사용자는 메모리 해제 등 관리 작업을 위한 코드를 작성하지 않아도 된다
  * 메모리 누수 및 메모리 반환, 해제된 메모리에 접근 등 문제를 해결
  * GC에 의해 효율적으로 메모리를 할당

## 메모리 기본사항
* 각 프로세스는 고유 개별 가상 주소 공간이 있다
* 개발자는 가상 주소 공간만 접근하고 실제 메모리는 조작하지 않는다
  * GC가 사용자 대신 가상 메모리를 할당 및 해제한다

## 가비지 수집 조건
* 시스템 실제 메모리가 부족한 경우
* 힙에 할당된 개체가 메모리 허용 범위를 초과
* GC.Collect 메서드가 호출
  * 아마 GC에서 수집하도록 사용자가 직접 명령하는 메서드인 듯하다

## Garbage Collection의 원리

### GC Root란?
* 현재 실행 중인 스레드의 지역 변수
* 정적 변수
* CPU에 레지스터에 등록된 오브젝트 등

### GC Root 목록
* GC는 Root 목록을 생성하고 순회한다
  * 이 목록은 상시 접근 가능한 메모리 주소로 이루어져 있다
  * 프로세스에 의해 생성된 Object들의 참조를 보유한다
  * Object의 참조가 있다면 이 Object는 alive한 상태로 마킹된다
* 각 GC Root는 하나의 Object가 아닌, Object로의 참조 혹은 그 여부다
  * 아무것도 연결되지 않은, 즉 참조가 없는 Object는 Garbage로 수집된다

### Object Graph
* 위의 참조에 근거해서 .Net은 그래프를 생성한다
* 메모리 프로파일러는 이 그래프를 보고 참조 여부를 추적한다

## Garbage Collection의 한계

### 미사용 오브젝트가 참조되어 수집되지 않는 경우
* 사실상 메모리 누수
  * 가용 메모리가 점점 늘어나는 현상을 말고는 발견할 수 있는 방법도 없다
* 가비지 컬렉터 자체는 풍부한 메모리 사용을 지향하기 위한 것
  * 따라서 객체가 언제 메모리로 반환되는지 여부 자체는 신경쓰지 않는다

### 힙의 파편화
* 힙에 하나의 큰 메모리 청크가 할당되고, 이 힙 구간에 할당된 여러 객체는 실행 중에 그 주소를 옮길 수 없다
  * 이 중 몇 객체의 라이프 사이클이 다른 객체보다 길다면, 파편화가 발생한다

## 출처
* <https://docs.microsoft.com/ko-kr/dotnet/standard/garbage-collection/fundamentals>
* <https://www.informit.com/articles/article.aspx?p=474652&seqNum=9>
* <https://luv-n-interest.tistory.com/922>
* <https://www.red-gate.com/simple-talk/development/dotnet-development/understanding-garbage-collection-in-net/>