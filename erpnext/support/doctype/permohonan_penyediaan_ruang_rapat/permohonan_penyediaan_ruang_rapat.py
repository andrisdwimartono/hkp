# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.support.doctype.risalah_rapat.risalah_rapat import get_department_abbr_by_session
import datetime

class PermohonanPenyediaanRuangRapat(Document):
	def on_submit(self):
		x = frappe.db.sql("""SELECT * FROM `tabPermohonan Penyediaan Ruang Rapat` WHERE name != '{0}' AND tanggal_rapat = '{1}' AND ruang_rapat = '{4}' AND ('{2}' BETWEEN waktu_mulai_rapat AND waktu_selesai_rapat OR '{3}' BETWEEN waktu_mulai_rapat AND waktu_selesai_rapat)""".format(self.name, self.tanggal_rapat, self.waktu_mulai_rapat, self.waktu_selesai_rapat, self.ruang_rapat), as_dict=1)
		if x:
			frappe.throw("Ada agenda rapat <a href='/app/permohonan-penyediaan-ruang-rapat/{0}'>{1}</a> di jam {2} s.d {3}".format(self.name, self.agenda_rapat, self.waktu_mulai_rapat, self.waktu_selesai_rapat))
			
	def validate(self):
		self.abbr = get_department_abbr_by_session()

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.tanggal_pengajuan, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabPermohonan Penyediaan Ruang Rapat` WHERE tanggal_pengajuan between '{0}' and '{1}'""".format("{0}-01-01".format(mydate.year), "{0}-12-31".format(mydate.year)), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/{3}/PPRP/{0}/{1}".format(bulan, mydate.year-2000, urut2, get_department_abbr_by_session())
		else:
			self.name = "001/{2}/PPRP/{0}/{1}".format(bulan, mydate.year-2000, get_department_abbr_by_session())

@frappe.whitelist()
def tolak_pengajuan(docname):
	if not frappe.db.sql("""SELECT * FROM `tabUser` WHERE name = '{0}' AND role_profile_name = 'UMUM'""".format(frappe.session.user), as_dict=1):
		frappe.throw("Hanya bisa dilakukan oleh ADU")
	a = frappe.db.sql("""SELECT * FROM `tabPermohonan Penyediaan Ruang Rapat` WHERE name = '{0}'""".format(docname), as_dict=1)
	if a:
		frappe.db.sql("""UPDATE `tabPermohonan Penyediaan Ruang Rapat` SET docstatus = 2 WHERE name = '{0}'""".format(docname), as_dict=1)
