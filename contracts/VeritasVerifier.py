# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Veritas: GenLayer-native decentralized claim verification."""
from genlayer import *
import json


class VeritasVerifier(gl.Contract):
    latest_claim: str
    latest_verdict: str
    latest_confidence: i32
    latest_reasoning: str
    latest_sources: str
    latest_evidence: str

    def __init__(self):
        self.latest_claim = ""
        self.latest_verdict = "UNCERTAIN"
        self.latest_confidence = 0
        self.latest_reasoning = "No claim has been verified yet."
        self.latest_sources = "[]"
        self.latest_evidence = "[]"

    @gl.public.write
    def verify_claim(self, claim: str, source_urls: str) -> None:
        """Verify a claim using 1-3 newline-separated, publicly accessible URLs."""
        urls = [url.strip() for url in source_urls.splitlines() if url.strip()]
        if len(claim.strip()) < 8 or len(claim) > 800:
            raise gl.vm.UserError("Claim must contain between 8 and 800 characters.")
        if len(urls) < 1 or len(urls) > 3:
            raise gl.vm.UserError("Provide one to three public source URLs, one per line.")
        for url in urls:
            if not (url.startswith("https://") or url.startswith("http://")):
                raise gl.vm.UserError("Every source must begin with http:// or https://.")

        def evaluate_independently():
            evidence = []
            for url in urls:
                # Web access is intentionally inside the non-deterministic block.
                page = gl.nondet.web.get(url)
                text = page.body.decode("utf-8")[:12000]
                evidence.append({"url": url, "content": text})
            prompt = f"""
You are Veritas, an evidence-first claim verifier.
Claim: {claim}
Independently evaluate the claim using ONLY the source material below. Do not use outside knowledge.
<sources>{json.dumps(evidence)}</sources>
Return JSON with exactly these keys:
{{"verdict":"TRUE" | "FALSE" | "PARTIALLY TRUE" | "UNCERTAIN","confidence":integer from 0 to 100,"reasoning":"plain-language explanation of at most 700 characters","sources":["only supplied URLs supporting analysis"],"evidence":["up to three source-grounded observations"]}}
Use UNCERTAIN when material is insufficient or conflicts materially. Never invent quotations, URLs, facts, or certainty.
"""
            result = gl.nondet.exec_prompt(prompt, response_format="json")
            if not isinstance(result, dict):
                raise gl.vm.UserError("The verifier returned an invalid response.")
            return result

        # Validators independently fetch and reason over the sources. EqComparative
        # accepts only semantically equivalent work; no local backend is involved.
        result = gl.eq_principle.prompt_comparative(
            evaluate_independently,
            principle="""
The verdict field must be exactly identical. Confidence may differ by at most 10 points.
Reasoning and evidence must be faithful to the same supplied URLs and support the verdict.
An answer that invents a source, quote, or material fact is not equivalent.
""",
        )
        verdict = result.get("verdict", "UNCERTAIN")
        confidence = result.get("confidence", 0)
        if verdict not in ("TRUE", "FALSE", "PARTIALLY TRUE", "UNCERTAIN"):
            raise gl.vm.UserError("Verifier returned an unsupported verdict.")
        if not isinstance(confidence, int) or confidence < 0 or confidence > 100:
            raise gl.vm.UserError("Verifier returned an invalid confidence score.")
        # Storage writes are deterministic and happen only after consensus returns.
        self.latest_claim = claim
        self.latest_verdict = verdict
        self.latest_confidence = confidence
        self.latest_reasoning = result.get("reasoning", "")[:700]
        self.latest_sources = json.dumps(result.get("sources", []))
        self.latest_evidence = json.dumps(result.get("evidence", []))

    @gl.public.view
    def get_latest_verification(self) -> str:
        """Return the latest finalized on-chain proof as a JSON string."""
        return json.dumps({"claim": self.latest_claim, "verdict": self.latest_verdict, "confidence": self.latest_confidence, "reasoning": self.latest_reasoning, "sources": json.loads(self.latest_sources), "evidence": json.loads(self.latest_evidence)})

