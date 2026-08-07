from services import Section


class SectionBridge:
    def __init__(self, args):
        self.args = args
        self.determine_function()

    # Determine which function to call based on the command
    def determine_function(self):
        args = self.args

        # Create section [section_name]
        if (
            hasattr(args, "section")
            and hasattr(args, "create")
            and hasattr(args, "section_name")
        ):
            Section.add_section(self.args.section_name)
