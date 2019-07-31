class Ledger:

    def __init__(self):
        self.is_malicious = False
        self.overlay_neighbours = {}

    def sharable_packet(self):
        pass

    def store_transaction(self, tx):
        pass

    def get_tx(self, hash):
        pass

    def get_current_balance(self, peer):
        pass

    def set_malicious(self):
        self.is_malicious = True


class Transaction:

    def __init__(self, source, target, sign, hash, links, counter, type="source", payload="ab12"):
        self.payload = payload
        self.source = source
        self.target = target
        self.sign = sign
        self.hash = hash
        # Last known state/coming after semantics
        self.links = links
        # The transaction place in the ledger/inclusion proof/synchronization help
        self.counter = counter
        self.type = type


class ChainLedger(Ledger):
    """
    Chain ledger - store chain per account, store all transactions related to a account
    in a linearly structured hash-chain
    """

    def __init__(self):
        super().__init__()
        self.chain = {}
        self.double_spends = {}
        self.last_counter = 0
        self.last_hash = 0

        self.in_counter = 0

    def store_transaction(self, tx: Transaction):
        # check integral consistency

        if tx.counter in self.chain.keys():
            # Transaction with this tx counter is already recorded
            if self.chain[tx.counter].hash == tx.hash:
                # The same transaction is already in the set
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
                    # There is a deeper fork, we need to search for
                    print("Inconsistency detected")
                    return tx.counter - 1, tx.counter

        elif self.last_counter == tx.counter and tx.links[0] == self.last_hash:
            # Consistent insert
            self.chain[tx.counter] = tx
            self.last_counter = max(self.last_counter, tx.counter)
            self.last_hash = tx.hash
            if self.last_counter + 1 == self.in_counter:
                self.last_counter = self.in_counter
                self.last_hash = self.chain[self.last_counter].hash
            return None
        else:
            # Inconsistent transaction
            self.chain[tx.counter] = tx
            self.in_counter = tx.counter
            return self.last_counter, tx.counter

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


class MergeSet(Ledger):

    def __init__(self, neighbours: dict):
        super().__init__()
        self.tx_set = set()
        self.overlay_neighbours = neighbours

    def store_transaction(self, tx):
        self.tx_set.add(tx)


class VectorClock(Ledger):
    pass


class BloomClock(Ledger):
    pass


class DAGChain(Ledger):
    pass


class MerkleTree(Ledger):
    pass
