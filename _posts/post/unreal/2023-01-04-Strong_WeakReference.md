---
title: "Hard Reference & Soft Reference"
classes: wide
categories: 
  - post
  - Unreal
sidebar:
  nav: "main"
author_profile: true
---

## Hard Reference

```c++
// PlayerCharacter.h
#include "Engine/StaticMesh.h"  // 헤더에서 직접 include
#include "Components/StaticMeshComponent.h"

UCLASS()
class MYGAME_API APlayerCharacter : public ACharacter
{
  GENERATED_BODY()

public:
  // Hard Reference - 에디터에서 직접 할당
  UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Weapon")
  UStaticMesh* WeaponMesh;
  
  // Hard Reference - 컴포넌트
  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
  UStaticMeshComponent* WeaponMeshComponent;
};

// PlayerCharacter.cpp
APlayerCharacter::APlayerCharacter()
{
  WeaponMeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("WeaponMeshComponent"));
  
  // Hard Reference - 생성자에서 직접 로드 (게임 시작시 바로 메모리에 로드됨)
  static ConstructorHelpers::FObjectFinder<UStaticMesh> WeaponMeshAsset(
      TEXT("/Game/Weapons/Sword_Mesh.Sword_Mesh"));
  
  if (WeaponMeshAsset.Succeeded())
  {
    WeaponMesh = WeaponMeshAsset.Object;
    WeaponMeshComponent->SetStaticMesh(WeaponMesh);
  }
}
```

* 컴파일 타임에 의존성이 결정된다
* 참조하는 오브젝트가 메모리에 항상 로드되어 있어야 한다
  * 이로 인해 초반 로딩 시간이 길어진다
  * 상시 메모리 사용량도 늘어난다
  * 해당 메모리에 빠르게 접근할 수 있다

## Soft Reference

```c++
// PlayerCharacter.h
#include "Engine/StreamableManager.h"

UCLASS()
class MYGAME_API APlayerCharacter : public ACharacter
{
  GENERATED_BODY()

public:
  APlayerCharacter();

  // Soft Reference - 경로만 저장, 실제 오브젝트는 로드되지 않음
  UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Weapon")
  TSoftObjectPtr<UStaticMesh> WeaponMeshSoft;

  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
  UStaticMeshComponent* WeaponMeshComponent;

  UFUNCTION(BlueprintCallable)
  void LoadWeaponAsync();
  
  UFUNCTION(BlueprintCallable)
  void LoadWeaponSync();

private:
    FStreamableManager StreamableManager;
};

// PlayerCharacter.cpp
APlayerCharacter::APlayerCharacter()
{
  WeaponMeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("WeaponMeshComponent"));
  
  // Soft Reference - 경로만 설정 (메모리에 로드되지 않음)
  WeaponMeshSoft = TSoftObjectPtr<UStaticMesh>(FSoftObjectPath(TEXT("/Game/Weapons/Sword_Mesh.Sword_Mesh")));
}

void APlayerCharacter::LoadWeaponAsync()
{
  // 비동기 로드
  StreamableManager.RequestAsyncLoad(
    WeaponMeshSoft.ToSoftObjectPath(),
    FStreamableDelegate::CreateLambda([this]()
    {
      if (UStaticMesh* LoadedMesh = WeaponMeshSoft.Get())
      {
        WeaponMeshComponent->SetStaticMesh(LoadedMesh);
      }
    })
  );
}

void APlayerCharacter::LoadWeaponSync()
{
  // 동기 로드
  if (UStaticMesh* LoadedMesh = WeaponMeshSoft.LoadSynchronous())
  {
    WeaponMeshComponent->SetStaticMesh(LoadedMesh);
  }
}
```

* 필요 시에 로드할 수 있다 (비동기 로드)
  * 초기 메모리 사용량이 적다
  * 로드 시 약간의 지연이 발생할 수 있다
* 대용량 에셋 관리에 효율적이다

## 메모리 상태 확인

```c++
void APlayerCharacter::CheckReferenceStatus()
{
  // Hard Reference의 경우
  bool bHardRefValid = (WeaponMesh != nullptr); // 항상 true (이미 로드됨)
  
  // Soft Reference의 경우  
  bool bSoftRefLoaded = (WeaponMeshSoft.Get() != nullptr); // 로드 후에만 true
  bool bSoftRefPathValid = WeaponMeshSoft.IsValid(); // 경로가 유효하면 true
}
```

## 출처
* <https://docs.unrealengine.com/4.26/ko/ProgrammingAndScripting/ProgrammingWithCPP/Assets/ReferencingAssets/>
* <https://hyo-ue4study.tistory.com/435>
* <https://docs.unrealengine.com/4.27/ko/ProductionPipelines/Redirectors/>
* <https://forums.unrealengine.com/t/can-someone-explain-soft-variable-references/444524/2>