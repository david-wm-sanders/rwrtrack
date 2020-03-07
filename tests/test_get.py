import pytest
from pathlib import Path


data_dir = Path(__file__).parent / "data"


@pytest.fixture
def load_file():
    def _load_file(file_path):
        with file_path.open("r", encoding="utf-8") as f:
            data = f.read()
        return data

    return _load_file


def test_request_stats():
    from rwrtrack.get import request_stats
    # TODO: mock a requests Response to test this
    pass


def test_extract_rows_blank(load_file):
    from rwrtrack.get import extract_rows
    html = load_file(data_dir / "stats_blank.html")
    rows = extract_rows(html)
    # Check that, when the table is empty, extract_rows returns an empty list
    assert rows == []


def test_extract_rows(load_file):
    from rwrtrack.get import extract_rows
    html = load_file(data_dir / "stats_20200306.html")
    rows = extract_rows(html)
    # Check that extract_rows has extracted the correct number of rows
    assert len(rows) == 10
    for row in rows:
        # Check each row is a HTML tr
        assert row.name == "tr"
        # Check each row has 18 elements within it
        contents = [c for c in row.contents if c != "\n"]
        assert len(contents) == 18


def test_convert_tp_to_mins():
    from rwrtrack.get import convert_tp_to_mins
    assert convert_tp_to_mins("4h 20min") == 260
    assert convert_tp_to_mins("0h 5min") == 5
    assert convert_tp_to_mins("1h 0min") == 60
    with pytest.raises(ValueError, match="not enough values to unpack"):
        convert_tp_to_mins("")
    # TODO: add more break cases and then fix code to improve handling of these cases


def test_convert_dm_to_metres():
    from rwrtrack.get import convert_dm_to_metres
    assert convert_dm_to_metres("2.5km") == 2500
    assert convert_dm_to_metres("2.0km") == 2000
    assert convert_dm_to_metres("0.5km") == 500
    assert convert_dm_to_metres("0.0km") == 0
    # TODO: add some break cases


def test_extract_stats():
    from rwrtrack.get import extract_stats
    # TODO: implement tests
    pass


def test_get_stats():
    from rwrtrack.get import get_stats
    # TODO: implement tests
    pass
