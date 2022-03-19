class BlackList:

    def __init__(self, blacklist_filename = 'blacklist.conf'):
        self.blacklist = set()
        with open(blacklist_filename, 'rt') as file:
            for line in file.readlines():
                self.blacklist.add(line.strip())

    def is_banned(self, url):
        for banned in self.blacklist:
            if banned in url:
                return True
        return False
