# coding: utf-8

import autism.compat

import json

if not autism.compat.py2k:
	import collections
	_UserDict = collections.UserDict
else:
	import UserDict
	_UserDict = UserDict.UserDict

__all__ = [
	"FormatDictProxy",
	"SerializeDictProxy",
	"PrefixDictProxy"
]

class FormatDictProxy(_UserDict):
	def __init__(self, dict, format=""):
		_UserDict.__init__(self, dict)
		self.format = str(format)
	
	def __repr__(self):
		return "FormatDictProxy({x!r})".format(self.data)

	def __getitem__(self, key):
		return self.data[self.format.format(str(key))]

	def __setitem__(self, key, value):
		self.data[self.format.format(str(key))] = value

	def __delitem__(self, key):
		del self.data[self.format.format(str(key))]

	def __contains__(self, key):
		return self.format.format(str(key)) in self.data

class SerializeDictProxy(_UserDict):
	def __init__(self, dict, encoder=None, decoder=None):
		_UserDict.__init__(self, dict)
		if encoder is None:
			encoder = json.dumps
		if decoder is None:
			decoder = json.loads
		self.encoder = encoder
		self.decoder = decoder

	def __getitem__(self, key):
		return self.decoder(self.data[key])
	
	def __setitem__(self, key, value):
		self.data[key] = self.encoder(value)

	def __contains__(self, key):
		return key in self.data

class PrefixDictProxy(FormatDictProxy):
	def __init__(self, backend, prefix=""):
		FormatDictProxy.__init__(self, backend, str(prefix) + "{}")

