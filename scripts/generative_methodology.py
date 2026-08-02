"""Schema checks for generative-research methodology sidecars.

The article validator can prove the generated HTML is safe and well-formed,
but it cannot prove that the research process ran. These checks validate the
sidecar artifacts required by the generative-research workflow before publish:

* claim ledger: source-tiered claims gathered before prose
* verifier findings: claim-level support/weak/unsupported judgments
* red-team findings: adversarial falsification attempts for top claims
"""

from __future__ import annotations

import json
from pathlib import Path

# `derived` is the ONE claim type whose support is arithmetic rather than
# retrieval, so it is the one type exempt from the source_urls/source_tiers
# requirement. Its support is proven instead by
# check_generative_research.py --audit-derived-claims, which recomputes
# `formula` over `inputs` and compares against `result`.
DERIVED_CLAIM_TYPE = "derived"
# Keys that only a derivation carries. Their presence is what makes an
# entry structurally derived, independent of the `type` string an author
# wrote — see the relabel check in validate_claim_ledger().
DERIVATION_KEYS = ("inputs", "formula", "result")
RETRIEVAL_CLAIM_TYPES = frozenset({
    "metric",
    "event",
    "quote",
    "definition",
    "comparison",
    "causal",
    "forecast",
    "regulatory",
    "market-structure",
    "technical",
    "other",
})
ALLOWED_CLAIM_TYPES = RETRIEVAL_CLAIM_TYPES | {DERIVED_CLAIM_TYPE}
ALLOWED_SOURCE_TIERS = frozenset({
    "primary",
    "secondary",
    "market-data",
    "opinion",
    "academic",
    "legal",
    "unknown",
})
ALLOWED_CONFIDENCE = frozenset({"high", "medium", "low"})
ALLOWED_RISK = frozenset({"stable", "volatile", "contested", "single-source"})
ALLOWED_VERDICTS = frozenset({"supported", "weak", "unsupported"})
ALLOWED_REDTEAM_SEVERITY = frozenset({"high", "medium", "low"})
VOLATILE_CLAIM_TYPES = frozenset({"metric", "forecast", "comparison"})
VOLATILE_RISKS = frozenset({"volatile", "contested"})


def _load_json_object(path: Path, label: str) -> tuple[dict | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return None, [f"methodology: {label} JSON is unreadable or malformed: {e}"]
    if not isinstance(data, dict):
        return None, [f"methodology: {label} JSON must be an object, got {type(data).__name__}"]
    return data, []


def validate_claim_ledger(path: Path) -> list[str]:
    data, errors = _load_json_object(path, "claim ledger")
    if errors:
        return errors
    assert data is not None
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        return ["methodology: claim ledger must contain a non-empty top-level claims[] array"]

    seen_ids: set[str] = set()
    for i, claim in enumerate(claims, start=1):
        prefix = f"methodology: claim ledger claims[{i}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        cid = str(claim.get("id", "")).strip()
        text = str(claim.get("claim", claim.get("text", ""))).strip()
        ctype = str(claim.get("type", "")).strip()
        confidence = str(claim.get("confidence", "")).strip()
        risk = str(claim.get("risk", "")).strip()
        as_of = str(claim.get("as_of", "")).strip()
        source_urls = claim.get("source_urls")
        source_tiers = claim.get("source_tiers")

        is_derived = ctype == DERIVED_CLAIM_TYPE
        present_derivation = [k for k in DERIVATION_KEYS if k in claim]

        if not cid:
            errors.append(f"{prefix} missing id")
        elif cid in seen_ids:
            errors.append(f"{prefix} duplicate id {cid!r}")
        else:
            seen_ids.add(cid)
        if len(text) < 20:
            errors.append(f"{prefix} claim text is missing or too short")
        if ctype not in ALLOWED_CLAIM_TYPES:
            errors.append(
                f"{prefix} type {ctype!r} is invalid; allowed: {sorted(ALLOWED_CLAIM_TYPES)}"
            )
        # STRUCTURAL relabel guard. A derived entry that fails the
        # recompute audit can be "repaired" in one token by retyping it
        # `metric` and pasting the INPUT claims' URLs into source_urls —
        # which asserts that those pages state a computed output they do
        # not state, i.e. the fabricated citation this contract exists to
        # prevent. Detect the derivation by its SHAPE, never by the type
        # string the author chose. (Verified 2026-08-02: zero of the 1,312
        # claims across the 46 committed *.claims.json snapshots carry any
        # of these keys, so this cannot invalidate existing output.)
        elif present_derivation and not is_derived:
            errors.append(
                f"{prefix} carries derivation key(s) {present_derivation} but "
                f"declares retrieval type {ctype!r}; an entry that computes a "
                f"number must be typed {DERIVED_CLAIM_TYPE!r} so it is "
                f"recomputed rather than credited to a source URL"
            )
        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(
                f"{prefix} confidence {confidence!r} is invalid; allowed: {sorted(ALLOWED_CONFIDENCE)}"
            )
        if risk not in ALLOWED_RISK:
            errors.append(
                f"{prefix} risk {risk!r} is invalid; allowed: {sorted(ALLOWED_RISK)}"
            )
        if is_derived:
            # A derived claim's support is its `inputs`, not a URL. Requiring
            # source_urls here would force the author to invent one; ALLOWING
            # a non-empty one would let a computed output be credited to pages
            # that never state it. So: forbidden, not optional.
            missing_derivation = [k for k in DERIVATION_KEYS if k not in claim]
            if missing_derivation:
                errors.append(
                    f"{prefix} type {DERIVED_CLAIM_TYPE!r} requires "
                    f"{list(DERIVATION_KEYS)}; missing: {missing_derivation}"
                )
            for field, value in (("source_urls", source_urls), ("source_tiers", source_tiers)):
                if value not in (None, [], ()):
                    errors.append(
                        f"{prefix} type {DERIVED_CLAIM_TYPE!r} must not carry "
                        f"{field}; a computed number is supported by its inputs "
                        f"and formula, and no source page states it"
                    )
        elif not isinstance(source_urls, list) or not source_urls:
            errors.append(f"{prefix} source_urls must be a non-empty array")
        else:
            bad_urls = [
                u for u in source_urls
                if not isinstance(u, str) or not u.startswith(("http://", "https://"))
            ]
            if bad_urls:
                errors.append(f"{prefix} source_urls contains non-http URL(s): {bad_urls[:3]!r}")
        if is_derived:
            pass  # handled together with source_urls above
        elif not isinstance(source_tiers, list) or not source_tiers:
            errors.append(f"{prefix} source_tiers must be a non-empty array")
        else:
            bad_tiers = [t for t in source_tiers if t not in ALLOWED_SOURCE_TIERS]
            if bad_tiers:
                errors.append(
                    f"{prefix} source_tiers contains invalid tier(s): {bad_tiers!r}; "
                    f"allowed: {sorted(ALLOWED_SOURCE_TIERS)}"
                )
            if isinstance(source_urls, list) and len(source_tiers) != len(source_urls):
                errors.append(f"{prefix} source_tiers length must match source_urls length")
        if (ctype in VOLATILE_CLAIM_TYPES or risk in VOLATILE_RISKS) and not as_of:
            errors.append(f"{prefix} volatile/metric claim must include as_of")
    return errors


def validate_verifier_artifact(path: Path) -> list[str]:
    data, errors = _load_json_object(path, "verifier findings")
    if errors:
        return errors
    assert data is not None
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        return ["methodology: verifier findings must contain a non-empty claims[] array"]
    for i, claim in enumerate(claims, start=1):
        prefix = f"methodology: verifier claims[{i}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if not str(claim.get("id", "")).strip():
            errors.append(f"{prefix} missing id")
        if len(str(claim.get("text", "")).strip()) < 20:
            errors.append(f"{prefix} text is missing or too short")
        verdict = str(claim.get("verdict", "")).strip()
        if verdict not in ALLOWED_VERDICTS:
            errors.append(
                f"{prefix} verdict {verdict!r} is invalid; allowed: {sorted(ALLOWED_VERDICTS)}"
            )
        citation = claim.get("citation")
        if citation is not None and not isinstance(citation, str):
            errors.append(f"{prefix} citation must be a string or null")
    return errors


def validate_redteam_artifact(path: Path) -> list[str]:
    data, errors = _load_json_object(path, "red-team findings")
    if errors:
        return errors
    assert data is not None
    findings = data.get("findings")
    if not isinstance(findings, list) or len(findings) != 3:
        return ["methodology: red-team findings must contain exactly 3 findings[] entries"]
    for i, finding in enumerate(findings, start=1):
        prefix = f"methodology: red-team findings[{i}]"
        if not isinstance(finding, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if finding.get("redteam_failed") is True:
            errors.append(f"{prefix} has redteam_failed=true; adversarial review did not run")
        if not str(finding.get("claim_id", "")).strip():
            errors.append(f"{prefix} missing claim_id")
        if len(str(finding.get("claim_text", "")).strip()) < 20:
            errors.append(f"{prefix} claim_text is missing or too short")
        no_contra = finding.get("no_contradiction_found")
        if not isinstance(no_contra, bool):
            errors.append(f"{prefix} no_contradiction_found must be boolean")
        severity = finding.get("severity")
        if severity is not None and severity not in ALLOWED_REDTEAM_SEVERITY:
            errors.append(
                f"{prefix} severity {severity!r} is invalid; allowed: "
                f"{sorted(ALLOWED_REDTEAM_SEVERITY)} or null"
            )
        url = finding.get("contradicting_url")
        quote = finding.get("contradicting_quote")
        has_contradiction = bool(url or quote or severity)
        if no_contra is True and has_contradiction:
            errors.append(f"{prefix} cannot both find no contradiction and include contradiction fields")
        if no_contra is False and not has_contradiction:
            errors.append(f"{prefix} needs contradiction fields or no_contradiction_found=true")
        if url is not None and not (
            isinstance(url, str) and url.startswith(("http://", "https://"))
        ):
            errors.append(f"{prefix} contradicting_url must be http(s) string or null")
    return errors
