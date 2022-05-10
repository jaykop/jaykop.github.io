---
title: "Job System"
classes: wide
categories: 
  - post
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---
   
## Job System

### Job이란?
* 단일 작업을 수행하는 작업 단위

### Job System이란?
* 스레드를 대신해 태스크를 만들어 멀티스레드 코드를 관리
* 여러 코어에 걸쳐 워커 스레드 그룹을 관리
* 일반적으로 컨텍스트 변경을 방지하기 위해 코어당 하나의 워커 스레드가 있으나 사용할 코어 예약도 가능
* 잡 대기열에 순서대로 잡을 배치하여 실행

```CSharp
public class RotationSpeedSystem : JobComponentSystem
{
    [BurstCompile]
    struct RotationSpeedRotation : IJobForEach<Rotation, RotationSpeed>
    {
        public float dt;

        public void Execute(ref Rotation rotation, [ReadOnly]ref RotationSpeed speed)
        {
            rotation.value = math.mul(math.normalize(rotation.value), quaternion.axisAngle(math.up(), speed.speed * dt));
        }
    }

    // Any previously scheduled jobs reading/writing from Rotation or writing to RotationSpeed 
    // will automatically be included in the inputDeps dependency.
    protected override JobHandle OnUpdate(JobHandle inputDeps)
    {
        var job = new RotationSpeedRotation() { dt = Time.deltaTime };
        return job.Schedule(this, inputDeps);
    } 
}
```

* 다른 시스템에서의 여러 job도 병렬 상태의 IComponentData를 상속한 Data로부터 read 작업을 수행할 수 있다
* 어떤 job이 Data에 write 작업을 수행하는 중에는 다른 job들은 작업을 수행할 수 없으며, 작업 스케줄링을 걸어둔다

### 작동 방식
* 모든 job 그리고 system은 어떤 ComponentType에 대하여 작업을 수행할 것인지를 선언한다
* JobComponentSystem은 JobHandle을 반환하고, EntityManager를 통해 raed 중인지 write 중인지 자동으로 정보를 제공한다
* 한 system이 A 컴포넌트에 대해 write 작업 중이고, 또 다른 system이 A 컴포넌트 읽기 작업을 하려 한다면, JobComponentSystem이 작업 타입 리스트를 살펴보고 write 작업 중인 시스템이 있음을 알릴 것이다.

## 안전 시스템
* 데드락 방지를 위해 데이터의 레퍼런스가 아닌 복사본을 이용해 처리
* bittable 데이터 타입에만 엑세스 가능
* memcopy를 이용해 데이터를 복사
  
## NativeContainer 
* 네이티브 메모리에 비교적 안전한 C# Wrapper 를 제공하여 관리되는 값 형식
* NavtiveContainer를 사용하면 Job을 통해 사본으로 작업하는 대신 주 스레드와 공유 된 데이터에 접근
* 기본 제공되는 타입은 NativeArray<T>

## 출처
* <https://redforce01.tistory.com/239>
* <https://redforce01.tistory.com/240?category=721608>
* <https://zprooo915.tistory.com/66>
* <https://mrbinggrae.tistory.com/223?category=882742>
* <https://docs.unity3d.com/Packages/com.unity.entities%400.1/manual/job_component_system.html?q=JobComponentSystem>