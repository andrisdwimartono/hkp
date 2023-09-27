# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DAFTARPERIKSASAATKUNJUNGANLAPANGAN(Document):
	pass

@frappe.whitelist()
def create_verifikasi(docname=None):
	if docname != "" and docname != None:
		check_verifikasi = frappe.db.sql("""SELECT * FROM `tabDAFTAR PERIKSA SAAT VERIFIKASI KUNJUNGAN LAPANGAN` WHERE kunjungan = '{0}'""".format(docname), as_dict=1)
		if check_verifikasi:
			frappe.throw("""Verifikasi sudah dibuat <a href='/app/daftar-periksa-saat-verifikasi-kunjungan-lapangan/{0}'>{0}</a>""".format(check_verifikasi[0].name))
		else:
			verifikasi_doc = frappe.get_doc({
				"doctype": "DAFTAR PERIKSA SAAT VERIFIKASI KUNJUNGAN LAPANGAN",
				"kunjungan": docname,
			})
			verifikasi_doc.save()
			frappe.db.commit()
			frappe.db.sql("""INSERT INTO `tabDAFTAR PERIKSA SAAT VERIFIKASI KUNJUNGAN LAPANGAN DETAIL`(name, creation, modified, modified_by, owner, docstatus, parent, parentfield, parenttype, idx, uraian, kriteria, hasil_pemeriksaan, tindakan_yang_harus_dilakukan, tenggat_waktu) 
				(SELECT name, creation, modified, '{1}' modified_by, '{1}' owner, 0 docstatus, '{2}' parent, parentfield, 'DAFTAR PERIKSA SAAT VERIFIKASI KUNJUNGAN LAPANGAN' parenttype, idx, uraian, kriteria, hasil_pemeriksaan, tindakan_yang_harus_dilakukan, tenggat_waktu FROM `tabDAFTAR PERIKSA SAAT KUNJUNGAN LAPANGAN DETAIL` WHERE parent = '{0}')""".format(docname, verifikasi_doc.owner, verifikasi_doc.name))
			frappe.db.commit()
			return verifikasi_doc.name