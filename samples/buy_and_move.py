#!/usr/bin/env python

"""Script to buy a crypto from another currency and then move the
crypto to a known address. Used to do DCA (Dollar Cost Averaging).

Example to buy 1000€ of BTC and send them to the hw_wallet defined on
Kraken:

$ ./buy_and_move.py 1000 EUR XBT hw_wallet
"""

from decimal import Decimal
import time
import sys

from clikraken.api.api_utils import load_api_keyfile
from clikraken.api.private.get_balance import get_balance
from clikraken.api.private.place_order import place_order
from clikraken.api.public.depth import depth
from clikraken.clikraken_utils import load_config

from abstract_automaton import AbstractAutomaton


class DollarCostAveragingAutomaton(AbstractAutomaton):
    state_file = "dca.json"
    decimal_fields = ["amount"]
    seconds_to_wait = 60

    def __init__(self, amount, frm, to, addr):
        self.frm = frm
        self.amount = amount
        self.to = to
        self.addr = addr
        super().__init__()

    def run(self):
        while self.state.startswith("wait_"):
            print("waiting for {}s in {}".format(self.seconds_to_wait, self.state))
            time.sleep(self.seconds_to_wait)
            self.execute_state()

    def init(self, data):
        data["frm"] = self.frm
        data["amount"] = self.amount
        data["to"] = self.to
        data["addr"] = self.addr
        data["pair"] = "X{}Z{}".format(self.to, self.frm)
        self.set_state("wait_for_balance", data)

    def wait_for_balance(self, data):
        bal = get_balance()
        if data["frm"] not in bal:
            print("not", data["frm"], "to buy", data["to"])
        elif bal[data["frm"]] < data["amount"]:
            print(
                "not enough {} ({} < {}) to buy {}".format(
                    data["frm"], bal[data["frm"]], data["amount"], data["to"]
                )
            )
        else:
            self.set_state("buy", data)

    def buy(self, data):
        d = depth(data["pair"], 10)
        asks = d[data["pair"]]["asks"]
        volume = 0
        sum = 0
        for price, vol, _ in asks:
            sum += Decimal(price) * Decimal(vol)
            volume += Decimal(vol)
        price = sum / volume
        # compute the amount from the current market asks
        # todo(fl) need to take the fees into account
        target_amount = data["amount"] / price
        res = place_order("buy", data["pair"], "market", target_amount)
        print(res)
        # todo(fl) wait for the order to be fulfilled and transfer
        # the crypto to the wallet


def main(argv):
    if len(argv) != 5:
        print(
            "Usage: {} <amount to spend> <currency to spend> <currency to buy> <address to move>".format(
                argv[0]
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    load_config()
    load_api_keyfile()

    dca = DollarCostAveragingAutomaton(Decimal(argv[1]), argv[2], argv[3], argv[4])

    dca.run()


if __name__ == "__main__":
    main(sys.argv)

# buy_and_move.py ends here