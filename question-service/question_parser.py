import os
import re


DIRECTION_PATTERN = re.compile(
    r"Directions\s*\((\d+)-(\d+)\)\s*:(.*?)(?=Q\d+\.|$)",
    re.IGNORECASE | re.DOTALL
)
def looks_like_code(text):
    code_keywords = [
        "#include",
        "int main",
        "printf",
        "cout",
        "cin",
        "System.out",
        "public static",
        "def ",
        "print(",
        "for(",
        "while(",
        "{",
        "}",
        ";"
    ]

    return any(
        keyword in text
        for keyword in code_keywords
    )
def clean_option(option_text):

    option_text = re.sub(
        r"\[\[IMAGE:.*?\]\]",
        "",
        option_text
    )

    if looks_like_code(option_text):
        return option_text.strip()


    lines = [
        line.strip()
        for line in option_text.splitlines()
        if line.strip()
    ]

    if len(lines) == 2:
        return f"{lines[0]}/{lines[1]}"

    return " ".join(lines)

def extract_questions(
        text: str,
        images=None,
        tables=None
    ):

    if images is None:
        images = []

    if tables is None:
        tables = []




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

        image_path = re.search(
            r"image_[^\]\s]+",
            directions_text
        )

        print("\n===================")
        print("GROUP RANGE:", start, "-", end)
        print("GROUP TYPE:", group_type)
        print(
            "IMAGE MATCH:",
            image_path.group(0) if image_path else None
        )
        print("DIRECTIONS PREVIEW:")
        print(directions_text[:500])
        print("===================\n")

        direction_groups.append(
            {
                "start": int(start),

                "end": int(end),

                "directions":
                directions_text.strip(),

                "shared_image_path":
                image_path.group(0) if image_path else None,

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

    

    print(
        "\nIMAGES REFERENCED:"
    )


    print(
        "\nIMAGE COUNTS:"
    )
    print("TABLES RECEIVED:")
    print(tables)
    print("TABLE COUNT:", len(tables))

    if tables:
        print("FIRST TABLE:", tables[0])



    
    print("\nDIRECTION GROUPS FOUND:")

    for group in direction_groups:

        print(
            group["start"],
            group["end"],
            group["group_type"]
        )

    for block in blocks:
        table_data = None

        question_match = re.search(
            r"^(Q\d+\..*?)(?=\(a\)|$)",
            block,
            flags=re.DOTALL | re.IGNORECASE
        )

        option_matches = re.findall(
            r"\(([a-e])\)\s*(.*?)(?=\([a-e]\)|Ans\.|Answer|$)",
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
            r"(?:Ans|Answer)\s*\.?\s*:?\s*\(([a-e])\)",
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

            question_text = re.sub(
                r"\[\[IMAGE:.*?\]\]",
                "",
                question_text
            )

            question_text = re.sub(
                r"(?m)^\d+\s*$",
                "",
                question_text
            ).strip()

            is_code = looks_like_code(question_text)
        options = []

        for _, option_text in option_matches:

            options.append(
                clean_option(option_text)
            )

        answer_match = re.search(
            r"(?:Ans|Answer)\s*\.?\s*:?\s*\(([a-e])\)",
            block,
            flags=re.IGNORECASE
        )

        answer = None

        if answer_match:
            answer = answer_match.group(1).lower()

        question_number = None

        question_number_match = re.search(
                r"Q(\d+)\.",
                question_text
            )
        directions = None

        shared_image_path = None
        table_data = None

        image_matches = re.findall(
            r"\[\[IMAGE:(.*?)\]\]",
            block
        )
        block = re.sub(
            r"\[\[IMAGE:.*?\]\]",
            "",
            block
        )

        if image_matches:

            image_file = image_matches[0].strip()

            shared_image_path = next(
                (
                    img
                    for img in images
                    if os.path.basename(img) == image_file
                ),
                None
            )

            if shared_image_path:

                relative_path = shared_image_path.replace(
                    "/app/uploads/",
                    ""
                )

                relative_path = relative_path.replace(
                    "\\",
                    "/"
                )

                shared_image_path = f"https://pdf2exam.org:/images/{relative_path}"

                print(
                    "FINAL IMAGE URL:",
                    repr(shared_image_path)
                )
        group_type = None
        if question_number_match:

            question_number = int(
                question_number_match.group(1)
            )
        print(
            "AUTO IMAGE:",
            question_number,
            shared_image_path
        )
       

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

                print(
                    "IMAGE FOUND FOR QUESTION:",
                    question_number,
                    shared_image_path
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
        print(
            "QUESTION:",
            question_number,
            "DESCRIPTION:",
            directions,
            "IMAGE:",
            shared_image_path,
            "TYPE:",
            group_type,
            "TABLE DATA:",
            table_data
        )
        table_data = None

        for group in direction_groups:

            if (
                question_number is not None
                and group["start"] <= question_number <= group["end"]
            ):

                table_data = tables
                break

        if (
            question_number == 1
            and len(tables) > 0
        ):
            table_data = tables[0]
        print(
            "QUESTION:",
            question_number,
            "TABLE:",
            table_data
        )

        questions.append(
            {
                "section": "General",

                "question":
                question_text,

                "is_code": 
                is_code,

                "description":
                directions,

                "image_path":
                str(shared_image_path)
                if shared_image_path
                else None,

                "table_data":
                table_data,

                "options":
                options,

                "correct_answer":
                answer,

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