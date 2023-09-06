# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class INFORMASIPEMBUKAANTENDER(Document):
	pass
@frappe.whitelist()
def get_peserta(informasi_pembuatan_penawaran_terkait):
	return frappe.db.sql("""SELECT a.* FROM `tabLAPORAN PENJELASAN TENDER _ PESERTA TENDER` a
			INNER JOIN `tabLAPORAN PENJELASAN TENDER` b ON b.name = a.parent		  
			WHERE b.informasi_pembuatan_penawaran = '{0}' ORDER BY idx ASC""".format(informasi_pembuatan_penawaran_terkait), as_dict=1)
