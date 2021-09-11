#!/usr/bin/env python3
""" Counts the occurrances of a TEI element and adds the corresponding @n="{count}" """

import re
import sys

elementname = "note"


def count_and_add_n(lines: list) -> list:
    n = 0
    orig_pattern = re.compile(f"<{elementname} ")
    for line in lines:
        if re.search(orig_pattern, line):
            print(f"  {line = }")
            n += 1
            pattern = re.compile(f"(<{elementname} .+?>)")
            match = re.search(pattern, line)
            orig_element = match.group(1)  # make a copy of the original element
            print(f"  {orig_element =}")
            new_element = orig_element  # this is a working copy
            new_element = check_and_remove_n(new_element)
            new_element = add_correct_n(new_element, str(n))
            print(f"  {new_element = }")
            pattern = re.compile(new_element)
            newline = re.sub(orig_element, new_element, line)
            print(f"  {newline = }")


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


def main():
    num_args = len(sys.argv)
    inputfile = ""

    if num_args > 1:
        inputfile = sys.argv[1]
    else:
        print(f"Usage: python3 countteinotes file.xml")
        exit(1)
    
    if inputfile[-3:] != "xml":
        print(f"Usage: python3 countteinotes file.xml")
        exit(1)

    outputfile = inputfile[0:-4] + "_out.tex"


    with open(inputfile) as f:
        lines = f.readlines()
        count_and_add_n(lines)

    # lines = unindent(lines)
    # lines = rmmultispaces(lines)
    #
    # buffer = "".join(lines)
    #
    # outbuffer = cleanup(buffer)
    
    # with open(outputfile, "w") as f:
    #     f.write(outbuffer)


if __name__ == "__main__":
    main()
