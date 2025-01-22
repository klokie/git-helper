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
OPENAI_API_KEY=your_api_key_here
```

This key can be generated in your [OpenAI dashboard](https://platform.openai.com/api-keys).

## Installation

1. Clone the repo

```bash
git clone [your-repo-url]
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

5. Run the script

```bash
python git-ai-commit.py
```
