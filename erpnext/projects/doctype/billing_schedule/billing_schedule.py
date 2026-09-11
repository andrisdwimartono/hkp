# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate

class BillingSchedule(Document):
	def validate(self):
		if self.status == "Completed":
			# check documents availability
			for d in self.documents:
				if d.avaibility != "Available":
					frappe.throw(_("Dokumen {0} belum tersedia!").format(d.document_name))

			# check expected_end_date, bond_validity_period, and sbu_validity_period vs billing_date
			if getdate(self.expected_end_date) < getdate(self.billing_date):
				frappe.throw(_("Tanggal Berakhirnya Proyek harus lebih besar dari Tanggal Tagihan!"))
			if getdate(self.bond_validity_period) < getdate(self.billing_date):
				frappe.throw(_("Masa Berlaku Jaminan harus lebih besar dari Tanggal Tagihan!"))
			if getdate(self.sbu_validity_period) < getdate(self.billing_date):
				frappe.throw(_("Masa Berlaku SBU harus lebih besar dari Tanggal Tagihan!"))

@frappe.whitelist()
def get_max_termin_by_project(project):
	return frappe.db.sql("""
		SELECT MAX(termin) as termin FROM `tabBilling Schedule` WHERE project=%(project)s
	""", {"project": project}, as_dict=True)

@frappe.whitelist()
def get_sbu_expired_date():
	return frappe.db.sql("""
		SELECT tanggal_expired as expired_date FROM `tabCompany Document` WHERE name='SBUJK - Konstruksi Sipil dan Elektrikal'
	""", as_dict=True)

