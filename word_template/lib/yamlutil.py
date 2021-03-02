from collections import Sequence, Mapping
from os import PathLike
from pathlib import Path
from typing import Dict, Any, List, Union

import ruamel.yaml


class YamlUtilError(Exception):
    pass


class YamlExploderError(YamlUtilError):
    pass


class YamlImploderError(YamlUtilError):
    pass


SEQUENCE_FILE = "!!Sequence"


yaml = ruamel.yaml.YAML(typ="rt")
yaml.constructor.yaml_constructors[
    "tag:yaml.org,2002:timestamp"
] = yaml.constructor.yaml_constructors["tag:yaml.org,2002:str"]


def read_yaml_dir(dname: PathLike) -> Union[List[Any], Dict[str, Any]]:
    """
    Read a directory structure as though it was a YAML file and return the contained
    object.

    :param dname: path-like object pointing to a directory to read.
    :return: Dictionary of the inferred YAML from the file tree.
    """

    dpath = Path(dname)

    if not dpath.is_dir():
        raise YamlImploderError(f"{dname} is not a directory.")

    if (dpath / SEQUENCE_FILE).exists():
        result: List[Any] = []
        # This directory is a sequence. Respect lexical order.
        for subpath in dpath.iterdir():
            if subpath.is_dir():
                result.append(read_yaml_dir(subpath))
            elif subpath.is_file():
                if subpath.name == SEQUENCE_FILE:
                    continue
                else:
                    pchunks = subpath.name.rsplit(".", 1)
                    if len(pchunks) == 2:
                        if pchunks[1] in ("yaml", "yml", "json"):
                            # This is a yaml file containing list element content.
                            with subpath.open("rt") as f:
                                result.append(yaml.load(f))
                            continue
                    with subpath.open("rt") as f:
                        result.append(f.read())
        return result
    else:
        result: Dict[str, Any] = {}
        for subpath in dpath.iterdir():
            if subpath.is_dir():
                result[subpath.name] = read_yaml_dir(subpath)
            else:
                pchunks = subpath.name.rsplit(".", 1)
                if len(pchunks) == 2:
                    if pchunks[1] in ("yaml", "yml", "json"):
                        # This is a yaml file containing list element content.
                        with subpath.open("rt") as f:
                            result[pchunks[0]] = yaml.load(f)
                        continue
                with subpath.open("rt") as f:
                    result[subpath.name] = f
        return result


def write_yaml_dir(dname: PathLike, obj: Union[List[Any], Dict[str, Any]]):
    """
    Write an object as an exploded YAML directory.
    :param dname: directory to start outputting into
    :param obj: object to start writing
    :return:
    """
    dpath = Path(dname)

    if not dpath.is_dir():
        raise YamlExploderError(f"{dname} is not a directory.")

    for k, v in enumerate(obj) if isinstance(obj, Sequence) else obj.items():
        k = str(k)
        e_outpath = dpath / k
        if isinstance(v, Sequence):
            e_outpath.mkdir()
            (e_outpath / SEQUENCE_FILE).touch(exist_ok=True)
            write_yaml_dir(e_outpath, k)
        elif isinstance(v, Mapping):
            e_outpath.mkdir()
            write_yaml_dir(e_outpath, k)
        else:
            e_outpath.write_text(str(obj))
