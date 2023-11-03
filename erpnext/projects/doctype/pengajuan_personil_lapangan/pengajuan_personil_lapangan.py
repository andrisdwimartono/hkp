# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PengajuanPersonilLapangan(Document):
	def on_submit(self):
		for d in self.detail:
			if d.employee and self.project:
				project_doc = frappe.get_doc("Project", self.project)
				project_doc.append("project_team", {
					"designation": d.designation,
					"employee": d.employee,
					"employee_name": d.employee_name,
					"user": d.user
				})
				project_doc.save(ignore_permissions=True)
