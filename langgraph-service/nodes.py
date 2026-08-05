import requests


def pdf_node(state):

    print("=" * 60)
    print("PDF NODE")
    print("PDF PATH:", state["pdf_path"])

    response = requests.post(
        "http://pdf-service:8001/process",
        params={
            "pdf_path": state["pdf_path"]
        }
    )

    print("PDF STATUS:", response.status_code)

    if response.status_code != 200:
        raise Exception(
            f"PDF Service Failed: {response.text}"
        )

    state["pdf_data"] = response.json()

    return state


def image_node(state):

    print("=" * 60)
    print("IMAGE NODE")

    response = requests.post(
        "http://image-service:8005/render",
        params={
            "pdf_path": state["pdf_path"]
        }
    )

    print("IMAGE STATUS:", response.status_code)

    if response.status_code != 200:
        raise Exception(
            f"Image Service Failed: {response.text}"
        )

    state["image_data"] = response.json()

    return state


def ocr_node(state):

    print("=" * 60)
    print("OCR NODE")

    pages = state["image_data"].get(
        "pages",
        []
    )

    extracted_text = []

    for page in pages:

        print("PROCESSING:", page)

        response = requests.post(
            "http://ocr-service:8004/extract",
            params={
                "image_path": page
            }
        )

        print(
            "OCR STATUS:",
            response.status_code
        )

        if response.status_code != 200:
            raise Exception(
                f"OCR Failed: {response.text}"
            )

        result = response.json()

        extracted_text.append(
            result.get(
                "text",
                ""
            )
        )

    state["ocr_data"] = extracted_text

    return state

def question_node(state):

    print("=" * 60)
    print("QUESTION NODE")

    if state.get("ocr_data"):

        full_text = "\n".join(
            state["ocr_data"]
        )

    else:

        full_text = state[
            "pdf_data"
        ].get(
            "text",
            ""
        )

    print("TEXT LENGTH:")
    print(len(full_text))
    print("=" * 60)
    print("PDF DATA KEYS:")
    print(state["pdf_data"].keys())

    print("IMAGES:")
    print(state["pdf_data"].get("images"))

    print("IMAGE COUNT:")
    print(len(state["pdf_data"].get("images", [])))
    print("=" * 60)

    response = requests.post(
    "http://question-service:8002/questions",
    json={
        "text": full_text,
        "images": state["pdf_data"].get("images", [])
    }
)

    print(
        "QUESTION STATUS:",
        response.status_code
    )

    print(
        "QUESTION RESPONSE:"
    )

    print(
        response.text
    )

    if response.status_code != 200:

        raise Exception(
            f"Question Service Failed: {response.text}"
        )

    state["questions"] = response.json().get(
        "questions",
        []
    )

    print(
        "QUESTIONS EXTRACTED:"
    )

    print(
        len(state["questions"])
    )

    return state

def rag_node(state):

    print("=" * 60)
    print("RAG NODE")
    print("QUESTIONS:")
    print(state["questions"])
    print("=" * 60)

    response = requests.post(
        "http://rag-service:8003/build",
        json={
            "data": state["questions"]
        }
    )

    print("RAG STATUS:",
          response.status_code)

    print("RAG RESPONSE:",
          response.text)

    if response.status_code != 200:
        raise Exception(
            f"RAG Service Failed: {response.text}"
        )

    state["rag_data"] = response.json()

    return state


def exam_node(state):

    response = requests.post(
        "http://exam-service:8006/save",
        json={
            "questions": state["questions"]
        }
    )

    print("EXAM STATUS:", response.status_code)
    print("EXAM RESPONSE:", response.text)

    if response.status_code != 200:

        state["exam_data"] = {
            "status": "error",
            "message": response.text
        }

        return state

    state["exam_data"] = response.json()

    return state