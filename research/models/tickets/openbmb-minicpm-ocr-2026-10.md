---
slug: openbmb-minicpm-ocr-2026-10
title: "OpenBMB open-sources MiniCPM-OCR 1.0 and the MiniCPM-OCR Jev verifier"
company: "OpenBMB"
model: "MiniCPM-OCR 1.0 / MiniCPM-OCR Jev"
status: released
status_note: |
  **Open-source release, reported 2026-10-28.** Per @AINativeF (13:16 UTC): the MiniCPM-OCR suite has
  two models. MiniCPM-OCR 1.0 is a ~1B model with claimed SOTA OCR speed and accuracy (93.68 on
  Real5-OmniDocBench, 54.7 on OCRBench v2). MiniCPM-OCR Jev is a 2B model-agnostic verifier that checks
  text, formulas and tables in OCR output (93.6 on JevOCRBench). With the DSpark SDK the suite processes
  up to 128 pages/minute, with day-0 support on Arm, Intel, NVIDIA, Houmo AI and others via FlagOS.

  A Chinese relay (@xiaoanlab) says it was open-sourced "today" and gives the OCR model as **1.3B**.
  The 1B vs 1.3B size is unresolved.

  **Verification `partial`:** two secondary relays; no @OpenBMB post or Hugging Face URL captured.
expected: "Open-sourced 2026-10-28 per relays. Open: OpenBMB post / HF card, licence, the exact parameter count (1B vs 1.3B)."
labels:
  - open-weights
  - ocr
  - document-ai
  - small-model
verification: partial
sources:
  - "https://x.com/AINativeF/status/2115432525992779910"
  - "https://x.com/xiaoanlab/status/2115432164829671614"
created_at: 2026-10-28
updated_at: 2026-10-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-28
    change: "Created — RELEASED / partial. Two relays report OpenBMB open-sourced MiniCPM-OCR 1.0 (~1B; one relay says 1.3B) and a 2B MiniCPM-OCR Jev verifier for OCR output, with self-reported SOTA on Real5-OmniDocBench and OCRBench v2, plus a DSpark SDK at up to 128 pages/min."
---
Separate artifact from [[openbmb-minicpm-v-4-7-2026-10]], the general vision-language model.

The interesting part is the verifier. A small model that flags suspect spans in OCR output targets
the real failure mode of document pipelines: confident but wrong text. All benchmark numbers are
OpenBMB's own.
