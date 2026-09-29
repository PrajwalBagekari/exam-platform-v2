import re


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
    )

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

    if scores[best_section] == 0:
        return "General Awareness"

    return best_section