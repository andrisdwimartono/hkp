# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PaymentCard(Document):
	pass

@frappe.whitelist()
def get_document(document, type):
	if type == "Sub Contract Hand Over":
		return frappe.get_doc("Sub Contract Hand Over", document)
	else:
		return frappe.get_doc("Supplier", document)