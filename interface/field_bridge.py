from services import Field


class FieldBridge:
    def __init__(self, args):
        self.args = args
        self.determine_function()

    # Determine which function to call based on the command
    def determine_function(self):
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
                self.args.section_name, self.args.field_name, self.args.value
            )

        # Field get [section_name] [field_name]
        elif (
            hasattr(args, "get")
            and hasattr(args, "section_name")
            and hasattr(args, "field_name")
        ):
            print(Field.get_value(self.args.section_name, self.args.field_name))
