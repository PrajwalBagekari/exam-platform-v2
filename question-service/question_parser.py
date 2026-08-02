import re
from collections import Counter

DIRECTION_PATTERN = re.compile(
    r"Directions\s*\((\d+)-(\d+)\)\s*:(.*?)(?=Q\d+\.)",
    re.IGNORECASE | re.DOTALL
)

def extract_questions(text: str):

    questions = []

    direction_groups = []

    direction_matches = (
        DIRECTION_PATTERN.findall(text)
    )
    
    for (
        start,
        end,
        directions_text
    ) in direction_matches:

        group_type = None

        direction_lower = (
            directions_text.lower()
        )

        if "line graph" in direction_lower:

            group_type = "line_graph"

        elif "pie chart" in direction_lower:

            group_type = "pie_chart"

        elif "table" in direction_lower:

            group_type = "table"

        elif "bar graph" in direction_lower:

            group_type = "bar_graph"

        direction_groups.append(
            {
                "start": int(start),

                "end": int(end),

                "directions":
                directions_text.strip(),

                "shared_image_path":
                image_path if (image_path := re.search(
                    r"image_[A-Za-z0-9+/=]+",
                    directions_text
                )) else None,

                "group_type":
                group_type
            }
        )

    print(
        "\nDIRECTION GROUPS FOUND:"
    )

    for group in direction_groups:

        print(
            f"GROUP {group['start']}-{group['end']}"
        )

        print(
            f"TYPE: {group['group_type']}"
        )

    pattern = (
        r"(Q\d+\..*?)"
        r"(?=Q\d+\.|Directions\s*\(\d+\-\d+\)|$)"
    )

    blocks = re.findall(
        pattern,
        text,
        flags=re.DOTALL
    )

    print(
        "TOTAL BLOCKS:"
    )

    print(
        len(blocks)
    )

    image_matches = re.findall(
        r"image_[A-Za-z0-9+/=]+",
        text
    )

    print(
        "\nIMAGES REFERENCED:"
    )

    print(
        image_matches
    )

    print(
        "\nIMAGE COUNTS:"
    )

    print(
        Counter(image_matches)
    )

    
    print("\nDIRECTION GROUPS FOUND:")

    for group in direction_groups:

        print(
            group["start"],
            group["end"],
            group["group_type"]
        )

    for block in blocks:

        question_match = re.search(
            r"^(Q\d+\..*?)(?=\([a]\)|$)",
            block,
            flags=re.DOTALL
        )

        option_matches = re.findall(
            r"\(([a-e])\)\s*(.*?)"
            r"(?=\([a-e]\)\s|Directions\s*\(\d+\-\d+\)|$)",
            block,
            flags=re.DOTALL | re.IGNORECASE
        )

        if len(option_matches) == 0:
            print("\n====================")
            print("OPTION MATCH FAILED")
            print(block[:1000])
            print("====================")
            break
        print("OPTION MATCHES:")
        print(option_matches[:5])

        answer_match = re.search(
            r"Ans<strong data-lexical-text=\"true\">\.\(</strong>([a-e])<strong data-lexical-text=\"true\">\)</strong>",
            block,
            flags=re.IGNORECASE
        )

        question_text = ""

        if question_match:

            question_text = (
                question_match
                .group(1)
                .strip()
            )

        options = []

        for _, option_text in option_matches:

            options.append(
                option_text.strip()
            )

        correct_answer = None

        if answer_match:

            correct_answer = (
                answer_match
                .group(1)
                .lower()
            )

        question_number = None

        question_number_match = re.search(
                r"Q(\d+)\.",
                question_text
            )

        if question_number_match:

            question_number = int(
                question_number_match.group(1)
            )

        

        if question_number_match:

            question_number = int(
                question_number_match.group(1)
            )

       # directions = None

        shared_image_path = None

        group_type = None
        print("\nDIRECTION GROUPS FOUND:")

        for group in direction_groups:

            if (
                question_number is not None
                and
                group["start"]
                <= question_number
                <= group["end"]
            ):

                directions = (
                    group["directions"]
                )

                shared_image_path = (
                    group["shared_image_path"]
                )

                group_type = (
                    group["group_type"]
                )

                break

        print(
                "QUESTION",
                question_number,
                "OPTIONS:",
                len(options)
            )

        print(
            "TYPE:",
            group_type
        )

        print(
            "DIRECTIONS:",
            directions
        )

        questions.append(
            {
                "section": "General",

                "question":
                question_text,

                "description":
                directions,

                "image_path":
                shared_image_path,

                "options":
                options,

                "correct_answer":
                correct_answer,

                "group_type":
                group_type
            }
        )

    print(
        "\n================================"
    )

    print(
        "QUESTIONS FOUND:"
    )

    print(
        len(questions)
    )

    print(
        "================================\n"
    )

    return questions