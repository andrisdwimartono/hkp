# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class KPIKaryawan(Document):
	def validate(self):
		if frappe.db.sql("""SELECT * FROM `tabKPI Karyawan` WHERE employee = '{0}' AND name != '{1}'""".format(self.employee, self.name), as_dict=1):
			frappe.throw("KPI Karyawan tersebut sudah dibuat")
