#!/usr/bin/env python3

import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def generate_commit_message(diff):
    """
    Sends the git diff to an AI API to generate a concise commit message.
    """
    client = OpenAI()  # Assumes OPENAI_API_KEY env var is set
    prompt = f"""
    Generate a concise, multi-line Git commit message based on this git diff:
    ```
    {diff}
    ```
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at writing concise git commit messages.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        if not response.choices or not response.choices[0].message.content:
            raise Exception("No response received from API")
        commit_message = response.choices[0].message.content.strip()
        return commit_message
    except Exception as e:
        sys.stderr.write(f"Error generating commit message: {e}\n")
        sys.exit(1)


def main():
    # Read the git diff from STDIN
    diff = sys.stdin.read().strip()
    if not diff:
        sys.stderr.write("Error: No git diff provided. Pipe a diff into this script.\n")
        sys.exit(1)

    # Generate the commit message
    commit_message = generate_commit_message(diff)
    print(commit_message)


if __name__ == "__main__":
    main()
