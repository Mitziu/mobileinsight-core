#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dm_log_config_msg.py

Define DMLogConfigMsg class, a QCDM Log Config message constructor.

Author: Jiayao Li
"""

__all__ = ["DMLogConfigMsg"]

import binascii
import math
import struct

from consts import *


# Thanks to ModemManager/libqcdm
class DMLogConfigMsg(object):
    _EQUIP_ID_MASK = 0xF000
    _ITEM_ID_MASK = 0x0FFF

    def __init__(self, op_name, type_id_list=None):
        self._op_number = LOG_CONFIG_OP_NUMBER[op_name]
        if self._op_number != LOG_CONFIG_OP_NUMBER["DISABLE"]:
            assert type_id_list
            self._item_lst = type_id_list
            # Set equip id
            equip_id_set = set([DMLogConfigMsg.get_equip_id(i) for i in type_id_list])
            assert len(equip_id_set) == 1
            for i in equip_id_set:
                self._equip_id = i
                break
        
    def binary(self):
        b = struct.pack("<BBBBI",   # little endian
                        COMMAND_CODE["DIAG_CMD_LOG_CONFIG"],
                        0, 0, 0,    # padding
                        self._op_number
                        )
        if self._op_number != LOG_CONFIG_OP_NUMBER["DISABLE"]:
            item_mask, highest = self._get_item_mask()
            b += struct.pack("<II", self._equip_id, highest + 1)
            b += item_mask
        return b

    @classmethod
    def get_equip_id(cls, type_id):
        return (type_id & cls._EQUIP_ID_MASK) >> 12

    def _get_item_mask(self):
        l = [i & DMLogConfigMsg._ITEM_ID_MASK for i in self._item_lst]
        highest = max(l)
        n_bytes = int(math.ceil((highest + 1) / 8.0))
        b = [0 for i in range(n_bytes)]
        for i in l:
            b[i / 8] |= 1 << (i % 8)
        b = "".join([chr(onebyte) for onebyte in b])
        return b, highest


# Test encoding
if __name__ == "__main__":
    tests = [   ("DISABLE", []),
                ("SET_MASK", [0x1001, 0x1007, 0x1008]),
                ("SET_MASK", [0xB0C0, 0xB179, 0xB187, 0xB193, 0xB195]),
                ("SET_MASK", [  0x4125, 0x4126, 0x4127, 0x4128,
                                0x4129, 0x412B, 0x412F]),
                ("SET_MASK", [0x7130, 0x7131, 0x7132, 0x7133, 0x7134, 0x7135, 0x7136, 0x7137, 0x7138, 0x7139, 0x713A, 0x713B, 0x713C, 0x713D, 0x713E, 0x7150, 0x7151, 0x7152, 0x7153, 0x7154, 0x7155, 0x7156, 0x7157, 0x7158, 0x7159, 0x7B3A]),
                ]
    import dm_endec_c
    for op_name, type_id_list in tests:
        if type_id_list:
            x = DMLogConfigMsg(op_name, type_id_list)
        else:
            x = DMLogConfigMsg(op_name)
        b1 = x.binary();
        b2 = dm_endec_c.encode_log_config(op_name, type_id_list)
        print " ".join(["%02x" % ord(c) for c in b1])
        print " ".join(["%02x" % ord(c) for c in b2])
        print ("Pass" if b1 == b2 else "Failed")
