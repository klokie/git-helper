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

```bash
OPENAI_API_KEY=sk-your-api-key-here
```

This key should start with `sk-` and can be generated in your [OpenAI dashboard](https://platform.openai.com/api-keys).

## Installation

1. Clone the repo

```bash
git clone https://github.com/klokie/git-helper
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set up environment variables

```bash
cp .env.example .env
```

4. Add your OpenAI API key to `.env`

5. Show usage

```bash
python git-ai-commit.py
```

## Usage

Get commit message for staged changes:

```bash
git diff --staged | ./git-ai-commit.py
```

Or for all changes since last commit:

```bash
git diff HEAD | ./git-ai-commit.py
```

You can also provide the diff text directly:

```bash
./git-ai-commit.py "diff --git a/file.txt b/file.txt ..."
```

Make an alias in your .zshrc or .bashrc:

```bash
alias gac="git diff --staged | python git-ai-commit.py"
```

## License

This project is open-sourced under the MIT License - see the [LICENSE](LICENSE) file for details.
