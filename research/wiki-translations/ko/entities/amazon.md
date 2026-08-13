---
slug: amazon
language: ko
source_file: research/wiki/entities/amazon.md
source_sha256: 890b5ac71375a12c18f9b88cf7a31b710ca8129869d02bbfcfe161a48d9024c6
title: Amazon
description: 하이퍼스케일러이자 Anthropic의 단일 최대 투자자. WSJ/Axios 보도에 따르면 CEO Andy Jassy가 Amazon 연구진이 모델을 탈옥시켰다고 재무부에 설명한 뒤 June 2026 Fable 5 / Mythos 5 수출 단속을 촉발한 당사자다.
---

**Amazon**이 LLM 위키에 등장하는 이유는 모델 개발사가 아니라 **June 2026 Fable 5 / Mythos 5(`claude-fable-5`) 수출 대치의 핵심 당사자**이자 **[[anthropic|Anthropic]]의 단일 최대 투자자**이기 때문이다(Amazon은 Anthropic의 $65B Series H에 **$5B를 투자**했고, Anthropic은 Amazon Bedrock과 Trainium에서 구동된다). 이 조합이 핵심이다. Amazon은 자사가 가장 많이 투자한 회사의 대표 모델이 금지되는 데 일조했다.

## 중요한 이유

- **수출 금지 촉발 과정에 남은 Amazon의 흔적(2026-06-14).** Axios와 [WSJ](https://www.wsj.com/tech/ai/amazon-ceos-talks-with-u-s-officials-triggered-crackdown-on-anthropic-models-dcc90578)를 인용한 보도에 따르면 **CEO Andy Jassy는 Scott Bessent 재무장관에게 직접 브리핑**하며, **Amazon 연구진이 일련의 프롬프트로 [[claude-fable-5|Fable 5]]를 탈옥**해 사이버 공격에 쓸 수 있는 출력을 생성했다고 설명했다. 백악관은 회의를 소집했고 연구진은 이를 재확인했다. 백악관 AI 책임자 [[federal-ai-policy|David Sacks]]가 공개적으로 밝힌 설명에 따르면, 행정부는 Dario Amodei에게 탈옥 문제를 고치거나 배포를 철회하라고 요구했지만 그가 거부했고 대통령 승인과 함께 수출통제가 뒤따랐다. **Fable 5와 Mythos 5 모두 36h+가 지난 뒤에도 모든 고객에게 오프라인 상태**였다(ARA digest 2026-06-14). 역량 오용 관점은 [[agentic-ai-security]]를 참고하라.
- **투자자와 피투자사의 충돌.** Amazon은 Anthropic의 최대 후원자이면서 동시에 프런티어 AI 경쟁사다(자체 Nova 모델과 Fable 5가 출시 당일 GA로 배포된 Bedrock 유통 계층을 보유). 피투자사의 대표 모델에 연방 금지를 촉발한 일은 [[ai-capex]] 확장에 얽힌 복잡한 동맹을 이번 주기에서 가장 선명하게 보여준다.
- **Cerebras + AWS 추론 파트너십(2026-06-14).** 별도로 **Cerebras와 AWS는 추론 스택을 재구성하는 추론 컴퓨팅 파트너십**을 발표했다. Amazon의 AI 영역이 투자, 유통(Bedrock), 실리콘(Trainium/Inferentia), 이제는 제삼자 추론 용량까지 아우른다는 점을 상기시킨다.
- **촉발 시점이 구체화됐지만 단서가 있다(2026-06-15).** The Information, Axios, WSJ의 재구성은 하나의 순서로 수렴했다. **June 9** [[claude-fable-5|Fable 5]] 출시 → 연구진이 Mythos를 탈옥한 것으로 알려진 뒤 **June 11** Amazon의 문제 제기 → **June 12** 긴급 지침과 전 세계 서비스 중단이며, **Jassy와 Scott Bessent 재무장관**의 대화가 지침에 영향을 줬다. **단서(Community Note):** Amazon *연구진*이 탈옥 작업을 했다는 사실만으로 **Amazon이 이를 상무부에 공식 신고했다고 확인되지는 않는다**. Amazon 연구실에서 수출 명령으로 이어지는 인과관계는 확립된 사실이 아니라 추론이다. AI 책임자 **David Sacks**는 별도로 "Anthropic이 수정을 거부했다"는 행정부의 설명을 공개 기록에 남겼다. [[federal-ai-policy]]를 참고하라(ARA digest 2026-06-15).

- **Amazon이 Nova 모델 제품군 대부분을 축소한다는 보도(2026-07-30, 단일 출처, 미확인).** Amazon은 **Nova Premier, Nova Omni, Nova Reel, Nova Canvas**를 지원 전용 모드로 전환하고, 엔지니어링과 컴퓨팅 자원을 Berkeley AI·로보틱스 연구자인 **Pieter Abbeel이 이끄는 새 Frontier Model Research 팀**으로 돌리는 것으로 알려졌다. 목표는 **later in 2026에 re:Invent 형식의 대표 모델을 공개**하는 것이며, Nova 이름을 유지할 가능성도 있다. **Nova 2 Lite, Nova 2 Sonic, Nova Act, Nova Forge**는 계속 활성 상태로 남는 것으로 전해졌다. 이는 Amazon의 기존 다중 모델 Nova 제품군에서 독자 개발 프런티어 모델 하나로 옮겨가는 전략적 전환이며, 다른 하이퍼스케일러의 "유명 연구자를 영입해 대표 모델 하나를 만든다"는 양상을 닮았다. 다만 2026-07-30 현재 Amazon의 발표 없이 단일 계정에만 근거한다(연결된 모델 티켓의 상태는 `rumored`)(ARA daily digest 2026-07-30).
- **계획 중인 Amazon 데이터센터가 기록적인 기후 오염원이 될 가능성으로 조사 대상이 됨(2026-08-08).** TechCrunch와 The Verge는 모두 **현장 발전소 때문에 미국 최대의 기후 오염원이 될 수 있는 Amazon의 계획 중 데이터센터**를 보도했다. 한 하이퍼스케일러의 특정 프로젝트에 [[ai-capex]] 확장의 배출 외부효과가 집중된 지금까지 가장 선명한 사례로, [[ai-capex]]에서 추적하는 요금 납부자 보호 약속·인허가 관문 논쟁과 맞닿아 있다(TechCrunch, The Verge; ARA daily digest 2026-08-10).

## 미해결 질문

- **Nova 축소 보도는 사실로 확인되는가?** Pieter Abbeel의 Frontier Model Research 팀 주장에는 아직 Amazon 발표가 없다. re:Invent 2026 발표나 Amazon의 공개적인 확인·부인을 지켜봐야 한다.
- **이 브리핑은 Amazon–Anthropic 관계를 훼손하는가?** 최대 투자자가 피투자사의 대표 모델 금지에 일조한 일은 전례가 없다. 이것이 진정한 보안 판단인지 경쟁적 책략인지는 아직 열려 있다.
- **탈옥이 금지를 정당화할 만큼 심각했는가?** [[anthropic|Anthropic]]은 자체 블로그에서 이 명령을 "오해"라고 부르며 같은 취약점이 GPT-5.5 같은 공개 모델에도 존재한다고 주장했다. Amazon의 재확인과 행정부의 대응 모두 검증 대상이 됐다.
