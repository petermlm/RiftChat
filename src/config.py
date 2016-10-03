from os.path import expanduser


class Config:
    host = "127.0.0.1"
    port = 8000

    server_file_name = expanduser("~/.rift_server")
    client_file_name = expanduser("~/.rift_client")

    def serverConf(file_name=None):
        if file_name is None:
            file_name = Config.server_file_name

        try:
            config = Config.readConfigFile(file_name)
        except FileNotFoundError:
            config = {"port": Config.port}

        config["host"] = Config.host
        print(config)
        return config

    def clientConf(file_name=None):
        if file_name is None:
            file_name = Config.client_file_name

        try:
            config = Config.readConfigFile(file_name)
        except FileNotFoundError:
            config = {"host": Config.host, "port": Config.port}

        return config

    def readConfigFile(file_name):
        config = {}

        with open(file_name, "r") as fd:
            for i in fd:
                Config.parseLine(config, i)

        return config

    def parseLine(config_file, line):
        key_value = line.split("=")

        if len(key_value) != 2:
            return

        if key_value[0] in ["host", "username"]:
            config_file[key_value[0]] = key_value[1]
        elif key_value[0] in ["port"]:
            config_file[key_value[0]] = int(key_value[1])
