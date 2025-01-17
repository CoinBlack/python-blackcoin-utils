# Copyright (C) 2018-2024 The python-bitcoin-utils developers
# Copyright (C) 2024 The python-blackcoin-utils developers
#
# This file is part of python-blackcoin-utils
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-blackcoin-utils, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from blackcoinutils.setup import setup
from blackcoinutils.transactions import Sequence
from blackcoinutils.keys import P2shAddress, PrivateKey
from blackcoinutils.script import Script
from blackcoinutils.constants import TYPE_RELATIVE_TIMELOCK


def main():
    # always remember to setup the network
    setup("mainnet")

    #
    # This script creates a P2SH address containing a CHECKSEQUENCEVERIFY plus
    # a P2PKH locking funds with a key as well as for 20 blocks
    #

    # set values
    relative_blocks = 20

    seq = Sequence(TYPE_RELATIVE_TIMELOCK, relative_blocks)

    # secret key corresponding to the pubkey needed for the P2SH (P2PKH) transaction
    p2pkh_sk = PrivateKey("PgxxTGsyU2L7iD9HemZk8bjVCSjYyDNqiM2TJdAjr5VuLnZLjYJB")

    # get the address (from the public key)
    p2pkh_addr = p2pkh_sk.get_public_key().get_address()

    # create the redeem script
    redeem_script = Script(
        [
            seq.for_script(),
            "OP_CHECKSEQUENCEVERIFY",
            "OP_DROP",
            "OP_DUP",
            "OP_HASH160",
            p2pkh_addr.to_hash160(),
            "OP_EQUALVERIFY",
            "OP_CHECKSIG",
        ]
    )

    # create a P2SH address from a redeem script
    addr = P2shAddress.from_script(redeem_script)
    print(addr.to_string())


if __name__ == "__main__":
    main()
