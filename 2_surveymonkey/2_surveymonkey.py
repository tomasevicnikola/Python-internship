import argparse
import json
import os
import sys
import requests
from dotenv import load_dotenv


BASE_URL = "https://api.surveymonkey.com/v3"


def load_questions(file_path):
    # Read survey questions from JSON file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading questions file: {e}")
        sys.exit(1)


def load_emails(file_path):
    # Read recipient emails from text file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            emails = [line.strip() for line in file if line.strip()]
        return emails
    except Exception as e:
        print(f"Error reading emails file: {e}")
        sys.exit(1)


def validate_data(data, emails):
    # Basic validation
    if len(emails) < 2:
        print("Error: there must be at least 2 recipient emails")
        sys.exit(1)

    if len(data) != 1:
        print("Error: JSON must contain exactly one survey")
        sys.exit(1)

    survey_name = next(iter(data))
    survey_pages = data[survey_name]

    if not isinstance(survey_pages, dict) or not survey_pages:
        print("Error: survey must contain at least one page")
        sys.exit(1)

    total_questions = 0

    for page_name, questions in survey_pages.items():
        if not isinstance(questions, dict) or not questions:
            print(f"Error: page '{page_name}' must contain at least one question")
            sys.exit(1)

        for question_name, question_data in questions.items():
            total_questions += 1

            if not isinstance(question_data, dict):
                print(f"Error: question '{question_name}' must be an object")
                sys.exit(1)

            if "Description" not in question_data or "Answers" not in question_data:
                print(
                    f"Error: question '{question_name}' must contain Description and Answers"
                )
                sys.exit(1)

            if len(question_data["Answers"]) < 2:
                print(f"Error: question '{question_name}' must contain at least 2 answers")
                sys.exit(1)

    if total_questions < 3:
        print("Error: survey must contain at least 3 questions in total")
        sys.exit(1)

    return survey_name, survey_pages


def create_survey(headers, survey_name):
    # Create survey in SurveyMonkey
    url = f"{BASE_URL}/surveys"
    payload = {"title": survey_name}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def create_page(headers, survey_id, page_name):
    url = f"{BASE_URL}/surveys/{survey_id}/pages"
    payload = {"title": page_name}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def create_question(
    headers, survey_id, page_id, question_name, question_data, position
):
    url = f"{BASE_URL}/surveys/{survey_id}/pages/{page_id}/questions"

    choices = []
    for answer in question_data["Answers"]:
        choices.append({"text": answer})

    payload = {
        "headings": [{"heading": question_data["Description"]}],
        "family": "single_choice",
        "subtype": "vertical",
        "answers": {"choices": choices},
        "position": position,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def main():
    # Load environment variables from .env
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Create a SurveyMonkey survey from JSON file"
    )
    parser.add_argument("questions_file", help="Path to JSON file with questions")
    parser.add_argument("emails_file", help="Path to text file with recipient emails")
    args = parser.parse_args()

    token = os.getenv("SURVEY_TOKEN")
    if not token:
        print("Error: SURVEY_TOKEN not found in .env file")
        sys.exit(1)

    # Read input files
    questions_data = load_questions(args.questions_file)
    emails = load_emails(args.emails_file)

    # Validate input data
    survey_name, survey_pages = validate_data(questions_data, emails)

    # Prepare API authentication headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        # Create survey
        survey = create_survey(headers, survey_name)
        survey_id = survey["id"]
        print(f"Survey created successfully. Survey ID: {survey_id}")

        total_created_questions = 0

        # Create all pages and their questions
        for page_name, questions in survey_pages.items():
            page = create_page(headers, survey_id, page_name)
            page_id = page["id"]
            print(f"Page created successfully: {page_name} (Page ID: {page_id})")

            position = 1
            for question_name, question_data in questions.items():
                create_question(
                    headers, survey_id, page_id, question_name, question_data, position
                )
                print(f"Question added: {question_name}")
                position += 1
                total_created_questions += 1

        print()
        print("Survey creation completed successfully.")
        print(f"Accepted recipients from file: {len(emails)}")
        print(f"Pages created: {len(survey_pages)}")
        print(f"Questions created: {total_created_questions}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()