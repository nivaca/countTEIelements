#!/usr/bin/env python3
""" Counts the occurrances of a TEI element and adds the corresponding @n="{count}" """

import re
import sys
import click


def check_if_needed(lines: list, elementname: str) -> bool:
    match = False
    orig_pattern = re.compile(f"<{elementname} ")
    for line in lines:
        if re.search(orig_pattern, line):
            match = True
    return match


def count_and_add_n(lines: list, elementname: str) -> list[list, int]:
    n = 0
    newlines: list[str] = []
    orig_pattern = re.compile(f"<{elementname} ")
    for line in lines:
        if re.search(orig_pattern, line):
            n += 1
            pattern = re.compile(f"(<{elementname} .+?>)")
            match = re.search(pattern, line)
            orig_element = match.group(1)  # make a copy of the original element
            new_element = orig_element  # this is a working copy
            new_element = check_and_remove_n(new_element)
            new_element = add_correct_n(new_element, str(n))
            line = re.sub(orig_element, new_element, line)
        newlines.append(line)
    return [newlines, n]


def check_and_remove_n(element: str) -> str:
    """ Checks if element has @n and if so removes it.
    Also cleanups the spaces. """
    if check_if_has_n(element):
        element = delete_existing_n(element)
    return element


def add_correct_n(element: str, nstring: str) -> str:
    pattern = re.compile(r'(<note .+)>')
    match = re.search(pattern, element)
    element: str = match.group(1)
    tail: str = f' n="{nstring}">'
    return element + tail


def check_if_has_n(element: str) -> bool:
    patterns = [re.compile(r'n="\d+"'),
                re.compile(r"n='\d+'")]
    has_pattern = False
    for pattern in patterns:
        if re.search(pattern, element):
            has_pattern = True
    return has_pattern


def delete_existing_n(element: str) -> str:
    patterns = [re.compile(r'n="\d+"'),
                re.compile(r"n='\d+'")]
    for pattern in patterns:
        if re.search(pattern, element):
            element = re.sub(pattern, "", element)
            element = cleanup_element(element)
            return element


def cleanup_element(element: str) -> str:
    """ Removes the multiple spaces and
    a sigle space before closing > """
    patterns = [(re.compile(r' +>'), '>'),
                (re.compile(r' {2,}]'), ' ')]
    for pattern in patterns:
        element = re.sub(pattern[0], pattern[1], element)
    return element


@click.command()
@click.option('--dry', default=False, help='Dry run (do not make any changes).')
@click.option('--elementname', default="note", help='XML element to be counted.')
@click.argument('inputfile')
def main(inputfile: str, elementname: str, dry: bool):
    # num_args = len(sys.argv)
    # inputfile = ""
    # if num_args > 1:
    #     inputfile = sys.argv[1]
    # else:
    #     print(f"Usage: python3 countteinotes file.xml")
    #     exit(1)
    #

    if inputfile[-3:] != "xml":
        print(f"{inputfile} is not an XML file. Aborting...")
        sys.exit(1)

    # outputfile = inputfile[0:-4] + "_out.xml"

    with open(inputfile) as f:
        lines = f.readlines()
        if not check_if_needed(lines, elementname):
            print(f"{inputfile} doesn't contain element <{elementname}>. Aborting...")
            sys.exit(1)
        outlist = count_and_add_n(lines, elementname)
        newlines = outlist[0]
        numchanges = outlist[1]

    if dry:
        print(f"  Dry run:")
        print(f"  {numchanges} instances of <{elementname}> would have been overwritten in {inputfile}.")
    else:
        with open(inputfile, "w") as f:
            f.writelines(newlines)
            print(f"  {numchanges} instances of <{elementname}> were overwritten in {inputfile}.")


if __name__ == "__main__":
    main()
