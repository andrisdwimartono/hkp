# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.projects.bot import send_message

class InformasiTender(Document):
	def after_insert(self):
		send_message("#{0} Tender baru '{1}' dari {2} telah dibuat.".format(self.name, self.nama_pekerjaan, self.customer), chat_id="-1002958782136")

	def validate(self):
		# get last status from database
		last_status = None
		last_hasil_tender = None
		if not self.get("__islocal"):
			last_status = frappe.db.get_value("Informasi Tender", self.name, "keputusan")
			last_hasil_tender = frappe.db.get_value("Informasi Tender", self.name, "hasil_tender")

		# if status changed to "Diikuti" or "Tidak Diikuti", send message
		if self.keputusan == "Diikuti" and last_status != "Diikuti":
			send_message("#{0} Tender '{1}' dari {2} diikuti ✅.".format(self.name, self.nama_pekerjaan, self.customer), chat_id="-1002958782136")
		elif self.keputusan == "Tidak Diikuti" and last_status != "Tidak Diikuti":
			send_message("#{0} Tender '{1}' dari {2} tidak diikuti ❌.".format(self.name, self.nama_pekerjaan, self.customer), chat_id="-1002958782136")
		elif self.keputusan == "" and last_status != "":
			send_message("#{0} Tender '{1}' dari {2} ditunda keputusannya ⏳.".format(self.name, self.nama_pekerjaan, self.customer), chat_id="-1002958782136")
		else:
			# if hasil_tender changed to "Lolos" or "Tidak Lolos", send message
			if self.hasil_tender == "Lolos" and last_hasil_tender != "Lolos":
				send_message("#{0} Tender '{1}' dari {2} lolos 🏆🏆🏆.".format(self.name, self.nama_pekerjaan, self.customer), chat_id="-1002958782136")
			elif self.hasil_tender == "Tidak Lolos" and last_hasil_tender != "Tidak Lolos":
				send_message("#{0} Tender '{1}' dari {2} tidak lolos 🚫.".format(self.name, self.nama_pekerjaan, self.customer), chat_id="-1002958782136")
			elif self.hasil_tender == "" and last_hasil_tender != "":
				send_message("#{0} Tender '{1}' dari {2} ditunda keputusan kelolosannya ⏳.".format(self.name, self.nama_pekerjaan, self.customer), chat_id="-1002958782136")
			else:
				# if change on another field, send update message
				if not self.get("__islocal"):
					send_message("#{0} Tender '{1}' dari {2} telah diperbarui oleh {3}.".format(self.name, self.nama_pekerjaan, self.customer, frappe.session.user), chat_id="-1002958782136")

def reminder_pengisian_tender():
	tenders = frappe.get_all("Informasi Tender", filters={"ingatkan_sebelum": ["!=", 0], "jatuh_tempo": ["!=", None]}, fields=["name"])
	for tender in tenders:
		tender = frappe.get_doc("Informasi Tender", tender.name)
		if tender.ingatkan_sebelum != 0 and tender.jatuh_tempo is not None and tender.jatuh_tempo != "" and tender.hasil_tender == "":
			# calculate reminder date with tanggal jatuh_tempo
			from frappe.utils import add_days, today, date_diff, getdate
			reminder_date = add_days(tender.jatuh_tempo, -tender.ingatkan_sebelum)
			if reminder_date <= getdate(today()):
				send_message("#{0} Pengisian tender '{1}' dari {2} akan jatuh tempo pada {3}. Harap segera diisi ⚠️⚠️⚠️.".format(tender.name, tender.nama_pekerjaan, tender.customer, tender.jatuh_tempo), chat_id="-1002958782136")

def reminder_jaminan_penawaran():
	tenders = frappe.get_all("Informasi Tender", filters={"ingatkan_sebelum_jaminan_penawaran": ["!=", 0], "jatuh_tempo_jaminan_penawaran": ["!=", None]}, fields=["name"])
	for tender in tenders:
		tender = frappe.get_doc("Informasi Tender", tender.name)
		if tender.ingatkan_sebelum_jaminan_penawaran != 0 and tender.jatuh_tempo_jaminan_penawaran is not None and tender.jatuh_tempo_jaminan_penawaran != "" and tender.hasil_tender == "":
			# calculate reminder date with tanggal jatuh_tempo_jaminan_penawaran
			from frappe.utils import add_days, today, date_diff, getdate
			reminder_date = add_days(tender.jatuh_tempo_jaminan_penawaran, -tender.ingatkan_sebelum_jaminan_penawaran)
			if reminder_date <= getdate(today()):
				send_message("#{0} Jaminan Penawaran t	ender '{1}' dari {2} akan jatuh tempo pada {3}. Harap segera diisi ⚠️⚠️⚠️.".format(tender.name, tender.nama_pekerjaan, tender.customer, tender.jatuh_tempo_jaminan_penawaran), chat_id="-1002958782136")