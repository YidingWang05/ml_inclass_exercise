"""Report Section A's missing-entry percentages without modifying the data."""

import argparse
import csv
from pathlib import Path


MISSING_MARKERS = {"", "nan", "na", "n/a", "null", "none", "<na>", "#n/a"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent / "data" / "q1.csv",
        help="CSV file to inspect (default: data/q1.csv beside this script).",
    )
    args = parser.parse_args()
    try:
        with args.csv_path.expanduser().open(encoding="utf-8-sig", newline="") as file:
            reader = csv.reader(file)
            columns = next(reader, [])
            missing_counts = [0] * len(columns)
            row_count = 0
            for row in reader:
                if not row:
                    continue
                if len(row) != len(columns):
                    raise ValueError(f"CSV line {reader.line_num} has an unexpected number of fields")
                row_count += 1
                for index, value in enumerate(row):
                    missing_counts[index] += value.strip().lower() in MISSING_MARKERS
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"Could not read CSV: {error}\n")
    if not row_count or not columns:
        parser.exit(1, "The CSV has no data rows; percentages are undefined.\n")

    width = max(map(len, columns))
    for column, count in zip(columns, missing_counts):
        print(f"{column:<{width}}  {100 * count / row_count:.2f}%")


if __name__ == "__main__":
    main()
