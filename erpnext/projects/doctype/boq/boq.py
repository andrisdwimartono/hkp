# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BOQ(Document):
	def validate(self):
		self.grand_total = 0
		for d in self.boq_detail:
			self.grand_total += d.total

@frappe.whitelist()
def get_harga(types, document_of_type):
	xs = frappe.db.sql("""SELECT * FROM `tab{0}` a WHERE a.name = '{1}'""".format(types, document_of_type), as_dict=1)
	if xs:
		return xs[0]