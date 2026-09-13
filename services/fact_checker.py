import json
from groq import Groq
from config import Config


class FactChecker:
    def _init_(self):
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL

    def verify_claim(self, claim: str, search_results: list[dict]) -> dict:
        """
        Search evidence ke mutabiq claim ki accuracy check karta hai.
        """
        evidence_lines = [
            f"- Source ({res['url']}): {res.get('snippet', '')}"
            for res in search_results
            if res.get("url")
        ]
        context = "\n".join(evidence_lines) if evidence_lines else "No online search evidence found."

        system_instruction = (
            "You are a strict Fact-Checking Auditor. Verify claims using ONLY the provided search evidence. "
            "Return valid JSON strictly following the requested structure without any surrounding markdown."
        )

        user_prompt = f"""
Claim to Audit: "{claim}"

Search Evidence:
{context}

Return a JSON object with these exact keys:
- "verdict": "TRUE" | "FALSE" | "MIXED" | "UNVERIFIED"
- "confidence": float between 0.0 and 1.0
- "explanation": a concise 2-sentence explanation of why the claim holds that verdict.
- "sources": list of URLs from the evidence used for verification.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
            )

            raw_content = (response.choices[0].message.content or "").strip()
            if not raw_content:
                raise RuntimeError("Groq returned an empty verification response.")

            result = json.loads(raw_content)
            if not isinstance(result, dict):
                raise RuntimeError("Groq verification response was not a JSON object.")
            return result

        except Exception as e:
            return {
                "verdict": "UNVERIFIED",
                "confidence": 0.0,
                "explanation": f"Failed to perform verification check: {str(e)}",
                "sources": [],
            }
