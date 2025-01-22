#!/usr/bin/env python3

import sys
import os
from openai import OpenAI

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(env_path):
    sys.stderr.write(f"Error: .env file not found at {env_path}\n")
    sys.exit(1)

with open(env_path) as f:
    env_content = f.read().strip()
    os.environ["OPENAI_API_KEY"] = env_content.split("=", 1)[1].strip().strip('"')

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("your_"):
    sys.stderr.write("Error: Invalid OPENAI_API_KEY in .env file\n")
    sys.exit(1)


def generate_commit_message(diff):
    """
    Sends the git diff to an AI API to generate a concise commit message.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.stderr.write("Error: OPENAI_API_KEY not found in environment variables\n")
        sys.exit(1)
    api_key = api_key.strip('"')  # Remove any quotes from the key

    client = OpenAI(api_key=api_key)
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
    # Check if running interactively without pipe
    if sys.stdin.isatty() and len(sys.argv) == 1:
        sys.stderr.write("""
Error: No git diff provided.

Usage:
    git diff --staged | python git-ai-commit.py
    # or
    git diff HEAD | python git-ai-commit.py
    # or
    python git-ai-commit.py "<diff text>"
""")
        sys.exit(1)

    # Read the git diff from STDIN or args
    if len(sys.argv) > 1:
        diff = " ".join(sys.argv[1:])
    else:
        diff = sys.stdin.read().strip()

    if not diff:
        sys.stderr.write("Error: Empty diff provided\n")
        sys.exit(1)

    # Generate the commit message
    commit_message = generate_commit_message(diff)
    print(commit_message)


if __name__ == "__main__":
    main()
