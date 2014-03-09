class Server:
    """
    Represents open stack server.
    """

    def __init__(self, name=None, ip=None, id=None):
        self.name = name
        self.ip = ip
        self.id = id
        self.available = False
