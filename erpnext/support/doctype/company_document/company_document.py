# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	today,
)

class CompanyDocument(Document):
	pass

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