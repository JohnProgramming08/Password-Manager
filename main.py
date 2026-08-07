from interface import CLI, ConfigBridge, SectionBridge, FieldBridge
from services import Config, Section, Field


def main():
    interface = CLI()
    args = interface.get_args()

    # Determine which subcommand was executed
    if hasattr(args, "config"):
        bridge = ConfigBridge(args)
    if hasattr(args, "section"):
        bridge = SectionBridge(args)
    if hasattr(args, "field"):
        bridge = FieldBridge(args)


if __name__ == "__main__":
    main()
