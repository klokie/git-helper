import os
import sys
from dotenv import load_dotenv
from openai import OpenAI


def is_interactive():
    return sys.stdin.isatty()


def main():
    load_dotenv()

    # Parse args
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    # Show usage if no input provided
    if len(args) == 0 and sys.stdin.isatty():
        print("Usage: git-smart [options] [diff]")
        print("Generate AI commit messages from git diffs")
        print("\nOptions:")
        print("  -v, --verbose  Show additional output")
        print("\nExamples:")
        print("  git diff | git-smart")
        print('  git-smart "$(git diff)"')
        sys.exit(1)

    # Get diff from stdin or command line arg
    if args:
        diff = args[0]
    else:
        try:
            diff = sys.stdin.read()
        except:
            print("Error reading from stdin")
            sys.exit(1)

    if not diff:
        print("No diff provided. Stage some changes or pipe a diff.")
        sys.exit(1)

    # Get system prompt
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts.md")
    try:
        with open(prompt_path) as f:
            system_prompt = f.read().split("\n\n", 1)[1].strip()
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        sys.exit(1)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Generate commit message
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"Generate a commit message for this diff:\n\n{diff}",
            },
        ],
    )

    suggested_message = response.choices[0].message.content
    if verbose:
        print("\nSuggested commit message:")
    print(suggested_message)

    # In non-interactive mode, just print the message and exit
    if not is_interactive():
        return

    # Get user input in interactive mode
    while True:
        try:
            if verbose:
                choice = input("\nAccept (a), edit (e), or reject (r)? ").lower()
            else:
                choice = input("\n(a)ccept/(e)dit/(r)eject? ").lower()
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
