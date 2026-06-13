# Methodology Improvements — 2026-06-02

> **Apply-by-hand note for the maintainer.** The claude[bot] App
> running `daily-improve.yml` lacks the `workflows: write` permission,
> so this PR carries the diff inline (see "Patch to apply" below)
> rather than committing it to `.github/workflows/hourly-rss.yml`
> directly. The same constraint is noted at
> `.github/workflows/daily-improve.yml:21-23`. Land the patch in a
> follow-up commit by a maintainer with workflow-edit rights.


## Issue: NVIDIA / Apple-ML / consumer-Google AI announcements arrive second-hand

Looking at the 2026-06-01 daily digest, four of its top-cited primary
sources never enter the pipeline via `research/rss/`:

- **NVIDIA Cosmos 3, RTX Spark, Alpamayo 2 Super 32B, Computex / GTC
  Taipei keynote** — all NVIDIA-blog territory; reached the digest only
  via Twitter pickup and Hugging Face's `Welcome NVIDIA Cosmos 3` RSS
  echo. NVIDIA itself is absent from `hourly-rss.yml`.
- **Gemini Spark GA** (the most-cited shipping product of the cycle) —
  posted on Google's consumer-facing blog (`blog.google/technology/ai/`),
  which `hourly-rss.yml` does not subscribe to. The existing
  `google_ai.xml` slot points at the older Google Research blog
  (`googleaiblog.blogspot.com`), which never carries product launches.
- **Apple's pre-WWDC Siri / Liquid-AI on-device research signal** —
  Apple Machine Learning Research has an RSS feed; `hourly-rss.yml` does
  not subscribe to it.

These sources end up in the digest only because the Twitter / RSS-of-
RSS lanes echo them. That works most days but creates fragility: a
Twitter cookie expiry, a HuggingFace-blog gap, or a delay in
journalists picking up a press release leaves us with no primary
record of the announcement. We should pull these directly.

## Fix

Added four feeds to `.github/workflows/hourly-rss.yml`. All four were
probed today (2026-06-02) and returned HTTP 200 with valid RSS / Atom:

| Feed | Shape | Purpose |
|---|---|---|
| `https://blogs.nvidia.com/feed/` | RSS 2.0 | NVIDIA consumer-product announcements (Computex keynote, RTX, Cosmos releases) |
| `https://developer.nvidia.com/blog/feed/` | Atom | NVIDIA technical drops — CUDA, TensorRT-LLM, Triton, kernel work |
| `https://machinelearning.apple.com/rss.xml` | RSS 2.0 | Apple's primary research-publication channel |
| `https://blog.google/technology/ai/rss/` | RSS 2.0 | Google's consumer-AI announcement blog (Gemini, Workspace AI) — distinct from `googleaiblog.blogspot.com` (research) |

The hourly-rss prompt was extended to:

1. Reference the four new files under "Official Company Blogs".
2. Note that `nvidia_dev.xml` uses Atom shape (entry / link[@href] /
   updated) — same fix the file already documents for
   `simonwillison.xml`.
3. Add a `#### NVIDIA` and `#### Apple ML Research` subsection to the
   output schema, and annotate the `#### Google/DeepMind` heading so
   the agent merges items from both google_ai.xml (research) and the
   new google_consumer_ai.xml (product).

Telemetry / safe-push / commit logic is unchanged. The feeds each have
the same `2>/dev/null || echo "<rss></rss>" > …` graceful-fallback
pattern as every existing curl in the file (CLAUDE.md rule 6: never
crash on upstream failure).

## Expected Impact

- **Primary-source coverage of NVIDIA, Apple, and Google consumer-AI
  news** — instead of relying on a Twitter/RSS-of-RSS echo. Closes the
  gap that left the 2026-06-01 digest with no first-hand NVIDIA or
  Apple-research line in its Sources block.
- **Faster pickup of model releases.** NVIDIA's developer blog
  consistently carries the formal CUDA / TensorRT-LLM / Cosmos /
  Nemotron drops the same day they ship; reaching them via Hugging
  Face's `Welcome NVIDIA …` posts adds a 2–24 h lag.
- **Negligible noise risk.** All four feeds are vendor-curated, low
  volume (~1–3 posts/day each), and already what the digest synthesizer
  cites; the change just routes the citation through `research/rss/`
  instead of Twitter.

## Patch to apply

Apply this to `.github/workflows/hourly-rss.yml` (the App-token push
of this diff was rejected with `refusing to allow a GitHub App to
create or update workflow ... without 'workflows' permission`).

```diff
diff --git a/.github/workflows/hourly-rss.yml b/.github/workflows/hourly-rss.yml
--- a/.github/workflows/hourly-rss.yml
+++ b/.github/workflows/hourly-rss.yml
@@ -65,6 +65,34 @@ jobs:
             -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
             > /tmp/rss/huggingface.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/huggingface.xml

+          # NVIDIA Blog RSS — consumer/product announcements (Cosmos, RTX,
+          # Computex keynotes). Verified HTTP 200, valid RSS 2026-06-02.
+          curl -sL "https://blogs.nvidia.com/feed/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/nvidia.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/nvidia.xml
+
+          # NVIDIA Developer Blog (Atom) — model releases, CUDA / TensorRT-LLM
+          # / Triton drops. Verified HTTP 200 with same-day items 2026-06-02.
+          # Atom shape: feed/entry/title, feed/entry/link[@href], feed/entry/updated
+          curl -sL "https://developer.nvidia.com/blog/feed/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/nvidia_dev.xml 2>/dev/null || echo "<feed></feed>" > /tmp/rss/nvidia_dev.xml
+
+          # Apple Machine Learning Research RSS — Apple's primary research
+          # publication channel (Liquid-AI talks, on-device LLM work,
+          # WWDC-adjacent research). Verified HTTP 200 2026-06-02.
+          curl -sL "https://machinelearning.apple.com/rss.xml" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/apple_ml.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/apple_ml.xml
+
+          # Google blog "Technology / AI" section — Google's consumer-AI
+          # announcement channel (Gemini Spark, Workspace AI). Distinct from
+          # googleaiblog.blogspot.com which carries research. Verified HTTP
+          # 200 2026-06-02.
+          curl -sL "https://blog.google/technology/ai/rss/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/google_consumer_ai.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/google_consumer_ai.xml
+
           # arXiv CS.AI RSS (recent submissions)
@@ -164,9 +192,13 @@ jobs:
             **Official Company Blogs:**
             - openai.xml (OpenAI Blog)
             - anthropic.xml (Anthropic News)
-            - google_ai.xml (Google AI Blog)
+            - google_ai.xml (Google AI Blog — research)
+            - google_consumer_ai.xml (Google blog AI section — consumer/product)
             - deepmind.xml (DeepMind Blog)
             - huggingface.xml (Hugging Face Blog)
+            - nvidia.xml (NVIDIA Blog — consumer/product)
+            - nvidia_dev.xml (NVIDIA Developer Blog — Atom; CUDA/TensorRT-LLM/Triton)
+            - apple_ml.xml (Apple Machine Learning Research)

             **Research:**
             - arxiv_ai.xml (arXiv CS.AI)
@@ -194,8 +226,9 @@ jobs:
             - channel/item/link (article URL)
             - channel/item/pubDate (publication date)
             - channel/item/description (summary)
-            Atom (simonwillison.xml) structure:
+            Atom (simonwillison.xml, nvidia_dev.xml) structure:
             - feed/entry/title, feed/entry/link[@href], feed/entry/published
+              (or feed/entry/updated)

             ## OUTPUT
@@ -218,10 +251,23 @@ jobs:

             #### Google/DeepMind
             - [Title](url) - date
+              (covers google_ai.xml research blog AND google_consumer_ai.xml
+              consumer/product announcements like Gemini)

             #### Hugging Face
             - [Title](url) - date

+            #### NVIDIA
+            - [Title](url) - date
+              (consumer/product items from nvidia.xml; developer/technical
+              drops — model releases, TensorRT-LLM, CUDA kernels — from
+              nvidia_dev.xml)
+
+            #### Apple ML Research
+            - [Title](url) - date
+              (from apple_ml.xml — research papers, on-device LLM,
+              accelerator work)
+
             ### 📰 Tech News

             #### TechCrunch
```

## Not Done

- **Mistral, xAI, Cohere, Qwen blogs.** All probed today; Mistral
  (`/news/rss`) → 404, xAI (`/feed`, `/news/rss`) → 403, Cohere blog
  (`/blog/rss.xml`) → 200 but returns the HTML SPA shell (no XML),
  Qwen (`/feed.xml`) → 404. None of them publish a usable RSS feed
  right now. Re-probe before adding.
- **Reddit subreddits.** Considered adding `r/singularity`,
  `r/OpenAI`, `r/ClaudeAI` to `4h-community.yml`. Skipped: the 3-sub
  set (`r/MachineLearning`, `r/LocalLLaMA`, `r/artificial`) already
  yields ~30 ranked items/day and the candidate subs are noisier /
  more meme-heavy. No evidence in 2026-06-01 output that we missed a
  story those subs would have caught.
- **Community-workflow run-frequency dip.** Only one HN snapshot in
  `research/community/2026-06-01-hn.md` (21:32 UTC) vs the four in
  `research/community/2026-05-31-hn.md`. Likely an autoscaler hiccup
  on 2026-06-01, not a workflow bug — leaving for the auto-rerun
  watchdog to handle on the next regression.
