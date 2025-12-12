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

### 캐릭터가 Random한 Idle Animation을 출력하게 하고 싶어요

* 적당히 Random한 AnimSequence를 출력하도록 하면 되지 않나? 라고 생각했다
  * **AnimMontage가 아닌, AnimSequence**가 끝난 타이밍을 정확히 체크해야 한다
  * 프레임이 일정하지 않은 환경에서는 단순히 DeltaTime으로 AnimSeqeunce의 Length를 체크해서 새로운 AnimSequence를 출력하기도 쉽지 않다.
    * AnimSequence가 끝나기도 전에 다른 AnimSequence가 시작되면서 튀는 게 눈에 보일 것이다
  * Animation Thread와 Game Thread는 분리되어 있다

### 예전에 시도했던 방법?

```c++
UAnimSequence* ULinkedAnimLayerInstance::SelectIdleAnimation()
{
	UAnimSequence* SelectedIdle = nullptr;
	if (const FAALocomotionAnimSets* AnimSets = GetAnimSets())
	{
		if (AnimSets->Idle.Num() > 0)
		{
			FRandomStream RandStream(FPlatformTime::Cycles());

			int32 IdleAnimIndex = RandStream.RandRange(0, AnimSets->Idle.Num() - 1);
			SelectedIdle = AnimSets->Idle[IdleAnimIndex];

			if (ensure(IsValid(SelectedIdle)))
			{
				NextIdleTime = GetWorld()->GetTimeSeconds() + RandStream.FRandRange(SelectedIdle->GetPlayLength(), SelectedIdle->GetPlayLength() * 10.0f);
			}
		}
	}
	

	return SelectedIdle;
}

void UAAALSLinkedAnimLayerInstance::SelectAnimation_Idle1()
{
	SelectedAnimation_Idle1 = SelectIdleAnimation();
}

void UAAALSLinkedAnimLayerInstance::SelectAnimation_Idle2()
{
	SelectedAnimation_Idle2 = SelectIdleAnimation();
}
```

* 예전 프로젝트에선 위와 같은 코드로 사용했다
* 하지만, 이는 상술한 제한 사항이 있다
  * 당시에는 거의 눈에 띄지 않았는데, 아마 이유는 하나의 Idle AnimSequence만 사용했거나, 설명 여러 개를 사용했더라도 Monster의 비전투 Idle에 사용했기 때문에 플레이어와 맞닥뜨린 상태에서는 거의 볼 일이 없었을 것이다

### 안전한 방법은 Random Sequence Player인데...

* AnimGraph에서 사용할 수 있는 Random Sequence Player로 Random한 Idle을 재생할 수 있긴 하다
  * 그러나 이건 AnimInstance의 멤버 변수를 pin으로 연결할 수 없다
  * 즉, uasset을 직접 할당해야 하는 노드다
* 그럼 로직을 Base AnimInstance에서 하고 적용될 Asset 할당은 AnimLayer로 관리하는 방법을 쓸 수가 없는데...
* ***그럼 RandomIdle도 AnimLayer로 관리하자***라는 결론에 이르렀다
  * 몬스터를 만들 때마다 RandomIdle AnimLayer를 만들어줘야 하는 오버헤드가 있다
    * 그럼 몬스터 Idle을 하나만 쓰든가 ㅂㄷㅂㄷ
  * 토글 정도는 제공해서 단일 Idle을 출력할 몬스터는 그냥 SequencePlayer를 재생하고, 그 외에는 LinkedAnimLayer를 사용하는 것으로 했다
* 그러니까 요는, **LinkedAnimLayer로 RandomIdle Layer를 구현**해서 쓰는 것
  * 더 좋은 방법이 있는지는... 아직 잘 모르겠다
