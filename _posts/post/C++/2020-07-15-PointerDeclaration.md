---
title: "포인터 선언"
classes: wide
categories: 
  - post
  - C++
sidebar:
  nav: "main"
author_profile: true
---

## An integer
```c++
int a;
```

## A pointer to an integer
```c++
int* pa;
```

## A pointer to a pointer to an integer
```c++
int** ppa;
```

## An array of ten integers
```c++
int a[10];
```

## An array of ten pointers to integers
```c++
int* p[10];
```

## A pointer to an array of ten integers
```c++
int (*a)[10];
```

## A pointer to a function that takes an integer as an argument and returns an integer 
```c++
int (*a)(int);
```

## An array of ten pointers to functions that take an integer argument and return an integer.
```c++
int (*a[10])(int);
```
