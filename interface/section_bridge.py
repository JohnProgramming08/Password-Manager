from services import Section


class SectionBridge:
    def __init__(self, args, vault_path="data/"):
        self.args = args
        self.vault_path = vault_path
        self.command = self.determine_function()

    # Determine which function to call based on the command
    def determine_function(self) -> str | None:
        args = self.args
        if not hasattr(args, "section"):
            return None

        # Section create [section_name]
        if hasattr(args, "create") and hasattr(args, "section_name"):
            Section.add_section(args.section_name, vault_path=self.vault_path)
            return "create"

        # section ls
        elif hasattr(args, "ls"):
            print(Section.list_sections(vault_path=self.vault_path))
            return "ls"

        # section rm [section_name]
        elif hasattr(args, "rm") and args.section_name:
            Section.remove_section(
                args.section_name, vault_path=self.vault_path
            )
            return "rm"
