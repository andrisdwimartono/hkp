# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import frappe
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification, make_notification_logs
from frappe.utils import (
	today,
)\


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def query_task(doctype, txt, searchfield, start, page_len, filters):
	from frappe.desk.reportview import build_match_conditions

	search_string = "%%%s%%" % txt
	order_by_string = "%s%%" % txt
	match_conditions = build_match_conditions("Task")
	match_conditions = ("and" + match_conditions) if match_conditions else ""

	return frappe.db.sql(
		"""select name, subject from `tabTask`
		where (`%s` like %s or `subject` like %s) %s
		order by
			case when `subject` like %s then 0 else 1 end,
			case when `%s` like %s then 0 else 1 end,
			`%s`,
			subject
		limit %s, %s"""
		% (searchfield, "%s", "%s", match_conditions, "%s", searchfield, "%s", searchfield, "%s", "%s"),
		(search_string, search_string, order_by_string, order_by_string, start, page_len),
	)

@frappe.whitelist()
def get_next_process_rule(doctype, docname):
	nprs = frappe.db.sql("""
	SELECT * FROM `tabProcess Rule` pr
	WHERE pr.parenttype = '{0}' AND pr.parent = '{1}' AND (pr.status = 'Unprocessed' or pr.status = 'No')
	ORDER BY pr.idx ASC
	LIMIT 1
	""".format(doctype, docname), as_dict=1)
	if nprs:
		if nprs[0].user == frappe.session.user:
			return nprs[0]
		else:
			return None
	else:
		return None

@frappe.whitelist()
def save_process_rule(docname, status, comment=""):
	nprs = frappe.db.sql("""
	SELECT pr.*, e.employee_name FROM `tabProcess Rule` pr
	LEFT JOIN `tabEmployee` e ON e.user_id = pr.user
	WHERE pr.name = '{0}'
	ORDER BY pr.idx ASC
	LIMIT 1
	""".format(docname), as_dict=1)
	if not nprs:
		return False
	else:
		if frappe.session.user != nprs[0].user:
			frappe.throw("Hanya bisa diproses oleh {0}".format(nprs[0].employee_name))

	frappe.db.sql("""
	UPDATE `tabProcess Rule` SET status = '{1}', comment = '{2}', process_time = now()
	WHERE name = '{0}'
	""".format(docname, status, comment))
	
	doc = frappe.get_doc(nprs[0].parenttype, nprs[0].parent)
	if status == 'Yes':
		doc.add_comment('Edit', '{0} telah {1}'.format(nprs[0].employee_name, nprs[0].aksi))
		npr = get_a_process_rule(nprs[0].name, 1)
		if npr:
			assigner = [npr.user]
			notify_user(npr.parenttype, npr.parent, nprs[0].user, assigner, "{0} membutuhkan {1} dari anda setelah proses {2} oleh {3}".format(nprs[0].parent, npr.aksi, nprs[0].aksi, nprs[0].employee_name))
			doc.add_comment('Edit', text='Notifikasi {0} terkirim ke {1}'.format(npr.aksi, npr.user))

	else:
		npr = get_a_process_rule(nprs[0].name, -1)
		doc.add_comment('Edit', '{0} menolak {1}'.format(nprs[0].employee_name, nprs[0].aksi))
		if npr:
			assigner = [npr.user]
			notify_user(npr.parenttype, npr.parent, nprs[0].user, assigner, "{0} telah menolak {1} {2} dan dikembalikan ke {3}".format(nprs[0].employee_name, nprs[0].aksi, nprs[0].parent, npr.employee_name))
			doc.add_comment('Edit', text='Notifikasi {0} terkirim ke {1}'.format(npr.aksi, npr.user))

			frappe.db.sql("""
			UPDATE `tabProcess Rule` SET status = 'Unprocessed', comment = null
			WHERE name = '{0}'
			""".format(npr.name))
	frappe.msgprint("Anda telah {0}".format(status))
	return True

def get_a_process_rule(name, seq):
	nprs = frappe.db.sql("""
	SELECT * FROM `tabProcess Rule` pr
	WHERE pr.name = '{0}'
	""".format(name), as_dict=1)
	if nprs:
		nprs2 = frappe.db.sql("""
		SELECT pr.*, e.employee_name FROM `tabProcess Rule` pr
		LEFT JOIN `tabEmployee` e ON e.user_id = pr.user
		WHERE pr.parenttype = '{0}' AND pr.parent = '{1}' AND pr.idx = {2}
		ORDER BY pr.idx ASC
		LIMIT 1
		""".format(nprs[0].parenttype, nprs[0].parent, (nprs[0].idx+seq)), as_dict=1)
		if nprs2:
			return nprs2[0]
		else:
			return None
	else:
		return None

def notify_user(doctype, docname, from_user, assigner, subject):
	notification_doc = {
		"type": "Alert",
		"document_type": doctype,
		"document_name": docname,
		"subject": subject,
		"from_user": from_user,
	}
	enqueue_create_notification(assigner, notification_doc)

@frappe.whitelist()
def get_process_rules(doctype):
	return frappe.db.sql("""SELECT b.* FROM `tabWorkflow` a 
	INNER JOIN `tabWorkflow Document State` b ON b.parent = a.name
	WHERE a.document_type = '{0}' AND a.is_active = 1
	ORDER BY b.idx ASC""".format(doctype), as_dict=1)

def set_default_process_rules(doc, method=None):
	return
	prs = frappe.db.sql("""
		SELECT wds.* FROM `tabWorkflow` w
		INNER JOIN `tabWorkflow Document State` wds ON wds.parent = w.name
		WHERE w.document_type = '{0}' AND w.is_optional_state = 1
		ORDER BY w.idx ASC
	""".format(doc.doctype), as_dict=1)
	if prs:
		for pr in prs:
			assigner = [pr.user]
			if frappe.flags.in_install:
				return
			notify_user(doc.doctype, doc.name, doc.owner, assigner, "{2} {0} membutuhkan {1} dari anda".format(doc.name, pr.state, doc.doctype))
			doc.add_comment('Edit', text='Notifikasi {0} terkirim ke {1}'.format(pr.state, pr.user))
		return

	frappe.db.sql("""UPDATE `tabProcess Rules` SET process_time = now() WHERE parent = '{0}' AND idx = 1 AND state = 'Dibuat';""".format(doc.name))

	prsn = frappe.db.sql("""SELECT * FROM `tabProcess Rules` WHERE parent = '{1}' AND parenttype = '{0}' AND idx=2;""".format(doc.doctype, doc.name), as_dict=1)
	
	if prsn:
		prn = prsn[0]
		assigner = [prn.user]
		if frappe.flags.in_install:
			return
		notify_user(doc.doctype, doc.name, doc.owner, assigner, "{3} {0} membutuhkan {1} dari anda setelah proses {2}".format(prn.parent, prn.state, 'Dibuat', doc.doctype))
		doc.add_comment('Edit', text='Notifikasi {0} terkirim ke {1}'.format(prn.state, prn.user))

@frappe.whitelist()
def notifikasi_schedule_aktivitas():
	employees = frappe.db.sql("""SELECT ec.*, e.employee_name, e.user_id, date_format(ec.tanggal, "%d-%m-%Y") dend FROM `tabSchedule Aktivitas` ec
						   INNER JOIN `tabEmployee` e ON e.name = ec.employee
						   WHERE ec.tanggal_notifikasi = '{0}'""".format(today()), as_dict=1)
	
	for d in employees:
		notification_doc = {
			"type": "Alert",
			"document_type": "Schedule Aktivitas",
			"document_name": d.name,
			"subject": "Schedule aktivitas {1} yang akan dilaksanakan di tanggal {2}".format(d.employee_name, d.agenda, d.dend),
			"from_user": d.user_id or "Administrator",
		}
		
		assigner = [d.user_id]
		for x in frappe.db.sql("""SELECT * FROM `tabPeserta Rapat` WHERE parent = '{0}'""".format(d.name), as_dict=1):
			assigner.append(x.user)
		notification_doc = frappe._dict(notification_doc)
		
		make_notification_logs(notification_doc, assigner)