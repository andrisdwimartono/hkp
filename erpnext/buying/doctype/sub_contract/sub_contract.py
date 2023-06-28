# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SubContract(Document):
	def validate(self):
		self.list_spesialisasi = ""
		for d in self.jenis_spesialisasi:
			if self.list_spesialisasi != "":
				self.list_spesialisasi = "{0}, {1}".format(self.list_spesialisasi, d.spesialisasi)
			else:
				self.list_spesialisasi = d.spesialisasi