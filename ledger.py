class Ledger:

    def sharable_packet(self):
        pass

    def store_transaction(self, tx):
        pass

    def get_tx(self, hash):
        pass


class Transaction:

    def __init__(self):
        self.payload = ""
        self.source = 12
        self.target = 13
        self.sign = ""
        self.hash = ""
        # Last known state/coming after semantics
        self.links = []
        # The transaction place in the ledger/inclusion proof/synchronization help
        self.counter = 0
        self.type = "source"


class ChainLedger(Ledger):
    """
    Chain ledger - store chain per account, store all transactions related to a account
    in a linearly structured hash-chain
    """

    def __init__(self):
        self.chain = {}
        self.double_spends = {}
        self.last_counter = 0
        self.last_hash = 0

        self.in_counter = 0
        self.in_last_hash = 0

    def store_transaction(self, tx: Transaction):
        # check integral consistency
        if self.chain[tx.counter].hash == tx.hash:
            # Transaction already in the set
            return None
        else:
            # Double spend detected
            if tx.counter not in self.double_spends.keys():
                self.double_spends[tx.counter] = set()
                self.double_spends[tx.counter].add(self.chain[tx.counter])
            self.double_spends[tx.counter].add(tx)
            print("Double spend detected ")
            if tx.links[0] != self.chain[tx.counter].links[0]:
                # Two transaction are pointing to different transactions
                print("Inconsistency detected")

        if self.last_counter == tx.counter and tx.links[0] == self.last_hash:
            # Consistent insert
            self.chain[tx.counter] = tx
            self.last_counter = max(self.last_counter, tx.counter)
            self.last_hash = tx.hash
        else:
            # Inconsistent transaction
            self.chain[tx.counter] = tx
            self.in_counter
            # Ask for other transactions

            #

    def is_consistent(self):
        last_hash = 0
        for i in range(self.last_counter - 1):
            if i + 1 in self.chain.keys():
                if self.chain[i + 1].links[0] != last_hash:
                    return False
                else:
                    last_hash = self.chain[i + 1].hash
            else:
                return False
        return True


class VectorClock(Ledger):
    pass


class BloomClock(Ledger):
    pass


class DAGChain(Ledger):
    pass


class MerkleTree(Ledger):
    pass
