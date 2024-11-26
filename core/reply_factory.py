from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id", None)

    if current_question_id is None:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        session["current_question_id"] = 0
        session["answers"] = {}

    else:
        success, error = record_current_answer(message, current_question_id, session)
        if not success:
            bot_responses.append(error)
            return bot_responses

        session["current_question_id"] += 1

    next_question, next_question_id = get_next_question(session["current_question_id"])

    if next_question:
        bot_responses.append(next_question)
        session["current_question_id"] = next_question_id
    else:
        bot_responses.append(generate_final_response(session))
        session["current_question_id"] = None  

    session.save()
    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id < 0 or current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question ID."

    question_data = PYTHON_QUESTION_LIST[current_question_id]
    valid_options = question_data["options"]

    try:
        answer_index = int(answer) - 1  
        if answer_index < 0 or answer_index >= len(valid_options):
            raise ValueError
        selected_option = valid_options[answer_index]
    except (ValueError, TypeError):
        return False, f"Invalid option. Please choose a number from 1 to {len(valid_options)}."

    session["answers"][current_question_id] = selected_option
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id < len(PYTHON_QUESTION_LIST):
        question_data = PYTHON_QUESTION_LIST[current_question_id]
        options = "\n".join(f"{i + 1}. {option}" for i, option in enumerate(question_data["options"]))
        return f"{question_data['question_text']}\n\nOptions:\n{options}", current_question_id
    return None, -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get("answers", {})
    correct_answers = sum(
        1 for ques_id, ans in answers.items()
        if 0 <= ques_id < len(PYTHON_QUESTION_LIST) and ans == PYTHON_QUESTION_LIST[ques_id]["answer"]
    )
    return f"You scored {correct_answers}/{len(PYTHON_QUESTION_LIST)}. Great job!"
