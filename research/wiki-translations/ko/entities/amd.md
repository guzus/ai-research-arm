---
slug: amd
language: ko
source_file: research/wiki/entities/amd.md
source_sha256: 49396fb33cf2a268c319551ca454efdb6e6b26437d3e0f1f313f5aef08c76686
title: AMD
description: 신뢰할 만한 대안 공급원 AI 가속기 업체. Helios가 Anthropic의 2 GW MI450 약정을 향해 증산되는 가운데 FY26Q2 데이터센터 매출은 $6.7B로 두 배(+107% YoY)가 됐고, 2026-08-07에는 모델 특화 실리콘 스타트업 Taalas를 인수했다.
---

**AMD**는 [[nvidia|NVIDIA]]의 AI 가속기 스택을 대체할 수 있는 제품을 대규모로 출하하는 유일한 업체다. Instinct GPU, EPYC 서버 CPU, 그리고 이들을 묶은 **Helios** 랙 규모 시스템을 제공한다. 프런티어 연구소가 단일 공급원 의존을 피하려 할 때 선택하는 구체적인 헤지 수단으로 2026년에 멀찍이 떨어진 #2에서 부상했기 때문에 이 문서에서 추적한다.

## 중요한 이유

- **FY26Q2: 데이터센터 부문 두 배 성장(2026-08-04 제출, 2026-08-05 다이제스트 수록).** 전체 매출은 역대 최고인 **$11.5B로 YoY 50% 증가**했으며, EPYC와 Instinct 수요에 힘입어 **Data Center 매출은 $6.7B로 YoY 107% 증가**, **Embedded는 $977M(+19%)**를 기록했다. CFO **Jean Hu**는 "매출이 전년 대비 50% 증가해 기록적인 $11.5 billion이 됐고… 이번 분기에 Data Center 사업이 **회사 매출의 58%**를 차지했다"고 말했으며, 하반기 데이터센터 매출이 가속될 것으로 예상했다. CEO **Lisa Su**는 "Helios가 증산을 시작한다"고 했다. 자본지출은 **분기 대비 두 배 넘게 증가해 $389M → $808M**이 됐고, 대부분 Helios 랙과 **HBM 공급 확보**에 쓰였다. AMD도 [[ai-capex]]에서 설명한 것과 같은 메모리 부족에 대비하는 셈이다. **주가는 정규장에서 7% 오른 뒤에도 시간 외 거래에서 약 9% 하락**했다. 호실적 후 하락하는 양상은 이제 AI 인프라 기업 실적 발표에 대한 2026년의 전형적인 반응이며, 같은 날 [[spacex]]도 같은 흐름을 보였다(SEC 8-K, accession 0000002488-26-000121; ARA daily digest 2026-08-05).
- **Anthropic 약정이 수요의 기반이다.** 2026-07-21 SemiAnalysis가 [[anthropic|Anthropic]]이 AMD 하드웨어를 단지 *평가 중*이라고 보도했던 내용은 2026-07-23 체결 계약으로 구체화됐다. **AMD는 Anthropic에 최대 $5B를 투자**하고 Anthropic은 훈련 및 Claude 서비스에 Helios를 통해 **최대 2 GW의 Instinct MI450 GPU**를 배치한다. "Helios가 증산을 시작한다"는 문장이 가리키는 계약이며, AMD를 [[neocloud]] 형태의 순환 금융(공급사가 고객에게 투자하고 고객이 공급사의 실리콘을 구매)에 직접 참여시킨다. [[ai-capex]] 거품 논쟁이 반복해서 다루는 바로 그 패턴이다.
- **대안 공급원 자체가 전략적 제품이다.** [[microsoft|Microsoft]]가 AMD로 방향을 틀고 Anthropic이 뒤따르자 The Decoder는 이를 "AI 칩에 대한 Nvidia의 장악력이 약해진다"고 표현했다. AMD는 NVIDIA, Microsoft, Google, Meta, [[openai|OpenAI]]와 함께 업계 공동 **"Open Weights and American AI Leadership" 서한에 서명**한 사실도 2026-07-25 확인됐다. 하드웨어 업체들이 모두 [[open-weights|오픈 웨이트]] 진영에 서고, AMD의 최대 공개 Instinct 고객인 Anthropic은 반대편에 놓였다.

- **AMD가 Taalas 인수 — 범용 GPU 업체가 모델 특화 ASIC을 사들임(2026-08-07).** AMD는 단일 모델을 실리콘에 직접 하드와이어하는 스타트업 **[[taalas|Taalas]]**를 인수했다. 이 주기의 모델 특화 실리콘 인수로는 Nvidia–Groq에 이어 **두 번째**다. 이날 Hacker News에서 댓글 수 기준 가장 큰 스레드(367 pts / 289 comments)였고, 핵심 논쟁은 정확하다. 웨이트를 마스크 세트에 새기면 재프로그래밍 가능성을 처리량과 맞바꾸므로, *어떤 모델이 고정할 가치가 있을 만큼 안정적인가*가 문제다. [[model-specific-silicon]]을 참고하라. **거래 조건도, AMD나 Taalas의 당사 발표도 나오지 않았으며**, 주변에서 돌던 **$20B 수치는 Nvidia–Groq 거래에 해당하므로 여기로 옮겨서는 안 된다**(The Register, HN; ARA daily digest 2026-08-07). 전략적 긴장은 스스로 만든 것이다. 위에서 설명한 AMD의 핵심 제안은 [[nvidia|NVIDIA]]에 맞선 *프로그래밍 가능한* 제2 공급원인데, 고정 기능 추론 부품은 정반대의 베팅이다. 같은 날 [[anthropic|Anthropic]]은 사내 실리콘 팀을 확인했고 [[etched]]의 기업가치는 $10B로 재평가돼, 맞춤형 추론 실리콘이 그날의 지배적인 인프라 주제가 됐다.

## 미해결 질문

- **AMD는 실제로 얼마를 지불했고, Taalas는 Instinct 내부에 들어가는가 아니면 옆에 놓이는가?** 거래 조건과 당사 발표가 없으므로 가격과 제품 통합 방식 모두 알 수 없다. 이번 winter에 출시 예정인 Taalas HC2가 인수 후에도 일정대로 나올지도 불명확하다.
- **Helios는 전망이 암시하는 속도로 출하되는가?** "증산 시작"과 2× 자본지출 증가는 의지 표명이다. Nvidia Rubin 세대와 비교한 MI450의 단위경제성은 공개되지 않았다.
- **AMD에도 HBM이 핵심 제약인가?** 자본지출 일부가 "HBM 공급 확보"에 쓰인 같은 시기에 DigiTimes는 2027 DRAM/HBM 용량이 60–70% 충전율로 모두 예약됐다고 보도했다. [[ai-capex]]와 [[micron]]을 참고하라.
- **데이터센터 부문이 두 배 성장했는데 왜 주가는 9% 하락하는가?** 실적과 반응의 간극은 시장이 성장보다 지속성을 가격에 반영하고 있음을 뜻한다. [[ai-capex]]가 추적하는 것과 같은 질문이다.
