"""Unit tests for src.utils.logger."""
import logging
from pathlib import Path


class TestSetupTrainingLogger:
    def test_returns_tuple_logger_and_path(self, tmp_path, monkeypatch) -> None:
        from src.utils import logger as log_module
        monkeypatch.setattr(log_module, "_LOGS_DIR", tmp_path)
        root, ts_path = log_module.setup_training_logger()
        assert isinstance(root, logging.Logger)
        assert isinstance(ts_path, Path)

    def test_creates_timestamped_log_file(self, tmp_path, monkeypatch) -> None:
        from src.utils import logger as log_module
        monkeypatch.setattr(log_module, "_LOGS_DIR", tmp_path)
        _, ts_path = log_module.setup_training_logger()
        assert ts_path.exists()

    def test_creates_latest_log_file(self, tmp_path, monkeypatch) -> None:
        from src.utils import logger as log_module
        monkeypatch.setattr(log_module, "_LOGS_DIR", tmp_path)
        log_module.setup_training_logger()
        assert (tmp_path / "train_latest.log").exists()

    def test_extra_name_appears_in_filename(self, tmp_path, monkeypatch) -> None:
        from src.utils import logger as log_module
        monkeypatch.setattr(log_module, "_LOGS_DIR", tmp_path)
        _, ts_path = log_module.setup_training_logger("mytest")
        assert "mytest" in ts_path.name

    def test_sentinel_start_written_to_log(self, tmp_path, monkeypatch) -> None:
        from src.utils import logger as log_module
        monkeypatch.setattr(log_module, "_LOGS_DIR", tmp_path)
        log_module.setup_training_logger("sentinel_test")
        content = (tmp_path / "train_latest.log").read_text(encoding="utf-8")
        assert log_module.SENTINEL_START in content

    def test_multiple_calls_do_not_duplicate_handlers(self, tmp_path, monkeypatch) -> None:
        from src.utils import logger as log_module
        monkeypatch.setattr(log_module, "_LOGS_DIR", tmp_path)
        log_module.setup_training_logger("dup1")
        _, _ = log_module.setup_training_logger("dup2")
        root = logging.getLogger()
        # setup_training_logger clears handlers each time, so count must be exactly 3
        assert len(root.handlers) == 3


class TestLogTrainingComplete:
    def test_writes_success_sentinel(self, tmp_path, monkeypatch) -> None:
        from src.utils import logger as log_module
        monkeypatch.setattr(log_module, "_LOGS_DIR", tmp_path)
        root, _ = log_module.setup_training_logger("complete_test")
        log_module.log_training_complete(root)
        content = (tmp_path / "train_latest.log").read_text(encoding="utf-8")
        assert log_module.SENTINEL_SUCCESS in content


class TestLogTrainingError:
    def test_writes_error_sentinel(self, tmp_path, monkeypatch) -> None:
        from src.utils import logger as log_module
        monkeypatch.setattr(log_module, "_LOGS_DIR", tmp_path)
        root, _ = log_module.setup_training_logger("error_test")
        log_module.log_training_error(root, ValueError("test error"))
        content = (tmp_path / "train_latest.log").read_text(encoding="utf-8")
        assert log_module.SENTINEL_ERROR in content

    def test_writes_exception_message(self, tmp_path, monkeypatch) -> None:
        from src.utils import logger as log_module
        monkeypatch.setattr(log_module, "_LOGS_DIR", tmp_path)
        root, _ = log_module.setup_training_logger("error_msg_test")
        log_module.log_training_error(root, RuntimeError("something broke"))
        content = (tmp_path / "train_latest.log").read_text(encoding="utf-8")
        assert "something broke" in content
