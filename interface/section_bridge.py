from services import Section


class SectionBridge:
    def __init__(self, args):
        self.args = args
        self.command = self.determine_function()

    # Determine which function to call based on the command
    def determine_function(self) -> str | None:
        args = self.args
        if not hasattr(args, "section"):
            return None

        # Section create [section_name]
        if hasattr(args, "create") and hasattr(args, "section_name"):
            Section.add_section(args.section_name)
            return "create"

        # section ls
        elif hasattr(args, "ls"):
            print(Section.list_sections())
            return "ls"
