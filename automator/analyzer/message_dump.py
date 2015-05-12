#! /usr/bin/env python
"""
message_dump.py

A simple message dump analyzer

Author: Yuanjie Li
"""

from analyzer import *

import xml.etree.ElementTree as ET
import io

class MsgDump(Analyzer):

	def dump_message(self,msg):
		self.msg_log_mem.append(msg)
		print msg.timestamp,msg.type_id
		ET.dump(msg.data)

	def __init__(self):
		Analyzer.__init__(self)
		# a message dump has no analyzer in from/to_list
		# it only has a single callback for the source
		self.msg_log=[] # in-memory message log
		self.add_source_callback(self.dump_message)