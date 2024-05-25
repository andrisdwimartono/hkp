# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import (
	today,
)

class USULANMENGIKUTITENDER(Document):
	def validate(self):
		if self.workflow_state == "Disetujui":
			self.keputusan = "Diikuti"
			# for d in self.process_rules:
			# 	if self.workflow_state == d.state:
			# 		self.catatan_direktur = d.comment
		elif self.workflow_state == "Rejected":
			self.keputusan = "Tidak Diikuti"
			# for d in self.process_rules:
			# 	if self.workflow_state == d.state:
			# 		self.catatan_direktur = d.comment
	
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabUSULAN MENGIKUTI TENDER` WHERE name like '%/{0}/{1}'""".format(bulan, mydate.year), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/SAR/USM/{0}/{1}".format(bulan, mydate.year, urut2)
		else:
			self.name = "01/SAR/USM/{0}/{1}".format(bulan, mydate.year)

	# def on_update(self):
	# 	for d in self.process_rules:
	# 		frappe.msgprint(str(d.state))
	# 		frappe.msgprint(str(d.comment))
	# 	if self.workflow_state == "Disetujui":
	# 		self.keputusan = "Diikuti"
	# 		for d in self.process_rules:
	# 			if self.workflow_state == d.state:
	# 				frappe.msgprint(d.comment)
	# 				frappe.db.sql("""UPDATE `tabUSULAN MENGIKUTI TENDER` SET catatan_direktur = '{0}' WHERE name = '{1}'""".format(d.comment, self.name))
	# 				frappe.db.commit()
	# 	elif self.workflow_state == "Rejected":
	# 		self.keputusan = "Tidak Diikuti"
	# 		for d in self.process_rules:
	# 			if self.workflow_state == d.state:
	# 				frappe.msgprint(d.comment)
	# 				frappe.db.sql("""UPDATE `tabUSULAN MENGIKUTI TENDER` SET catatan_direktur = '{0}' WHERE name = '{1}'""".format(d.comment, self.name))
	# 				frappe.db.commit()