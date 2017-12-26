### Understanding blockchains by building one.
# Core concept: chunks of data (blocks) chained together with unique hashes.


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.cur_trans = []


    def new_block(self):
        """Creates a new block, adds it to the chain"""
        pass

    def new_trans(self):
        """Adds a new transaction to the list of transactions"""
        pass

    @staticmethod
    def hash_block(self):
        """Hashes a block of data. """
        pass

    def last_block(self):
        """ Returns last block in the chain so we can add a new block"""
        pass


