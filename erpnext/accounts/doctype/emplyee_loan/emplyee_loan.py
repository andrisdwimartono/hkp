# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class EmployeeLoan(Document):
	def validate(self):
		self.total_budget = 0
		for d in self.details:
			self.total_budget = self.total_budget+d.budget_amount
		if self.docstatus == 0:
			self.outstanding_amount = self.total_budget

	# def on_submit(self):
		# budget_approval_plan_doc = frappe.get_doc({
		# 	"doctype" : "Budget Approval Plan",
		# 	"posting_date": today()
		# 	})
		# budget_approval_plan_doc.append("budget_approval_plan_detail", {
		# 	"peminta": self.owner,
		# 	"total_budget": self.total_budget,
		# 	"purpose": self.purpose,
		# 	"employee_loan": self.name
		# })
		# budget_approval_plan_doc.save()