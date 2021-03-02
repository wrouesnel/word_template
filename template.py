
import click
import docxtpl
import ruamel.yaml

@click.command()
@click.argument("template",nargs=1)
@click.argument("output",nargs=1)
@click.argument("inputs", nargs=-1)
def main():
    """Execute a Word document template to the output file, using the supplied inputs.

    Inputs may either be YAML files or exploded YAML folders.
    """

    

if __name__ == "__main__":
    main(auto_envvar_prefix="TEMPLATE")