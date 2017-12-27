### Understanding blockchains by building one.
# Core concept: chunks of data (blocks) chained together with unique hashes.
# Within each block is a hash backwards to the previous block. This gives the
# chain immutability: If a previous block was compromised, all subsequent
# blocks would have the incorrect hash.
from time import time
import hashlib
import json
from 

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.cur_trans = []
        
        # Create genesis block. Has no predecessors.
        self.new_block(proof=100, prev_hash=1)


    def new_block(self, proof, prev_hash=None):
        """Creates a new block, adds it to the chain.
        :param proof: <int> proof from proof of work algorithm.
        :param prev_hash: <str> hash of previous block.
        :return: <dict> dictionary representation of new block. 
        """ 
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.cur_trans,
            'proof' : proof,
            'prev_hash' : prev_hash or self.hash(self.chain[-1]) # given or hash last block
        }

        # Rest transactions 
        self.cur_trans = []

        self.chain.append(block)

        return block

    def new_trans(self, sender, receiver, payload):
        """Adds a new transaction to the list of transactions
        
        :param sender: <str> sender's address
        :param receiver: <str> destinations of payload
        :param payload: <str> information to be sent
        :return: <int> index of the block to hold this transaction
        """

        #
        self.cur_trans.append({
            'sender' : sender,
            'receiver' : receiver,
            'payload' : payload
        }) 
        
        # Index of block this transaction WILL BE added to. i.e. next mined
        # block 
        return self.last_block['index'] + 1




    @staticmethod
    def hash_block(block):
        """Hashes a block of data using SHA-256 
        :param block: <dict> block of data
        :return: <str> SHA-256 hash of the blocks data"""
       
        # Dictionaries are not sorted by default, so we must do that first. 
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ Returns last block in the chain so we can add a new block"""
        return self.chain[-1]

