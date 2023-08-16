import pathlib

import pytest


@pytest.fixture
def sample_text_file(tmp_path: pathlib.Path) -> pathlib.Path:
    example_file = tmp_path / "temp-example.txt"
    example_file.write_text("just some example text here")
    return example_file


LOCAL_RESOURCES_DIR = pathlib.Path(__file__).parent / "resources"
