# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.projects.utils import get_process_rules
import datetime

class DAFTARPERIKSASAATKUNJUNGANLAPANGAN(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.tanggal, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabDAFTAR PERIKSA SAAT KUNJUNGAN LAPANGAN` WHERE name like '%/{2}/{0}/{1}'""".format(bulan, mydate.year, self.project), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "DPL/{2}/{3}/{0}/{1}".format(bulan, mydate.year, urut2, self.project)
		else:
			self.name = "DPL/001/{2}/{0}/{1}".format(bulan, mydate.year, self.project)

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
			for d in get_process_rules("DAFTAR PERIKSA SAAT VERIFIKASI KUNJUNGAN LAPANGAN"):
				verifikasi_doc.append("process_rules", {
					"jabatan" : d.jabatan,
					"jabatan_abbr" : d.jabatan_abbr,
					"state" : d.state,
					"employee" : d.employee,
					"initial" : d.initial,
					"employee_name" : d.employee_name,
					"user" : d.user
				})
			
			verifikasi_doc.save()
			frappe.db.commit()
			frappe.db.sql("""INSERT INTO `tabDAFTAR PERIKSA SAAT VERIFIKASI KUNJUNGAN LAPANGAN DETAIL`(name, creation, modified, modified_by, owner, docstatus, parent, parentfield, parenttype, idx, uraian, kriteria, hasil_pemeriksaan, tindakan_yang_harus_dilakukan, tenggat_waktu) 
				(SELECT name, creation, modified, '{1}' modified_by, '{1}' owner, 0 docstatus, '{2}' parent, parentfield, 'DAFTAR PERIKSA SAAT VERIFIKASI KUNJUNGAN LAPANGAN' parenttype, idx, uraian, kriteria, hasil_pemeriksaan, tindakan_yang_harus_dilakukan, tenggat_waktu FROM `tabDAFTAR PERIKSA SAAT KUNJUNGAN LAPANGAN DETAIL` WHERE parent = '{0}')""".format(docname, verifikasi_doc.owner, verifikasi_doc.name))
			frappe.db.commit()
			return verifikasi_doc.name