from interface.cli import get_arguments
from services import Config, Reader, Writer


def main():
    args = get_arguments()
    if args.command == "config":
        confg_service = Config()
        confg_service.init_config_file()

    elif args.command == "read" and None not in [args.section, args.field]:
        print(Reader.get_value(args.section, args.field))

    elif (
        args.command == "write"
        and args.subcommand == "section"
        and args.section is not None
    ):
        Writer.add_section(args.section)

    elif (
        args.command == "write"
        and args.subcommand == "field"
        and None not in [args.section, args.field, args.value]
    ):
        Writer.set_field(args.section, args.field, args.value)


if __name__ == "__main__":
    main()
