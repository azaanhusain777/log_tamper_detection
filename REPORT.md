# Log Tamper Detection Using SHA-256

## Overview

This project implements a simple tamper detection system for log files using SHA-256 hashing. Each log entry is stored in `data.json` with its own hash and the hash of the previous entry. This creates a basic hash chain, similar to the idea used in blockchains, where changing one record breaks the chain from that point onward.

The main script is `logs.py`. It can add new log entries and verify whether the stored logs have been modified.

## How It Works

Each log entry contains:

- `index`: position of the log entry
- `timestamp`: time when the entry was created
- `message`: actual log message
- `previous_hash`: hash of the previous log entry
- `current_hash`: SHA-256 hash of the current entry

The hash is calculated using:

```text
SHA256(index + timestamp + message + previous_hash)
```

For the first log entry, `previous_hash` is set to `0`. For every next entry, `previous_hash` is copied from the previous entry's `current_hash`.

## Tamper Detection Logic

During verification, the program reads all entries from `data.json` and recalculates the hash for each entry. It then compares the recalculated hash with the stored `current_hash`.

The program reports tampering if:

- a log message, timestamp, index, or previous hash was changed
- a stored `current_hash` does not match the recalculated hash
- the `previous_hash` of an entry does not match the actual hash of the entry before it
- required fields are missing from any log entry
- `data.json` is not valid JSON

This means even a small manual edit in the file can be detected.

## Usage

To verify the log file:

```bash
python3 logs.py verify
```

To add new log entries:

```bash
python3 logs.py add --count 3
```

The script also supports an interactive menu:

```bash
python3 logs.py
```

Before adding new logs, the program verifies the existing file. If tampering is already detected, it refuses to append new entries. This avoids extending a corrupted chain.

## Files Used

- `logs.py`: main program for adding logs and checking tampering
- `data.json`: stores all log entries and their hashes

## Limitations

This project detects modification, but it does not prevent someone from editing both the log data and all hashes manually. For stronger protection, the latest trusted hash should be stored somewhere separate, such as a secure server, database, or signed file.


