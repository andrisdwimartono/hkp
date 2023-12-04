# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	today,
)

class MasterItemPekerjaan(Document):
	def autoname(self):
		self.name = """MK/{0}""".format(self.sub_contract_hand_over)

	def validate(self):
		dts = frappe.db.sql("""SELECT * FROM `tabMaster Item Pekerjaan` WHERE sub_contract_hand_over = '{0}' AND name != '{1}'""".format(self.sub_contract_hand_over, self.name), as_dict=1)
		if dts:
			frappe.throw("""Kontrak Item Pekerjaan untuk SPK ini sudah dibuat <a href="/app/master-item-pekerjaan/{0}">{0}</a>""".format(dts[0].name))
		# self.revisi = self.revisi+1
		# self.append("detail_revisi", {
		# 	"tanggal_revisi": today(),
		# 	"revisi": self.revisi
		# })

		bobot_total = 0
		bobot_total_gr = 0
		vol_kontrak_gr = 0

		for d in reversed(self.detail):
			if d.group != 1:
				bobot_total = bobot_total+d.bobot

				bobot_total_gr = bobot_total_gr+d.bobot
				vol_kontrak_gr = vol_kontrak_gr+d.vol_kontrak
			else:
				d.bobot = bobot_total_gr
				d.vol_kontrak = None
				
				bobot_total_gr = 0
				vol_kontrak_gr = 0
		if bobot_total != 100:
			frappe.throw("Total Bobot harus 100")
