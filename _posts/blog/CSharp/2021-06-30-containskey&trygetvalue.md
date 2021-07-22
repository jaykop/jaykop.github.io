---
title: "ContainsKey & TryGetValue"
classes: wide
categories: 
  - blog
  - CSharp
sidebar:
  nav: "main"
author_profile: true
---

## TryGetValue vs. ContainsKey?
```csharp
// key가 있는지 체크
public bool ContainsKey(TKey key)
{
  return (this.FindEntry(key) >= 0);
}

// key가 있는지 체크
// key를 발견 시, value에 out 키워드로 값을 담음
public bool TryGetValue(TKey key, out TValue value)
{
  int index = this.FindEntry(key);
  if (index >= 0)
  {
    value = this.entries[index].value;
    return true;
  }
  value = default(TValue);
  return false;
}
```

* 지정한 키가 해당 Dictionary에 있는지 여부를 확인하는 메서드
* Boolean 반환 
  * 있는 경우 -> true
  * 없는 경우 -> false
  * 값의 존재 여부를 체크한 뒤, 그 값을 받아오는 방식은 TryGetValue를 사용하는 것을 권장

```csharp
// Dictionary[key]
public TValue this[TKey key] 
{
  get {
      int i = FindEntry(key);
      if (i >= 0) return entries[i].value;
      ThrowHelper.ThrowKeyNotFoundException();
      return default(TValue);
  }
  set {
      Insert(key, value, false);
  }
}
// 따라서 아래와 같은 경우는 overhead가 발생
if (dic.ContainsKey(key))
{
   getValue = dic[key];
}
```

## 출처   
* <https://ckhyeok.tistory.com/37>
* <https://m.blog.naver.com/PostView.nhn?blogId=crusaderholy&logNo=100112263890&proxyReferer=https:%2F%2Fwww.google.com%2F>
* <https://stackoverflow.com/questions/39885203/is-there-a-reason-why-one-should-use-containskey-over-trygetvalue>