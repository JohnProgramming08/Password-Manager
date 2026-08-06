import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["config", "write", "read"],
        help="specify the command you wish to use",
    )
    parser.add_argument(
        "--subcommand",
        choices=["field", "section"],
        help="specify whether a field or section is being written",
    )
    parser.add_argument(
        "-s", "--section", help="specify the name of the section"
    )
    parser.add_argument("-f", "--field", help="specify the name of the field")
    parser.add_argument("-v", "--value", help="specify the value of the field")

    args = parser.parse_args()
    return args
