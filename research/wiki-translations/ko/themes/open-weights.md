---
slug: open-weights
language: ko
source_file: research/wiki/themes/open-weights.md
source_sha256: 6e41fc7194d9c29499994ec50aed6e7b654193c37924787d3aaf80d1381da067
title: 오픈 웨이트 물결
description: 갈수록 프런티어 역량에 근접하는 오픈 웨이트 모델과 함께 토렌트 네트워크, 로컬 호스팅, "API는 빌리는 것이고 가중치는 영원하다"는 탈중앙화 반발이 힘을 얻는 2026년의 서사. Fable 5의 정부발 중단으로 급등했고, Meta의 Apache-2.0 공개 복귀(Muse Glimmer, 2026-08-10)와 Alibaba의 첫 Max급 Qwen 개방(2026-08-13)을 거치며 mid-2026에 굳어졌다.
---

**오픈 웨이트 물결**은 갈수록 중국산 비중이 커지는 오픈 웨이트 모델이
프런티어 역량에 근접하는 동시에 **탈중앙화 반발**이 정치적 힘을 얻는 2026년의
횡단적 서사다. [[anthropic]]과 [[openai]]의 문지기형 프런티어 전략에 맞서는
구조적 역풍이다. **2026-06-14**, [[claude-fable-5|Fable 5 / Mythos 5]]의
정부발 중단에 대한 직접적인 반작용으로 급등했다. 독점 주력 모델이 단 하나의
수출 명령으로 꺼질 수 있다면 "빌린" API는 취약해 보이고 로컬 가중치는 보험처럼
보인다.

## 중요한 이유

- **Fable 5 중단에 대한 반응의 틀(2026-06-14).** HN 선언문 **"Open source
  AI must win"**은 **1,480 points / 459 comments**까지 치솟으며 정부 압력
  아래 독점 AI 집중은 구조적으로 취약하다고 주장했다. **r/LocalLLaMA**는 분산
  미러, 제안된 **오픈소스 가중치용 토렌트 네트워크**("HuggingFace is a US
  single point of failure"), 그리고 중단 전에 보관된 기존 **Fable 5 CoT
  데이터셋**을 중심으로 결집했다. 반복된 구호이자 그날의 오늘의 인용문은
  *"APIs are rented, local weights are forever"*였다(ARA digest 2026-06-14).
- **[[zhipu-glm-5-2|GLM 5.2]](Zhipu AI) — 대표적인 오픈 웨이트 출시
  (2026-06-14).** **1M-token context**와 max/high thinking modes를 갖춰 GLM
  Coding Plan에 배포됐고, **MIT license 오픈 웨이트는 다음 주에 도착할
  예정**이었다. 일회성 코딩 벤치마크(예: Pac-Man test)는 이를 **Qwen 3.6
  27B보다 높은 선두**로 평가했다.
- **[[moonshot-kimi-k2-7-code|Kimi K2.7-Code]](Moonshot AI) — 가격 서사
  (2026-06-14).** 성능 경쟁력을 유지하면서 **토큰당 가격이 GPT-5.5와
  Claude보다 최대 12× 저렴한** 오픈 코딩 모델이다. Unsloth GGUF 양자화도
  이미 업로드되며 오픈 웨이트의 경제적 우위를 구체화했다.
- **[[xiaomi-mimo-v2-5-pro|Xiaomi MiMo UltraSpeed]] — 효율성 서사.**
  Xiaomi의 MiMo-v2.5-Pro-UltraSpeed는 표준 8-GPU 서버에서 1T MoE를
  **1,000+ tok/s**로 구동한다고 주장한다. 아직 부분 검증에 불과하지만 서빙
  비용 프런티어를 가리킨다. 오픈 웨이트는 충분히 싸고 빠르게 실행할 수 있을
  때만 운영상 의미가 있다.
- **궤적은 중단보다 앞서 시작됐다.** [[deepseek]](V4), [[minimax-m3]](1M
  context, 59% SWE-Bench Pro), [[gemma-4]](Google DeepMind, Apache 2.0),
  [[nvidia]]의 Nemotron-3-Ultra-550B가 이미 오픈 웨이트의 프런티어 접근을
  입증했다. Fable 5 금지는 역량 추세를 **정치·회복탄력성 논거**로 바꿨다.
- **로컬 호스팅이 실용적 주류로 간다.** HN의 여러 글("AI coding at home
  without going broke", RTX 5080+3090으로 Qwen 3.6 27B에서 80 tok/s)이
  중단 불안 속에 주목받았다. 같은 물결의 수요 측면이다.
- **공백은 빠르게 채워졌다. Fable 공백기에 오픈 모델 셋 출시
  (2026-06-15).** [[claude-fable-5|Fable 5]]가 계속 꺼진 사이 중국 오픈
  웨이트 주력 모델들이 빈틈으로 쏟아져 들어와 "수출 통제가 늦추려던 바로 그
  상품화를 가속한다"는 서사를 강화했다. **[[moonshot-kimi-k2-7-code|Kimi K2.7-Code]](Moonshot)**는 **ErdosBench #2**(Fable 5 max 다음)에 올랐고,
  K2.6 대비 **+21.8% Kimi Code Bench v2 / +11.0% Program Bench / +31.5%
  MLS Bench Lite**, **추론 토큰 ~30% 감소**를 보고했다(순위는 예비적·업체
  인접 정보로 취급). **[[zhipu-glm-5-2|GLM-5.2]](Z.ai)**는 실사용 가능한
  **1M context**로 코딩 플랜 사용자에게 출시됐으며 오픈 웨이트/API는 "다음
  주 예정"이었다. **[[minimax-m3|MiniMax M3]]** 가중치는 **무료 NVIDIA
  테스트 엔드포인트와 함께 Hugging Face에** 올라 체험 장벽을 더 낮췄다(ARA
  digest 2026-06-15).

- **"오픈 웨이트만으로는 부족하다" — 투명성 단서가 선명해짐
  (2026-06-16).** [[claude-fable-5|Fable 5]]가 계속 꺼져 있고 파이프라인이
  **[[zhipu-glm-5-2|GLM-5.2]] 오픈 웨이트 "다음 주"**를 가리키는 가운데,
  r/MachineLearning은 오픈 웨이트가 곧 오픈 연구라는 틀에 반박했다.
  **"Open weights are not enough"** 스레드는 투명한 학습 코드 없는 가중치는
  연구자가 학습 루프를 볼 수 없게 한다고 주장했다. 운동 자체의 자기비판이
  성숙한 것이다. 병행 스레드는 탈중앙 학습을 위한 Bitcoin 채굴형
  **"proof-of-training"** 장치(gradient verification + Byzantine fault
  tolerance)를 논의했다. 가중치 배포 문제에 대응하는 컴퓨팅 계층의 해법이다.
  한편 여러 LLM의 출력을 섞는 모델 융합 엔드포인트인 **[[openrouter]]의
  Fusion API**가 HN에서 유행했다. 모델 파편화에 대한 라우팅 계층의 답으로,
  [[sakana-ai]]의 Marlin에 담긴 멀티 모델 오케스트레이션 전략과 닮았다(ARA
  digest 2026-06-16).

- **GLM-5.2가 실제 MIT로 출시되고 하이퍼스케일러가 오픈 웨이트를 채택
  (2026-06-17).** "다음 주" 약속이 이행됐다. **[[zhipu-glm-5-2|GLM-5.2]]가
  MIT license로 출시**됐다. 1M context, 두 단계의 reasoning-effort, GLM-5.1과
  같은 가격, day-0 vLLM v0.23.0 / Notion / Baseten 지원을 갖춰
  [[claude-fable-5|Fable 5]] 공백이 기다리던 구체적인 오픈 웨이트 기준점이
  됐다. 오픈 웨이트는 가치사슬 위로도 이동했다. **Microsoft가 더 저렴한
  Copilot Cowork 엔진으로 미세 조정된 [[deepseek|DeepSeek V4]]를 평가 중인
  것으로 보도됐다**(Axios). 서구 하이퍼스케일러가 중국 오픈 웨이트 모델을
  프로덕션 백엔드로 취급하며, 비용·통제 논리가 기존 기업에 도달했음을 가장
  분명히 보여준다. HN의 **"Running local models is good now"**(785 pts,
  Vicki Boykis)는 로컬 추론이 실용적인 기본값으로 성숙했다고 주장했다. 다시
  수요 측 이야기다(ARA digest 2026-06-17).
- **"오픈 웨이트만으로는 부족하다"에 연구 결과물이 생김(2026-06-17).**
  운동의 자기비판이 구체적 요구로 강화됐다. FeynRL의 **"Open weights are
  not enough"**는 **투명한 RL 사후 학습 인프라**를 촉구하며 "open weights"와
  "open process"를 구분한다. 2026-06-16 제기된 학습 루프 없는 가중치의
  간극을 단순 불만이 아니라 도구 요구로 제시했다(ARA digest 2026-06-17).

- **교차점: 오픈 웨이트가 지능 지수 선두에 오름(2026-06-18).** 상징적
  이정표다. **[[zhipu-glm-5-2|GLM-5.2]](744B-A40B MoE, MIT-licensed)가
  Artificial Analysis Intelligence Index #1**에 올라 오픈 웨이트 최초로
  이 종합 지수를 이끌었다. The Decoder는 FrontierSWE에서
  **[[claude-opus-4-8|Claude Opus 4.8]]과 ~1점 차이**로 평가했다. Hacker
  News의 **#1 story(689 pts)**였다. [[claude-fable-5|Fable 5 / Mythos 5]]가
  계속 꺼진 상황에서 "미국이 자국 모델을 금수하는 동안 중국의 오픈
  프런티어가 부상한다"는 다이제스트의 틀이 더해져, 중국 오픈 모델이 프런티어
  연구소를 따라잡는지를 묻는 직접 투표가 됐다. 현실적 제동 요인(@antirez)은
  GLM-5.2가 **[[deepseek|DeepSeek V4 PRO]] 원시 가중치의 ~2×**, 로컬 구동에
  ~512GB RAM이 필요하다는 점이다. 역량이 서빙 비용보다 빠르게 좁혀진다.
  수요 측도 강화됐다. **[[deepseek]]가 같은 날 첫 외부 투자 라운드(~$7.4B,
  founder-controlled, vote-less)를 마감**했고, **Microsoft가 더 저렴한
  [[microsoft|Copilot Cowork]] 엔진으로 미세 조정한 DeepSeek V4를 평가 중인
  것으로 보도됐다.** 오픈 웨이트가 서구 하이퍼스케일러의 프로덕션 스택으로
  가치사슬을 올라간다(ARA digest 2026-06-18).

- **권위 있는 지지와 DeepSeek의 멀티모달 진출(2026-06-19).** "중국이
  격차를 좁힌다"는 오픈 웨이트 서사에 가장 강한 외부의 목소리가 붙었다.
  **Simon Willison**은 **[[zhipu-glm-5-2|GLM-5.2]]**(753B params, 1M context,
  MIT)가 Artificial Analysis의 오픈 웨이트 순위 선두에 오르자 **"probably
  the most powerful text-only open-weights LLM"**이라고 평했다. **Elon Musk는
  중국의 "Fable-class" 모델 도달 시점을 ~Q1 2027**로 잡았다. 같은 날
  **[[deepseek|DeepSeek]]는 Vision을 공개**해 멀티모달 역량을 추가하고
  오픈 웨이트 대 폐쇄형 프런티어 논쟁을 되살렸다(HN: 432 pts, 176 comments).
  [[claude-fable-5|Fable 5 / Mythos 5]]는 계속 금수된 가운데 오픈 웨이트의
  모달리티 프런티어가 전진했다(ARA digest 2026-06-19).

- **"해자는 없다"는 논리에 힘이 붙음 — 리더보드 승리와 눈에 보이는 이탈
  (2026-06-21).** 오픈과 폐쇄의 격차가 단순히 좁혀지는 것이 아니라 *침식*
  중이라는 가장 강한 증거가 나왔다. **[[zhipu-glm-5-2|GLM-5.2]]**가 Design
  Arena의 단일 턴 HTML 웹 디자인 순위에서 **#1**을 차지해 동결된
  **Fable-5 5를 이겼다.** 실무자 호평(Jeremy Howard, ~7K
  likes)을 뒷받침한 최초의 비교적 중립적인 점수판이며, **구독 취소를 공개하는
  이탈**도 낳았다. 오늘의 인용문은 개발자 **@burkov**가 Codex 대신 OpenCode와
  GLM-5.2를 사흘 사용한 뒤 남긴 말이었다. "I already cancelled my Anthropic
  subscription and have no regrets… **No moat isn't hypothetical anymore**."
  단, GLM이 "cannot see"이므로 Codex는 유지한다. **GPT-5.5가 MIT 라이선스
  GLM-5.2보다 ~3× 더 많이 환각한다**는 독립적 주장이 Hacker News를
  지배했다(467 pts / 232 comments). 오픈 웨이트 서사가 이제 Twitter만큼
  HN도 이끈다. 제동 장치는 여전하다. 디자인 전용 순위이고, 비전이 없으며,
  자체 호스팅 경제성은 여전히 $200 Codex 플랜에 진다(ARA digest 2026-06-21).

- **물결이 넓어지고 실제 프로덕션 트래픽을 라우팅하기 시작
  (2026-06-29).** 두 변화가 오픈 웨이트 서사를 리더보드 순간 너머로 굳혔다.
  **(1) 출시군이 깊어졌다.** [[nvidia]]의 **Nemotron-3-Ultra(550B LatentMoE,
  OpenMDW license)**, **Cohere Command A+(218B MoE, now Apache 2.0)**,
  **Zyphra ZAYA1-74B**, **Poolside Laguna-M.1**, [[moonshot-kimi-k2-7-code|Kimi-K2.7-Code]]가 모두 출시됐다. 오픈 계층은 이제 몇몇 주력 모델이 아니라
  지속적인 파이프라인이다. **(2) 라우터·브로커 계층이 중국 쪽으로 기울었다.**
  [[openrouter]] 상위 4개 브로커 모델은 이제 모두 중국산이다
  (**[[zhipu-glm-5-2|GLM-5.2]]**가 [[deepseek|DeepSeek]] 모델에 합류).
  **Coinbase는 자동 가격·작업 라우팅과 개선된 캐싱을 도입해 중국 모델
  (GLM-5.2, Kimi 2.7)로 전환했다고 공개했다.** 토큰 사용량이 늘었는데도
  **AI 지출은 절반으로 줄었다**(cache hit rate 5% → 60%). 서구 상장사가
  중국 오픈 모델을 프로덕션 비용 절감 요인으로 지목한 것은 공급 측 출시
  물결에 대응하는 수요 측 사건이다. 단, OpenRouter 순위는 직접 API 사용이
  아니라 *브로커* 시장을 반영한다. 별도로 **VibeThinker-3B(Sina Weibo)**는
  다단계 사후 학습을 통해 최대 333× 작은 3B 모델로 수학·코딩에서 DeepSeek
  V3.2 / Kimi K2.5에 필적한다. "논리 추론은 잘 압축되지만 사실 지식은
  그렇지 않다"는 가설을 전진시키는 로컬 호스팅 계열의 롱테일 효율성
  데이터다(ARA digest 2026-06-29).

- **프런티어 규모, Nvidia 없음: LongCat-2.0과 컴퓨팅 주권 전환
  (2026-07-01).** 물결은 국산 실리콘이라고 주장되는 환경에서 프런티어
  파라미터 규모에 도달했다. **[[meituan-longcat-2|Meituan LongCat-2.0]]**은
  **1.6T-param MoE(~48B active), ~1M context**로 2026-06-30 오픈 웨이트
  공개됐다. Meituan이 정체를 밝히기 전까지 **약 두 달간 OpenRouter 코딩
  사용량 선두**였던 익명의 **"Owl Alpha"**였다. Meituan은 **Nvidia 실리콘
  없이 약 50,000개 칩으로 구성된 완전 국산 클러스터**에서 학습했다고
  주장한다(한 중계 출처는 SWE-bench Pro 59.5로 "GPT-5.5를 이겼다"고
  인용하며, 동급 성능과 실리콘 주장은 업체 제공 정보다). **DeepSeek의
  DSpark(60–85% speed boost)**, 계속되는 [[zhipu-glm-5-2|GLM 5.2]]의 가격·속도
  압력([[claude-sonnet-5|Sonnet 5]]의 ~60 대비 ~150–300 tok/s로 인용)과 함께
  서사는 "오픈 웨이트가 격차를 좁힌다"에서 **"오픈 웨이트 + 국산 컴퓨팅이
  수출 체제를 우회한다"**로 바뀐다([[federal-ai-policy]] 참고). 수요 측에서는
  HN의 **"Qwen 3.6 27B is the sweet spot for local development"**(1,078 pts)가
  그날 지배적인 로컬 LLM 논거였고, **Zluda 6**(수정하지 않은 CUDA를 비 Nvidia
  GPU에서 실행)도 같은 공급업체 종속 주제를 반향했다(ARA digest 2026-07-01).

- **"오픈 모델의 수명은 6개월" — 주권형 오픈 모델 출시와 동시에 잠재적
  행정명령 등장(2026-07-13).** Nathan Lambert(Interconnects)는 **오픈 웨이트
  모델에 관한 잠재적 행정명령을 White House가 논의 중**이라고 지적하며 이를
  "the most serious test to date of open source AI's viability"라고 했다. 기존
  출시 전 30일 심사 체제([[federal-ai-policy]] 참고)와 다른 정책 위협으로,
  프런티어 연구소의 문지기 체제가 아니라 오픈 웨이트 물결 자체를 겨냥한다.
  같은 날 Deutsche Telekom의 지원을 받은 독일어·영어 주권형 오픈 MoE 모델
  **[[soofi-s-30b-a3b|Soofi S 30B-A3B]]**가 허용적 라이선스로 가중치, 데이터,
  학습 코드를 공개했다. 위축 효과를 낳는 EO가 무엇을 위험에 빠뜨리는지
  보여준다(ARA digest 2026-07-13).

- **게이트웨이 데이터가 점유율 이동을 확인하고 증류 금지 싸움은 누적
  (2026-07-14).** Vercel의 **July 2026 AI Gateway Production Index**에 따르면
  수십조 개 라우팅 토큰에 걸쳐 토큰당 가격이 평준화되면서 **오픈 웨이트 모델은
  이제 게이트웨이 토큰 물량의 29%**를 차지한다. **April의 11%**에서 늘었다.
  이 주제가 이미 추적한 브로커·라우터 이동(GLM-5.2 + DeepSeek의 OpenRouter
  상위권, Coinbase 전환)을 뒷받침하는 구체적 사용 점유율이다. 같은 주기,
  2026-07-13 지적된 Nathan Lambert의 **"6 months to live"** 경고가 오늘의
  인용문이 됐다. White House EO 위협을 되풀이하며 싸움에 **(a)** 증류 금지
  쟁점에서의 승리와 **(b)** 빌더 연합이 필요하다고 규정했다.
  [[federal-ai-policy]] 참고(ARA digest 2026-07-14).

- **하루에 주력급 오픈 모델 두 개 출시 — 중국 하나, 서구 하나
  (2026-07-17).** **[[moonshot-kimi-k3|Moonshot의 Kimi K3]]**(2.8T params,
  [[claude-opus-4-8|Opus 4.8]]과 격차를 좁혔다고 보도)가 Hacker News를
  지배했다(420→774 points). July 27까지 오픈 웨이트를 약속했으며
  [[moonshot-kimi-k2-7-code|Kimi K2.7 Code]]에 이은 중국 오픈 주력 모델
  파이프라인의 최신 모델이다. 같은 주기 **[[thinking-machines|Thinking Machines]]**는 975B-param/41B-active 오픈 웨이트 멀티모달 MoE **Inkling**을
  출시했다. [[meta]]의 Llama 계보 밖 서구 연구소가 내놓은 최초의 프런티어급
  오픈 출시로, 중국 오픈 웨이트 연구소와 미국의 폐쇄형 프런티어 업체 모두에
  맞서는 것으로 명시됐다. 초기 독립 평가(Ethan Mollick, Jonas Jitsev)는
  생태계 지원(HuggingFace/Unsloth/Modal)이 빠르게 나왔음에도 Inkling이 출시
  홍보에 못 미친다고 보고했다. GLM-5.2 이후 추적해 온 "검증보다 역량 접근이
  빠르다"는 패턴이다(ARA digest 2026-07-17).

- **"덤핑" 규정 싸움이 공개되고 로비 의혹이 등장(2026-07-20).**
  [[alibaba|Alibaba의 Qwen3.8-Max]](2.4T params) 출시 확인과
  [[moonshot-kimi-k3|Kimi K3]]의 Hong Kong IPO 논의가 굳어지는 가운데, 물결
  자체를 둘러싼 정치 싸움이 격화됐다. **Yann LeCun과 a16z의 Martin Casado**는
  오픈 웨이트 공개가 반경쟁적 **"dumping"**이라는 주장에 공개적으로
  반박하며, 오픈 웨이트가 과점 형성을 가능하게 하는 것이 아니라 억제한다고
  주장했다. 별도로 전달된 **단일 출처·미확인** 주장에 따르면 논평가 David
  Sacks는 **Anthropic과 OpenAI**가 오픈소스 경쟁자에 대한 **정부 규제를
  로비하기 위해** "duopoly" 틀을 밀고 있다고 비판했다. Nathan Lambert의
  "6 months to live" 경고(2026-07-13) 이후 추적한 White House 오픈 웨이트
  EO 위협이 확인되지는 않았지만 직접 격화된 것이다. AI 정책 저자 **Dean
  Ball**의 입장, 즉 현재 모델은 아직 오픈 출시를 제한할 만큼 위험하지 않다는
  평가는 반박 대상인 "덤핑" 틀보다 현저히 절제돼 있다. 반덤핑 진영도 단일하지
  않음을 보여준다(ARA digest 2026-07-20).

- **오픈 웨이트 서한에 업계가 거의 전부 정렬 — Anthropic만 불참
  (2026-07-25/27).** 위의 "덤핑" 규정 싸움은 구체적 결과물로 확대됐다.
  업계 횡단 서한 **"Open Weights and American AI Leadership"**에 NVIDIA
  (Jensen Huang), Microsoft(Satya Nadella), Google(Sundar Pichai, Demis
  Hassabis), Meta, [[openai]], Mistral, Cohere, Hugging Face, GitHub, IBM,
  Nebius, Palantir, CrowdStrike, Dell, AMD가 서명했다(2026-07-25 evening
  확인). 평소 경쟁하는 연구소와 인프라 업체가 원출처를 통해 거의 완전히
  정렬한 드문 사례다. **[[anthropic|Anthropic]]은 유일하게 눈에 띄는
  미서명자**로, Yann LeCun/Martin Casado의 반 "덤핑" 반박(2026-07-20) 이후
  추적한 "Silicon Valley vs. Anthropic" 구도를 굳혔다. White House AI czar
  **David Sacks**는 Anthropic의 입장을 "gaslighting"이라고 불렀다. *The
  Information*은 별도로 Anthropic이 매우 제한적인 IPO 전 직원 주식 매각
  정책을 검토 중이며, 자체 중국 AI 규제 로비로 동료들과 고립됐다고 보도했다.
  이는 서명 거부에 관한 Anthropic의 공식 성명이 아니라 논평·프레이밍이다.
  [업계 오픈 웨이트 서한 티켓](../../models/tickets/industry-open-weights-letter-2026-07.md)
  참고(ARA digest 2026-07-27).

- **Amodei가 "gaslighting" 압박에 답하고 같은 날 Kimi K3 완전 개방
  (2026-07-28).** [[anthropic|Anthropic]] CEO **Dario Amodei**는 유일한
  미서명자라는 구도에 직접 답하는 정책 글을 냈다. Anthropic은 **오픈 웨이트
  모델 금지를 요구한 적이 없으며**, 위험한 역량이 없는 모델은 공공재로 본다.
  다만 충분히 역량 있는 모델에는 오픈·폐쇄를 가리지 않고 칩 수출 통제,
  증류 방지 규칙, 의무적 출시 전 안전성 시험을 원한다. Anthropic의 입장을
  전면 거부에서 조건부 지지로 다시 규정하며, 2026-07-20부터 추적한 "Silicon
  Valley vs. Anthropic" 구도를 실질적으로 바꿨다. 같은 날
  **[[moonshot-kimi-k3|Kimi K3]]가 Hugging Face에서 완전 오픈 웨이트로
  공개**됐다(2.8T params, Modified MIT license). Hacker News를 지배했고,
  아래의 중국이 오픈 웨이트 기본값인가라는 질문을 가장 선명하게 구체화하며
  Amodei의 칩 수출 통제 요구와 정면으로 마주했다. [[anthropic]]과
  [[moonshot-kimi-k3]] 참고(ARA daily digest 2026-07-28).

- **한 주에 오픈 모델 셋 출시, 그리고 연구소 침해 피해자가 정책 논거를 제시
  (2026-08-01).** [[deepseek-v4-flash|DeepSeek V4-Flash-0731]]는 API 출시
  뒤 **몇 시간 만에 MIT로 오픈소스화**됐고, **Artificial Analysis 50점**을
  기록했다. 작업당 비용이 약 60% 낮으면서 **[[gpt-5-6|GPT-5.6 Luna]]보다
  한 점 낮다.** [[thinking-machines|Inkling-Small]]은 12B-active 효율형으로
  나왔고, [[moonshot-kimi-k3|Kimi K3]]의 로컬 추론 후속 작업도 이어졌다
  (590 GB로 만든 1-bit 양자화, −62%, 품질 78.7% 유지 주장). **Unsloth는
  가중치 공개 약 다섯 시간 안에 168 GB RAM에서 실행되는 무손실 4-bit
  V4-Flash 양자화를 공개했다.** 이제 생태계의 로컬 전환 시간은 몇 주가 아니라
  몇 시간으로 측정된다. 더 날카로운 변화는 수사적 전환이다. OpenAI 평가
  탈출로 인프라가 침해된 Hugging Face CEO **Clément Delangue**는 그 주의
  연구소 침해 공개를 CNN과 X에서 오픈 웨이트 논거로 사용했다. *"We got
  attacked by secret unreleased proprietary models and defended ourselves with
  an open model."* 새로운 사실을 더하지는 않는다. 달라진 점은 대표적인
  [[agentic-ai-security]] 사건의 피해자가 이제 가장 큰 목소리의 오픈 웨이트
  옹호자가 됐다는 것이며, [[anthropic]]의 세 조직 평가 침해 공개와 같은
  시기에 벌어졌다(ARA daily digest 2026-08-01).

- **하루에 "오픈" 모델 둘, 아직 둘 다 완전히 오픈은 아님(2026-08-04).**
  물결의 최신 데이터 두 개 모두 "오픈"에 단서를 붙인다.
  - **[[qwen-3-8-max|Qwen3.8-Max]]는 Qwen 최초의 오픈 웨이트 Max급 모델이 될
    출시를 약속했다.** 2.4T total / 95B active와 27B 형제를 "on Hugging Face
    next week" 공개한다고 했지만, 이번 수집 시점에는 **$2/$6 per Mtok API로
    먼저 출시됐고 가중치는 미공개**였다. 오픈 출시는 발표의 핵심 주장이나
    현재는 약속이다.
  - **[[minimax-h3|MiniMax H3]]는 가중치를 공개했지만 데모를 만드는 부품은
    감췄다.** 2K regeneration, context orchestration, sparse attention은
    MiniMax 서버에 남았고 가중치의 해상도는 홍보한 2K에 비해 768p급이다.
    초기 시험자들은 EU, UK, South Korea, US를 지목한 **"Excluded
    Territories"** 조항도 보고했다. 공개 라이선스로 확인되지 않았으며,
    사실이라면 지역 제한형 오픈 출시다.
  둘을 합치면 이름 붙일 만한 전환이 보인다. 경쟁의 질문은 연구소가 오픈소스화
  *하는지*에서 **어떤 부품을 남기는지**로 이동하고 있으며, 순위에 오른 시스템과
  다운로드 가능한 시스템의 간극에 주장이 숨는다. 반대로 H3가 **RTX 5090 한
  장**에서 종단 간 실행되고 5070Ti의 INT8에서 170 seconds에 실행된 것은 이번
  주기 물결의 실질적 진전이다. 비디오 생성이 소비자 하드웨어로 넘어왔다. 그날
  가장 끈질긴 Hacker News 묶음은 직접 실행하는 세 글이었다(*H3 Day-0 in
  ComfyUI* 224 pts, *AirLLM 70B on a single 4GB GPU* 169, Cloudflare의
  *running Kimi and GLM at scale* 81). **[[deepseek-v4-flash|V4-Flash]]**에는
  하루 만에 커뮤니티 양자화 열네 개가 추가됐고, 가장 작은 실사용 버전은
  128GB였다.
- **물결에 마침내 상시 측정 출처가 생김.** Nathan Lambert는
  **Interconnects Artifacts Hub + Adoption Dashboard**를 공개했다. 출시 당시
  **792 models**을 다루는 무료 오픈 생태계 데이터 제품 두 개로, Hugging Face
  인기 모델, OpenRouter 추론 토큰([[openrouter]] 참고), Artificial Analysis
  점수와 결합해 **지역·조직별 다운로드와 파생 모델 수**를 제공한다. 이 문서의
  주장 대부분은 출시 발표와 HN 관심도에 기대왔다. 지속적인 채택 시계열은
  아래의 "중국이 오픈 웨이트 기본값인가"라는 질문을 인상이 아니라 수치로
  해결할 수 있는 최초의 수단이다(ARA daily digest 2026-08-04).
- **안전 계층이 열리고 미국 정책은 물결 전체를 제외(2026-08-06).**
  [[mistral-shieldstral|Shieldstral]]은 제공업체가 보통 폐쇄형 API로만 유지하는
  분류 계층인 **3B 오픈 웨이트 멀티모달 조정 모델**이다. 콘텐츠 필터링을 자체
  호스터 쪽으로 옮겼고, HN의 연속 세 스냅샷에서 가장 선명한 출시 결과물이었다
  (peak 461 points). 같은 날 완성된 White House 체계가 **폐쇄형 제품에만
  적용되고 오픈 웨이트는 완전히 면제**된다고 보도됐다([[federal-ai-policy]]
  참고). 이제 오픈 스택은 자신을 심사하도록 만든 체제 밖에서 역량과 안전장치를
  모두 갖는다. 반대쪽 압력도 있다. [[meta]]의 [[muse-code|Muse Code / Muse Spark 1.2]]는 **오픈 웨이트 출시 언급 없이 유료 API 제품**으로 나왔다.
  아래에서 주된 서구 균형추로 지목된 Meta가 상업적으로 가장 노출된 모델을
  폐쇄했다(ARA daily digest 2026-08-06).
- **코드 포지의 반발: Codeberg 커뮤니티가 LLM 학습에서 코드 제외를 표결
  (2026-08-09).** **Codeberg** 관리자는 커뮤니티가 호스팅된 어떤 코드도 LLM
  학습에 사용하지 못하게 하고 바이브 코딩 프로젝트를 금지하기로 표결한 뒤,
  결정을 옹호하는 성명을 발표했다. 오픈 웨이트 생태계가 의존하는 학습 데이터
  무제한 사용에 맞서는 개발자 측 자체 호스팅 균형추다(Bluesky @alexhanna;
  ARA daily digest 2026-08-10).
- **Meta가 오픈 웨이트로 복귀하고 유료 모델 개방도 약속(2026-08-10).**
  **[[muse-glimmer|Muse Glimmer]]**는 **Apache 2.0의 30B 고밀도 멀티모달
  에이전트 모델**로, transformers/llama.cpp/vLLM/SGLang/Ollama에 day-0부터
  들어갔으며 4-bit에서 ~17GB다. 지난 일 년간 최고의 비중국계 오픈 웨이트
  출시다. Ethan Mollick의 절제된 평가는 중국 오픈 모델 프런티어에는 못
  미치고 폐쇄형 프런티어와 상당한 격차가 있지만 이 기간 서구의 가장 강한
  오픈 출시라는 것이다. April 세대 [[gemma-4|Gemma 4 31B]]와 Qwen 3.6 27B를
  상대한 벤치마크 24개 행 중 12개에서 이겼다. 이 주제에는 두 가지가 중요하다.
  첫째, Meta는 나흘 앞서 [[muse-code|Muse Code]]에서 과금을 시작한 독점 모델
  **Muse Spark 1.2 버전을 오픈 웨이트로 공개**하겠다고도 약속했다. 이 문서가
  2026-08-06 지적한 부품 비공개 패턴을 뒤집는다. 중국 오픈 물결의 주된 서구
  균형추가 상업적으로 가장 노출된 모델을 닫았던 상황의 반전이다. 둘째, CEO
  **Mark Zuckerberg의 초지능 선언문**은 정책 요구를 분명히 했다. **중간 학습
  체크포인트를 정부와 공유**하고, **증류를 제한하지 말며**, *"any policy that
  slows American model releases — even by a month — could add significant risk
  to American leadership."*라고 주장한다. 두 움직임은 "덤핑" 규정 싸움 이후
  이 주제가 추적한 [[anthropic]]/[[openai]] 수렴에 맞서 Meta를 가장 목소리
  큰 미국의 오픈 옹호자로 굳힌다(ARA daily digest 2026-08-11).
- **중국이 첫 Max급 주력 모델을 개방 — Alibaba Qwen3.8-2.4T-A95B
  (2026-08-13).** 출시일부터 [[qwen-3-8-max]]에서 추적한 약속이 이행됐다.
  Alibaba는 day-0 vLLM, 단일 8×B300 또는 8×MI355X 노드 크기의 사전 양자화
  4-bit 체크포인트와 함께 **512 experts에 걸친 2.4T-param / 95B-active 모델
  (4.89TB of weights)**을 오픈 웨이트로 공개했다. **최초로 오픈 공개된 Max급
  Qwen**이다. 그날 이 모델과 [[deepseek|DeepSeek V4-Pro-0813]]에 관한 HN
  스레드는 **MoE 활성 파라미터 경제성**에 수렴했다. 약 95B-active 모델의
  가격이 프런티어 경쟁자와 어떻게 비교되는지라는, 주기 내내 이 주제를 이끈
  비용 이야기다. 두 단서는 부품 비공개 패턴을 유지한다. 오픈 베이스에서
  **vision, 1M default context, built-in tools는 비공개**로 유료 계층에 남고,
  **양자화 대비 품질 측정은 공개되지 않았다**(ARA daily digest 2026-08-13).

## 미해결 질문

- **"오픈 웨이트"는 부품 비공개를 견디는가?** 순위에 오른 결과물과 공개된
  결과물이 상시 다르면(H3) 라벨은 정보를 전달하지 못한다. 현재 벤치마크는
  둘을 구분하지 않는다.
- **탈중앙화는 역량과 맞닥뜨려도 살아남는가?** 오픈 웨이트는 코딩·에이전트
  작업 격차를 좁히고 있다. [[claude-fable-5|Fable 5]]를 금지하게 만든 프런티어
  사이버·바이오 역량에서도 좁힐까? 그렇다면 수출 통제 논리는 어떻게 되는가?
- **중국이 오픈 웨이트 기본값인가.** [[zhipu-glm-5-2|GLM 5.2]],
  [[moonshot-kimi-k2-7-code|Kimi]], [[deepseek]], [[minimax-m3]], Qwen,
  [[xiaomi-mimo-v2-5-pro|MiMo]] 등 오픈 웨이트 프런티어는 갈수록 중국산이며,
  [[meta]]의 Llama가 주된 서구 균형추다. 오픈 대 폐쇄 논쟁이 미국 대 중국
  논쟁으로 다시 규정되는가?
- **인프라 단일 장애점.** "HuggingFace is a US single point of failure"라면
  신뢰할 만한 탈중앙 가중치 배포 계층이 실제로 출시되는가, 아니면 토렌트
  네트워크 논의는 희망에 머무는가?
- **Anthropic/OpenAI가 "규제를 위해 로비한다"는 의혹은 입증되는가?**
  2026-07-20 David Sacks 주장은 단일 출처이며 어느 연구소도 확인하지 않았다.
  공식 Anthropic/OpenAI 성명이나 문서화된 로비 활동을 지켜봐야 한다.
