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
from blackcoinutils.script import Script
from blackcoinutils.keys import P2wpkhAddress, P2wshAddress, P2shAddress, PrivateKey


def main():
    # always remember to setup the network
    setup("mainnet")

    # could also instantiate from existing WIF key
    priv = PrivateKey.from_wif("PdiUUh8dnXB36B2XcbPdodUX5Ujoj2VDubJwcW1V8DJu69XHZWGg")

    # compressed is the default
    print("\nPrivate key WIF:", priv.to_wif(compressed=True))

    # get the public key
    pub = priv.get_public_key()

    # compressed is the default
    print("Public key:", pub.to_hex(compressed=True))

    # get address from public key
    address = pub.get_segwit_address()

    # print the address and hash - default is compressed address
    print("Native Address:", address.to_string())
    segwit_hash = address.to_witness_program()
    print("Segwit Hash (witness program):", segwit_hash)
    print("Segwit Version:", address.get_type())

    # test to_string
    addr2 = P2wpkhAddress.from_witness_program(segwit_hash)
    print("Created P2wpkhAddress from Segwit Hash and calculate address:")
    print("Native Address:", addr2.to_string())

    #
    # display P2SH-P2WPKH
    #

    # create segwit address
    addr3 = (
        PrivateKey.from_wif("PdiUUh8dnXB36B2XcbPdodUX5Ujoj2VDubJwcW1V8DJu69XHZWGg")
        .get_public_key()
        .get_segwit_address()
    )
    # wrap in P2SH address
    addr4 = P2shAddress.from_script(addr3.to_script_pub_key())
    print("P2SH(P2WPKH):", addr4.to_string())

    #
    # display P2WSH
    #
    p2wpkh_key = PrivateKey.from_wif(
        "PdiUUh8dnXB36B2XcbPdodUX5Ujoj2VDubJwcW1V8DJu69XHZWGg"
    )
    script = Script(
        ["OP_1", p2wpkh_key.get_public_key().to_hex(), "OP_1", "OP_CHECKMULTISIG"]
    )
    p2wsh_addr = P2wshAddress.from_script(script)
    print("P2WSH of P2PK:", p2wsh_addr.to_string())

    #
    # display P2SH-P2WSH
    #
    p2sh_p2wsh_addr = P2shAddress.from_script(p2wsh_addr.to_script_pub_key())
    print("P2SH(P2WSH of P2PK):", p2sh_p2wsh_addr.to_string())


if __name__ == "__main__":
    main()
