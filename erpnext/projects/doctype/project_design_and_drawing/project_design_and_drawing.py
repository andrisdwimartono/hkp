# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class ProjectDesignandDrawing(Document):
	def validate(self):
		return
		# is_changed = False
		# for d in self.preliminary_design:
		# 	#hanya kalau upload ulang, baru dianggap ada perubahan
		# 	#belum diubah
		# 	#project material item sudah diganti drawing
		# 	if d.sub_section != d.sub_section_last or d.date != d.date_last or d.project_material_item != d.project_material_item_last or (d.document != d.document_last and d.document != None and d.document != "") or d.completeness != d.completeness_last or d.drawing_number != d.drawing_number_last or d.information != d.information_last:
		# 		is_changed = True
		# 		# d.project_document_type_last = d.project_document_type
		# 		# if d.project_document_type_history == "" or d.project_document_type_history == None:
		# 		# 	d.project_document_type_history = """{0}""".format(d.project_document_type or "")
		# 		# else:
		# 		# 	d.project_document_type_history = """{0}<br>{1}""".format(d.project_document_type_history, d.project_document_type)
			
		# 		d.sub_section_last = d.sub_section
		# 		if d.sub_section_history == "" or d.sub_section_history == None:
		# 			d.sub_section_history = """{0}""".format(d.sub_section or "")
		# 		else:
		# 			d.sub_section_history = """{0}<br>{1}""".format(d.sub_section_history, d.sub_section)
			
		# 		d.date_last = d.date
		# 		if d.date_history == "" or d.date_history == None:
		# 			d.date_history = """{0}""".format(d.date or "")
		# 		else:
		# 			d.date_history = """{0}<br>{1}""".format(d.date_history, d.date)

		# 		d.project_material_item_last = d.project_material_item
		# 		if d.project_material_item_history == "" or d.project_material_item_history == None:
		# 			d.project_material_item_history = """{0}""".format(d.project_material_item or "")
		# 		else:
		# 			d.project_material_item_history = """{0}<br>{1}""".format(d.project_material_item_history, d.project_material_item)
			
		# 		d.document_last = d.document
		# 		if d.document_history == "" or d.document_history == None:
		# 			d.document_history = """{0}""".format(d.document or "")
		# 		else:
		# 			d.document_history = """{0}<br>{1}""".format(d.document_history, d.document)
				
		# 		if d.document_history_display == "" or d.document_history_display == None:
		# 			d.document_history_display = """<a href="{0}">{0}</a>""".format(d.document or "")
		# 		else:
		# 			d.document_history_display = """{0}<br><a href="{1}">{1}</a>""".format(d.document_history_display, d.document)

		# 		d.completeness_last = d.completeness
		# 		if d.completeness_history == "" or d.completeness_history == None:
		# 			d.completeness_history = """{0}""".format(d.completeness or "")
		# 		else:
		# 			d.completeness_history = """{0}<br>{1}""".format(d.completeness_history, d.completeness)
			
		# 		d.drawing_number_last = d.drawing_number
		# 		if d.drawing_number_history == "" or d.drawing_number_history == None:
		# 			d.drawing_number_history = """{0}""".format(d.drawing_number or "")
		# 		else:
		# 			d.drawing_number_history = """{0}<br>{1}""".format(d.drawing_number_history, d.drawing_number)
			
		# 		d.information_last = d.information
		# 		if d.information_history == "" or d.information_history == None:
		# 			d.information_history = """{0}""".format(d.information or "")
		# 		else:
		# 			d.information_history = """{0}<br>{1}""".format(d.information_history, d.information)
					
		# 	if is_changed:
		# 		d.revision = d.revision+1
		# 		if d.date_changed_history == "" or d.date_changed_history == None:
		# 			d.date_changed_history = """{0}""".format(datetime.today().strftime('%d-%m-%Y'))
		# 		else:
		# 			d.date_changed_history = """{0}<br>{1}""".format(d.date_changed_history, datetime.today().strftime('%d-%m-%Y'))
