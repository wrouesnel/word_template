# Jinja2 Templating for Word Documents

Simple wrapper utility implementing the `word-template` command which allows using Jinja2 and the
[docxtpl](https://docxtpl.readthedocs.io/en/latest/) library from th command line to template Word
documents. Check out the documentation for this library as it implements a few extensions which
make it more useful for working with Microsoft Word documents.

## Usage

```bash
word-template <template> <output> [inputs...]
```

Template should be a `docx` word document marked up with the Jinja2-formatting used by `docxtpl`.
Output is the name of the output file - this should have a `docx` suffix as it will be a `docx` file.

Inputs is a list of files or directories in either YAML or JSON format, or PNG graphics files to
insert images.

The underlying Jinja context is constructed from the file names and keys of the variables. For example
with the following directory structure:

```
context/
    just_some_text.txt
    file.json
    otherfile.yaml
    subdir/
        image1.png
    table_data/
        !!Sequence
        a
        b
        c
```

The resulting context would be referred to as:
* `context.file.<some key>` - return a key which is defined in the top level hash in `context/file.json`
* `context.subdir.image1` - return the image in `context/subdir/image1.png`, allowing it to be inserted by `docxtpl`
* `context.table_data` - return the contents of the directory as a Sequence type - i.e. a list. The order is determined
  by the lexical order of the filenames, and the !!Sequence file is ignored - it is used as a placeholder to activate
  this behavior.
* `context.just_some_text` - return just the contents of the `context/just_some_text.txt` file.

Note that the behavior of the context constructor is always to remove the last dotted extension fom files.
This is not done for directories, but you will cause problems if you insist on this (since it clases with Jinja syntax).

The general idea of the context constructor is to allow you to switch between laying out your structured data in the
directory structure (specifically for handling things like images) and laying out the data in structured YAML and JSON
files. If you need to insert YAML or JSON literally, the simply omitting the `.yaml`, `.yml` or `.json` extensions.

See [example/](example/) for a full example.
