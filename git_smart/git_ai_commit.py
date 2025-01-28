import os
import sys
from dotenv import load_dotenv
from openai import OpenAI


def is_interactive():
    return sys.stdin.isatty()


def main():
    load_dotenv()

    # Get diff from stdin or command line arg
    if len(sys.argv) > 1:
        diff = sys.argv[1]
    else:
        diff = sys.stdin.read()

    if not diff:
        print("No diff provided. Stage some changes or pipe a diff.")
        sys.exit(1)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Generate commit message
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates git commit messages. Generate a concise, meaningful commit message based on the git diff provided.",
            },
            {
                "role": "user",
                "content": f"Generate a commit message for this diff:\n\n{diff}",
            },
        ],
    )

    suggested_message = response.choices[0].message.content
    print(f"\nSuggested commit message:\n{suggested_message}")

    # In non-interactive mode, just print the message and exit
    if not is_interactive():
        return

    # Get user input in interactive mode
    while True:
        try:
            choice = input("\nAccept (a), edit (e), or reject (r)? ").lower()
            if choice == "a":
                print(suggested_message)
                break
            elif choice == "e":
                edited = input("Enter your edited message: ")
                print(edited)
                break
            elif choice == "r":
                print("Message rejected")
                break
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled")
            sys.exit(1)


if __name__ == "__main__":
    main()
