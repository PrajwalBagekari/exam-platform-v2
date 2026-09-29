import os
import re
import requests

SECTION_KEYWORDS = {
    "Computer Knowledge": [
        "sql",
        "database",
        "normalization",
        "network",
        "tcp",
        "udp",
        "ip address",
        "osi",
        "linux",
        "windows",
        "computer",
        "programming",
        "java",
        "python",
        "c++",
        "c language",
        "data structure",
        "operating system",
        "dbms",
        "compiler",
        "algorithm",
        "binary tree",
        "stack",
        "queue",
        "html",
        "css",
        "javascript",
        "cloud",
        "cyber security",
        "firewall",
        "router",
        "switch",
    ],
    "Quantitative Aptitude": [
        "profit",
        "loss",
        "interest",
        "simple interest",
        "compound interest",
        "ratio",
        "proportion",
        "average",
        "percentage",
        "time and work",
        "speed",
        "distance",
        "train",
        "boat",
        "probability",
        "permutation",
        "combination",
        "mixture",
        "alligation",
        "partnership",
        "discount",
        "number series",
        "simplification",
        "quadratic equation",
    ],
    "Reasoning Ability": [
        "puzzle",
        "seating arrangement",
        "blood relation",
        "syllogism",
        "coding decoding",
        "direction sense",
        "statement",
        "assumption",
        "conclusion",
        "cause and effect",
        "alphabet series",
        "ranking",
        "order",
        "mirror image",
        "embedded figure",
        "logical reasoning",
        "input output",
    ],
    "English Language": [
        "synonym",
        "antonym",
        "grammar",
        "vocabulary",
        "fill in the blanks",
        "reading comprehension",
        "passage",
        "para jumbles",
        "error spotting",
        "sentence improvement",
        "phrase replacement",
        "english",
        "choose the correct word",
    ],
    "General Awareness": [
        "government",
        "history",
        "geography",
        "economy",
        "constitution",
        "current affairs",
        "sports",
        "books and authors",
        "awards",
        "india",
        "capital",
        "currency",
        "who among the following",
    ],
}

SECTIONS = list(SECTION_KEYWORDS.keys()) + [
    "Data Interpretation"
]


def detect_section(
    question_text: str,
    description: str | None = None,
    group_type: str | None = None,
    is_code: bool = False,
) -> str:

    if group_type in {
        "table",
        "bar_graph",
        "pie_chart",
        "line_graph",
    }:
        return "Data Interpretation"

    if is_code:
        return "Computer Knowledge"

    combined_text = (
        f"{question_text or ''} {description or ''}"
    ).lower()

    combined_text = re.sub(
        r"\s+",
        " ",
        combined_text,
    ).strip()

    scores = {}

    for section, keywords in SECTION_KEYWORDS.items():

        score = 0

        for keyword in keywords:
            if keyword in combined_text:
                score += 1

        scores[section] = score

    best_section = max(
        scores.items(),
        key=lambda item: item[1]
    )[0]

    best_score = scores[best_section]

    # High confidence keyword classification
    if best_score >= 2:
        return best_section

    # OpenRouter fallback
    try:

        prompt = f"""
You are an expert competitive exam classifier.

Classify the following question into EXACTLY ONE category.

Categories:
- Computer Knowledge
- Quantitative Aptitude
- Reasoning Ability
- English Language
- General Awareness
- Data Interpretation

Rules:
1. Return ONLY the category name.
2. No explanation.
3. No extra text.
4. No markdown.

Question:
{question_text}

Description:
{description or ""}
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": (
                    f"Bearer {os.getenv('OPENROUTER_API_KEY')}"
                ),
                "Content-Type": "application/json",
            },
            json={
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "temperature": 0,
                "max_tokens": 20,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Return ONLY one category name from: "
                            "Computer Knowledge, "
                            "Quantitative Aptitude, "
                            "Reasoning Ability, "
                            "English Language, "
                            "General Awareness, "
                            "Data Interpretation."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            },
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()

        content = (
            result.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        predicted_section = (
            content.strip()
            if content
            else ""
        )

        if predicted_section in SECTIONS:
            return predicted_section

    except Exception as e:
        print(
            f"Section detection failed: {e}"
        )

    # Original fallback behavior
    if best_score > 0:
        return best_section

    return "General Awareness"