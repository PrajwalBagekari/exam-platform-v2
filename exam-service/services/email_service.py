import os
import base64
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def send_result_email(
    email,
    exam_name,
    score,
    total_questions,
    pdf_path,
):
    configuration = sib_api_v3_sdk.Configuration()

    configuration.api_key[
        "api-key"
    ] = os.getenv(
        "BREVO_API_KEY"
    )

    api_instance = (
        sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(
                configuration
            )
        )
    )

    with open(pdf_path, "rb") as f:
        pdf_content = (
            base64.b64encode(
                f.read()
            ).decode("utf-8")
        )

    email_data = (
        sib_api_v3_sdk.SendSmtpEmail(
            to=[
                {
                    "email": email
                }
            ],
            sender={
                "email": "results@pdf2exam.org",
                "name": "PDF2Exam"
            },
            subject=f"{exam_name} Result",
            html_content=f"""
            <h2>Exam Result</h2>

            <p>
            Exam: {exam_name}
            </p>

            <p>
            Score: {score}/{total_questions}
            </p>

            <p>
            Thank you for using PDF2Exam.
            </p>
            """,
            attachment=[
                {
                    "content": pdf_content,
                    "name": "Exam_Result.pdf"
                }
            ]
        )
    )

    try:

        api_instance.send_transac_email(
            email_data
        )

        print(
            "Result email sent"
        )

        return True

    except ApiException as e:

        print(
            f"Brevo Error: {e}"
        )

        return False