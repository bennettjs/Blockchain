### Understanding blockchains by building one.
# Core concept: chunks of data (blocks) chained together with unique hashes.
# Within each block is a hash backwards to the previous block. This gives the
# chain immutability: If a previous block was compromised, all subsequent
# blocks would have the incorrect hash.

# Proof of Work (PoW): hard to find, easy to verify. Needed to create a new
# block. This is what miners are trying to solve. They get coins for solving
# it.
# Find a p' such that hash(p * p') has some desired characteristic. p' is the
# previous p (proof) and p' is the new proof. 

from time import time
import hashlib
from flask import Flask
from flask import jsonify
from flask import request


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

    def proof_of_work(self, last_proof):
        """Find p' such that hash(p * p') yields a desired characteristic.
        p is the previous proof and p' is the new one. 
        :param last_proof: <int> proof for the previous block
        :return: <int> 
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof


    @staticmethod
    def valid_proof(p, p_prime):
        """Checks to see if the p' satisfies the proof condition (set in this
        function.

        :param p: <int> previous proof.
        :param p_prime: <int> current proof.
        :return: <bool> True if p_prime is a valid proof, otherwise False. 
        """
        g = f'{p}{p_prime}'.encode() #Concat p and p', converts to bytes
        hash_g = hashlib.sha256(g).hexdigest()
        
        # In this case our condition is that the first 3 digits of the hash are
        # all zeroes. 
        return hash_g[:3] == "000" 


    @staticmethod
    def hash_block(block):
        """Hashes a block of data using SHA-256 
        :param block: <dict> block of data
        :return: <str> SHA-256 hash of the blocks data
        """
       
        # Dictionaries are not sorted by default, so we must do that first. 
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ Returns last block in the chain so we can add a new block"""
        return self.chain[-1]

### Now for the flask/API part:

# Creates the node/webserver for this blockchain.
app = Flask(__name__)

# Iniiate the blockchain:
blockchain = Blockchain()

# Create API endpoints to interact with the blockchain:

@app.route('/', methods=['GET'])
def home():
    return "Let's get to mining"

@app.route('/chain', methods=['GET'])
def show_chain():
    response = {'chain' : blockchain.chain, 'length' : len(blockchain.chain)}
    return jsonify(response), 200 

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'receiver', 'payload']

    # Input validation. all checks that all the values in iterable are True.
    if not all(k in values for k in required):
        return "missing values", 400

    # Create new transaction:
    index = blockchain.new_trans(values['sender'], values['receiver'], values['payload'])
    
    response = {'message': f'The transaction will be in block {index}'}
    return jsonify(response), 201 

@app.route('/mine', methods=['GET'])
def mine():
"""
1) Calculate proof of work.
2) Reward miner by adding transaction
3) Create new block on the chain.
"""
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


