"""
Centralized logging setup for all training runs.

Creates two log files simultaneously:
  - results/logs/train_latest.log       : overwritten at each run — always the current one
  - results/logs/train_YYYYMMDD_HHMMSS.log : timestamped archive of each run

How to watch progress in real-time (Windows PowerShell):
    Get-Content results/logs/train_latest.log -Wait

How to check if training is done:
    Look for "TRAINING COMPLETE" or "ERROR" as the last line of train_latest.log
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

_LOGS_DIR = Path(__file__).resolve().parent.parent.parent / "results" / "logs"

# Sentinel strings written at start/end of every training run
SENTINEL_START = "=== TRAINING STARTED ==="
SENTINEL_SUCCESS = "=== TRAINING COMPLETE — SUCCESS ==="
SENTINEL_ERROR = "=== TRAINING FAILED — SEE ERROR ABOVE ==="

_FORMAT = "%(asctime)s [%(levelname)s] %(name)s — %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_training_logger(extra_name: str = "") -> tuple[logging.Logger, Path]:
    """
    Configure root logger to write to console + two log files.

    Call this once at the start of scripts/train_pipelines.py.

    Args:
        extra_name: Optional suffix for the timestamped filename (e.g. "pipeline_A").

    Returns:
        (root_logger, timestamped_log_path)
    """
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"_{extra_name}" if extra_name else ""
    ts_path = _LOGS_DIR / f"train_{timestamp}{suffix}.log"
    latest_path = _LOGS_DIR / "train_latest.log"

    formatter = logging.Formatter(_FORMAT, datefmt=_DATE_FORMAT)
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicates on re-import
    root.handlers.clear()

    # 1. Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    # 2. Timestamped file — permanent archive
    ts_handler = logging.FileHandler(ts_path, mode="w", encoding="utf-8")
    ts_handler.setFormatter(formatter)
    root.addHandler(ts_handler)

    # 3. train_latest.log — always the most recent run (overwritten)
    latest_handler = logging.FileHandler(latest_path, mode="w", encoding="utf-8")
    latest_handler.setFormatter(formatter)
    root.addHandler(latest_handler)

    root.info(SENTINEL_START)
    root.info("Log file (timestamped) : %s", ts_path)
    root.info("Log file (latest)      : %s", latest_path)
    root.info(
        "Watch in real-time (PowerShell) : "
        "Get-Content results/logs/train_latest.log -Wait"
    )

    return root, ts_path


def log_training_complete(logger: logging.Logger) -> None:
    """Write the success sentinel — last line of a successful training run."""
    logger.info(SENTINEL_SUCCESS)


def log_training_error(logger: logging.Logger, exc: Exception) -> None:
    """Write the error sentinel — last line of a failed training run."""
    logger.error("Exception: %s", exc, exc_info=True)
    logger.error(SENTINEL_ERROR)
