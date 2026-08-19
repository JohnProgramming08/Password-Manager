from interface import CLI, ConfigBridge, SectionBridge, FieldBridge, SyncBridge
from services import Config, Section, Field
import logging


def main():
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    interface = CLI()
    args = interface.get_args()

    # Determine which subcommand was executed
    if hasattr(args, "config"):
        bridge = ConfigBridge(args)
    if hasattr(args, "section"):
        bridge = SectionBridge(args)
    if hasattr(args, "field"):
        bridge = FieldBridge(args)
    if hasattr(args, "sync"):
        bridge = SyncBridge(args)


if __name__ == "__main__":
    main()
