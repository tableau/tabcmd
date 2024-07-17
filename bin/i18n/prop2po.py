"""
Updated from https://github.com/mivek/prop2po to handle encoding
License: MIT
TO DO: contribute changes back and go back to installing from pypi
"""

import click


@click.command()
@click.argument('source', type=click.File('rt', encoding='utf-8'))
@click.argument('destination', type=click.File('wt', encoding='utf-8'))
@click.option('-l', '--language', type=click.STRING, help='The translation language')
@click.option('-p', '--project', type=click.STRING, help='The name of the project')
@click.option('-e', '--encoding', type=click.STRING, help='The encoding wanted')
def to_po(source, destination, encoding, language, project):
    """Converts a property file to a Gettext PO file.

    SOURCE is the path of the property file to convert.

    DESTINATION is the path of the Gettext PO file to create
    """

    header = """msgid ""
msgstr ""
"MIME-Version: 1.0"
"Content-Type: text/plain; charset={encoding}"
"Content-Transfer-Encoding: 8bit"
"X-Generator: prop2po"
"Project-Id-Version: {project}"
"Language: {language}"
# Copyright (C) YEAR Tableau Software 
"""
    lines = source.readlines()
    destination.write(header.format(
        language=language,
        project=project,
        encoding=encoding
    ))
    for line in lines:
        if not line.isspace():
            parts = line.split('=')
            # TODO it fails on comments/lines with less than two parts after splitting
            try:
                destination.write('#:\n' + 'msgid "' + parts[0] + '"\n' 'msgstr "' + parts[1][:-1] + '"\n\n')
            except IndexError as e:
                print("FAILED on line{}".format(line))


if __name__ == '__main__':
    to_po()