from __future__ import annotations

import argparse
import logging
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DEFAULT_PATHS


HEADER_LINE = "Date,Time,Direction,Contact,Phone,Content,Type"
EXPECTED_COLS = ["date", "time", "direction", "contact", "phone", "content", "type"]
CURRENCY_RE = re.compile(r"(\d[\d\s,.]*)\s*(?:XAF|FCFA|F)\b", re.IGNORECASE)
USER_ID_RE = re.compile(r"raw_user_(\d+)", re.IGNORECASE)
MESSAGE_EXPORT_RE = re.compile(
    r"Messages with MobileMoney (\d{4}-\d{2}-\d{2}) (\d{6})",
    re.IGNORECASE,
)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def find_data_files(directories: list[Path]) -> list[Path]:
    files: list[Path] = []
    for directory in directories:
        if not directory.exists():
            continue
        files.extend(sorted(directory.glob("*.csv")))
        files.extend(sorted(directory.glob("*.xlsx")))
    return files


def read_sms_export(file_path: Path) -> pd.DataFrame:
    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
        lines = handle.read().splitlines()

    start_idx = 0
    for idx, line in enumerate(lines):
        if line.strip() == HEADER_LINE:
            start_idx = idx
            break

    content = "\n".join(lines[start_idx:])
    df = pd.read_csv(pd.io.common.StringIO(content))
    df["source_file"] = file_path.name
    return df


def read_excel_export(file_path: Path) -> pd.DataFrame:
    df = pd.read_excel(file_path, header=None, dtype=str)
    header_idx = None
    for idx in range(len(df)):
        row = [normalize_header_value(val) for val in df.iloc[idx].tolist()]
        mapped_row = [normalize_column_map().get(val, val) for val in row]
        if mapped_row[: len(EXPECTED_COLS)] == EXPECTED_COLS:
            header_idx = idx
            break

    if header_idx is None:
        raise ValueError(f"Could not find header row in {file_path.name}")

    df = df.iloc[header_idx + 1 :].copy()
    df.columns = EXPECTED_COLS
    df = df[EXPECTED_COLS].copy()
    df = normalize_columns(df)
    df["source_file"] = file_path.name
    return df


def read_input_file(file_path: Path) -> pd.DataFrame:
    if file_path.suffix.lower() == ".xlsx":
        return read_excel_export(file_path)
    return read_sms_export(file_path)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [normalize_header_value(col) for col in df.columns]
    df = df.rename(columns=normalize_column_map())
    df = df.loc[:, ~df.columns.duplicated()]
    return df


def normalize_header_value(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"\s+", "_", text.strip().lower())
    text = re.sub(r"[^a-z0-9_]+", "", text)
    return text


def normalize_column_map() -> dict[str, str]:
    return {
        "date": "date",
        "time": "time",
        "heure": "time",
        "direction": "direction",
        "contact": "contact",
        "phone": "phone",
        "telephone": "phone",
        "contenu": "content",
        "content": "content",
        "type": "type",
    }


def derive_user_id(source_file: str) -> str:
    match = USER_ID_RE.search(source_file)
    if match:
        return f"user_{int(match.group(1)):02d}"
    match = MESSAGE_EXPORT_RE.search(source_file)
    if match:
        return f"msg_{match.group(1)}_{match.group(2)}"
    stem = Path(source_file).stem
    return re.sub(r"[^a-zA-Z0-9_]+", "_", stem).lower()


def parse_amount(text: str | float | int | None) -> float | None:
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return None
    match = CURRENCY_RE.search(str(text))
    if not match:
        return None
    raw = match.group(1).replace(" ", "").replace(",", "")
    try:
        return float(raw)
    except ValueError:
        return None


def classify_transaction(text: str | float | int | None) -> str:
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return "other"
    lowered = str(text).lower()
    if "solde" in lowered or "balance" in lowered:
        return "balance"
    if "adjustment" in lowered or "ajustement" in lowered:
        return "adjustment"
    if "recu" in lowered or "received" in lowered:
        return "receive"
    if "retrait" in lowered or "withdraw" in lowered:
        return "withdraw"
    if "transfert" in lowered or "transfer" in lowered:
        return "transfer"
    if "paiement" in lowered or "payment" in lowered:
        return "payment"
    return "other"


def build_interim_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    expected = {"date", "time", "direction", "contact", "phone", "content", "type"}
    missing = expected.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    df = df.copy()
    df["user_id"] = df["source_file"].apply(derive_user_id)
    df["datetime"] = pd.to_datetime(
        df["date"].astype(str) + " " + df["time"].astype(str),
        errors="coerce",
    )
    df["amount"] = df["content"].apply(parse_amount)
    df["transaction_type"] = df["content"].apply(classify_transaction)
    df["currency"] = "XAF"

    return df[
        [
            "source_file",
            "user_id",
            "date",
            "time",
            "datetime",
            "direction",
            "contact",
            "phone",
            "type",
            "transaction_type",
            "amount",
            "currency",
            "content",
        ]
    ]


def run_pipeline(raw_dirs: list[Path], output_path: Path) -> Path:
    input_files = find_data_files(raw_dirs)
    if not input_files:
        raise FileNotFoundError("No input files found in raw input directories.")

    frames: list[pd.DataFrame] = []
    for input_file in input_files:
        logging.info("Reading %s", input_file)
        frames.append(read_input_file(input_file))

    combined = pd.concat(frames, ignore_index=True)
    interim = build_interim_transactions(combined)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    interim.to_csv(output_path, index=False)
    logging.info("Saved interim transactions to %s", output_path)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build interim SMS transactions dataset.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_PATHS.interim_dir / "transactions_interim.csv",
        help="Output CSV path for interim transactions.",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()
    run_pipeline(DEFAULT_PATHS.raw_input_dirs, args.output)


if __name__ == "__main__":
    main()
