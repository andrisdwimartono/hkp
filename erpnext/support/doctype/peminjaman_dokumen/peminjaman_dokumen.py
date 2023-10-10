# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	today,
)

class PeminjamanDokumen(Document):
	pass

@frappe.whitelist()
def alert_kembalikan():
	x = add_days(today(), -1)
	peminjamans = frappe.db.sql("""SELECT * FROM `tabPeminjaman Dokumen` WHERE workflow_state = 'Disetujui' AND tanggal_mengembalikan = '{0}'""".format(x), as_dict=1)
	if peminjamans:
		for d in peminjamans:
			doc = frappe.get_doc("Peminjaman Dokumen", d.name)
			assigner = [doc.owner]
			for x in doc.process_rules:
				assigner.append(d.user)
			doc.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user))
			notification_doc = {
				"type": "Alert",
				"document_type": doc.doctype,
				"document_name": doc.name,
				"subject": "Peminjaman Dokumen {0} harus dikembalikan besok tanggal {1}".format(doc.name, doc.tanggal_dikembalikan),
				"from_user": doc.owner,
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)
