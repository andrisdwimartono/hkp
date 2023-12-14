# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	today,
)
import datetime

class PeminjamanDokumen(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.tanggal_pinjam, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabPeminjaman Dokumen` WHERE tanggal_pinjam between '{0}' and '{1}'""".format("{0}-01-01".format(mydate.year), "{0}-12-31".format(mydate.year)), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/ADU/PDOK/{0}/{1}".format(bulan, mydate.year-2000, urut2)
		else:
			self.name = "001/ADU/PDOK/{0}/{1}".format(bulan, mydate.year-2000)

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
