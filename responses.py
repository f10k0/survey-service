from __future__ import annotations


def is_user_participated(responses: list, user_email: str,
                         survey_id: int) -> bool:
    for response in responses:
        if (response["user_email"] == user_email
                and response["survey_id"] == survey_id):
            return True
    return False


def add_response(responses: list, user_email: str, survey_id: int,
                 question: str, answer: str) -> dict:
    response = {
        "user_email": user_email,
        "survey_id": survey_id,
        "question": question,
        "answer": answer,
    }
    responses.append(response)
    return response


def get_survey_statistics(responses: list, survey_id: int) -> dict:
    stats: dict[str, int] = {}
    for response in responses:
        if response["survey_id"] == survey_id:
            answer = response["answer"]
            stats[answer] = stats.get(answer, 0) + 1
    return stats


def get_user_responses(responses: list, user_email: str) -> list:
    return [
        response for response in responses
        if response["user_email"] == user_email
    ]
