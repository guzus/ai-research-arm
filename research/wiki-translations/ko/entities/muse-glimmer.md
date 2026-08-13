---
slug: muse-glimmer
language: ko
source_file: research/wiki/entities/muse-glimmer.md
source_sha256: ef0c0ebaab198b1d399b9186dbdc63f3b5a848054e082da05ba9ed3469a75cd9
title: Muse Glimmer
description: Meta가 Apache 2.0으로 2026-08-10 공개한 30B 고밀도 멀티모달 에이전트 모델. 출시 당일(day-0)부터 transformers/llama.cpp/vLLM/SGLang/Ollama를 지원하며, Muse Spark에서 증류되어 벤치마크 24개 항목 중 12개에서 최고 성능을 기록했다.
---

**Muse Glimmer**는 [[meta|Meta]]가 2026-08-10 **Apache 2.0**으로 공개한 30B 고밀도 멀티모달 에이전트 모델이다. 가중치는 Hugging Face에서 제공되며 transformers, llama.cpp, vLLM, SGLang, Ollama를 출시 당일인 day-0부터 지원한다. 최근 유료 제품 중심의 행보를 보이던 Meta가 [[open-weights|오픈 웨이트]]로 돌아왔음을 알리는 모델이기도 하다. 독점 모델 계보인 **Muse Spark**에서 증류되었고([[muse-code]] 참고), 소비자용 GPU 한 장에서 구동되며(4-bit 기준 ~17GB), 벤치마크 24개 항목 중 12개에서 최고 성능을 기록했다.

## 주목할 이유

- **오픈 웨이트로의 귀환.** 이번 출시는 Meta가 폐쇄형 유료 모델([[muse-code|Muse Code / Muse Spark 1.2]])을 잇달아 내놓던 흐름을 끊었다. CEO Mark Zuckerberg가 초지능 선언문을 통해 오픈 웨이트를 미국 정책으로 추진한 지 며칠 만에 이뤄진 공개이기도 하다. Meta는 별도로 **Muse Spark 1.2**의 오픈 웨이트 버전도 제공하겠다고 약속했다. 나흘 전 유료화를 시작한 독점 모델로, 공개 시점에 관한 표현은 "곧"에서 "향후 몇 주 안에"로 구체화됐다(여전히 실제 출시가 아닌 약속 단계다). [[open-weights|오픈 웨이트]] 참고.
- **역량 평가.** **벤치마크 24개 항목 중 12개에서 최고 성능**을 기록했으며, Gemma 4 31B보다 19개, Qwen 3.6 27B보다 14개 항목에서 앞섰다. 강점은 **에이전트형 도구 사용**(MCP Atlas 75.5, DeepSearch QA 74.6, AA-LCR 80.0)에 집중됐고, 에이전트가 컴퓨터를 직접 다루는 영역에서는 약점을 보였다(Qwen은 OSWorld, TerminalBench 및 대부분의 멀티모달 평가에서 선두이며, [[gemma-4|Gemma 4]]는 두 가지 주요 안전성 지표 모두에서 앞선다). SWE-Bench Pro 점수는 51.2 대 50.2로, 실행 간 편차 범위 안의 동률이다. 비교 대상 두 모델은 모두 **April 세대**다. Ethan Mollick의 절제된 평가는 Glimmer가 중국 오픈 모델의 최전선에는 못 미치고 폐쇄형 최전선 모델과는 상당한 격차가 있지만, **지난 일 년간 나온 비중국계 오픈 웨이트 모델 중에서는 최고**라는 것이다.
- **로컬 추론의 경제성.** Meta에 따르면 4-bit 빌드는 **15개 벤치마크에서 평균 성능 저하가 ~1%에 그치면서 용량은 완전 정밀도의 55GB+에서 ~17GB로 줄었다.** DFlash 추측 디코딩 드래프터는 RTX 5090에서 처리량을 2–4× 높이지만(74.9 → 233.4 tok/s), Mac 통합 메모리에서는 그 향상 폭이 대략 절반에 불과하다. 즉, "노트북에서 실행"한다는 홍보 문구가 겨냥하는 기기에서 속도 향상이 가장 작다. 2-bit GGUF는 사람이 지켜보지 않는 저장소 버그 탐색 작업에서 RAM 14GB로 100+회의 도구 호출을 완료했다.
- **100+개 언어와 조절 가능한 추론 노력 수준**을 지원하며, 멀티모달 입력용 전용 지각 인코더도 갖췄다.

## 남은 질문

- **Muse Spark 1.2 오픈 웨이트는 실제로 언제 공개되는가?** "Meta가 오픈 웨이트로 돌아왔다"는 평가를 떠받치는 핵심은 이 약속이며, 일정 표현은 "곧"에서 "향후 몇 주 안에"로 바뀌었다.
- **30B 고밀도 아키텍처를 더 큰 규모로 확장할 수 있는가?** Spark에서 증류된 Glimmer는 중간급 에이전트 모델이다. Meta의 오픈 모델 계보가 ([[moonshot-kimi-k3|Kimi K3]]와 [[qwen-3-8-max|Qwen3.8]]처럼) 최전선 규모까지 확장될지는 아직 답이 없다.
