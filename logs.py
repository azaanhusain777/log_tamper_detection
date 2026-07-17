import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path(__file__).with_name("data.json")
HASH_FIELDS = ("index", "timestamp", "message", "previous_hash")


def calc_hash(index, timestamp, message, previous_hash):
    data = str(index) + timestamp + message + previous_hash
    return hashlib.sha256(data.encode()).hexdigest()


def load_logs():
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r") as f:
        return json.load(f)


def save_logs(logs):
    with DATA_FILE.open("w") as f:
        json.dump(logs, f, indent=4)


def create_log(message, logs):
    index = len(logs) + 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    previous_hash = "0" if not logs else logs[-1]["current_hash"]
    current_hash = calc_hash(index, timestamp, message, previous_hash)

    return {
        "index": index,
        "timestamp": timestamp,
        "message": message,
        "previous_hash": previous_hash,
        "current_hash": current_hash,
    }


def add_logs(count):
    if count <= 0:
        print("Count must be greater than 0.")
        return

    issues = verify_logs()
    if issues:
        print("Cannot add new logs because tampering was detected:")
        for issue in issues:
            print(f"- {issue}")
        return

    logs = load_logs()

    for number in range(1, count + 1):
        message = input(f"Enter log entry {number}: ")
        logs.append(create_log(message, logs))

    save_logs(logs)
    print(f"{count} log entry added successfully.")


def verify_logs():
    try:
        logs = load_logs()
    except json.JSONDecodeError as error:
        return [f"data.json is not valid JSON: {error}"]

    issues = []
    expected_previous_hash = "0"

    for position, log in enumerate(logs, start=1):
        missing_fields = [
            field for field in (*HASH_FIELDS, "current_hash") if field not in log
        ]
        if missing_fields:
            issues.append(
                f"Entry {position} is missing field(s): {', '.join(missing_fields)}"
            )
            continue

        if log["previous_hash"] != expected_previous_hash:
            issues.append(
                "Entry "
                f"{position} has an invalid previous_hash. "
                f"Expected {expected_previous_hash}, found {log['previous_hash']}."
            )

        recalculated_hash = calc_hash(
            log["index"], log["timestamp"], log["message"], log["previous_hash"]
        )
        if log["current_hash"] != recalculated_hash:
            issues.append(
                "Entry "
                f"{position} was tampered with. "
                f"Expected current_hash {recalculated_hash}, "
                f"found {log['current_hash']}."
            )

        expected_previous_hash = log["current_hash"]

    return issues


def print_verification_result():
    issues = verify_logs()

    if not issues:
        print("No tampering detected. Log file is valid.")
        return

    print("Tampering detected:")
    for issue in issues:
        print(f"- {issue}")


def interactive_menu():
    while True:
        print("\n1. Add logs")
        print("2. Verify tamper detection")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                count = int(input("How many log entries do you want to add? "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            add_logs(count)
        elif choice == "2":
            print_verification_result()
        elif choice == "3":
            break
        else:
            print("Invalid option.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Add log entries and detect tampering using SHA-256 hash chaining."
    )
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add log entries")
    add_parser.add_argument(
        "-c", "--count", type=int, default=1, help="Number of log entries to add"
    )

    subparsers.add_parser("verify", help="Check data.json for tampering")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == "add":
        add_logs(args.count)
    elif args.command == "verify":
        print_verification_result()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
