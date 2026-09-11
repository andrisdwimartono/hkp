# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet

class ProjectDocumentation(NestedSet):
	def autoname(self):
		if self.is_group == 1 or self.is_group == '1' or self.is_group == True or self.is_group == 'True' or self.is_group == 'yes':
			self.name = """PD-{0}-{1}""".format(
				self.project,
				self.project_name.replace(' ', '-')
			)
		else:
			count = frappe.db.count("Project Documentation", {
				'parent_project_documentation': self.parent_project_documentation,
			})

			parent_doc = frappe.get_doc("Project Documentation", self.parent_project_documentation)

			# check if name exist
			while frappe.db.exists("Project Documentation", "PD-{0}#{1}".format(
				parent_doc.project,
				str(count+1)
			)):
				count += 1

			self.name = """PD-{0}#{1}""".format(
				parent_doc.project,
				str(count+1)
			)
	
	def validate(self):
		# if group, no file
		if self.is_group == 1 or self.is_group == '1' or self.is_group == True or self.is_group == 'True' or self.is_group == 'yes':
			if self.parent != 'HKP':
				frappe.throw(_("Group only can be created under HKP"))
			self.file = None
		else:
			# file must exist
			if not self.file:
				frappe.throw(_("File is required"))
			# must have parent
			if not self.parent:
				frappe.throw(_("Only group can be created without parent"))
			elif self.parent == 'HKP':
				frappe.throw(_("HKP is not a valid parent"))