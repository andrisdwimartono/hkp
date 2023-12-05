# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SubContractHandOver(Document):
	def validate(self):
		checking = frappe.db.sql("""SELECT * FROM `tabSPK Histories` WHERE parent = '{0}' AND sub_contract_hand_over = '{1}'""".format(self.sub_contract, self.name))
		if len(checking) == 0:
			sub_contract_doc = frappe.get_doc("Sub Contract", self.sub_contract)
			sub_contract_doc.append("spk_histories", {
				"sub_contract_hand_over": self.name,
				"project": self.project,
				"project_name": self.project_name,
				"job_name": self.job_name,
				"start_work": self.start_work,
				"finish_work": self.finish_work,
				"budget_amount": self.budget_amount
			})
			sub_contract_doc.save(ignore_permissions=True)
			frappe.db.commit()
		self.sisa = self.budget_amount-self.total_terbayar