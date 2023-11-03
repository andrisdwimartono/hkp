# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, today
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification

class LAPORANTINDAKANPERBAIKANDANPENCEGAHAN(Document):
	pass
	# def validate(self):
	# 	ltbc = frappe.db.sql("""SELECT * FROM `tabLAPORAN TINDAKAN PERBAIKAN DAN PENCEGAHAN` WHERE name = '{0}'""".format(self.name), as_dict=1)
	# 	if self.workflow_state == "Dibuat":
	# 		self.dibuat_pada = now()
	# 		owner = frappe.db.sql("""SELECT * FROM `tabEmployee` WHERE user_id = '{0}'""".format(self.owner), as_dict=1)
	# 		if owner:
	# 			self.dibuat_oleh = owner[0].name
	# 			self.dibuat_oleh_nama = owner[0].employee_name
				
	# 	if self.workflow_state == "Disetujui":
	# 		if self.disetujui_oleh_user == frappe.session.user:
	# 			assigner = []
	# 			assigner.append(self.diperiksa_oleh_user)
	# 			assigner.append(self.disetujui_oleh_user)
	# 			notification_doc = {
	# 				"type": "Alert",
	# 				"document_type": self.doctype,
	# 				"document_name": self.name,
	# 				"subject": """Laporan {0} sudah disetujui!""".format(self.name),
	# 				"from_user": self.owner,
	# 			}
	# 			enqueue_create_notification(assigner, notification_doc)
	# 			self.disetujui_pada = now()
	# 		else:
	# 			frappe.throw("""Hanya bisa disetujui oleh {0}""".format(self.disetujui_oleh_user))
	# 	if self.workflow_state == "Diperiksa":
	# 		if self.diperiksa_oleh_user == frappe.session.user:
	# 			self.diperiksa_pada = now()
	# 			assigner = []
	# 			assigner.append(self.diperiksa_oleh_user)
	# 			assigner.append(self.disetujui_oleh_user)
	# 			notification_doc = {
	# 				"type": "Alert",
	# 				"document_type": self.doctype,
	# 				"document_name": self.name,
	# 				"subject": """Laporan {0} sudah diperiksa!""".format(self.name),
	# 				"from_user": self.owner,
	# 			}
	# 			enqueue_create_notification(assigner, notification_doc)
	# 		else:
	# 			frappe.throw("""Hanya bisa diperiksa oleh {0}""".format(self.diperiksa_oleh_user))
			
	# 	if self.disetujui_oleh_user and not ltbc:
	# 		assigner = []
	# 		assigner.append(self.disetujui_oleh_user)
	# 		notification_doc = {
	# 			"type": "Alert",
	# 			"document_type": self.doctype,
	# 			"document_name": self.name,
	# 			"subject": """Laporan {0} perlu disetujui oleh anda!""".format(self.name),
	# 			"from_user": self.owner,
	# 		}
	# 		enqueue_create_notification(assigner, notification_doc)
	# 		self.disetujui_pada = now()
	# 	if self.diperiksa_oleh_user and not ltbc:
	# 		assigner = []
	# 		assigner.append(self.diperiksa_oleh_user)
	# 		notification_doc = {
	# 			"type": "Alert",
	# 			"document_type": self.doctype,
	# 			"document_name": self.name,
	# 			"subject": """Laporan {0} perlu diperiksa oleh anda!""".format(self.name),
	# 			"from_user": self.owner,
	# 		}
	# 		enqueue_create_notification(assigner, notification_doc)

def get_permission_query_conditions(user):
	return """(`tabLAPORAN TINDAKAN PERBAIKAN DAN PENCEGAHAN`.`owner` = '{owner}') or (`tabLAPORAN TINDAKAN PERBAIKAN DAN PENCEGAHAN`.`disetujui_oleh_user` = '{owner}') or (`tabLAPORAN TINDAKAN PERBAIKAN DAN PENCEGAHAN`.`diperiksa_oleh_user` = '{owner}' AND (`tabLAPORAN TINDAKAN PERBAIKAN DAN PENCEGAHAN`.workflow_state = 'Disetujui' or `tabLAPORAN TINDAKAN PERBAIKAN DAN PENCEGAHAN`.workflow_state = 'Diperiksa'))""".format(
			owner=frappe.session.user,
		)