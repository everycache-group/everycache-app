from argparse import ArgumentParser, RawTextHelpFormatter

if __name__ == "__main__":
    commands = ["run", "db-recreate", "db-populate"]
    commands_choices = ", ".join(commands)

    parser = ArgumentParser(
        description=f"available commands: {commands_choices}",
        add_help=True,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("command", type=str, help="command to execute")

    args = parser.parse_args()

    command = args.command

    if command not in commands:
        parser.error(
            f"unsupported command: {command}; available commands: {commands_choices}"
        )
        exit(1)

    if command == "run":
        import settings
        from app import app
        from database.connection import recreate_db_schema

        recreate_db_schema()

        app.run(host="0.0.0.0", port="5000", debug=settings.DEBUG)
    elif command == "db-recreate":
        from database.connection import recreate_db_schema

        recreate_db_schema()
    elif command == "db-populate":
        from database.populate import populate

        populate()

    exit(0)
