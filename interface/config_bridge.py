from services import Config


class ConfigBridge:
    def __init__(self, args):
        self.args = args
        self.determine_function()

    # Determine which function to call based on the command
    def determine_function(self):
        args = self.args
        # Config init
        if hasattr(args, "config") and args.command == "init":
            config_service = Config()
            config_service.init_config_file()
