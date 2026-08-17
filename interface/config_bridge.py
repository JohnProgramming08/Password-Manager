from services import Config


class ConfigBridge:
    def __init__(self, args, config_path="data/config.json"):
        self.args = args
        self.config_path = config_path
        self.command = self.determine_function()

    # Determine which function to call based on the command
    def determine_function(self) -> str | None:
        args = self.args
        if not hasattr(args, "config"):
            return None

        # Config init
        if hasattr(args, "init"):
            config_service = Config(config_path=self.config_path)
            config_service.init_config_file()
            return "init"

        # config password attempt_limit [limit_value]
        elif hasattr(args, "attempt_limit") and hasattr(args, "limit_value"):
            config_service = Config(config_path=self.config_path)
            config_service.set_attempt_limit(args.limit_value)
            return "attempt_limit"

        # config email [email_value]
        elif hasattr(args, "email") and args.email_value:
            config_service = Config(config_path=self.config_path)
            config_service.set_email(args.email)
            return "email"
