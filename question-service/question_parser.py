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
    print("\n=== TABLES RECEIVED ===")
    print(tables)
    print("COUNT:", len(tables))




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

                "group_image_file":
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
    usable_tables = []

    for table in tables:
        rows = table.get("rows", [])

        if rows:
            usable_tables.append({
                "rows": rows
            })


    table_index = 0

    for group in direction_groups:

        group["table_data"] = None

        if group["group_type"] != "table":
            continue

        if table_index >= len(usable_tables):
            print(
                f"NO TABLE FOUND FOR GROUP "
                f"{group['start']}-{group['end']}"
            )
            continue

        table = usable_tables[table_index]

        group["table_data"] = (
            table.get("rows")
            if isinstance(table, dict)
            else table
        )
        print("\nUSABLE TABLES:")
        print(usable_tables)

        print("USABLE TABLE COUNT:")
        print(len(usable_tables))  

        print(
            f"TABLE ATTACHED TO GROUP "
            f"{group['start']}-{group['end']}"
        )

        print(group["table_data"])
        

        table_index += 1
    is_code = False

    for block in blocks:

        group_type = None
        directions = None
        table_data = None
        group_images = []
        

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
        if question_number_match:
            question_number = int(
                question_number_match.group(1)
            )
        directions = None
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

    
        question_images = []
        all_images = []
        for image_file in image_matches:
            

            image_file = image_file.strip()

            matched_image = next(
                (
                    img
                    for img in images
                    if os.path.basename(img) == image_file
                ),
                None
            )

            if matched_image:

                relative_path = matched_image.replace(
                    "/app/uploads/",
                    ""
                ).replace(
                    "\\",
                    "/"
                )

                image_url = (
                    f"https://pdf2exam.org/images/{relative_path}"
                )

                question_images.append(image_url)

            else:

                question_images.append(image_file)
        

            print("\nDIRECTION GROUPS FOUND:")


        for group in direction_groups:

            if (
                question_number is not None
                and
                group["start"]
                <= question_number
                <= group["end"]
            ):

                directions = group["directions"]
                table_data = group.get("table_data")
                print(
                    f"QUESTION {question_number} "
                    f"MATCHED GROUP "
                    f"{group['start']}-{group['end']}"
                )

                print("TABLE DATA:")
                print(table_data)

                if table_data == []:
                    table_data = None

                directions = directions.strip()
                print(
                    "QUESTION",
                    question_number,
                    "TABLE RECEIVED:",
                    table_data
                )

                image_file = group["group_image_file"]

                if image_file:
                    print("GROUP IMAGE FILE:", image_file)

                    print("AVAILABLE IMAGES:")
                    for img in images:
                        print(" ->", os.path.basename(img))

                    matched_image = next(
                        (
                            img
                            for img in images
                            if os.path.basename(img) == image_file
                        ),
                        None
                    )
                    print("MATCHED IMAGE:", matched_image)

                    if matched_image:

                        relative_path = matched_image.replace(
                            "/app/uploads/",
                            ""
                        )

                        relative_path = relative_path.replace(
                            "\\",
                            "/"
                        )

                        group_images.append(
                            f"https://pdf2exam.org/images/{relative_path}"
                        )

                        print(
                            "GROUP IMAGE URL:",
                            group_images
                        )
                print(
                    "QUESTION IMAGE:",
                    question_images
                )

                print(
                    "GROUP IMAGE:",
                    group_images
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

            "GROUP IMAGE:",
            group_images,
            "TYPE:",
            group_type,
            "TABLE DATA:",
            table_data
        )

        print(
            "QUESTION:",
            question_number,
            "TABLE:",
            table_data,
            "IS_CODE:",
            is_code
        )


        if question_images:
            all_images.extend(question_images)

        if group_images:
            for img in group_images:
                if img not in all_images:
                    all_images.append(img)

        print(
            "FINAL IMAGES:",
            all_images
        )
        if (
            table_data is None
            and question_number == 1
            and usable_tables
        ):
            table_data = usable_tables[0]["rows"]
        if question_number == 1:
            print("\n====================")
            print("Q1 TABLE ATTACHED")
            print(table_data)
            print("====================")
        print(
            f"QUESTION {question_number} FINAL TABLE:"
        )

        print(table_data)


        questions.append(
            {
                "section": "General",

                "question":
                question_text,

                "is_code": 
                is_code,

                "description":
                directions,

                

                "table_data":
                table_data,

                "options":
                options,

                "correct_answer":
                answer,

                "group_type":
                group_type,

                "image_paths":
                    all_images,

                "image_path":
                    all_images[0]
                    if all_images
                    else None,

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
