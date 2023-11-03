import frappe
from frappe.utils import (
	add_days,
	today,
	getdate,
)
from frappe import _

from frappe.desk.doctype.notification_log.notification_log import make_notification_logs

def update_lead_phone_numbers(contact, method):
	if contact.phone_nos:
		contact_lead = contact.get_link_for("Lead")
		if contact_lead:
			phone = mobile_no = contact.phone_nos[0].phone

			if len(contact.phone_nos) > 1:
				# get the default phone number
				primary_phones = [
					phone_doc.phone for phone_doc in contact.phone_nos if phone_doc.is_primary_phone
				]
				if primary_phones:
					phone = primary_phones[0]

				# get the default mobile number
				primary_mobile_nos = [
					phone_doc.phone for phone_doc in contact.phone_nos if phone_doc.is_primary_mobile_no
				]
				if primary_mobile_nos:
					mobile_no = primary_mobile_nos[0]

			lead = frappe.get_doc("Lead", contact_lead)
			lead.db_set("phone", phone)
			lead.db_set("mobile_no", mobile_no)

@frappe.whitelist()
def get_hasil_pembukaan_tender(doctype):
	return frappe.db.sql("""SELECT b.* FROM `tabWorkflow` a 
	INNER JOIN `tabWorkflow Document State` b ON b.parent = a.name
	WHERE a.document_type = '{0}' AND a.is_active = 1
	ORDER BY b.idx ASC""".format(doctype), as_dict=1)

@frappe.whitelist()
def get_customer_notif():
	x = add_days(today(), -2)
	y = getdate(x)
	weekdays =["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	weekdaysid =["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu"]
	customers = frappe.db.sql("""SELECT * FROM tabCustomer c
						   WHERE (c.jenis_notifikasi = 'Custom' AND c.notifikasi_di_tanggal = '{0}')
						   OR (c.jenis_notifikasi = 'Bulanan' AND c.tanggal_notifikasi = {1})
						   OR (c.jenis_notifikasi = 'Mingguan' AND c.hari_notifikasi = '{2}')""".format(x, y.day, weekdays[y.weekday()]), as_dict=1)
	for d in customers:
		if d.disabled != 1:
			if d.jenis_notifikasi == 'Mingguan':
				notification_doc = {
					"type": "Alert",
					"document_type": "Customer",
					"document_name": d.name,
					"subject": "Pelanggan {0} perlu anda kunjungi di hari {1}".format(d.customer_name, weekdaysid[y.weekday()]),
					"from_user": "Administrator",
				}
				
				assigner = ["Administrator"]
				crm_employees = frappe.db.sql("""SELECT DISTINCT u.name user_id FROM `tabHas Role` hr
									INNER JOIN tabUser u ON u.name = hr.parent
									WHERE hr.role IN ('Pemasaran', 'Manajer Pemasaran') AND hr.parenttype = 'User'""", as_dict=1)
				for cr in crm_employees:
					assigner.append(cr.user_id)
				notification_doc = frappe._dict(notification_doc)
				
				make_notification_logs(notification_doc, assigner)
			
			if d.jenis_notifikasi == 'Bulanan' or d.jenis_notifikasi == 'Custom':
				notification_doc = {
					"type": "Alert",
					"document_type": "Customer",
					"document_name": d.name,
					"subject": "Pelanggan {0} perlu anda kunjungi di tanggal {1}".format(d.customer_name, y.day if d.jenis_notifikasi == 'Bulanan' else d.notifikasi_di_tanggal),
					"from_user": "Administrator",
				}
				
				assigner = ["Administrator"]
				crm_employees = frappe.db.sql("""SELECT DISTINCT u.name user_id FROM `tabHas Role` hr
									INNER JOIN tabUser u ON u.name = hr.parent
									WHERE hr.role IN ('Pemasaran', 'Manajer Pemasaran') AND hr.parenttype = 'User'""", as_dict=1)
				for cr in crm_employees:
					assigner.append(cr.user_id)
				notification_doc = frappe._dict(notification_doc)
				
				make_notification_logs(notification_doc, assigner)