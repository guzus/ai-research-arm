---
slug: qwen-3-8-max
language: ko
source_file: research/wiki/entities/qwen-3-8-max.md
source_sha256: 1fcf5a263d70be432686cc077cc9306b56dcf2cc8f33851682359c6d76e3ef73
title: Qwen3.8-Max
description: Alibaba가 2026-08-04 Mtok당 $2/$6에 출시하고 2026-08-13 Qwen3.8-2.4T-A95B로 오픈 웨이트를 공개한 2.4T 매개변수 / 활성 95B MoE 주력 모델로, 공개된 최초의 Max급 Qwen이다.
---

**Qwen3.8-Max**는 [[alibaba|Alibaba]]의 주력 텍스트 모델이다. **2.4 trillion-parameter
/ 95 billion-active mixture-of-experts** 구조와 **1M-token context**를 갖췄고,
2026-08-04 **million input 토큰당 $2 / million output 토큰당 $6**에 출시됐다.
오픈 웨이트 릴리스는 **2026-08-13 `Qwen3.8-2.4T-A95B`**라는 이름으로 나왔다.
이는 **공개된 최초의 Max급 Qwen**이며, **512 experts에 걸친 95B active parameters**와
**4.89TB의 가중치**를 제공한다(ARA 다이제스트 2026-08-13).

이 모델은 2026-07-20부터 [[alibaba]] 페이지에서 "곧 오픈 웨이트로 공개"될
모델로 추적해 온 결과물이며, 2026-07-21에는 [[claude-fable-5|Claude Fable 5]]에
이어 종합 #2라고 자체 보고한 프리뷰가 공개됐다.

## 중요한 이유

- **주장의 핵심은 가격이다.** Fable 5의 $10/$50에 비해 Mtok당 $2/$6은
  입력/출력 기준으로 대략 **5×/8× 저렴**하다. 역량 주장이 독립 평가에서도
  유지된다면 추론량을 움직이는 것은 벤치마크 표가 아니라 가격이다.
  [[open-weights|오픈 웨이트]]를 참고하라.
- **벤치마크 표는 Alibaba 자체 자료이며, 빠진 모델이 핵심 단서다.** 공급업체
  수치는 [[claude-opus-4-8|Opus 4.8]]과 비교 가능한 시험 **54개 중 51개**,
  [[gpt-5-6|GPT-5.6-Sol]]을 상대로 **46/54**에서 이겼다고 주장하지만,
  [[claude-fable-5|Fable 5]]을 상대로는 **37/49**로 떨어진다. 또한
  [[moonshot-kimi-k3|Kimi K3]]와 [[claude-opus-5|Opus 5]]를 **완전히 제외**했다.
  "프런티어를 능가한다"는 구도라면 가장 먼저 포함해야 할 두 모델이다.
- **첫 독립 사용 결과는 출시 홍보보다 차분했다.** @emollick의 셰이더 시험은
  "견고하지만 Kimi K3 수준은 아니다"라는 결론이었고, @teortaxesTex는 에이전트형
  벤치마크(NL2Repo, DeepSWE, Agent's Last Exam)가 훨씬 작은
  [[deepseek-v4-flash|DeepSeek V4-Flash]]와 비슷하다고 평가했다. 상업적으로
  중요한 비교 대상은 훨씬 저렴한 이 모델이다.
- **16-day 자율 코딩 수치는 감사되지 않았고 벌써 흔들린다.** 홍보 문구는
  무인으로 **16-day** 실행해 265 commits, 127 PRs, 151 issues를 만들었다는
  주장으로 바뀌었지만, 같은 자료의 두 번째 전달에서는 **"10+ days"**로
  표현됐다. 로그나 하네스는 공개되지 않았으며, 커밋·PR 수는 승인된 작업이
  아니라 산출량을 뜻한다.
- **Hacker News를 장악한 뒤 포화됐다.** AI 부문에서 **five consecutive
  windows** 선두를 차지하며 점수가 115 → 464 → 653 → 861 → 960으로 올랐지만,
  주기별 증가폭은 프런트 페이지에서 사라질 때까지 단조롭게 줄었다.
- **오픈 웨이트 릴리스에 이름이 있는 플랫폼과 날짜가 생겼다(2026-08-07/08).**
  Alibaba는 `Qwen3.8-2.4T-A95B`의 **ModelScope page**를 준비했다. 이를
  **최초의 오픈 웨이트 Qwen-Max급 모델**이라고 설명하고 **following Wednesday**
  공개를 예고했으며, `Qwen3.8-27B`는 별도 페이지에서 뒤따를 예정이었다.
  이 준비 페이지는 2.4T-parameter / A95B≈95B-active라는 해석을 확인하고,
  출시 당일의 "다음 주 오픈 웨이트" 약속을 구체적인 산출물 목표로 굳혔다.
  다만 이 수집 시점에는 가중치가 아직 공개되지 않았다(r/LocalLLaMA,
  Latent.Space AINews 경유; ARA 일일 다이제스트 2026-08-09).
- **오픈 웨이트가 실제로 공개됐다 — `Qwen3.8-2.4T-A95B` 출시(2026-08-13).**
  Alibaba는 2.4T/95B-active 모델을 오픈 웨이트로 공개했다. **4.89TB의 가중치와
  512 experts**, **day-0 vLLM support**, 단일 8×B300 또는 8×MI355X node에
  맞춘 **사전 양자화 4-bit checkpoints**가 제공된다. vLLM은
  `Inferact/Qwen3.8-2.4T-A95B-NVFP4`를 **1.32 TiB**로, **MXFP4 build를
  1.45 TiB**로 공개했다. Unsloth는 **397GB의 동적 1-bit build**를 공개했지만
  여전히 410GB+ RAM 또는 VRAM이 필요하다. **양자화에 따른 품질 측정치는
  공개되지 않았다.** 모델 카드는 이 모델이 **Alibaba 자체 상용 주력 모델의
  기반**이라고 확인한다. **비전, 기본 1M context, 내장 도구는 유료 계층에만
  남겨 뒀다.** 즉 오픈 릴리스는 순위에 오른 상용 시스템 전체가 아니라
  텍스트-and-1M-context 기반 모델이다. "대부분의 사람이 실제로 실행할 수 있는
  크기"인 **27B sibling**(`Qwen3.8-27B`)은 **Friday 14 August** 공개 예정이다.
  출시 관련 HN 스레드는 **MoE active-parameter economics**, 즉 ~95B-active
  모델이 프런티어 경쟁 모델 대비 어떻게 가격을 책정하는지에 주목했다
  (ARA 다이제스트 2026-08-13).

## 미해결 질문

- **오픈 웨이트는 상용 모델의 동작과 일치하는가?** 비전, 기본 1M context,
  내장 도구가 유료 계층에만 남아 있어 순위에 오른 시스템과 다운로드 가능한
  기반 모델은 구성 요소가 다르다. 이 위키가 [[open-weights]]에서 추적하는
  구성 요소 비공개 패턴이다.
- **공급업체의 승리 주장은 제외된 모델을 상대로도 재현되는가?** Kimi K3 또는
  Opus 5와의 독립적인 정면 비교는 아직 없다.
- **27B sibling이 실제로 가장 많이 실행될 산출물인가?** 2.4T MoE는 로컬
  추론으로 쓰기 어렵다. `Qwen3.8-27B`(2026-08-14 예정)가 실질적인 채택을
  이끌 수 있으며, 양자화에 따른 품질 측정치는 아직 공개되지 않았다.
