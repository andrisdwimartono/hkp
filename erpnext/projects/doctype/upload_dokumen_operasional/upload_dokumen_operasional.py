# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet

class UploadDokumenOperasional(NestedSet):
	def autoname(self):
		if self.parent_upload_dokumen_operasional:
			nm = ""
			if self.document_name:
				nm = self.document_name
			else:
				if self.ruang == "Izin Kerja":
					nm = self.ruang_1
				if self.ruang == "Rencana Kerja":
					nm = self.ruang_2
				if self.ruang == "Laporan":
					nm = self.ruang_3
			self.name = """{1}-{0}""".format(nm, self.project)
		else:
			self.name = self.project

	def validate(self):
		if not self.document_name:
			if self.parent_upload_dokumen_operasional:
				self.document_name = self.project
			else:
				if self.ruang == "Izin Kerja":
					self.document_name = self.ruang_1
				if self.ruang == "Rencana Kerja":
					self.document_name = self.ruang_2
				if self.ruang == "Laporan":
					self.document_name = self.ruang_3
