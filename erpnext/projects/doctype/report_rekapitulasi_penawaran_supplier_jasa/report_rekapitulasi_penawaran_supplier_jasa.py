# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReportREKAPITULASIPENAWARANSUPPLIERJASA(Document):
	pass

@frappe.whitelist()
def get_data(project, jenis_pekerjaan):
	return frappe.db.sql("""
		SELECT a.name penawaran, a.bulan, a.tahun, a.jenis_pekerjaan, a.harga_rap, a.total_nilai, a.peringkat FROM `tabREKAPITULASI PENAWARAN SUPPLIER JASA` a
		WHERE project = '{0}' AND jenis_pekerjaan = '{1}'
		ORDER BY a.total_nilai ASC;
	""".format(project, jenis_pekerjaan), as_dict=1)