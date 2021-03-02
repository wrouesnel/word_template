from pathlib import Path
from typing import List, Any, Dict

import click
import docxtpl
import jinja2

from lib.yamlutil import read_yaml_dir, yaml


@click.command()
@click.argument("template",type=click.Path(exists=True, readable=True, dir_okay=False, path_type=str),nargs=1)
@click.argument("output",type=click.Path(exists=False, readable=True, dir_okay=False, path_type=str), nargs=1)
@click.argument("inputs", type=click.Path(exists=True, readable=True, dir_okay=True, path_type=str), nargs=-1)
def main(template: str, output: str, inputs: List[str]):
    """Execute a Word document template to the output file, using the supplied inputs.

    Inputs may either be YAML files or exploded YAML folders.
    """

    doc = docxtpl.DocxTemplate(template)

    # Check context files make sense
    context: Dict[str,Any] = {}
    for input in inputs:
        input = Path(input)
        if input.is_dir():
            context[input.name] = read_yaml_dir(input)
        else:
            with input.open("rt") as f:
                context[input.name] = yaml.load(f)

    jinja_env = jinja2.Environment()

    doc.render(context=context, jinja_env=jinja_env)
    doc.save(output)

if __name__ == "__main__":
    main(auto_envvar_prefix="TEMPLATE")