import json
from groq import Groq
from config import Config


class ClaimExtractor:
    """Extracts verifiable claims from a pitch transcript using Groq."""

    def __init__(self):
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL

    def extract_claims(self, transcript: str) -> list[dict]:
        """
        Extract specific and verifiable claims from a pitch transcript.

        Returns:
            list[dict]: Extracted claims with id, claim, and category.
        """

        if not transcript or not transcript.strip():
            return []

        prompt = f"""
You are an expert AI Pitch Auditor.

Analyze the following startup pitch transcript and extract ONLY
specific, verifiable claims.

Look for claims such as:
- Revenue
- Market size / TAM / SAM / SOM
- Number of users or customers
- Growth percentages
- Market share
- Funding
- Customer metrics
- Pricing or financial figures
- Industry statistics
- Performance metrics
- Other factual claims that can be verified using external sources

Do NOT extract:
- Opinions
- Vague statements
- Marketing language
- Future plans
- Personal statements
- Questions

Return ONLY a valid JSON array.

Each object MUST contain exactly these fields:
{{
    "id": 1,
    "claim": "Concise factual claim",
    "category": "Financial"
}}

Allowed categories:
- Financial
- Market Size
- Traction
- Growth
- Funding
- Industry Fact
- Performance
- General Fact

If there are no verifiable claims, return:
[]

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You extract factual, verifiable claims from "
                            "startup pitches and return strict JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content

            if not content:
                return []

            data = json.loads(content)

            # Handle {"claims": [...]} response
            if isinstance(data, dict):
                claims = data.get("claims", [])
            else:
                claims = data

            if not isinstance(claims, list):
                return []

            # Validate and normalize claims
            validated_claims = []

            for index, item in enumerate(claims, start=1):
                if not isinstance(item, dict):
                    continue

                claim = item.get("claim")
                category = item.get("category")

                if not claim:
                    continue

                validated_claims.append(
                    {
                        "id": index,
                        "claim": str(claim).strip(),
                        "category": str(category or "General Fact").strip(),
                    }
                )

            return validated_claims

        except json.JSONDecodeError:
            return []

        except Exception as e:
            print(f"Claim extraction error: {e}")
            return []