# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	today,
)

class CompanyDocument(Document):
	def validate(self):
		if self.employee and self.check_is_sertifikat_karyawan(self.parent_company_document):
			xs = frappe.db.sql("""SELECT * FROM `tabEmployee Certificate` WHERE parent = '{0}' AND company_document = '{1}'""".format(self.employee, self.name), as_dict=1)
			if xs:
				emp_doc = frappe.db.sql("""update `tabEmployee Certificate` set document = '{0}', date_accquired = '{1}', date_end = '{2}' where name = '{3}'""".format(self.document, self.tanggal_terbit, self.tanggal_expired, self.name))
			else:
				emp_doc = frappe.get_doc("Employee", self.employee)
				emp_doc.append("employee_certificate", {
					"certificate": "K3-Ketinggian-Tower Latice",
					"company_document": self.name,
					"document": self.document,
					"date_accquired": self.tanggal_terbit,
					"date_end": self.tanggal_expired
				})
				emp_doc.save(ignore_permissions=True)
			frappe.db.commit()
			

	def check_is_sertifikat_karyawan(self, docname):
		docs = frappe.db.sql("""SELECT * FROM `tabCompany Document` WHERE name = '{0}'""".format(docname), as_dict=1)
		while docs and docs[0].parent_company_document != None and docs[0].parent_company_document != "":
			if docs[0].parent_company_document == "Sertifikat Karyawan":
				return True
			docs = frappe.db.sql("""SELECT * FROM `tabCompany Document` WHERE name = '{0}'""".format(docs[0].parent_company_document), as_dict=1)
		return False


@frappe.whitelist()
def get_company_document_obsolete():
	x = add_days(today(), -90)
	company_documents = frappe.db.sql("""SELECT a.*, date_format(a.tanggal_expired, "%d-%m-%Y") dend FROM `tabCompany Document` a WHERE a.tanggal_expired = '{0}'""".format(x), as_dict=1)
	for d in company_documents:
		notification_doc = {
			"type": "Alert",
			"document_type": "Company Document",
			"document_name": d.name,
			"subject": "Dokumen Perusahaan {0} akan expired di {1}".format(d.name, d.dend),
			"from_user": d.owner or "Administrator",
		}
		
		assigner = [d.owner]
		adu_employees = frappe.db.sql("""SELECT DISTINCT u.name user_id FROM `tabHas Role` hr
							   INNER JOIN tabUser u ON u.name = hr.parent
							   WHERE hr.role IN ('ADU') AND hr.parenttype = 'User'""", as_dict=1)
		for hr in adu_employees:
			assigner.append(hr.user_id)
		notification_doc = frappe._dict(notification_doc)
		from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
		make_notification_logs(notification_doc, assigner)