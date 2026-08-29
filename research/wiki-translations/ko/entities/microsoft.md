---
slug: microsoft
language: ko
source_file: research/wiki/entities/microsoft.md
source_sha256: f2a4920a53aadb6c9c4e35ce1b8fcc35c8251ac739a29c7023222f67399f31bb
title: Microsoft
description: 하이퍼스케일러이자 프런티어 모델 개발사. Build 2026에서 완전한 자사 MAI 모델 스택을 출시하고 Project Polaris를 GitHub Copilot의 기본 엔진으로 채택했다. CEO Satya Nadella는 Microsoft가 Anthropic에 $5B를 투자했음에도 Anthropic의 Fable을 공개적으로 "편집 통제를 받는다"고 평했으며(2026-07-18), MAI-Thinking-1은 최초로 "처음부터 자체 개발한" 추론 모델로서 Microsoft Foundry에 출시됐다(2026-08-13).
---

Microsoft는 Redmond에 본사를 둔 하이퍼스케일러다. [[openai]]의 핵심 컴퓨팅·유통 파트너로 지낸 지 세 해 만에 이제 자체 프런티어급 **MAI** 모델 제품군을 개발하고 출시하고 있다. **Build 2026**(Fort Mason, SF; June 2–3)은 원래의 2023 OpenAI 통합 이후 Microsoft의 최대 AI 제품 출시였으며, 단일 공급업체 의존에서 벗어나려는 Microsoft의 엔지니어링 전략을 지금까지 가장 분명하게 보여준 사건이었다.

## 중요한 이유

**Build 2026 — MAI 공세(2026-06-03).** Satya Nadella는 Windows를 "에이전트 플랫폼"으로 재정의했다. *"에이전트는 단순한 기능이 아닙니다. 업무를 위한 새로운 운영체제입니다."* 기조연설에서는 **"증류 제로, 지능을 직접 소유하라"**는 구호 아래 자사 모델 스택을 출시했다.

- **MAI-Thinking-1** — 35B MoE, 256K 컨텍스트, **97% AIME 2025**, **53% SWE-Bench Pro**. 알려진 바로는 **Claude Opus 4.6과 동급**이며 명시적으로 "증류 없이 개발"됐다. Microsoft Foundry에서 비공개 프리뷰로 제공됐고 [[openrouter]] / Fireworks / Baseten에도 공개됐다. 외부의 SWE-Bench / AIME 재현 실험이 프런티어급 품질을 뒷받침한다면, 원래의 o1 / Claude 추론 모델 물결 이후 주요 비증류 추론 모델로는 최초가 된다.
- **MAI-Code-1-Flash** — 5B, **51% SWE-Bench Pro**(HN: 246 pts, 출시 당일 최고 인기 글). 다만 오픈 웨이트 **[[minimax-m3]]**가 같은 주 59%로 근소하게 앞섰다. **프로덕션 도입(2026-06-04):** MAI-Code-1-Flash는 **GitHub Copilot과 VS Code**에 순차 도입되기 시작했다. 완성, PR diff 리뷰, 채팅을 **[[openai]] 인프라를 거치지 않는** 경로에서 처리한다. 이는 팔월 Project Polaris의 기본 전환에 앞서 Microsoft의 대표 개발자 제품에서 MAI 모델이 OpenAI 추론을 대체한 최초의 구체적 사례다(ARA digest 2026-06-04).
- **MAI-Image 2.5 / MAI-Voice 2 / MAI-Transcribe 1.5**, 그리고 약 10× 저렴한 비용으로 GPT-5.5 수준의 품질을 낸다고 주장하는 McKinsey 특화 변형 모델도 공개됐다.
- **Project Polaris**는 **2026년 팔월부터 기본 GitHub Copilot 코딩 엔진**이 되며, 자동 마이그레이션과 선택 가능한 석 달 폴백을 제공하면서 GPT-4 Turbo를 대체한다. Polaris는 여러 파일을 리팩터링할 때 추론 단계에서 연쇄 사고와 트리형 사고를 사용한다. Claude Code의 개발자 점유율에 맞서는 Microsoft의 전략적 거점이다.

**플랫폼 + 실리콘.** **Windows Agent Framework v1.0**은 **MIT 라이선스**로 출시됐다(로컬 Windows, Windows 365 Cloud PCs, Azure Arc 엣지 전반의 에이전트 지원). **Windows Local AI**(시스템 수준 NPU 런타임)는 Windows 11 24H2의 **KB5039239 on June 9**에 도입되며 Snapdragon X Elite / Intel Lunar Lake / AMD XDNA용 Phi-4-mini-silicon 모델을 번들로 제공한다. **MAIA 200** 커스텀 실리콘은 NVIDIA GB200 대비 약 30% 개선된 $/perf를 주장하며, [[ai-capex]] 비용 기반을 정면으로 겨냥한다. 별도의 **GitHub Copilot 독립형 앱**(HN: 78 pts)도 에이전트 코딩 접점을 강화한다.

**멀티 스택 결별.** Microsoft가 같은 주 Copilot을 OpenAI에서 이전한 가운데, **[[openai]]의 GPT-5.5, GPT-5.4와 Codex가 Amazon Bedrock에서 GA**에 도달하며 Azure 독점 시대도 막을 내렸다. 2023 통합 이후 처음으로 양측 모두 대체 스택을 갖게 됐다. Microsoft에는 자체 모델이 있고, OpenAI에는 Azure 외 유통망이 생겼다. 공생 관계는 위험을 분산한 양방향 관계로 바뀌고 있다.

**Copilot Cowork GA — 모델 교체 가능성을 고려한 설계(2026-06-18).** **Copilot Cowork**는 **멀티 모델 지원**과 **사용량 기반 가격(약 $0.01/task)**을 갖추고 **전 세계에서 정식 출시**됐다. "모든 조직"을 위한 장기 실행 에이전트로 소개됐다. 전략적으로 눈에 띄는 대목은 같은 주 Axios가 보도한 내용이다. **Microsoft는 중국에서 미세 조정된 [[deepseek|DeepSeek V4]]를 [[openai]] 또는 [[anthropic]]보다 저렴한 Cowork 요금제로 검토하고 있다.** 이는 Build-2026의 "지능을 소유하거나 대체하라"는 기조를 자사 MAI 모델에서 프로덕션 백엔드용 *중국산 오픈 웨이트*까지 확장한 것이다. Microsoft가 비용에 따라 엔진을 교체할 수 있도록 에이전트 스택을 설계하고 있다는 지금까지 가장 명확한 신호다. 대표적인 프런티어 파트너에 대한 의존을 줄이는 동시에 [[open-weights]]를 가치사슬 상단으로 끌어올린다(ARA digest 2026-06-18).

**Foundry에서 Claude GA — 두 프런티어 스택을 모두 제공하는 유일한 클라우드(2026-06-30).** [[anthropic|Anthropic의]] [[claude-opus-4-8|Claude Opus 4.8]]과 **Haiku 4.5**가 **Azure의 Microsoft Foundry에서 정식 출시**됐다. **Azure 인증, 청구, 약정 사용분 차감**을 기본 지원하며(프롬프트 캐싱 + 확장 사고 지원), Quantum-X800 InfiniBand와 **[[nvidia|NVIDIA]] GB300 NVL72(Blackwell Ultra)**에서 실행된다. 알려진 바로는 **NVIDIA 실리콘에서 이뤄진 Anthropic의 첫 배포**다. @claudeai, @nvidia, @Azure가 한 시간 안에 공동 발표했다. 이로써 **Microsoft는 하나의 플랫폼에서 [[openai|OpenAI]]와 Anthropic 프런티어 모델을 모두 제공하는 유일한 클라우드**가 됐다. 이는 Build-2026의 자사 MAI / "지능을 소유하거나 대체하라"는 기조를 대체하는 것이 아니라 보완하는 위험 분산책이다. *회의적 관점:* "Foundry에서 GA"는 대부분 조달·청구 통합에 해당한다. 실제로 새로운 사실은 Azure 기본 인증·청구와 NVIDIA GPU 경로이며("NVIDIA 최초"라는 최상급 표현은 처음에 단일 출처에만 근거했다)(ARA digest 2026-06-30).

**주의할 점.** Microsoft의 **Majorana 2** 양자 칩 주장(약 1,000× 신뢰성, 2029 목표)은 반론에 부딪혔다. *Scientific American*에 따르면 여러 물리학자가 공개된 측정 데이터가 나오기 전까지는 이를 "허위"라고 평가했다.

**Copilot 앱 통합, 잉여 용량을 판매하는 "Frontier Co."(2026-07-04).** Microsoft는 소비자용과 기업용 **Copilot 앱을 통합**해 팔월에 단일 앱으로 출시할 것으로 알려졌다. 잘 쓰이지 않는 기능(예: Copilot Podcasts)은 줄이고, 추가 요금을 받는 새로운 백그라운드 작업용 **"AutoPilot"** 에이전트를 더한다. [[anthropic]] 및 [[openai]]와 함께 벌이는 광범위한 AI "슈퍼 앱" 경쟁의 일부다. 이와 별도로 Microsoft는 **$2.5B 규모의 "Frontier Co." 사업부를 출범**시키고, 6,000명의 직원을 AI 고객사에 직접 배치했다. Build-2026 자사 MAI 스택과 결합한 서비스·유통 강화 전략이다(ARA digest 2026-07-04).

**Nadella, Fable을 "편집 통제를 받는다"고 평가(2026-07-18).** Satya Nadella는 [[anthropic|Anthropic]]의 **[[claude-fable-5|Fable]]** 모델을 공개적으로 **"편집 통제를 받는다"**고 표현했다. Microsoft가 **$5B 지분 투자**를 한 회사를 겨냥한 이례적인 공개 비판이자, 주요 AI 투자사와 피투자사 사이에서 지금까지 드러난 가장 첨예한 공개 갈등이다. Microsoft가 경쟁 관계인 자체 MAI 스택을 구축하는 시기와도 맞물렸다(ARA digest 2026-07-18).

**수십억 달러 규모 Mistral 인프라 계약(2026-07-21).** Microsoft와 프랑스 AI 연구소 Mistral은 유럽 전역에 AI 인프라를 구축하는 수십억 달러 규모 계약을 체결했다. Microsoft의 자사 MAI 모델 추진과는 별개의 유통·컴퓨팅 협력이다. 자체 모델에 더해 Foundry의 [[openai]], [[anthropic]], 그리고 이제 Mistral 컴퓨팅까지 확보한 Microsoft의 위험 분산형 멀티 파트너 전략을 특히 유럽 시장으로 확장한다(ARA digest 2026-07-22).

**MAI-Thinking-1, 최초의 "처음부터 자체 개발한" 추론 모델로 공식화(2026-08-13).** Microsoft AI CEO **Mustafa Suleyman**은 **MAI-Thinking-1**을 회사가 **"처음부터 자체 개발한" 최초의 추론 모델**이라고 설명했다. 이제 **Microsoft Foundry**에서 제공되며, 앞서 추적한 Build 2026의 "증류 없음" 주장을 Suleyman의 핵심 메시지로 다시 제시한 것이다. **발표에는 벤치마크나 모델 카드가 포함되지 않았으므로**, 이 문서가 Build 2026 이후 제기해 온 프런티어 동급 성능 여부는 여전히 미결 상태다(ARA daily digest 2026-08-13).

## 미해결 질문

- **"증류 없음" 주장은 재현 실험을 견딜 수 있는가?** MAI-Thinking-1의 프런티어 동급 성능 주장은 이번 출시를 지탱하는 핵심 주장이다. 향후 두 주 동안 진행될 외부 SWE-Bench / AIME 실행이 검증 수단이다.
- **Copilot의 Polaris 마이그레이션은 [[openai]] 추론 사용량을 얼마나 빠르게 잠식할까?** GPT-4 Turbo가 기본값에서 제외되면 OpenAI의 최대 유통 채널에서 발생하는 매출을 측정할 수 있는 문제가 된다.
- **멀티 스택 균형.** Microsoft와 OpenAI가 모두 대체 스택을 갖춘 지금, 파트너십은 위험 분산 관계로 안정될까, 아니면 공개 경쟁으로 쇠퇴할까?
