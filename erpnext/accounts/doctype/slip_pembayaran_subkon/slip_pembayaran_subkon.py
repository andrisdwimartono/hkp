# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SlipPembayaranSubkon(Document):
	def on_submit(self):
		a = frappe.db.sql("""
				SELECT sum(a.paid) total_paid FROM `tabSlip Pembayaran Subkon` a
				WHERE a.docstatus = 1 AND a.sub_contract_hand_over = '{0}'
				GROUP BY a.sub_contract_hand_over
		""".format(self.sub_contract_hand_over), as_dict=1)
		if a:
			if a[0]:
				frappe.db.sql("""
					UPDATE `tabSub Contract Hand Over` SET total_terbayar = {0}, sisa = budget_amount-total_terbayar WHERE name = '{1}'
				""".format(a[0].total_paid, self.sub_contract_hand_over))
				frappe.db.commit()
	
	def on_cancel(self):
		a = frappe.db.sql("""
				SELECT sum(a.paid) total_paid FROM `tabSlip Pembayaran Subkon` a
				WHERE a.docstatus = 1 AND a.sub_contract_hand_over = '{0}'
				GROUP BY a.sub_contract_hand_over
		""".format(self.sub_contract_hand_over), as_dict=1)
		if a:
			if a[0]:
				frappe.db.sql("""
					UPDATE `tabSub Contract Hand Over` SET total_terbayar = {0}, sisa = budget_amount-total_terbayar WHERE name = '{1}'
				""".format(a[0].total_paid, self.sub_contract_hand_over))
				frappe.db.commit()
@frappe.whitelist()
def get_outstanding(hand_over_progress):
	total = frappe.db.sql("""SELECT SUM(total) total FROM `tabSlip Pembayaran Subkon` WHERE docstatus = 0 AND hand_over_progress = '{0}'""".format(hand_over_progress), as_dict=1)
	if total:
		return total[0].total

@frappe.whitelist()
def get_total(hand_over_progress):
	tot = 0
	total3 = frappe.db.sql("""SELECT total_cost total FROM `tabHand Over Progress` WHERE name = '{0}'""".format(hand_over_progress), as_dict=1)
	if total3:
		return total3[0].total
	else:
		return 0
	total = frappe.db.sql("""SELECT SUM(progress_amount) total FROM `tabHand Over Progress Achieved` WHERE parent = '{0}'""".format(hand_over_progress), as_dict=1)
	total2 = frappe.db.sql("""SELECT SUM(progress_discount) total FROM `tabHand Over Progress Discount` WHERE parent = '{0}'""".format(hand_over_progress), as_dict=1)
	if total :
		tot=tot+ total[0].total
	if total2 :
		tot= tot-total2[0].total
	return tot