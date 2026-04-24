# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RealisasiKPI(Document):
	def validate(self):
		if self.approver and self.user_approver is None:
			frappe.throw("Approver tidak memiliki akun user.")
		self.check_employee_kpi_per_month()

	def on_submit(self):
		if self.user_approver != frappe.session.user:
			frappe.throw("Hanya approver yang dapat mensubmit Realisasi KPI ini.")

	def check_employee_kpi_per_month(self):
		# if employee already have kpi in same month of date, throw error
		if frappe.db.sql("""
			SELECT
				*
			FROM `tabRealisasi KPI`
			WHERE name != '{0}' AND employee = '{1}' AND MONTH(date) = MONTH('{2}') AND YEAR(date) = YEAR('{2}')
		""".format(self.name, self.employee, self.date)):
			frappe.throw("Employee already have KPI in this month.")


def get_permission_query_conditions(user):
	employee = frappe.db.sql("""SELECT * FROM `tabEmployee` where user_id = '{0}'""".format(frappe.session.user), as_dict=1)
	if employee and employee[0].name:
		return """(`tabRealisasi KPI`.employee = '{0}' or `tabRealisasi KPI`.approver = '{0}')""".format(employee[0].name)
	else:
		return ""

def update_aktivitas_pekerjaan():
	list_jabatan_kpi = frappe.db.sql("""
		SELECT
			*
		FROM `tabDesignation KPI`
	""", as_dict=1)
	for jabatan_kpi in list_jabatan_kpi:
		list_realisasi_kpi = frappe.db.sql("""
			SELECT
				*
			FROM `tabRealisasi KPI`
			WHERE designation = '{0}'
		""".format(jabatan_kpi.parent), as_dict=1)
		for realisasi_kpi in list_realisasi_kpi:
			frappe.db.sql("""
				UPDATE `tabRealisasi KPI Detail`
				SET aktivitas_pekerjaan = '{0}'
				WHERE parent = '{1}' AND kpi = '{2}'
			""".format((jabatan_kpi.aktivitas_pekerjaan or ""), realisasi_kpi.name, jabatan_kpi.kpi))
		frappe.db.commit()
		print("Updated Realisasi KPI for Designation: " + jabatan_kpi.parent)