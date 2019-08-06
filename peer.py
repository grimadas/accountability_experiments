from ledger import Ledger, Transaction
from networkx import Graph


class Peer:

    def __init__(self, ledger: Ledger, witness_strategy, init_network: Graph, max_risk=0.1):
        # storage layer
        self.ledger = ledger
        # estimated topology network
        self.network = init_network

        # Estimate network convergence rate

        # Network has weight between peer?

        # T-consistency: What is the t when peer will be consistent

    def receive_tx(self):
        pass

    def get_witnesses(self, tx: Transaction):
        """
        Witness selection: based on the transaction select peer that would minimize double spend risk. Possible
        scenarios:
        1. You receive a transaction from peer P1, estimate the risk and choose witnesses that would
        minimize the risk of successful double-spend;
        Send confirmation transaction after estimating the risk.
        2. When you receive double-signed transaction you update your local ledger and gossip further if needed.
        3. When you receive one-signed transaction you included as possibly unconfirmed and gossip further if needed.
        :param tx:
        :return:
        """
        pass
