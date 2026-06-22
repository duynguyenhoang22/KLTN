import sys
import pytest

sys.path.insert(0, "src")
exit_code = pytest.main(["tests"])
sys.exit(exit_code)
