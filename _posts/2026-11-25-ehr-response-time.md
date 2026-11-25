---
layout: post
title: e-HR 응답 18초를 1초로 줄인 과정
title_en: Cutting e-HR response from 18 s to 1 s
summary: DB, 서버, 화면 세 층의 병목을 함께 고쳐 핵심 화면 응답을 1초 이내로 줄인 기록
project: ehr
tags: [oracle, performance]
---

> 구조 확인용 샘플 글입니다. 실제 내용으로 바꿔 주세요.

2018년부터 쌓인 Spring·Oracle 인사 시스템에서 핵심 화면 응답이 최대 18초까지 걸렸습니다.

## 접근

느린 원인을 수치로 먼저 찾은 뒤, DB·서버·화면 세 층의 병목을 함께 고쳤습니다.

- 쿼리를 고정했습니다.
- 반복 조회는 캐시로 돌렸습니다.
- 결재는 동시에 처리하도록 바꿨습니다.

```java
// 예시: 반복 조회를 캐시로 돌리는 형태
@Cacheable("codes")
public List<Code> findCodes(String group) {
    return codeMapper.selectByGroup(group);
}
```

## 결과

응답은 18초에서 1초 이내로 줄었고, 일괄 결재는 최대 5건을 동시에 처리합니다.
