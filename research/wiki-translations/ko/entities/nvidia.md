---
slug: nvidia
language: ko
source_file: research/wiki/entities/nvidia.md
source_sha256: b55180c8d5b1961c1346de48a60812a40d74edab52e118b949838fdd941ef7a0
title: NVIDIA
description: 지배적인 AI 가속기 공급업체이자 2026-08-10 보도된 월가의 약 ~$500B AI 인프라 금융 패키지의 중심축. Ilya Sutskever의 Safe Superintelligence에 약 ~$5B을 지원하고, 1T 매개변수 Nemotron 4를 목표로 하는 오픈 웨이트 Nemotron 계열과 자체 ~$500B 패키지의 잔존가치 보증을 추진한다.
images:
  - url: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/NVIDIA_H100_%28%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan%29_007.png/1280px-NVIDIA_H100_%28%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan%29_007.png"
    alt: AI 학습과 추론에서 NVIDIA의 역할을 보여주는 NVIDIA H100 가속기 근접 사진.
    caption: AI 자본지출 확대의 중심에 있는 가속기 등급인 NVIDIA H100 하드웨어.
    credit: "Geekerwan / Wikimedia Commons (CC BY 3.0)"
    source_url: "https://commons.wikimedia.org/wiki/File:NVIDIA_H100_(%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan)_007.png"
  - url: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Nvidia_DGX_Station%2C_world%27s_most_powerful_desktop%2C_a_Supercomputer_at_the_office.webm/1280px--Nvidia_DGX_Station%2C_world%27s_most_powerful_desktop%2C_a_Supercomputer_at_the_office.webm.jpg"
    alt: NVIDIA의 로컬 및 데이터센터 AI 시스템 사례로 제시된 데스크사이드 AI 슈퍼컴퓨터 NVIDIA DGX Station.
    caption: 이 문서의 데스크사이드 AI 슈퍼컴퓨터 논의에 맥락을 제공하는 DGX Station급 하드웨어.
    credit: "Charbax / Wikimedia Commons (CC BY 3.0)"
    source_url: "https://commons.wikimedia.org/wiki/File:Nvidia_DGX_Station,_world%27s_most_powerful_desktop,_a_Supercomputer_at_the_office.webm"
---

**NVIDIA**는 AI 학습 및 추론 가속기의 지배적 공급업체다. 이 회사의 GPU와 그 수요는 [[ai-capex]] 초호황의 구조적 중심에 있다. 실적은 "수요가 실제로 존재한다"는 대표 지표이고, [[coreweave]]와 [[nebius]] 같은 [[neocloud|네오클라우드]] 업체는 부채로 하드웨어를 사서 다시 임대한다. 2026년에는 실리콘 위에 자체 **오픈 웨이트 모델**인 Nemotron 계열까지 점점 더 많이 출시했다.

## 중요한 이유

- **수요·공급의 핵심 지표.** NVIDIA의 **FY27 Q1 실적은 매출 $81.62B(+85% Y/Y)**, 데이터센터 $75.25B, 투자자 기대를 넘는 **Q2 가이던스 $91B**, 신규 **$80B 자사주 매입**이었다. [[ai-capex]] 구축에서 수요가 실제라는 대표 신호다. Jensen Huang은 "인류 역사상 최대의 인프라 확장… 에이전트형 AI가 도래했다"고 말했다. 그런데도 주가는 시간 외에서 약 3% 하락하며 **"예상을 웃돌아도 하락 마감"** 패턴을 이어갔다. 시장은 분기가 아니라 *서사*에 가격을 매긴다(ARA digest 2026-05-21). 같은 징후가 2026-06-05 [[broadcom]]에는 훨씬 더 강하게 나타났다(AVGO −12.6%, *상향되지 않은* 가이던스로 약 $320B 증발). [[ai-capex]]를 참고하라.
- **GTC Taipei 기조연설(2026-06-01).** Jensen Huang의 Computex 기조연설은 열한 가지 발표를 내놓았다. Windows에서 GB300으로 최대 **1-trillion-parameter** 모델을 로컬 실행하는 최초의 데스크사이드 AI 슈퍼컴퓨터 **DGX Station for Windows**, 로보틱스·자율주행 월드 모델 계열 **Cosmos 3**, L4 로보택시용 32B 오픈 웨이트 VLA **Alpamayo 2 Super**, 휴머노이드 레퍼런스 **Isaac GR00T**, 소비자 Windows 노트북에서 1 PFLOP 온디바이스 추론을 제공하는 **RTX Spark**(fall 2026), 그리고 "회사 역사상 가장 빠른 제품 출시"인 **Vera CPU**가 핵심이다. DGX Station + RTX Spark + OpenShell 조합은 명백한 **Windows-on-NVIDIA** 제안이며 [[microsoft]] Build 2026보다 24h 앞서 공개됐다.
- **Nemotron-3-Ultra-550B, 오픈 웨이트 승부(2026-06-05).** NVIDIA는 **Nemotron-3-Ultra-550B-A55B**를 공개했다. **LatentMoE 하이브리드**(Mamba-2 + MoE + Attention + MTP), **총 550B / 활성 55B**, **1M 컨텍스트**, **NVFP4 사전 학습**, 전환 가능한 추론을 갖췄다. **데이터센터 전용**(8×GB200 / 16×H100)이며 **OpenMDW 1.1** 아래 상업 이용이 가능하다. GTC 표현대로 가중치뿐 아니라 가중치 + 데이터셋 + 코드를 공개해 "**진정으로 개방**"됐다. Google's [[gemma-4]]와 함께 Hacker News와 r/LocalLLaMA를 지배하며 2026 오픈 웨이트 물결의 양 끝을 이뤘다. 한쪽은 데이터센터 규모의 Nemotron 550B, 다른 쪽은 16 GB 노트북에서 접근 가능한 Gemma다. NVIDIA는 맞춤형 멀티모달 기업 안전 모델 **Nemotron 3.5 Content Safety**도 Hugging Face에 공개했다(ARA digest 2026-06-05).

- **Anthropic의 첫 NVIDIA 실리콘 배포(2026-06-30).** [[anthropic]]의 [[claude-opus-4-8|Claude Opus 4.8]]과 **Haiku 4.5**가 **[[microsoft|Microsoft Foundry]] on Azure**에서 **NVIDIA GB300 NVL72(Blackwell Ultra)** 및 **Quantum-X800 InfiniBand** 시스템으로 GA가 됐다. 보도상 **Anthropic 모델이 NVIDIA GPU에서 실행된 최초 사례**다. 기존 스택은 AWS Trainium과 Google TPU에 기대었다. NVIDIA를 네이티브로 쓰지 않던 마지막 주요 프런티어 연구소가 이제 Blackwell Ultra에서 주력 모델을 제공한다는 주목할 수요 견인 지표이며, [[ai-capex]] 구축의 중심에서 이 실리콘의 입지를 강화한다. *("NVIDIA 최초"라는 최상급 표현은 처음에는 단일 출처였다.)* (ARA digest 2026-06-30).

- **하루에 자본·제휴 움직임 세 건이 겹쳤다(2026-07-28).** NVIDIA는 [[openai]]의 오하이오 남부 **10-gigawatt 데이터센터 캠퍼스**(SoftBank 개발, 총비용 약 ~$500B)에 **약 ~$250B 금융 안전망**을 논의 중인 것으로 전해졌다. 별도로 OpenAI가 Nvidia 칩을 사는 **약 ~$350B 논의**도 있어 한 관찰 계정은 순환금융이라고 지적했다([[openai]], [[ai-capex]] 참고). 따로 NVIDIA는 [[safe-superintelligence|Ilya Sutskever의 Safe Superintelligence]]에 SSI의 **$32B 투자 후 기업가치**를 기준으로 **약 ~$5B**을 약정한 것으로 보도됐다. 두 회사가 컴퓨팅 파트너십을 확인한 지 몇 시간 뒤였고, 2024년 설립 이래 공개된 첫 상당한 SSI 지원이다. 단순 현금 지급이 아니라 마일스톤 조건부로 설명됐다. NVIDIA의 새 **Open Secure AI Alliance**에는 Hugging Face, [[microsoft]], Palo Alto Networks, [[salesforce]], SAP, Red Hat, Cloudflare가 참여해 AI 보안 도구를 내놓았지만 공개 회원 명단에는 **OpenAI가 눈에 띄게 빠졌다**. 검증되지 않은 한 전달자는 내부 결정이 직원 "반발"을 불렀다고 주장한다(ARA daily digest 2026-07-28).

- **대만 칩 밀수 수사가 형사사건으로 전환(2026-07-29).** 대만 법원은 2026-07-28부터 구금된 NVIDIA 직원에 대해 **문서 위조와 배임** 혐의를 들어 계속 구금하도록 했다. 이미 구금된 Super Micro 연계 유통업자와 데이터센터 운영자가 포함된 **더 넓은 네트워크**와 사건을 연결했다. 직원 한 명의 구금으로 시작한 사건(모델 티켓 `nvidia-taiwan-smuggling-probe-2026-07` 참고)이 수출 통제를 피해 중국에 들어간 칩을 둘러싼 다자간 형사 수사로 확대됐다. 대만 정부가 NVIDIA 직원을 직접 조치한 첫 사례다(ARA daily digest 2026-07-29).

- **두 번째 공급원이 분기 수치로 확인되고 HBM이 공통 제약이 됐다(2026-08-05).** [[amd]]는 데이터센터 매출 **$6.7B, YoY 107% 증가**, 회사 전체의 58%를 기록했고 **Helios가 [[anthropic]]의 2 GW MI450 약정에 맞춰 증산을 시작**했다. "신뢰할 수 있는 두 번째 공급원"을 서사가 아니라 숫자로 만든 첫 분기 실적이다. 같은 주기에 TrendForce는 **NVIDIA가 early Q3 2026부터 Rubin Ultra의 HBM 구성을 재평가해 왔으며 최종 사양은 아직 정해지지 않았다**고 보도했다. 2027 HBM 비트 출하량은 50–60% 증가할 전망이지만 수요에는 여전히 못 미친다. 이제 두 업체는 가속기 설계가 아니라 메모리 배분에 맞춰 일정을 짠다. [[ai-capex]]와 [[micron]]을 참고하라(ARA daily digest 2026-08-05).

## 미해결 질문

- **오픈 웨이트 모델 출시는 실리콘 해자를 잠식할까, 더 깊게 할까?** Nemotron은 데이터센터 전용이고 NVFP4 네이티브다. NVIDIA 하드웨어에서 가장 잘 실행되는 모델은 증정품이 아니라 수요 견인 장치다.

## 월가가 NVIDIA를 중심으로 부채 기반 약 ~$500B을 조성하다 (2026-08-10)

**약 ~$500B AI 인프라 금융 패키지**가 NVIDIA를 중심으로 조성 중이라고 보도됐다. **Apollo, Blackstone, BlackRock's Global Infrastructure Partners, Brookfield, Goldman Sachs, KKR**가 거론됐다. CNBC 전달 내용은 익명의 한 명에게 의존했고, 이후 FT를 인용한 전달은 자본이 아니라 **부채**라고 명시했다. 가치가 하락하는 GPU 자산을 담보로 한 레버리지라는 중요한 차이다. **이름이 공개된 어느 참여자도 확인하지 않았다.** 이 신디케이트에 연결된 첫 실명 수단은 임원 발언(Jensen Huang, Brookfield's Bruce Flatt, BlackRock's Larry Fink, Blackstone's Jon Gray)과 함께 발표된 **Nvidia–IREN "DSX AI factories" 파트너십**이다. 그럼에도 IREN은 발표가 나온 세션에 약 **6.1% 하락** 마감했다. OpenAI Ohio 안전망 이래 이 페이지가 추적한 장부외 금융 패턴이 어떻게 이어지는지는 [[ai-capex]]를 참고하라(CNBC/FT 전달; ARA daily digest 2026-08-11).

## 25% 안전망이 구체화되고 Nemotron 계열은 에이전트로 전환하다 (2026-08-11/12)

- **프로젝트별 25% 안전망 보도(2026-08-11/12).** *The Information*에 따르면 NVIDIA는 ~$500B 패키지 안에서 개별 프로젝트 손실의 **최대 25%**를 흡수할 수 있다. **자사 GPU가 판매된 프로젝트**도 포함된다. "새 자산군" 틀이 답하려던 순환성이 정확히 드러난다. **공개된 조건표는 없다.** 2026-08-10 항목의 "CNBC 익명 단일 출처"와 "지분이 아닌 부채"라는 단서가 여전히 적용된다. 2026-08-13 WSJ는 **Jensen Huang이 이 지원을 잔존가치 보증으로 규정했다**고 보도했다. NVIDIA는 **자신이 노후화 일정을 정하는 하드웨어의 재판매 하한을 보증**한다. 안전망을 공급업체가 통제하는 감가상각으로 읽는 근거다(ARA daily digest 2026-08-12/13).
- **Nemotron 3.5 Lightning + NeMo Switchyard, 에이전트 물량 제안(2026-08-11/12).** NVIDIA는 **항시 가동 에이전트**를 겨냥한 **오픈 웨이트 30B mixture-of-experts**, 활성 매개변수 **약 ~3B**인 **Nemotron 3.5 Lightning**과 각 단계를 수행 가능한 가장 저렴한 모델로 보내는 라우팅 라이브러리 **NeMo Switchyard**를 출시했다. [[meta]]가 자체 30B 에이전트 모델([[muse-glimmer]])을 오픈 웨이트로 공개한 지 **27시간 뒤**였다. 제안의 핵심은 벤치마크 우위가 아니라 **에이전트 *물량***이다. 순위표가 아니라 [[openai]]와 [[anthropic]] 트래픽을 겨냥한다. 라우팅 경제성에 관한 가장 구체적인 공개 수치도 나왔다. **LangChain이 에이전트 작업 145개로 Switchyard를 벤치마크한 결과, 프런티어 모델이 필요했던 턴은 7%뿐이었고 라우팅은 정확도 여섯 점을 희생해 비용을 74% 줄였다.** 에이전트 트래픽이 얼마나 과잉 서비스되는지 보여주는 공개 추정치다. 2026-08-13 **Nemotron 3.5 Lightning은 Perplexity Agent API에서 백만 토큰당 $0.0115/$0.17**에 제공되기 시작했다. 이 주기에 널리 유통된 에이전트 모델 중 가장 저렴한 요금표다(The Information, The Decoder, LangChain; ARA daily digest 2026-08-12/13).
- **Nemotron 4 개발 보도, 이제 최첨단을 겨냥하다(2026-08-11/13).** *The Information*과 The Decoder에 따르면 NVIDIA는 **일조 매개변수를 목표로 하는 오픈 웨이트 계열**을 개발 중이다. **중국 연구소들은 이미 넘어선 규모**이며 **서구 오픈소스 경쟁을 촉진**하는 것이 목표다. The Information은 NVIDIA가 **Nemotron 4를 최첨단으로 만들려 한다**고 별도 보도했다. 그렇게 되면 **최대 고객인 모델 연구소들과 경쟁**하게 된다. 아래의 Nemotron 계열 잠식 질문이 가장 날카로운 형태로 제기된다. 보도 단계로 취급해야 하며 아직 산출물은 없다(ARA daily digest 2026-08-12/13).

## 미해결 질문

- **TSMC 상한.** TSMC는 2026-06-05 **미국 확장에도 AI 칩 수요를 충족할 수 없다**고 경고했다. NVIDIA 가이던스 바로 상류에 놓인 강한 공급 제약이다([[ai-capex]] 참고).
- **"예상을 웃돌아도 하락 마감" 신호.** 시장은 왜 공급 측에서 가장 강력한 단일 지표를 계속 매도하는가? 성장이 이미 가격에 반영됐기 때문인가, 초호황의 지속성에 대한 초기 의심인가?
