# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class PreliminaryDesign(Document):
	def validate(self):
		is_changed = False
		for d in self.details:
			if (d.document != d.document_last and d.document != None and d.document != ""):
				is_changed = True
				d.document_last = d.document
				if d.document_history == "" or d.document_history == None:
					d.document_history = """{0}""".format(d.document or "")
				else:
					d.document_history = """{0}<br>{1}""".format(d.document_history, d.document)
				
				if d.document_history_display == "" or d.document_history_display == None:
					d.document_history_display = """<a href="{0}">{0}</a>""".format(d.document or "")
				else:
					d.document_history_display = """{0}<br><a href="{1}">{1}</a>""".format(d.document_history_display, d.document)
					
			if is_changed:
				d.revision = d.revision+1
				if d.date_changed_history == "" or d.date_changed_history == None:
					d.date_changed_history = """{0}""".format(datetime.today().strftime('%d-%m-%Y'))
				else:
					d.date_changed_history = """{0}<br>{1}""".format(d.date_changed_history, datetime.today().strftime('%d-%m-%Y'))
