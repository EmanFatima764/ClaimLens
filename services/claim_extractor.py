import json
from groq import Groq
from config import Config


class ClaimExtractor:
    """Extracts factual and externally verifiable claims from a pitch transcript."""

    def __init__(self):
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL

    def extract_claims(self, transcript: str) -> list[dict]:
        """
        Extract factual claims from a startup pitch that can potentially
        be verified using external sources.
        """

        if not transcript or not transcript.strip():
            return []

        prompt = f"""
You are an expert AI Pitch Auditor.

Your task is to identify factual claims in the startup pitch below.

A claim should be extracted if it states something that could potentially
be checked or verified using data, documents, websites, reports, or other
external evidence.

EXTRACT CLAIMS SUCH AS:

1. Business metrics
- Number of users
- Number of customers
- Revenue
- ARR / MRR
- Sales
- Profit
- Growth rate
- Retention rate
- Conversion rate

2. Market claims
- TAM
- SAM
- SOM
- Market size
- Market growth
- Market share
- Industry statistics

3. Funding and company information
- Funding raised
- Investment amount
- Valuation
- Number of employees
- Number of companies using the product

4. Product/performance claims
- "Our AI achieves 95% accuracy"
- "We reduce processing time by 60%"
- "Our system is 3x faster"
- "We process 10,000 documents per month"

5. Customer claims
- Customer count
- Named customer relationships
- Customer results
- Case-study statistics

6. Pricing and financial claims
- "$49 per month"
- "$10,000 annual contract"
- "We generated $100K in revenue"

7. Other factual claims
Any specific statement that can reasonably be checked against an
external source.

DO NOT extract:

- Opinions
- Personal beliefs
- Questions
- Purely hypothetical statements
- Future plans
- Goals that have not happened yet
- Generic marketing statements with no factual information

IMPORTANT:

Do NOT require a number for every claim.

For example:

"We currently serve hospitals across Pakistan."

This can be a factual claim.

"We have partnerships with three universities."

This is also a factual claim.

"According to WHO, X causes Y."

This is also a factual claim.

Return ONLY this JSON structure:

{{
    "claims": [
        {{
            "id": 1,
            "claim": "Exact concise factual claim",
            "category": "Traction"
        }}
    ]
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

If there are genuinely no factual claims, return:

{{
    "claims": []
}}

Do not add explanations outside the JSON.

PITCH TRANSCRIPT:
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
                            "You are a factual claim extraction engine. "
                            "Extract useful, specific, externally verifiable "
                            "claims from startup pitches."
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

            # Debugging
            print("RAW CLAIM EXTRACTOR RESPONSE:")
            print(content)

            data = json.loads(content)

            if not isinstance(data, dict):
                return []

            claims = data.get("claims", [])

            if not isinstance(claims, list):
                return []

            validated_claims = []

            for index, item in enumerate(claims, start=1):

                if not isinstance(item, dict):
                    continue

                claim = item.get("claim")
                category = item.get("category", "General Fact")

                if not claim:
                    continue

                validated_claims.append(
                    {
                        "id": index,
                        "claim": str(claim).strip(),
                        "category": str(category).strip(),
                    }
                )

            return validated_claims

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Model response: {content if 'content' in locals() else 'None'}")
            return []

        except Exception as e:
            print(f"Claim extraction error: {e}")
            return []
