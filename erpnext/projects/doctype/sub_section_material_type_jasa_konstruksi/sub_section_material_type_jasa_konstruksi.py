# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SubSectionMaterialTypeJasaKonstruksi(Document):
	def on_trash(self):
		frappe.db.sql("""DELETE FROM `tabSub Section Material Type Entries` WHERE type = '{0}' AND document_of_name = '{1}'""".format(self.doctype, self.name))
	def validate(self):
		document_names = []
		for d in self.services:
			xx = frappe.db.sql("""SELECT * FROM `tabSub Section Material Type Entries` WHERE document_name = '{0}'""".format(d.name), as_dict=1)
			if xx:
				document_names.append(xx[0].name)
				a_doc = frappe.get_doc("Sub Section Material Type Entries", xx[0].name)
				a_doc.type 						= self.doctype
				a_doc.document_of_name 			= self.name
				a_doc.sub_section 				= self.sub_section
				a_doc.sub_project_sub_section 	= self.sub_project_sub_section
				a_doc.item 						= d.upah
				a_doc.item_name 				= d.upah
				a_doc.uom 						= d.uom
				a_doc.location 					= d.location
				a_doc.year 						= d.year
				a_doc.price 					= d.price
				a_doc.description				= d.description
				a_doc.document_name 			= d.name
				a_doc.save(ignore_permissions=True)
			else:
				a_doc = frappe.get_doc({
					"doctype"					: "Sub Section Material Type Entries",
					"type"						: self.doctype,
					"document_of_name"			: self.name,
					"sub_section"				: self.sub_section,
					"sub_project_sub_section"	: self.sub_project_sub_section,
					"item"						: d.upah,
					"item_name"					: d.upah,
					"uom"						: d.uom,
					"location"					: d.location,
					"year"						: d.year,
					"price"						: d.price,
					"description"				: d.description,
					"document_name"				: d.name
				})
				a_doc.insert(ignore_permissions=True)
				document_names.append(a_doc.name)
		aa = frappe.db.sql("""SELECT * FROM `tabSub Section Material Type Entries` WHERE type = '{0}' AND document_of_name = '{1}'""".format(self.doctype, self.name), as_dict=1)
		for a in aa:
			if a.name not in document_names:
				frappe.db.sql("""DELETE FROM `tabSub Section Material Type Entries` WHERE type = '{0}' AND document_of_name = '{1}' AND name = '{2}'""".format(self.doctype, self.name, a.name))
