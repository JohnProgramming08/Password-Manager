from services import Field


class FieldBridge:
    def __init__(self, args, vault_path="data/"):
        self.args = args
        self.vault_path = vault_path
        self.command = self.determine_function()

    # Determine which function to call based on the command
    def determine_function(self) -> str | None:
        args = self.args
        if not hasattr(args, "field"):
            return None

        # Field set [section_name] [field_name] [value]
        elif (
            hasattr(args, "set")
            and hasattr(args, "section_name")
            and hasattr(args, "field_name")
            and hasattr(args, "value")
        ):
            Field.set_field(
                self.args.section_name,
                self.args.field_name,
                self.args.value,
                vault_path=self.vault_path,
            )
            return "set"

        # Field get [section_name] [field_name]
        elif (
            hasattr(args, "get")
            and hasattr(args, "section_name")
            and hasattr(args, "field_name")
        ):
            value = Field.get_value(
                self.args.section_name,
                self.args.field_name,
                vault_path=self.vault_path,
            )
            if value is not None:
                print(value)
            return "get"

        # field ls [section_name]
        elif (
            hasattr(args, "ls")
            and hasattr(args, "section_name")
            and args.section_name
        ):
            list_output = Field.list_fields_in_section(
                args.section_name,
                values=args.values,
                vault_path=self.vault_path,
            )
            if list_output:
                print(list_output)

            return "ls section"

        # field ls
        elif hasattr(args, "ls"):
            list_output = Field.list_fields(
                values=args.values, vault_path=self.vault_path
            )
            if list_output:
                print(list_output)

            return "ls"

        # field rm [section_name] [field_name]
        elif hasattr(args, "rm") and args.section_name and args.field_name:
            Field.remove_field(
                args.section_name, args.field_name, vault_path=self.vault_path
            )
            return "rm"
