# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class PreliminaryDesign(Document):
	def validate(self):
		#detail_lasts = frappe.db.sql("""SELECT * FROM `tabPreliminary Design Detail` WHERE parent = '{0}'""".format(self.name), as_dict=1)
		#frappe.throw(str(detail_lasts[0]["name"]))
		
		for d in self.details:
			is_changed = False
			detail_last = frappe.db.sql("""SELECT * FROM `tabPreliminary Design Detail` WHERE parent = '{0}' AND name = '{1}'""".format(self.name, d.name), as_dict=1)
			
			if detail_last:
				if str(d.no_gambar) != str(detail_last[0].no_gambar):
					is_changed = True
					
				if str(d.sub_section) != str(detail_last[0].sub_section):
					is_changed = True
					
				if str(d.drawing) != str(detail_last[0].drawing):
					is_changed = True
					
				if str(d.document_no) != str(detail_last[0].document_no):
					is_changed = True
				
				if str(d.date) != str(detail_last[0].date):
					is_changed = True
					
				if str(d.document) != str(detail_last[0].document):
					is_changed = True
					
				if str(d.completeness) != str(detail_last[0].completeness):
					is_changed = True
					
				if str(d.information) != str(detail_last[0].information):
					is_changed = True
					
				if str(d.submit_date) != str(detail_last[0].submit_date):
					is_changed = True
					
				if str(d.letter_no_submit) != str(detail_last[0].letter_no_submit):
					is_changed = True
					
				if str(d.return_date) != str(detail_last[0].return_date):
					is_changed = True
					
				if str(d.letter_no_return) != str(detail_last[0].letter_no_return):
					is_changed = True
				
				if is_changed:
					d.revision = d.revision+1
					frappe.get_doc({
						"doctype": "Preliminary Design Detail2",
						"document_name": d.name,
						"no_gambar": d.no_gambar,
						"sub_section": d.sub_section,
						"drawing": d.drawing,
						"document_no": d.document_no,
						"date": d.date,
						"project_material_item": d.project_material_item,
						"document": d.document,
						"revision": d.revision,
						"completeness": d.completeness,
						"drawing_number": d.drawing_number,
						"information": d.information,
						"submit_date": d.submit_date,
						"letter_no_submit": d.letter_no_submit,
						"return_date": d.return_date,
						"letter_no_return": d.letter_no_return
					}).insert(
						ignore_permissions=True
					)
					frappe.db.commit()
					remind_user(self.name, document_name=d.document_no)
			else:
				d.revision = 0
				frappe.get_doc({
					"doctype": "Preliminary Design Detail2",
					"document_name": d.name,
					"no_gambar": d.no_gambar,
					"sub_section": d.sub_section,
					"drawing": d.drawing,
					"document_no": d.document_no,
					"date": d.date,
					"project_material_item": d.project_material_item,
					"document": d.document,
					"revision": d.revision,
					"completeness": d.completeness,
					"drawing_number": d.drawing_number,
					"information": d.information,
					"submit_date": d.submit_date,
					"letter_no_submit": d.letter_no_submit,
					"return_date": d.return_date,
					"letter_no_return": d.letter_no_return
				}).insert(
					ignore_permissions=True
				)
				frappe.db.commit()
				# remind_user(self.name, document_name=d.document_no)
		# is_changed = False
		# for d in self.details:
		# 	if (d.document != d.document_last and d.document != None and d.document != ""):
		# 		is_changed = True
		# 		d.document_last = d.document
		# 		if d.document_history == "" or d.document_history == None:
		# 			d.document_history = """{0}""".format(d.document or "")
		# 		else:
		# 			d.document_history = """{0}<br>{1}""".format(d.document_history, d.document)
				
		# 		if d.document_history_display == "" or d.document_history_display == None:
		# 			d.document_history_display = """<a href="{0}">{0}</a>""".format(d.document or "")
		# 		else:
		# 			d.document_history_display = """{0}<br><a href="{1}">{1}</a>""".format(d.document_history_display, d.document)
					
		# 	if is_changed:
		# 		d.revision = d.revision+1
		# 		if d.date_changed_history == "" or d.date_changed_history == None:
		# 			d.date_changed_history = """{0}""".format(datetime.today().strftime('%d-%m-%Y'))
		# 		else:
		# 			d.date_changed_history = """{0}<br>{1}""".format(d.date_changed_history, datetime.today().strftime('%d-%m-%Y'))

@frappe.whitelist()
def get_histories(docname):
	ppd2s = frappe.db.sql("""SELECT * FROM `tabPreliminary Design Detail2` WHERE document_name = '{0}' ORDER BY revision ASC""".format(docname), as_dict=1)

	if ppd2s:
		for d in ppd2s:
			frappe.msgprint("""
					<div class='row'>
					<div class='col-3'>
						Sub Section
					</div>
					<div class='col-9'>
						: {1}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Judul Gambar
					</div>
					<div class='col-9'>
						: {2}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						No Gambar
					</div>
					<div class='col-9'>
						: {3}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Tanggal
					</div>
					<div class='col-9'>
						: {4}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Dokumen
					</div>
					<div class='col-9'>
						: <a href='{6}'>{6}</a>
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Revisi
					</div>
					<div class='col-9'>
						: {7}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Kemajuan
					</div>
					<div class='col-9'>
						: {8}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Infromation
					</div>
					<div class='col-9'>
						: {10}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Submit Date
					</div>
					<div class='col-9'>
						: {11}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Letter No
					</div>
					<div class='col-9'>
						: {12}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Return Date
					</div>
					<div class='col-9'>
						: {13}
					</div>
					</div>
					<div class='row'>
					<div class='col-3'>
						Letter No
					</div>
					<div class='col-9'>
						: {14}
					</div>
					</div>
			""".format(d.no_gambar or "", d.sub_section or "", d.drawing or "", d.document_no or "", d.date or "", d.project_material_item or "", d.document or "", d.revision or "", d.completeness or "", d.drawing_number or "", d.information or "", d.submit_date or "", d.letter_no_submit or "", d.return_date or "", d.letter_no_return or ""))
	else:
		frappe.msgprint("Belum ada data")

def remind_user(docname, document_name=None):
	predes = None
	doc2 = frappe.db.sql("""SELECT * FROM `tabPreliminary Design` WHERE name = '{0}' limit 1""".format(docname), as_dict=1)
	if doc2:
		predes=doc2[0]
	notification_doc = {
		"type": "Alert",
		"document_type": predes.doctype,
		"document_name": predes.name,
		"subject": "Perubahan Preliminary Design untuk dokumen no {0} di {1}".format(document_name, predes.name),
		"from_user": predes.owner or "Administrator",
	}
	
	assigner = [predes.owner]
	adu_employees = frappe.db.sql("""SELECT DISTINCT u.name user_id FROM `tabHas Role` hr
						INNER JOIN tabUser u ON u.name = hr.parent
						WHERE hr.role IN ('Operasional', 'Direktur Operasi') AND hr.parenttype = 'User'""", as_dict=1)
	for hr in adu_employees:
		assigner.append(hr.user_id)
	notification_doc = frappe._dict(notification_doc)
	from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
	make_notification_logs(notification_doc, assigner)