# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PermintaanPerbaikan(Document):
	def validate(self):
		total_biaya = 0
		for d in self.tindakan_permintaan_perbaikan:
			total_biaya = total_biaya+d.biaya
		self.total_biaya = total_biaya