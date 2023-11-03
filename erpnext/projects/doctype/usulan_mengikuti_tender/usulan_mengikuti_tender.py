# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

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