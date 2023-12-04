# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class REKAPITULASIPENAWARANSUPPLIERJASA(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.posting_date, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabREKAPITULASI PENAWARAN SUPPLIER JASA` WHERE name like '%/{2}/{0}/{1}'""".format(bulan, mydate.year, self.project), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "RPSJ/{2}/{3}/{0}/{1}".format(bulan, mydate.year, urut2, self.project)
		else:
			self.name = "RPSJ/001/{2}/{0}/{1}".format(bulan, mydate.year, self.project)

	def validate(self):
		# frappe.msgprint(
		# 	msg='This file does not exist',
		# 	title='Error',
		# 	raise_exception=FileNotFoundError,
		# 	primary_action={
		# 		'label': 'Perform Action',
		# 		'server_action': 'erpnext.projects.utils.get_process_rules',
		# 		#'client_action': 'erpnext.projects.utils.get_process_rules',
		# 		#'args': args
		# 	}
		# )
		esjs = frappe.db.sql("""
			SELECT * FROM `tabREKAPITULASI PENAWARAN SUPPLIER JASA` WHERE project = '{0}' AND supplier = '{1}' AND name != '{2}'
		""".format(self.project, self.supplier, self.name), as_dict=1)
		# for esj in esjs:
		# 	frappe.throw("Project dan Supplier sudah dibuat <a href='/app/rekapitulasi-penawaran-supplier-jasa/{0}'>{0}</a>".format(esj.name))
		total_nilai = 0
		for d in self.details:
			if d.value > 100 or d.value < 0:
				frappe.throw("Nilai harus 0 s/d 100")
			total_nilai = total_nilai+(d.bobot*d.value/100)
		self.total_nilai = total_nilai
		self.peringkat = 1
		frappe.db.sql("""
			UPDATE `tabREKAPITULASI PENAWARAN SUPPLIER JASA` SET total_nilai = {0} WHERE name = '{1}'
		""".format(total_nilai, self.name))
		frappe.db.commit()
		
		esjs_nilai = frappe.db.sql("""
			SELECT * FROM `tabREKAPITULASI PENAWARAN SUPPLIER JASA` WHERE project = '{0}' and docstatus in (0, 1) order by total_nilai desc
		""".format(self.project), as_dict=1)
		peringkat = 1
		for x in esjs_nilai:
			if x.name == self.name:
				self.peringkat = peringkat
			else:
				frappe.db.sql("""
					UPDATE `tabREKAPITULASI PENAWARAN SUPPLIER JASA` SET peringkat = {0} WHERE name = '{1}'
				""".format(peringkat, x.name))
				frappe.db.commit()
			peringkat = peringkat+1

@frappe.whitelist()
def get_details(kriteria_penilaian):
	if kriteria_penilaian:
		fs = frappe.db.sql("""
			SELECT * FROM `tabKriteria Penilaian Detail` WHERE parent = '{0}'
		""".format(kriteria_penilaian), as_dict=1)
		return fs
	
@frappe.whitelist()
def get_panduan_penilaian(kriteria_penilaian):
	if kriteria_penilaian:
		fs = frappe.db.sql("""
			SELECT * FROM `tabKriteria Penilaian` WHERE name = '{0}'
		""".format(kriteria_penilaian), as_dict=1)
		return fs