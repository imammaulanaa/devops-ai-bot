"""
CLI script to test AI code generation without going through the API.

Usage:
    python -m scripts.generate_code --prompt "Create a FastAPI CRUD API"
"""

import argparse
import sys

from dotenv import load_dotenv

load_dotenv()

from backend.services.ai_service import generate_code


def main():
    parser = argparse.ArgumentParser(description="Generate code using the AI service.")
    parser.add_argument("--prompt", required=True, help="Prompt for code generation")
    args = parser.parse_args()

    print(f"\n[*] Prompt: {args.prompt}\n")

    try:
        result = generate_code(args.prompt)
        print("=== GENERATED CODE ===\n")
        print(result)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
