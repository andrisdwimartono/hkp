# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AbsensiHKPDetail(Document):
	def validate(self):
		emp = frappe.db.sql("""SELECT * FROM `tabEmployee` WHERE emp_code = '{0}'""".format(self.emp_code), as_dict=1)
		if emp:
			self.employee = emp[0].name
			self.employee_name = emp[0].employee_name
