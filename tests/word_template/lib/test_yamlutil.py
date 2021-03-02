from pathlib import Path

from word_template.lib.yamlutil import read_yaml_dir


def test_read_yaml_dir(root_dir: Path):
    result = read_yaml_dir(root_dir / "example")
    pass
