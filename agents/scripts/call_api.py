import argparse

import httpx


def main() -> None:
    parser = argparse.ArgumentParser(description="Call the joke agent API.")
    parser.add_argument("topic", nargs="+", help="Topic for the joke")
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000",
        help="Base URL of the joke agent API",
    )
    args = parser.parse_args()

    response = httpx.post(
        f"{args.url.rstrip('/')}/v1/invoke",
        json={"message": " ".join(args.topic)},
        timeout=60,
    )
    response.raise_for_status()
    print(response.json()["response"])


if __name__ == "__main__":
    main()
