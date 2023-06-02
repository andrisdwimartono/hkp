# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BudgetApprovalPlan(Document):
	def validate(self):
		if len(self.budget_approval_plan_detail) == 0:
			for d in frappe.db.sql("""
			SELECT
				fpep.project_name as pos_anggaran,
				fpep.owner as peminta,
				fpep.total_budget as total_budget,
				fpep.purpose as purpose,
				fpep.name as form_payment_entry_project,
				null as form_payment_entry
			FROM
				`tabForm Payment Entry Project` fpep
			WHERE
				fpep.docstatus = 1 AND fpep.outstanding_amount > 0
			UNION
			SELECT
				'Kantor' as pos_anggaran,
				fpe.owner as peminta,
				fpe.total_budget as total_budget,
				fpe.purpose as purpose,
				null as form_payment_entry_project,
				fpe.name as form_payment_entry
			FROM
				`tabForm Payment Entry` fpe
			WHERE
				fpe.docstatus = 1 AND fpe.outstanding_amount > 0
			""", as_dict=1):
				se_child = self.append("budget_approval_plan_detail")
				se_child.pos_anggaran = d.pos_anggaran
				se_child.peminta = d.peminta
				se_child.total_budget = d.total_budget
				se_child.purpose = d.purpose
				se_child.form_payment_entry_project = d.form_payment_entry_project
				se_child.form_payment_entry = d.form_payment_entry			
