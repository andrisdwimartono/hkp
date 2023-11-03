# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LaporanRingkasanAktivitasProyek(Document):
	def validate(self):
		if self.workflow_state == 'Disetujui' and self.notifikasi:
			assigner = []
			for d in self.notifikasi:
				if d.user:
					assigner.append(d.user)
					self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user))
			notification_doc = {
				"type": "Alert",
				"document_type": self.doctype,
				"document_name": self.name,
				"subject": "Laporan ringkasan aktivitas proyek {0} {1}".format(self.project, self.project_name),
				"from_user": self.owner,
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)

@frappe.whitelist()
def get_detail(project, start_date):
	laps = frappe.db.sql("""
			   	SELECT * FROM `tabLaporan Ringkasan Aktivitas Proyek` a
				WHERE a.project = '{0}' AND a.finish_date < '{1}'
			   	ORDER BY a.finish_date DESC
			   	LIMIT 1""".format(project, start_date), as_dict=1)
	if laps:
		return frappe.db.sql("""SELECT * FROM `tabLaporan Ringkasan Aktivitas Proyek Detail` b
					  WHERE parent = '{0}'""".format(laps[0].name), as_dict=1)
	return None
