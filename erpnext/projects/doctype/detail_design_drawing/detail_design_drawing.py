# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DetailDesignDrawing(Document):
	def validate(self):
		# check project unique
		is_project_exist = frappe.db.sql("""
			SELECT name FROM `tabDetail Design Drawing` WHERE project = '{0}' AND name != '{1}'
		""".format(self.project, self.name), as_dict=1)
		if is_project_exist:
			frappe.throw("Project sudah ada di detail design drawing lain ({0}).".format(is_project_exist[0].name))