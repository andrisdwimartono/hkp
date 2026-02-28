# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class FormPaymentEntry(Document):
	def validate(self):
		self.total_budget = 0
		for d in self.details:
			self.total_budget = self.total_budget+d.budget_amount
		if self.docstatus == 0:
			self.outstanding_amount = self.total_budget

	def on_submit(self):
		budget_approval_plan_doc = frappe.get_doc({
			"doctype" : "Budget Approval Plan",
			"posting_date": today()
			})
		budget_approval_plan_doc.append("budget_approval_plan_detail", {
			"peminta": self.owner,
			"total_budget": self.total_budget,
			"purpose": self.purpose,
			"form_payment_entry": self.name
		})
		budget_approval_plan_doc.save()

## Membuat API
@frappe.whitelist()
def get_detail(form_payment_entry):
      return frappe.db.sql("""SELECT * FROM `tabForm Payment Entry` WHERE parent = '{0}'""".format(form_payment_entry), as_dict=1)

def get_permission_query_conditions(user):
	if frappe.session.user != "hasta.rizkiamalia@gmail.com" and frappe.session.user != "hasta.yunikeu@gmail.com" and frappe.session.user != "hasta.vaniaharyani@gmail.com" and frappe.session.user != "kasir@gmail.com" and frappe.session.user != "hasta.nurainihaqiqi@gmail.com" and frappe.session.user != "hasta.fauziyyah@gmail.com" and frappe.session.user != "hasta.tahtaalf@gmail.com" and frappe.session.user != "Administrator":
		return "(`tabForm Payment Entry`.owner NOT IN ('hasta.rizkiamalia@gmail.com', 'hasta.yunikeu@gmail.com', 'hasta.vaniaharyani@gmail.com', 'kasir@gmail.com', 'hasta.nurainihaqiqi@gmail.com', 'hasta.fauziyyah@gmail.com', 'hasta.tahtaalf@gmail.com', 'Administrator'))"
	else:
		return ""