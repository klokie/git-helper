# Git AI Commit

AI-powered commit message generator that analyzes your git diff and suggests meaningful commit messages.

The script will:

1. Get the git diff of staged changes
2. Send the diff to OpenAI API
3. Generate a commit message
4. Let you accept/reject/edit the suggested message

## Requirements

- Python 3.8+
- OpenAI API key
- Git installed and configured

## Environment Variables

Create a `.env` file with your OpenAI API key:

```sh
OPENAI_API_KEY=sk-your-api-key-here
```

This key should start with `sk-` and can be generated in your [OpenAI dashboard](https://platform.openai.com/api-keys).

## Installation

1. Clone the repo

```sh
git clone https://github.com/klokie/git-helper
```

2. Install dependencies

```sh
pip install .
```

3. Set up environment variables

```sh
cp .env.example .env
```

4. Add your OpenAI API key to `.env`

5. Show usage

```sh
git_ai_commit
```

## Usage

Get commit message for staged changes:

```sh
git diff --staged | git_ai_commit
```

Or for all changes since last commit:

```sh
git diff HEAD | git_ai_commit
```

You can also provide the diff text directly:

```sh
git_ai_commit "diff --git a/file.txt b/file.txt ..."
```

Make an alias in your .zshrc or .shrc:

```sh
alias gac="git diff --staged | git_ai_commit"
```

## License

This project is open-sourced under the MIT License - see the [LICENSE](LICENSE) file for details.
