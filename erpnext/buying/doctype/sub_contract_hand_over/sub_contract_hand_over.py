# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class SubContractHandOver(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.posting_date, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabSub Contract Hand Over` WHERE project{0}""".format(" = '{0}'".format(self.project) if self.project else " is null"), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/{4}-SPK/{3}/{0}/{1}".format("0{0}".format(mydate.month) if mydate.month < 10 else mydate.month, mydate.year-2000, urut2, self.project if self.project else "GKM", "OPS" if self.project else "LOG")
		else:
			self.name = "001/{3}-SPK/{2}/{0}/{1}".format("0{0}".format(mydate.month) if mydate.month < 10 else mydate.month, mydate.year-2000, self.project if self.project else "GKM", "OPS" if self.project else "LOG")

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