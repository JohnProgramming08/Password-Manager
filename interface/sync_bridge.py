from services import Sync


class SyncBridge:
    def __init__(self, args, config_path="data/config.json"):
        self.args = args
        self.config_path = config_path
        self.vault_path = config_path.split("/")[0]
        self.command = self.determine_function()

    def determine_function(self) -> str | None:
        args = self.args
        if not hasattr(args, "sync"):
            return None

        # sync push
        if hasattr(args, "push"):
            sync = Sync("http://127.0.0.1:8000", vault_path=self.vault_path)
            sync.push()
            return "push"

        elif hasattr(args, "pull"):
            sync = Sync("http://127.0.0.1:8000", vault_path=self.vault_path)
            sync.pull()
            return "pull"
