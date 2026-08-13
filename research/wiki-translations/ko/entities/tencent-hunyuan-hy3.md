---
slug: tencent-hunyuan-hy3
language: ko
source_file: research/wiki/entities/tencent-hunyuan-hy3.md
source_sha256: 425690b1d3085d1e4b457ab03ee0ceb94c95f8a04918d29d6a28f8a561a0494d
title: 텐센트 훈위안 Hy3
description: Apache 2.0을 적용한 Tencent Hunyuan의 295B 매개변수 오픈 웨이트 MoE 모델. MCP-Atlas 벤치마크에서 새로운 오픈 모델 SOTA를 기록한 것으로 보도됐으며 2026-07-06에 출시됐다.
---

**Hy3**는 Tencent Hunyuan이 2026-07-06에 출시한 **295B 매개변수의
전문가 혼합** 오픈 웨이트 모델이다. **Apache 2.0** 라이선스를 적용했고
상업적으로 사용할 수 있는 API를 제공한다. 독립 보도에 따르면 이 모델은
**MCP-Atlas** 벤치마크에서 [[zhipu-glm-5-2]]를 넘어 오픈 웨이트 모델의
새로운 SOTA에 올랐다. 또한 훨씬 작은 컴퓨트 구성으로 과학 벤치마크에서
GPT-5.5를 능가했다는 별도의 주장도 나왔다.

## 중요한 이유

Hy3는 [[zhipu-glm-5-2]], [[minimax-m3]], 그리고 [[deepseek]]의 프런티어
야심과 함께 빨라지는 **중국 오픈 웨이트** 출시 주기에 합류한 최신 모델이다.
이는 오픈 모델이 프런티어와의 격차를 좁히는 광범위한 [[open-weights]]
흐름의 일부다. 또 다른 오픈 웨이트 출시작인
[[mistral-robostral-navigate]]와 같은 다이제스트 주기에 나왔다는 사실은
여러 연구소의 경쟁력 있는 오픈 모델이 이제 같은 날에도 출시됨을 보여준다.

서로 독립적인 이차 출처 세 곳(ML 연구자, 뉴스 수집 계정, 일본어 매체)은 구체적인
매개변수 수와 라이선스, 벤치마크 주장에 관해 일치한다. 그러나 Tencent
Hunyuan의 공식 일차 출처는 확보되지 않았으므로 `verification: partial`이다.

## 열린 질문

- **공식 확인.** Tencent Hunyuan의 일차 출처(블로그, 모델 카드 또는 공식 계정)가
  이러한 세부 사항을 뒷받침하는가?
- **벤치마크의 지속성.** MCP-Atlas SOTA와 GPT-5.5를 능가했다는 과학 분야
  결과가 오염 가능성을 고려한 독립 평가에서도 유지되는가?
