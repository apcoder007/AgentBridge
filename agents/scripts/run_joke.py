from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from agent_service.graph import invoke_joke  # noqa: E402


def main() -> None:
    topic = " ".join(sys.argv[1:]).strip() or "programming"
    result = invoke_joke(topic)

    print(f"Topic: {result['topic']}")
    print(f"Joke: {result['joke']}")
    print(f"Steps: {' -> '.join(result['steps'])}")


if __name__ == "__main__":
    main()
