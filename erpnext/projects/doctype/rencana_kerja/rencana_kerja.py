# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RencanaKerja(Document):
	def validate(self):
		checking = frappe.db.sql(
		""" SELECT * FROM `tabJenis Pekerjaan Except` WHERE parent = '{0}' AND pekerjaan = '{1}'
		""".format(self.jenis_pekerjaan, self.pekerjaan), as_dict=1)
		if checking:
			frappe.throw("""Jenis Pekerjaan {0} tidak boleh di Pekerjaan {1}""".format(self.jenis_pekerjaan, self.pekerjaan))
