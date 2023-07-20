# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SlipPembayaranSubkon(Document):
	pass
@frappe.whitelist()
def get_outstanding(hand_over_progress):
	total = frappe.db.sql("""SELECT SUM(total) total FROM `tabSlip Pembayaran Subkon` WHERE docstatus = 0 AND hand_over_progress = '{0}'""".format(hand_over_progress), as_dict=1)
	if total:
		return total[0].total

@frappe.whitelist()
def get_total(hand_over_progress):
	tot = 0
	total = frappe.db.sql("""SELECT SUM(progress_amount) total FROM `tabHand Over Progress Achieved` WHERE parent = '{0}'""".format(hand_over_progress), as_dict=1)
	total2 = frappe.db.sql("""SELECT SUM(progress_discount) total FROM `tabHand Over Progress Discount` WHERE parent = '{0}'""".format(hand_over_progress), as_dict=1)
	if total :
		tot=tot+ total[0].total
	if total2 :
		tot= tot-total2[0].total
	return tot