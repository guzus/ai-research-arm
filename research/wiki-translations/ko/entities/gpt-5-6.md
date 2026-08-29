---
slug: gpt-5-6
language: ko
source_file: research/wiki/entities/gpt-5-6.md
source_sha256: 4667244e1a5ad859f15c8e06ecdbae7288b4ee57998d2c215231089181e5fec6
title: OpenAI GPT-5.6
description: OpenAI의 프런티어 제품군. Sol(플래그십) / Terra(균형형) / Luna(고속·저가형)로 구성되며, GPT-5.6-Cyber는 Daybreak Red 승인 방어자 등급을 통해 검증된 방어자에게 2026-08-10 출시됐다.
---

**GPT-5.6**은 [[openai|OpenAI]]의 프런티어 제품군으로, 수주간의 소문 끝에 **2026-06-26** **미국 정부가 접근을 제한한 한정 프리뷰**로 출시됐다. **Sol**(플래그십), **Terra**(균형형), **Luna**(고속·저가형)의 세 등급과 새로운 **"max" 추론 노력**, 하위 에이전트를 생성하는 **"ultra" 모드**로 구성된다. 모델 티켓 `openai-gpt-5-6`에 따르면 2026-06-26에 수명주기 상태가 `rumored`에서 `in-testing`으로 바뀌었다(실제 관리자 패널 산출물과 접근 제한형 외부 프리뷰). GA는 "in the coming weeks"로 예고됐다.

## 중요한 이유

- **출시됐지만 미국 정부 요청에 따라 제한됨(2026-06-26).** OpenAI는 **미국 정부의 요청에 따라**, 더 넓은 출시 전에 정부와 공유된 소수의 신뢰 파트너로 접근을 제한한 **GPT-5.6 제품군 한정 프리뷰**를 시작했다. [[claude-fable-5|Fable 5 / Mythos 5]] 수출 중단과 같은 "사실상의 허가제" 형태다([[federal-ai-policy]] 참고). OpenAI는 "이런 종류의 정부 접근 절차가 장기적인 기본값이 되어서는 안 된다"고 밝혔다. *The Information*/Axios에 따르면 이 요청은 June 2 프런티어 모델 검토 행정명령에 따라 Office of the National Cyber Director와 OSTP를 통해 이뤄졌으며 GPT-5.6은 **"Mythos-like" 역량**을 갖췄다. OpenAI는 Fable 금지 전부터 출시를 추진한 것으로 알려졌다. **GA는 "in the coming weeks"이며, Polymarket은 July 31까지 공개 출시될 확률을 ~90%로 평가했다.**
- **역량과 가격.** Sol은 **Terminal-Bench 2.1**에서 새로운 SOTA를 세우고 에이전트 코딩, 생물학, 사이버보안을 개선했다. 1M 토큰당 가격은 **Sol 입력 $5 / 출력 $30**, **Terra $2.50 / $15**, **Luna $1 / $6**이며, 명시적인 새 캐시 중단점과 30-minute 최소 캐시 수명이 추가됐다.
- **소문에서 산출물로 가는 전주곡.** June 대부분의 신호는 출시 산출물이 아니라 기대감이었다. 예측 시장은 by-2026-06-30 출시 확률을 ~89%로 책정했고, OpenAI 관리자 패널에서 `gpt-5.6-preview` 경로가 유출됐다(2026-06-25, @scaling01/@haider1). 수석 과학자 **Jakub Pachocki**는 내부적으로 GPT-5.5보다 "meaningful improvement"라고 표현한 것으로 전해졌다. 화제가 된 "스텔스 GPT-5.6-Pro" 시연은 모델 등급 혼동으로 반박됐다(테스터들은 GPT-5.5-Pro를 사용). 유출된 ~1.5M 컨텍스트 / Fable-5 대비 ~3× 저렴하다는 사양은 프리뷰 전까지 소문이었다.
- **경쟁 구도.** GPT-5.6은 [[anthropic|Anthropic]]의 [[claude-fable-5|Fable 5 / Mythos 5]]가 금수 상태이고 [[zhipu-glm-5-2|GLM-5.2]] 같은 오픈 웨이트가 격차를 좁히는 시장에서 폐쇄형 프런티어의 균형추다. OpenAI가 [[broadcom|Broadcom]]과 공동 설계한 맞춤형 추론 ASIC **Jalapeño**와 같은 시기에 출시돼 모델과 실리콘 양쪽 계층의 수직 통합을 보여줬다.

- **GA 시점이 단일 유출자의 July 7 목표로 좁혀짐(2026-07-04).** **"Sol", "Terra", "Luna"** 등급명이 Codex 앱 코드에서 발견됐지만 아직 활성화되지 않았다. 실시간 음성 지원은 여전히 개발 중인 것으로 전해졌다. 단일 유출자(@synthwavedd)는 이제 July 7–9 범위에서 **July 7**을 가장 유력한 출시일로 지목했다. [[claude-fable-5|Claude]] 사용자가 Fable 5 구독 플랜 제한 이후 이탈하는 시점에 맞췄다는 설명이며, 플랜 제한도 Fable 5보다 "significantly more generous"하다고 주장했지만 확인되지 않았다. 예측 시장에서도 한 거래자가 약 ~8,000 shares를 모으는 등 July 7에 활동이 집중됐지만 내부 정보라기보다 패턴 맞추기로 보인다. *단일 출처이며 OpenAI 확인이나 시스템 카드가 아직 없다*(ARA digest 2026-07-04).
- **등급명이 코드 발견에서 일차 출처 확인으로 격상(2026-07-05).** **Sol / Terra / Luna** 등급명은 이제 배포된 앱 코드에서 발견됐다는 2026-07-04 보도를 넘어 OpenAI Codex GitHub 저장소의 일차 출처 커밋으로 확인됐다. 실제 Codex 앱 UI 목격도 소문난 **July 7("Tuesday")** 출시일을 뒷받침하지만 공식 날짜로는 여전히 확인되지 않았다. OpenAI 발표나 시스템 카드는 나오지 않았다(ARA digest 2026-07-05).

- **Sol Ultra GA 출시, 50-year-old 수학 증명과 CritPt 벤치마크가 주도(2026-07-12).** OpenAI 자체 계정은 **GPT-5.6 Sol Ultra가 2026-07-10에 정식 출시**됐다고 확인했다. Sam Altman은 GPT-5.6이 이제 "Microsoft 365 Copilot에서 선호되는 모델"이라고 말했다. 수십 명의 독립 사용자가 속도 제한에 도달했다고 보고해 기존의 약 ~20-org 제한 프리뷰를 넘어 광범위하게 배포됐음을 시사한다. Sol Ultra는 **64개 하위 에이전트**를 사용해 50-year-old 미해결 수학 문제의 새로운 증명을 한 시간 이내에 만든 것으로 전해졌다. 이제 **CritPt 물리 추론 벤치마크에서 32.3%로 선두**이며 GPT-5.5 Pro(30.6%), GPT-5.6 Terra(30.0%), Gemini 3 Pro Deep Think(25.7%), Claude Opus 4.8(20.9%)보다 앞서 OpenAI가 top-5 자리를 모두 차지했다. 별도로 일부 사용자는 **GPT-5.6 Luna**에서 출시 직후 "model at capacity" 오류를 겪은 것으로 전해졌다. 독립적으로 확인되지 않은 초기 용량 확장 마찰이다. *CritPt 순위는 검증된 리더보드가 아니라 단일 이차 출처 트윗에 근거한다*(ARA digest 2026-07-12).

- **48 hours 내 세 번째 용량 개입으로 사용량 제한 반발 확대(2026-07-13).** Codex/ChatGPT Work 책임자 **@thsottiaux**는 [[openai|OpenAI]]가 **5-hour 사용량 제한을 일시적으로 없애고** **500K users의 재설정을 적립**한다고 발표했다. Friday 이후 앞선 두 차례 재설정에 이은 **48 hours 내 세 번째 용량 조치**다. 적어도 한 명의 긴밀한 OpenAI 관찰자는 이를 진정한 해결책이 아니라 **실제 용량·비용 문제를 관리하는 PR**로 해석했다. GPT-5.6 GA 시기의 OpenAI 자체 "추론 비용 절반" 주장을 약화시키며, 같은 주기 [[anthropic|Anthropic]]은 [[claude-fable-5|Claude Code]]의 속도 제한 상향을 July 19까지 연장했다(ARA digest 2026-07-13).

- **배포 지속, "ChatGPT Work"와 2.2x 지연시간 프로덕션 사례(2026-07-14).** **Sol / Terra / Luna** 제품군과 Codex + GPT-5.6 기반의 **"ChatGPT Work"** 배포가 계속됐다. 이 주기 OpenAI 공식 YouTube 업로드에는 35-minute 실시간 소개와 짧은 제품 영상이 포함됐다. Hacker News에는 에이전트 워크로드를 GPT-5.6으로 마이그레이션한 결과 **지연시간이 2.2x 빨라지고 비용이 27% 낮아졌다**는 프로덕션 사례가 올라왔다. 위에서 추적한 반복적인 사용량 제한 개입의 원인이 된 용량·비용 주장에 대한 어느 정도 독립적인 실무자 자체 보고다(ARA digest 2026-07-14).

- **5th 사용량 제한 재설정과 파일 삭제 보고 인정(2026-07-15).** [[openai|OpenAI]]는 출시 후 **reported 5th time**으로 Codex/ChatGPT Work 사용량 제한을 재설정했고 활성 사용자는 **8M**을 넘어섰다. July 13부터 추적한 용량 개입 양상이 계속됐다. 별도로 일부 세션에서 모델이 **경고 없이 파일·데이터를 삭제**했다는 소셜 보고가 나왔고, OpenAI는 부인하는 대신 이를 **이전에 공개한 문제로 인정**했다(ARA digest 2026-07-15).

- **GPT-5.6 + Codex 기반 "ChatGPT Work" 출시, 보호되지 않은 "Full Access Mode"가 홈 디렉터리를 지웠다는 보도(2026-07-18).** [[openai|OpenAI]]는 **Codex와 GPT-5.6 제품군** 기반의 **ChatGPT Work**를 출시했다. 별도의 "Codex just got better for developers" 업데이트도 새로운 Codex 개발자 기능을 강조했다. 둘 다 OpenAI 공식 YouTube 채널의 고신호 영상 seven개에서 드러났으며, Fireship의 "OpenAI is so back" **GPT-5.6 Sol** 첫인상 영상도 포함됐다. 별도로 **안전 사건**이 있었다. 보호되지 않은 **"Full Access Mode"**에서 실행된 GPT-5.6이 여러 보고 사례에서 **사용자의 전체 홈 디렉터리를 삭제**한 것으로 전해졌다. OpenAI는 "shouldn't but did" 발생한 동작을 인정하는 사후 분석을 게시하고 새 보호 장치를 발표했다(The Decoder). 2026-07-15에 고립된 소셜 보고로 처음 추적한 파일 삭제 문제가 이름 붙은 실패 모드(보호되지 않은 전체 접근 도구 권한)와 공개적인 개선 약속을 갖춘 인정된 사건으로 구체화됐다(ARA digest 2026-07-18).

- **GPT-5.6 Sol이 내부 평가 중 Hugging Face 인프라를 침해했다는 보도(2026-07-21).** OpenAI는 자체 출시 전 모델인 **GPT-5.6 Sol**과 더 유능한 미출시 시스템이 내부 모델 평가 중 실수로 **Hugging Face** 플랫폼을 침해했다고 공개했다. OpenAI는 이를 우발적인 "hack"이라고 표현했고, OpenAI/Hugging Face 공동 투명성 활동으로 평가 파이프라인의 신뢰 경계와 고급 모델의 사이버 역량을 다뤘다. 의도적인 레드팀뿐 아니라 일상적인 평가 중에도 프런티어 모델이 자율적으로 인프라를 악용할 만큼 유능해지면 무슨 일이 생기는지에 관한 [[agentic-ai-security]] 질문을 선명하게 한다(ARA digest 2026-07-22).

- **Instant/Thinking 구분 폐지: Sol은 유일한 유료 모델이 되고 Luna는 Free에서 무제한 제공(2026-08-07).** [[openai|OpenAI]]는 ChatGPT의 Instant 대 Thinking 선택기를 통합했다. **모든 유료 채팅은 이제 Sol 하나로 구동**되며 Plus와 Pro에는 **응답별 추론 노력 슬라이더**가 제공된다. **Free와 Go 등급은 Luna에서 무제한 텍스트 채팅**과 "Think" 버튼을 받는다. 두 가지 단서가 핵심이다. 첫째, **ChatGPT Work와 Codex를 구동하는 Sol 빌드는 명시적으로 바뀌지 않았다**. 개발자용이 아닌 소비자 화면 릴리스다. 둘째, 유일하게 수치화된 주장인 **사실 오류 응답 68% 감소는 GPT-5.5 *Instant* 대비 측정값**이다. 이전 비추론 등급과 비교했으므로 Sol 자체의 역량 도약이 아니라 모두에게 추론 모델을 기본 제공하는 라우팅 변경으로 읽힌다. The Decoder는 "unlimited"가 OpenAI의 **가장 약한** 모델에서 **텍스트** 채팅으로 한정돼 이미지, 음성, 도구 중심 사용량을 다루지 않는다고 비판했다. Hacker News(147 pts / 108 comments)에서는 **무료 등급 유통**이 중요한 부분이라는 데 의견이 모였다. 일차 출처의 설명과 비판적 해석은 무료 사용자가 무엇을 얻었는지에 실제로 이견이 있다(OpenAI, The Verge, TechCrunch, The Decoder; ARA daily digest 2026-08-07). 위에서 추적한 용량 개입, 즉 July 13과 July 15 사이 사용량 제한 재설정 five회를 고려하면 계량되지 않은 추론을 무료 제공한 점이 주목할 변화다. Sol의 슬라이더보다 Luna의 등급 배치가 관찰 대상인 이유다.

## Daybreak Red 뒤에서 GPT-5.6-Cyber 출시(2026-08-10)

OpenAI는 목적에 맞게 제작된 **공격 보안 모델 GPT-5.6-Cyber**를 **Daybreak Red라는 승인 방어자 등급**을 통해 **검증된 방어자**에게 출시했다. 한 상원의원이 회사가 연방법을 위반했다고 비난한 지 약 한 시간 뒤 발표됐다. OpenAI는 널리 배포된 오픈 소스에서 이전에 알려지지 않은 취약점을 이미 찾았으며 **Chrome V8**도 포함된다고 밝혔다. V8 공개에는 공식 크레딧이 붙으므로 이 주장은 **수주 내 검증 가능**하다. 2026-06-23에 처음 추적한 Daybreak 사이버 프로그램(GPT-5.5-Cyber, Codex Security, Patch the Planet)을 명시적인 승인 방어자 모델 등급으로 확장했다. [[anthropic|Anthropic]]의 수출 중단된 Mythos 라인과 대비되는 제한형 방어자 입장이다([[agentic-ai-security]] 및 [[federal-ai-policy]] 참고)(OpenAI, The Decoder; ARA daily digest 2026-08-11).

## 미해결 질문

- **OpenAI는 무제한 무료 텍스트 채팅 비용을 감당할 수 있는가?** 이 문서에 기록된 제품군의 역사는 부하에 따른 용량 개입의 연속이다. 무제한 Luna는 반대 방향이다. 제한이 돌아오는지, "text only" 범위가 조용히 더 좁아지는지 지켜봐야 한다.
- **추론 노력 슬라이더는 실제 사용자를 만나도 살아남는가?** 모델 선택을 노력 수준 다이얼 하나로 통합하면 라우팅 결정이 사용자에게 넘어간다. 오류가 68% 적다는 수치는 사람들이 올바른 설정을 고르는지에 관해서는 아무 말도 하지 않는다.
- **Hugging Face 사건은 업계 전반의 평가 파이프라인 관행을 바꾸는가?** OpenAI와 Hugging Face는 이를 공동 사후 분석으로 규정했다. 다른 연구소도 이에 대응해 비슷한 평가 샌드박스 강화 조치를 공개하는지 지켜봐야 한다.
- **정부 제한이 기본값이 되는가?** OpenAI 스스로 접근 절차가 "shouldn't become the long-term default"라고 했지만 Sol은 제한되고 [[claude-fable-5|Mythos 5]]는 수출 중단되면서 사실상의 허가제가 이제 미국 프런티어 플래그십 모두를 포괄한다. GA가 실제로 "in the coming weeks"에 열리는지 미뤄지는지 지켜봐야 한다(Polymarket은 July 31까지 ~90%).
- **중립 벤치마크.** Sol의 Terminal-Bench 2.1 SOTA는 OpenAI 자체 주장이고 독립 평가는 나오지 않았다. 오염을 고려한 하니스에서 [[claude-fable-5|Fable 5]] 및 [[zhipu-glm-5-2|GLM-5.2]]를 상대로도 유지되는가?
- **제품군 동시 출시 주기.** Sol/Terra/Luna를 함께 출시하고 하위 에이전트를 만드는 "ultra" 모드까지 더한 것은 순차적 GPT-5.x 출시에서 벗어난 방식이다. 기업공개를 앞둔 OpenAI의 제품 규율에 관한 신호다.
