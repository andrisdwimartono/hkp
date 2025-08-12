# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HandOverProgress(Document):
	def validate(self):
		if self.hand_over_progress_achieved:
			self.total_achieved = 0
			for d in self.hand_over_progress_achieved:
				self.total_achieved = self.total_achieved+d.progress_amount
		
		if self.hand_over_progress_discount:
			self.total_discount = 0
			for d in self.hand_over_progress_discount:
				self.total_discount = self.total_discount+d.progress_discount
		self.total_cost = self.total_achieved-self.total_discount+self.rounded_cost
		if self.progress_sequence == 0:
			self.total_cost = self.total_cost+self.down_payment
	def on_submit(self):
		if self.sub_contract_hand_over:
			if self.progress_achieved < 100:
				frappe.db.sql("""UPDATE `tabSub Contract Hand Over` SET status = 'Sedang Diproses' WHERE name = '{0}'""".format(self.sub_contract_hand_over))
			else:
				frappe.db.sql("""UPDATE `tabSub Contract Hand Over` SET status = 'Selesai' WHERE name = '{0}'""".format(self.sub_contract_hand_over))

@frappe.whitelist()
def check_progress(sub_contract_hand_over = None):
    if sub_contract_hand_over:
        return frappe.db.sql("""
        SELECT COUNT(*)+1 progress_sequence, max(down_payment_percent) down_payment_percent, max(down_payment) down_payment FROM `tabHand Over Progress` hop 
        WHERE hop.sub_contract_hand_over = '{0}' AND hop.docstatus = 1 AND progress_sequence != 0
        """.format(sub_contract_hand_over), as_dict=1)
    return 0

@frappe.whitelist()
def get_last_discounts(sub_contract_hand_over = None):
	# if sub_contract_hand_over:
	# 	return frappe.db.sql("""
	# 	SELECT hopd.remarks, hopd.progress_discount FROM `tabHand Over Progress Discount` hopd
	# 	INNER JOIN (SELECT * FROM `tabHand Over Progress` hop
	# 	WHERE hop.sub_contract_hand_over = '{0}' AND hop.docstatus = 1
	# 	ORDER BY hop.progress_sequence DESC
	# 	LIMIT 1) hop ON hop.name = hopd.parent
	# 	ORDER BY hopd.idx ASC
	# 	""".format(sub_contract_hand_over), as_dict=1)
	if sub_contract_hand_over:
		return frappe.db.sql("""SELECT CONCAT('Progres Fisik ', b.progress_sequence) remarks, a.paid progress_discount 
					   FROM `tabSlip Pembayaran Subkon` a 
					   INNER JOIN `tabHand Over Progress` b ON a.hand_over_progress = b.name
					   WHERE a.sub_contract_hand_over = '{0}' AND a.docstatus = 0
					   ORDER BY b.progress_sequence ASC, a.modified ASC""".format(sub_contract_hand_over), as_dict=1)
	return None

@frappe.whitelist()
def check_hand_over_progress(hand_over_progress = None):
    if hand_over_progress:
        return frappe.db.sql("""
        SELECT hop.total_cost budget_amount, concat(hop.contractor_name, ' ', hop.progress_achieved, '% ', hop.project_name)purpose FROM `tabHand Over Progress` hop
        WHERE hop.name = '{0}' AND hop.docstatus = 1
        """.format(hand_over_progress), as_dict=1)
    return None