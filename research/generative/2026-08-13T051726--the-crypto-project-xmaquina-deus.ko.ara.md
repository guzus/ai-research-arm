---
eyebrow: 프로젝트 프로필 · 암호화폐 × 피지컬 AI · 2026-05-16
title: 'XMAQUINA: TGE 11일 전, 휴머노이드 로봇 기업에 대한 토큰화 익스포저'
deck: 비상장 로봇 기업 지분을 분할해 판매하고 veToken 보유자가 거버넌스를 맡는 Base 기반 DAO. 출시 가격은 아직 공개되지 않았다.
lede: XMAQUINA는 휴머노이드 로봇 스타트업의 지분을 매입하고 Base에 배포된 ERC-20인 **$DEUS**를 통해 해당 포지션의 거버넌스를 수행하는 DAO다. 토큰은 2026년 오월 12일 온체인에 배포됐으며, 토큰 생성 이벤트는 오늘로부터 열하루 뒤인 **2026년 오월 27일**로 예정돼 있다. TGE 전 현재 컨트랙트 보유자는 1,044명, DEX 유동성은 약 $110이며 공개된 포트폴리오 포지션은 Apptronik 하나다. 제안 자체는 실재하지만 법적 구조에는 물음표가 붙고, 오월 27일 판매될 대상의 대부분은 아직 포부에 머문다. 현재 배포된 유일한 지분 배분은 Snapshot 투표로 승인된 단일 지분이다.
stats:
- label: 최대 공급량
  value: '1'
  unit: B
  note: '오늘 Base에서 874.1M 발행'
- label: 조달 자본
  value: $10
  unit: M+
  note: 여러 차수에 걸친 약 2,000명의 기여자
- label: 온체인 보유자
  value: '1,044'
  note: Base 메인넷 · 2026-05-16
- label: TGE
  value: 오월 27일
  note: '사전판매 DEUS 110M 잠금 해제'
---

## 01. 실제로 무엇을 사는가

[xmaquina.io](https://www.xmaquina.io/)의 공식 설명은 DEUS 보유자가 "DEUS 보유자의 거버넌스를 받는 세계 선도 로봇 기업의 트레저리"에 익스포저를 얻는다는 것이다. 구체적으로 DAO는 기여자 자본으로 비상장 로봇 기업의 IPO 전 지분을 취득하고, DEUS를 스테이킹해 발행하는 투표예치 토큰(xDEUS)을 통해 해당 포지션의 거버넌스를 수행한다. 향후 회수금과 매출이 DAO로 돌아오면 투표로 지분 취득, DEUS 바이백, 스테이킹 보상 가운데 용도를 정한다는 구상이다.

DAO는 목표 시장을 네 가지 분야로 공개 분류한다.

| 분야 | 매입 대상 | 명시된 후보 |
|---|---|---|
| 휴머노이드 기업 | 로봇 제조사의 IPO 전 지분 | Apptronik, 1X, Agility, Figure AI |
| 피지컬 AI 스택 | 액추에이터, 센서, 칩, 인프라 | 공개되지 않음 |
| 로봇 프로토콜 | 초기 Web3 로봇 프로젝트 | 공개되지 않음 |
| 휴머노이드 AI | 지능 레이어·VLA 모델 | Neura Robotics |

이 가운데 DAO 투표로 실제 승인된 기업은 **Apptronik** 한 곳뿐이다. "BOT-1"은 **98.05%** 지지로 통과했으며 투표는 `snapshot.xmaquina.io`에서 진행됐다. 홈페이지의 다른 모든 기업은 현재 보유 종목이 아니라 목표다. 프로젝트는 Apptronik 포지션이 취득 후 100% 넘게 상승했다고 주장한다. 이 수치는 원자료로 독립 검증할 수 없으므로 시장가격으로 평가된 수치가 아니라 프로젝트 측 주장으로 봐야 한다.

:::callout(kind=warn, label="\"익스포저\"의 법적 의미")
미국 비상장 지분에 대한 익스포저를 토큰화하는 행위는 XMAQUINA 보유자가 거주하는 대부분의 관할권에서 규제 대상이다. 사이트는 DEUS를 기초 지분에 대한 청구권이 아니라 거버넌스 토큰이라고 신중하게 부른다. 백서에는 회수금을 지분율에 따라 배분한다는 약속이 없고, 거버넌스가 유입 자금을 "DEUS 바이백과 스테이킹 보상"에 쓸 수 있다는 내용만 있다. 비상장 증권 포트폴리오를 추종하는 토큰을 미국 보유자가 합법적으로 살 수 있는지가 이 상품의 성립을 좌우하는 미해결 문제다.
:::

## 02. 토큰

DEUS는 Base의 `0x940A319B75861014A220D9c6c144d108552B089B`에 배포된 ERC-20이다. Solidity 0.8.28, MIT 라이선스를 사용하며 Basescan에서 소스가 검증됐다. 컨트랙트에는 짚고 넘어갈 세 가지 비기본 동작이 묶여 있다.

- **LayerZero OFT** — 옴니체인 전송 기능으로, 같은 토큰을 Base, Solana, peaq(CoinGecko가 명시한 세 체인) 사이에서 이동할 수 있다.
- **ERC-5805 투표·위임** — 위임을 지원하는 온체인 투표 잔액으로, 표준 veToken 기반 구조다.
- **소유자 제한 전송 플래그와 자식 토큰 보호 장치** — 컨트랙트 차원에서 전송을 일시정지할 수 있으며, 단방향 "자식으로 표시" 호출로 추가 발행을 영구 차단할 수 있다.

배분은 [docs.xmaquina.io](https://docs.xmaquina.io/dao/tokenomics)에 다음과 같이 제시돼 있다.

:::bars
- label: DAO 트레저리
  value: '30.00%'
  pct: 30
- label: 제네시스 경매
  value: '23.24%'
  pct: 23
- label: 핵심 기여자
  value: '12.50%'
  pct: 13
- label: 유동성·생태계
  value: '8.26%'
  pct: 8
- label: 전략적 기여자
  value: '8.00%'
  pct: 8
- label: DEUS 개발 랩
  value: '7.50%'
  pct: 8
- label: 재단
  value: '7.50%'
  pct: 8
- label: RCM 프로토콜
  value: '2.00%'
  pct: 2
- label: 어드바이저
  value: '1.00%'
  pct: 1
:::

교차 자료에서 두 가지를 짚을 수 있다. 첫째, Impossible Finance의 리서치 보고서는 현재 문서 페이지와 일치하지 않는 다소 다른 배분(Genesis 30%, Liquidity 3.5%)을 인용한다. 문서가 더 최근의 권위 있는 버전으로 추정된다. 둘째, 현재 컨트랙트의 온체인 "최대 총공급량"은 명시된 상한 **1,000,000,000**에 비해 **874,148,340**이다. 약 125.8M의 차이는 아직 발행되지 않은 배분(TGE에 예정된 사전판매 110M 블록과 생태계 준비금)과 부합한다.

오월 27일 TGE 거버넌스 제안은 이벤트에 공급량의 12.8%인 **128,067,280 DEUS**와 **$150,000 USDC**를 배정했다. 최종 커뮤니티 사전판매에 110M, 유동성 부트스트래핑에 약 18M과 스테이블코인을 쓴다. 약 19M표가 행사된 투표에서 96% 찬성으로 통과됐다.

## 03. 문서와 온체인의 거버넌스

xDEUS veToken 모델은 이제 표준이 된 Curve·Aerodrome 방식을 따른다. DEUS를 스테이킹해 양도 불가능한 투표예치 포지션을 발행하고, 잠금 기간에 비례하는 투표권을 얻는다. 운영상 제안은 Snapshot(오프체인 의사 표시)과 Aragon OSx(온체인 실행)에서 모이며, "거버넌스가 승인한 멀티시그"가 운영 결제를 처리한다.

거버넌스 문서 페이지에는 정족수 기준, 제안 제출 기준, 투표 기간이 공개돼 있지 않다. 이 메커니즘은 사람이 읽을 수 있는 형태가 아니라 Aragon OSx 설정에 들어 있다. 현재 DAO Portal에서 한 실행 경로를 표본 확인할 수 있지만, 외부 관찰자는 온체인 컨트랙트를 읽지 않고는 매개변수를 재현할 수 없다. 스테이킹 전에 공개적으로 요구할 가치가 있다.

:::callout(kind=danger, label="검증해야 할 중앙화 지점")
토큰을 자유롭게 전송할 수 있게 되기 전에 세 가지 컨트랙트 동작을 주시해야 한다. 소유자가 제어하는 전송 플래그(현재는 꺼져 있지만 소유자가 변경 가능), Basescan 검증 소스에 첨부된 보안 감사 부재, 운영 결제를 통제하는 멀티시그 서명자 집합이다. 어느 것도 반드시 탈락 사유는 아니다. 대부분의 veToken 시스템이 출시 기간에 비슷한 지점을 갖는다. 하지만 권한을 포기하거나 공식 감사를 받기 전까지 각각은 단일 장애점이다.
:::

## 04. 주도자와 자금 제공자

:::kv
- term: CEO·공동창업자
  def: Mauricio Zolliker — 전 peaq 성장·사업개발 책임자
- term: CMO
  def: Jessica Alvarez — 마케팅·커뮤니케이션 경력 10년 이상
- term: 팀 규모
  def: '정규직 7명, 시간제 두 명(Impossible Finance 리서치, mid-2025 기준)'
- term: 주요 어드바이저
  def: Michael Ganser(전 Cisco SVP), Simon Dedic(Moonrock Capital 공동창업자), Anil Lulla(Delphi Digital 공동창업자)
- term: 공개된 기관 투자자
  def: Borderless Capital, Moonrock, MH Ventures, Generative Ventures, Fundamental Labs, Waterdrip, vVv, Clairvoyant Labs, Signal Ventures, Wise3 Ventures, Mulana, EoT Ventures, CoinIX, Advanced Blockchain
- term: 여러 차수의 총 조달액
  def: 약 2,000명의 기여자로부터 $10M+
- term: 본사
  def: 스페인(The AI Insider의 2026년 일월 $10M 조달 보도 기준)
:::

투자자 구성에서 두 가지 결론을 얻을 수 있다. 투자자는 실리콘밸리 딥테크 VC보다 아시아·EU의 암호화폐 전문 펀드군(Moonrock, MH, Waterdrip, KuCoin Ventures 파트너)에 몰려 있다. 토큰 출시에는 자연스럽지만, 향후 회수 경로가 미국 로봇 기업 M&A를 거친다면 유의할 점이다. 반면 엔젤 명단은 무게감이 있다. 전 Cisco SVP, Delphi 공동창업자, Moonrock 창업자가 모두 합쳐 공급량 약 1%의 어드바이저 티어에 있다는 점은 허울뿐인 배치보다 실제 확신을 시사한다.

## 05. 타임라인

:::timeline
- date: '2024 Q4'
  headline: 프리시드 마감.
  body: Impossible Finance 기준 추정 FDV $20–25M. Advanced Blockchain AG가 전략적 투자자로 명시됨.
- date: '2025-08'
  headline: 플랫폼 가동.
  body: XMAQUINA.io 출시, 제네시스 경매 시작(Impossible Finance 기준 Wave 1 FDV 약 $37M, 이후 차수는 $40M과 $45M으로 상승).
- date: '2025-Q4'
  headline: BOT-1 통과.
  body: '첫 온체인 거버넌스 투표: Apptronik 전략적 배분, Snapshot에서 98.05% 찬성.'
- date: '2026-01'
  headline: $10M 조달 이정표.
  body: 누적 경매 수익이 천만 달러를 넘어섬. DAO는 "지분 확보를 계속할 자본을 완전히 갖췄다"고 선언.
- date: '2026-05-12'
  headline: Base에서 DEUS 컨트랙트 가동.
  body: 제네시스 경매 참여자 청구 시작(33% 즉시 지급, 67%는 12개월 선형 베스팅).
- date: '2026-05-27'
  headline: TGE 예정.
  body: '최종 커뮤니티 사전판매 DEUS 110M, 유동성 부트스트랩에 약 18M + $150K USDC. 전송 활성화 예상.'
:::

## 06. 가격에 반영해야 할 위험

이런 유형의 상품, 즉 미국 비상장 지분에 대한 토큰화 익스포저를 보유한 DAO는 암호화폐에서 법적 위험이 가장 큰 영역에 있다. 보유자에게 미칠 피해가 큰 순서로 대략 정리하면 다음과 같다.

1. **증권 분류.** SEC나 그에 상응하는 EU 규제기관이 DEUS를 기초 포트폴리오에 대한 증권성 청구권으로 분류하면 이차 거래와 거래소 상장은 무너진다. 프로젝트의 방어 논리는 DEUS가 수익분배가 아닌 거버넌스 토큰이라는 것이다. 방어 가능하지만 검증되지는 않았다.
2. **현재의 단일 자산 집중.** 트레저리에서 공개된 지분 포지션은 현재 Apptronik 하나이며, 나머지는 스테이블코인과 구체적으로 공개되지 않은 암호화폐다. "다각화된 휴머노이드 로봇 익스포저"가 제안이라면, "비상장 지분 하나와 낙관론"이 현재 현실이다.
3. **감사 보장 없는 스마트 컨트랙트 위험.** Basescan에는 검증된 소스에 대해 제출된 감사 보고서가 표시되지 않는다. 컨트랙트는 짧고 OpenZeppelin 패턴을 따르지만, DAO가 배분하는 $10M+ 자본을 담을 토큰에 이런 공백이 있는 것은 이례적이다.
4. **소유자가 변경할 수 있는 전송 플래그.** 소유자 권한을 포기하거나 DAO 자체 멀티시그로 이전하기 전까지 배포자는 원칙상 전송을 다시 일시정지할 수 있다. 현재 소유자가 누구인지 추적할 가치가 있다.
5. **Apptronik 시가평가는 프로젝트 주장.** Apptronik 익스포저가 "몇 달 만에 +100%" 올랐다는 수치는 독립 자료가 없다. 비상장 지분 가치평가는 본질적으로 유동성 없는 평가액이다. 손익이 아니라 마케팅 수치로 봐야 한다.
6. **TGE 전 유동성이 얕다.** 현재 DEX 풀은 약 $110다. 자유 전송 첫 주에는 거친 가격 발견을 예상해야 한다.

## 07. 실행하기 전에 직접 검증할 것

오월 27일 사전판매나 TGE 이후 2차 시장 참여를 고려한다면 믿음에 맡기지 말고 직접 확인할 항목은 다음과 같다.

- 사전판매 가격과 지갑당 한도. 현재 가져올 수 있었던 자료에는 아직 공개되지 않았으며, TGE 전 주의 최종 블로그 글에 나올 가능성이 있다.
- 멀티시그 서명자 집합과 컨트랙트 소유권이 배포자 EOA에서 이전됐는지 여부. Basescan의 컨트랙트에서 직접 확인한다.
- Apptronik 배분의 달러 규모와 DAO의 실제 신고 지분. [dao.xmaquina.io](https://dao.xmaquina.io/)의 DAO Portal에 이제 표시돼야 한다.
- 스테이킹 전 xDEUS 잠금 조건. 최소 잠금 기간, 잠금 기간에 따른 투표권 기울기다. 이 메커니즘은 문서 페이지가 아니라 Aragon OSx 설정에 있다.
- 지금부터 TGE 사이에 게시되는 감사. 이 정도 트레저리 규모의 토큰이 감사 없이 출시된다면 의미 있는 부정적 신호다.

논지는 일관된다. 휴머노이드 로봇 비상장 지분은 접근하기 어렵고, 로봇 역량은 빠르게 복리 성장하며, 토큰화 DAO 구조는 그 접근성 격차를 메울 수 있는 상품이다. DEUS가 법률, 거버넌스, 유동성 기준을 실제로 넘는지는 앞으로 육십 일 안에 판가름 난다.

---

## 08. 출처

1. [xmaquina.io](https://www.xmaquina.io/) — 공식 홈페이지, 분야, 명시된 후보.
2. [DEUS 토큰 페이지](https://www.xmaquina.io/deus-token)와 [로봇 토큰 페이지](https://www.xmaquina.io/robotics-token) — 토큰 효용 설명.
3. [docs.xmaquina.io/dao/tokenomics](https://docs.xmaquina.io/dao/tokenomics) — 공식 배분표.
4. [docs.xmaquina.io/dao/governance](https://docs.xmaquina.io/dao/governance) — xDEUS·Aragon OSx 모델.
5. [Basescan 컨트랙트](https://basescan.org/token/0x940A319B75861014A220D9c6c144d108552B089B) — 공급량, 보유자, 검증된 소스, 감사 부재.
6. [XMAQUINA 청구 가이드](https://www.xmaquina.io/blog/how-to-claim-your-deus-tokens) — 33% 즉시 지급·12개월 베스팅.
7. [XMAQUINA 블로그: DAO의 다음 단계](https://www.xmaquina.io/blog/the-next-steps-for-the-dao) — Wave 1.5 수치, 거버넌스 준비 상태.
8. [XMAQUINA 블로그: $10M 조달](https://www.xmaquina.io/blog/10m-raised-to-reclaim-the-robotics-capital-markets) — 공개된 기관 투자자와 엔젤.
9. [XMAQUINA 블로그: DAO Portal](https://www.xmaquina.io/blog/introducing-the-xmaquina-dao-portal) — Apptronik BOT-1, 98.05% 찬성으로 통과.
10. [Impossible Finance 리서치 보고서](https://blog.impossible.finance/xmaquina-research-report/) — 팀 이력, 프리시드 FDV, 대체 배분표.
11. [Phemex: TGE 승인](https://phemex.com/news/article/xmaquina-approves-deus-token-generation-event-with-110-million-deus-for-presale-42899) — 투표 수, DEUS 128M + USDC $150K 배분.
12. [TradingView·CoinMarketCal](https://www.tradingview.com/news/coinmarketcal:c0cabbee9094b:0-xmaquina-deus-tge-27-may-2026/) — TGE 날짜 2026-05-27.
13. [BlockchainReporter](https://blockchainreporter.net/xmaquina-launches-deus-token-on-base-blockchain-expanding-web3-robot-investment-opportunities-on-chain/) — 2026-05-12 Base 출시.
14. [The AI Insider](https://theaiinsider.tech/2026/01/15/spain-based-dao-xmaquina-raises-10m-for-early-stage-robotics-investments/) — 스페인 본사, $10M 조달 보도.
15. [CoinGecko](https://www.coingecko.com/en/coins/xmaquina) — 현재 유동성(약 $110), 명시된 체인(Base, Solana, peaq).
