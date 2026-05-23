# AI Industry Map

This note documents the working model from the Oracle run on 2026-05-23:
to understand the AI industry, study the stack that turns scarce inputs into
cognitive labor and then distributes that labor through products, workflows,
devices, and services.

The highest-explanatory-power variables are:

- Compute supply
- Model capability
- Inference economics
- Distribution
- Data and feedback loops
- Trust, security, and regulation
- Capital and geopolitics

## Core Mental Model

The AI industry is not only a model race. It is a value chain:

```text
electricity + chips + data + talent + capital
  -> compute infrastructure
  -> model production
  -> model serving and middleware
  -> applications and workflow automation
  -> productivity gains, new products, and labor substitution
```

The upstream layers explain who can build. The downstream layers explain who
gets paid.

## Areas To Understand

| Priority | Area | What to understand | Why it matters |
|---:|---|---|---|
| 1 | Compute economics | Training vs. inference, GPUs/TPUs, HBM, networking, utilization, cost per task | Compute constrains capability, margins, and speed of execution. |
| 2 | Chips and datacenters | Nvidia, AMD, custom ASICs, TSMC, HBM, advanced packaging, cloud capacity, power, cooling, grid access | AI is increasingly constrained by physical infrastructure, not just software. |
| 3 | Foundation models | Transformers, multimodal models, diffusion, post-training, RLHF/RLAIF, reasoning models, evaluations | This explains what models can and cannot do. |
| 4 | Inference and productization | Latency, routing, caching, distillation, quantization, RAG, tool use, agents, observability | Most commercial success depends on serving useful outputs reliably and cheaply. |
| 5 | Distribution and workflow ownership | Microsoft, Google, Apple, Meta, Amazon, Salesforce, Adobe, ServiceNow, vertical SaaS, consumer apps | Value often accrues to whoever owns the user, workflow, procurement channel, or system of record. |
| 6 | Data and feedback loops | Public data, licensed data, proprietary enterprise data, synthetic data, human feedback, telemetry, privacy | Durable advantage increasingly comes from task-specific data, evals, and usage feedback. |
| 7 | Open vs. closed models | Frontier APIs, open weights, local deployment, edge deployment, sovereign AI, commoditization pressure | Open models lower costs and spread capability; closed labs may retain advantages in scale, reliability, safety, and distribution. |
| 8 | Enterprise adoption economics | ROI, procurement, security review, workflow redesign, integration cost, liability | Deployment is limited by organizational change and measurable value, not only model quality. |
| 9 | Safety, security, and governance | Hallucination, misuse, privacy, copyright, cyber risk, evaluations, audits, incident response | Trust and regulation determine where AI can be deployed. |
| 10 | Geopolitics and capital flows | U.S.-China competition, export controls, national AI strategies, talent flows, sovereign compute | AI is strategic infrastructure. Capital, chips, energy, and talent are national-competition variables. |

## Economic Layers

1. Natural and financial inputs: electricity, land, water, grid access, permits,
   capital, and talent.
2. Chip supply chain: accelerators, HBM, EDA, foundries, advanced packaging,
   and networking.
3. Compute infrastructure: hyperscale clouds, neoclouds, colocation, and
   datacenter operators.
4. Model production: frontier labs, open-model labs, pretraining,
   post-training, safety, and evaluation.
5. Model serving and middleware: APIs, inference optimization, vector
   databases, orchestration, agents, monitoring, and security.
6. Applications: coding, office productivity, search, creative tools, customer
   support, education, legal, healthcare, finance, industrial AI, and robotics.
7. Integration and services: consulting, systems integration, data labeling,
   human-in-the-loop review, compliance, and AI operations.
8. Real-economy capture: productivity gains, labor substitution, cheaper
   software, automated services, and better decision systems.

## Main Bottlenecks

- Power and grid access: datacenters need large, reliable, permitted power.
- Advanced chips: accelerators, HBM, packaging, and networking determine who
  can train and serve competitive models.
- Capital expenditure: frontier AI increasingly looks like software plus
  industrial infrastructure.
- Inference unit economics: the key question is whether a model can produce
  valuable output at acceptable cost, latency, and reliability.
- Reliable agents: production agents need evaluation, permissions, recovery,
  auditability, and security controls.
- High-quality domain data: the valuable data is often proprietary, regulated,
  messy, or locked inside enterprise systems.
- Distribution: models are easier to copy than customer relationships,
  contracts, installed workflows, and platform control.
- Trust and compliance: enterprises need privacy, access control, audit logs,
  indemnity, and predictable behavior.
- Talent and organizational change: firms need researchers, infrastructure
  engineers, product engineers, and AI-capable operators.
- Regulatory clarity and IP: copyright, data provenance, safety obligations,
  liability, and model transparency shape what can be built and sold.

## Minimum Learning Path

1. Basic ML and deep learning: supervised learning, neural networks,
   transformers, embeddings, diffusion, and reinforcement learning.
2. Modern model lifecycle: pretraining, post-training, alignment, evaluation,
   deployment, and monitoring.
3. Compute stack: GPUs/TPUs, HBM, networking, datacenters, cloud pricing,
   training economics, and inference economics.
4. Product stack: APIs, RAG, agents, tool use, evals, latency, reliability,
   security, and workflow integration.
5. Market structure: frontier labs, hyperscalers, chip companies, open-source
   labs, SaaS incumbents, vertical AI startups, and systems integrators.
6. Business models: API pricing, subscriptions, usage-based SaaS, compute
   resale, enterprise licenses, automation services, and data products.
7. Adoption economics: where AI saves time, where it creates new work, where it
   fails, and how companies measure ROI.
8. Governance and geopolitics: AI Act, NIST AI RMF, export controls, privacy
   law, copyright, model safety, and national compute strategies.
9. Sector deep dives: coding, customer support, search, advertising, finance,
   healthcare, education, defense, manufacturing, and robotics.
10. Weekly primary signals: model releases, benchmark shifts, chip supply,
    cloud capex, power constraints, regulation, and enterprise case studies.

## Questions That Explain The Industry

- Who controls compute?
- Who controls distribution?
- Who owns the data?
- Who can serve inference cheaply?
- Who can make AI reliable inside real workflows?
- Who bears legal and operational risk?
- Who captures the productivity gains?

This question set is more useful than tracking every model leaderboard change.

## Primary References

- [Stanford HAI AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report)
- [Epoch AI Trends](https://epoch.ai/trends)
- [IEA Energy and AI](https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai)
- [EU guidelines for general-purpose AI model providers](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)
