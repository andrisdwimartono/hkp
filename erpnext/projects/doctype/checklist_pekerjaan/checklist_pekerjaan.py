# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ChecklistPekerjaan(Document):
	pass

@frappe.whitelist()
def get_detail(laporan_pengajuan_penagihan):
	return frappe.db.sql("""SELECT lppd.* FROM `tabLaporan Pengajuan Penagihan` lpp
					  INNER JOIN `tabLaporan Pengajuan Penagihan Detail` lppd ON lpp.name = lppd.parent
					  WHERE lpp.name = '{0}' AND lppd.group != 1 AND lppd.vol_terpasang_saat_ini > 0
					  ORDER BY lppd.idx ASC
					  """.format(laporan_pengajuan_penagihan), as_dict=1)