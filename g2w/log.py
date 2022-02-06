import yaml

# @todo #/DEV Support loggers definition from environment variables.


class Log:
    config: dict = {}

    def __init__(self, file: str, level: str, fmt: str = None):
        """
        @file:  The yaml file with logging configuration.
        @level: The default logging level for all loggers.
        @fmt:   The default format message for primary(default) logger.
        """
        self.file = file
        self.level = level
        self.fmt = fmt

    def read(self) -> dict:
        # @todo #/DEV Handle the IO exception here during YAML parsing
        with open(self.file, "r") as stream:
            self.config = yaml.safe_load(stream)
        # @todo #/DEV Handle the case when no loggers defined
        for name in self.config["loggers"]:
            self.config["loggers"][name]["level"] = self.level
        if self.fmt is not None:
            self.config["formatters"]["default"]["fmt"] = self.fmt
        return self.config
