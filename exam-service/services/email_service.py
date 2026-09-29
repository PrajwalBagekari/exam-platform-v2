import os

import sib_api_v3_sdk

from sib_api_v3_sdk.rest import ApiException


def send_result_email(
    email: str,
    user_name: str,
    exam_name: str,
    score: int,
    total_questions: int,
    attempted: int,
    skipped: int,
    review: int,
) -> bool:

    configuration = (
        sib_api_v3_sdk.Configuration()
    )

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

    percentage = (
        round(
            (score / total_questions) * 100,
            2,
        )
        if total_questions > 0
        else 0
    )

    html_content = f"""
    <html>
    <body>

    <h1>Exam Result</h1>

    <p>Hello {user_name},</p>

    <p>
        Thank you for attempting the exam.
    </p>

    <hr>

    <h2>Result Summary</h2>

    <table border="1" cellpadding="8">

        <tr>
            <td><b>Exam</b></td>
            <td>{exam_name}</td>
        </tr>

        <tr>
            <td><b>Score</b></td>
            <td>{score}/{total_questions}</td>
        </tr>

        <tr>
            <td><b>Percentage</b></td>
            <td>{percentage}%</td>
        </tr>

        <tr>
            <td><b>Attempted</b></td>
            <td>{attempted}</td>
        </tr>

        <tr>
            <td><b>Skipped</b></td>
            <td>{skipped}</td>
        </tr>

        <tr>
            <td><b>Review</b></td>
            <td>{review}</td>
        </tr>

    </table>

    <br>

    <p>
        Regards,<br>
        PDF2Exam Team
    </p>

    </body>
    </html>
    """

    email_data = (
        sib_api_v3_sdk.SendSmtpEmail(
            to=[
                {
                    "email": email,
                    "name": user_name,
                }
            ],
            sender={
                "email": "results@pdf2exam.org",
                "name": "PDF2Exam",
            },
            subject=f"{exam_name} Result",
            html_content=html_content,
        )
    )

    try:

        api_instance.send_transac_email(
            email_data
        )

        print(
            f"Result email sent to {email}"
        )

        return True

    except ApiException as e:

        print(
            f"Brevo Error: {e}"
        )

        return False