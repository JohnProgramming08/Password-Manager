import argparse


class CLI:
    # Top level parser
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.subparsers = self.parser.add_subparsers(help="subcommand help")
        self.init_config_parser()
        self.init_config_init_parser()
        self.init_config_password()
        self.init_config_password_attempt_limit_parser()
        self.init_section_parser()
        self.init_section_create_parser()
        self.init_section_list_parser()
        self.init_section_remove_parser()
        self.init_field_parser()
        self.init_field_set_parser()
        self.init_field_get_parser()
        self.init_field_list_parser()
        self.init_field_remove_parser()
        self.args = self.parser.parse_args()

    # Config parser
    def init_config_parser(self):
        config_parser = self.subparsers.add_parser(
            "config", help="password manager configuration commands"
        )
        config_parser.set_defaults(config="activated")
        self.config_subparsers = config_parser.add_subparsers(
            help="subcommand help"
        )

    # Config init parser
    def init_config_init_parser(self):
        config_init_parser = self.config_subparsers.add_parser(
            "init", help="setup initial environment"
        )
        config_init_parser.set_defaults(init="activated")

    # Config password parser
    def init_config_password(self):
        config_password_parser = self.config_subparsers.add_parser(
            "password", help="master password configuration"
        )
        config_password_parser.set_defaults(password="activated")
        self.config_password_subparsers = config_password_parser.add_subparsers(
            help="subcommmand help"
        )

    # Config password attempt_limit parser
    def init_config_password_attempt_limit_parser(self):
        config_password_attempt_limit_parser = (
            self.config_password_subparsers.add_parser(
                "attempt_limit", help="set a cap on failed password attempts"
            )
        )
        config_password_attempt_limit_parser.set_defaults(
            attempt_limit="activated"
        )
        config_password_attempt_limit_parser.add_argument(
            "limit_value", help="the value you want the limit to be", type=int
        )

    # Section parser
    def init_section_parser(self):
        section_parser = self.subparsers.add_parser(
            "section", help="password manager section commands"
        )
        section_parser.set_defaults(section="activated")
        self.section_subparsers = section_parser.add_subparsers(
            help="subcommand help"
        )

    # Section create parser
    def init_section_create_parser(self):
        section_create_parser = self.section_subparsers.add_parser(
            "create", help="create a new section"
        )
        section_create_parser.set_defaults(create="activated")
        section_create_parser.add_argument(
            "section_name", help="name the section you want to create"
        )

    # Section list parser
    def init_section_list_parser(self):
        section_list_parser = self.section_subparsers.add_parser(
            "ls", help="list all sections"
        )
        section_list_parser.set_defaults(ls="activated")

    # Section remove parser
    def init_section_remove_parser(self):
        section_remove_parser = self.section_subparsers.add_parser(
            "rm", help="remove a section"
        )
        section_remove_parser.set_defaults(rm="activated")
        section_remove_parser.add_argument(
            "section_name", help="specify a section"
        )

    # Field parser
    def init_field_parser(self):
        field_parser = self.subparsers.add_parser(
            "field", help="password manager field commands"
        )
        field_parser.set_defaults(field="activated")
        self.field_subparsers = field_parser.add_subparsers(
            help="subcommand help"
        )

    # Field set parser
    def init_field_set_parser(self):
        field_set_parser = self.field_subparsers.add_parser(
            "set", help="set a field value"
        )
        field_set_parser.set_defaults(set="activated")
        field_set_parser.add_argument(
            "section_name", help="the name of the section holding the field"
        )
        field_set_parser.add_argument(
            "field_name", help="the name of the field"
        )
        field_set_parser.add_argument(
            "value", help="the value the field should have"
        )

    # Field get parser
    def init_field_get_parser(self):
        field_get_parser = self.field_subparsers.add_parser(
            "get", help="get the value of a field"
        )
        field_get_parser.set_defaults(get="activated")
        field_get_parser.add_argument(
            "section_name", help="the name of the section holding the field"
        )
        field_get_parser.add_argument(
            "field_name", help="the name of the field"
        )

    # Field list parser
    def init_field_list_parser(self):
        field_list_parser = self.field_subparsers.add_parser(
            "ls", help="list all fields"
        )
        field_list_parser.set_defaults(ls="activated")
        field_list_parser.add_argument(
            "-s", "--section_name", help="specify a specific section"
        )
        field_list_parser.add_argument(
            "-v", "--values", help="enable field values", action="store_true"
        )

    # Field remove parser
    def init_field_remove_parser(self):
        field_remove_parser = self.field_subparsers.add_parser(
            "rm", help="remove a field"
        )
        field_remove_parser.set_defaults(rm="activated")
        field_remove_parser.add_argument(
            "section_name", help="specify the section"
        )
        field_remove_parser.add_argument("field_name", help="specify the field")

    def get_args(self):
        return self.args
