# -*- coding: utf-8 -*-

"""
clikraken.api.private.get_deposit_methods

This module queries the DepositMethods method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import OrderedDict

import clikraken.global_vars as gv
from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import process_options

OPTIONS = (
    (("-a", "--asset"), {"default": gv.DEFAULT_ASSET, "help": "asset being deposited"}),
)

MANDATORY_OPTIONS = ("asset",)


def get_deposit_methods(**kwargs):
    """Get deposit methods."""

    args = process_options(kwargs, OPTIONS, MANDATORY_OPTIONS)

    return get_deposit_methods_api(args)


def get_deposit_methods_api(args):
    """Get deposit methods."""

    # Parameters to pass to the API
    api_params = {
        "asset": args.asset,
    }

    res = query_api("private", "DepositMethods", api_params, args)

    return res


def get_deposit_methods_cmd(args=None):
    """Get deposit methods."""
    res = get_deposit_methods_api(args)
    m_list = []
    for method in res:
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        method_dict = OrderedDict()
        # Remove leading Z or X from asset pair if it is of length 4
        method_dict["asset"] = (
            args.asset[1:]
            if len(args.asset) == 4 and args.asset[0] in ["Z", "X"]
            else args.asset
        )
        method_dict["method"] = method["method"]
        method_dict["fee"] = method["fee"]
        method_dict["limit"] = method["limit"]
        method_dict["gen-address"] = method["gen-address"]
        m_list.append(method_dict)

    if not m_list:
        return

    # Sort alphabetically
    m_list = sorted(
        m_list,
        key=lambda method_dict: "{}{}".format(
            method_dict["asset"], method_dict["method"]
        ),
    )

    if args.csv:
        print(csv(m_list, headers="keys"))
    else:
        print(tabulate(m_list, headers="keys"))


def init(subparsers):
    parser_deposit_methods = subparsers.add_parser(
        "deposit_methods",
        aliases=["dm"],
        help="[private] Get deposit methods",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    for (args, kwargs) in OPTIONS:
        parser_deposit_methods.add_argument(*args, **kwargs)
    parser_deposit_methods.set_defaults(sub_func=get_deposit_methods_cmd)
