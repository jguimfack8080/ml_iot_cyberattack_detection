"""Unit tests for src.main (CLI entry point)."""
import sys
import pytest


class TestParseArgs:
    def test_default_pipeline_is_both(self) -> None:
        from src.main import parse_args
        args = parse_args.__wrapped__() if hasattr(parse_args, "__wrapped__") else None
        # Use sys.argv patching instead
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py", "--train"]
        try:
            from src.main import parse_args
            args = parse_args()
            assert args.pipeline == "both"
        finally:
            sys.argv = old_argv

    def test_pipeline_a_accepted(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py", "--train", "--pipeline", "A"]
        try:
            from src.main import parse_args
            args = parse_args()
            assert args.pipeline == "A"
        finally:
            sys.argv = old_argv

    def test_pipeline_b_accepted(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py", "--train", "--pipeline", "B"]
        try:
            from src.main import parse_args
            args = parse_args()
            assert args.pipeline == "B"
        finally:
            sys.argv = old_argv

    def test_invalid_pipeline_raises(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py", "--train", "--pipeline", "C"]
        try:
            from src.main import parse_args
            with pytest.raises(SystemExit):
                parse_args()
        finally:
            sys.argv = old_argv

    def test_train_flag_default_false(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py"]
        try:
            from src.main import parse_args
            args = parse_args()
            assert args.train is False
        finally:
            sys.argv = old_argv

    def test_evaluate_flag_default_false(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py"]
        try:
            from src.main import parse_args
            args = parse_args()
            assert args.evaluate is False
        finally:
            sys.argv = old_argv

    def test_explain_flag_default_false(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py"]
        try:
            from src.main import parse_args
            args = parse_args()
            assert args.explain is False
        finally:
            sys.argv = old_argv


class TestMain:
    def test_main_no_action_returns_1(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py"]
        try:
            from src.main import main
            result = main()
            assert result == 1
        finally:
            sys.argv = old_argv

    def test_main_with_train_flag_returns_0(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py", "--train"]
        try:
            from src.main import main
            result = main()
            assert result == 0
        finally:
            sys.argv = old_argv

    def test_main_with_evaluate_flag_returns_0(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py", "--evaluate"]
        try:
            from src.main import main
            result = main()
            assert result == 0
        finally:
            sys.argv = old_argv

    def test_main_with_explain_flag_returns_0(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py", "--explain"]
        try:
            from src.main import main
            result = main()
            assert result == 0
        finally:
            sys.argv = old_argv
