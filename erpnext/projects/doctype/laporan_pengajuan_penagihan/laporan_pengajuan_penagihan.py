# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import (
	today,
)

class LaporanPengajuanPenagihan(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabLaporan Pengajuan Penagihan` WHERE name like '%/{0}/{1}'""".format(bulan, mydate.year), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/DKD/LPN/{0}/{1}".format(bulan, mydate.year, urut2)
		else:
			self.name = "01/DKD/LPN/{0}/{1}".format(bulan, mydate.year)

	def validate(self):
		bobot_total = 0
		bobot_total_gr = 0
		vol_kontrak_gr = 0
		vol_terpasang_lalu_gr = 0
		vol_terpasang_saat_ini_gr = 0
		vol_terpasang_sd_saat_ini_gr = 0
		bobot_terpasang_lalu_gr = 0
		bobot_terpasang_saat_ini_gr = 0
		bobot_terpasang_sd_saat_ini_gr = 0

		for d in reversed(self.detail):
			if d.group != 1:
				bobot_total = bobot_total+d.bobot

				bobot_total_gr = bobot_total_gr+d.bobot
				vol_kontrak_gr = vol_kontrak_gr+d.vol_kontrak
				vol_terpasang_lalu_gr = vol_terpasang_lalu_gr+d.vol_terpasang_lalu
				vol_terpasang_saat_ini_gr = vol_terpasang_saat_ini_gr+d.vol_terpasang_saat_ini
				vol_terpasang_sd_saat_ini_gr = vol_terpasang_sd_saat_ini_gr+d.vol_terpasang_sd_saat_ini
				bobot_terpasang_lalu_gr = bobot_terpasang_lalu_gr+d.bobot_terpasang_lalu
				bobot_terpasang_saat_ini_gr = bobot_terpasang_saat_ini_gr+d.bobot_terpasang_saat_ini
				bobot_terpasang_sd_saat_ini_gr = bobot_terpasang_sd_saat_ini_gr+d.bobot_terpasang_sd_saat_ini
			else:
				d.bobot = bobot_total_gr
				d.vol_kontrak = None
				d.vol_terpasang_lalu = vol_terpasang_lalu_gr
				d.vol_terpasang_saat_ini = vol_terpasang_saat_ini_gr
				d.vol_terpasang_sd_saat_ini = vol_terpasang_sd_saat_ini_gr
				d.bobot_terpasang_lalu = bobot_terpasang_lalu_gr
				d.bobot_terpasang_saat_ini = bobot_terpasang_saat_ini_gr
				d.bobot_terpasang_sd_saat_ini = bobot_terpasang_sd_saat_ini_gr

				bobot_total_gr = 0
				vol_kontrak_gr = 0
				vol_terpasang_lalu_gr = 0
				vol_terpasang_saat_ini_gr = 0
				vol_terpasang_sd_saat_ini_gr = 0
				bobot_terpasang_lalu_gr = 0
				bobot_terpasang_saat_ini_gr = 0
				bobot_terpasang_sd_saat_ini_gr = 0
		if bobot_total != 100:
			frappe.throw("Total Bobot harus 100")

# @frappe.whitelist()
# def get_termin(sub_contract_hand_over):
# 	termin = 0
# 	periode = ''
# 	lpps = frappe.db.sql("""SELECT MAX(termin) termin, periode FROM `tabLaporan Pengajuan Penagihan` WHERE sub_contract_hand_over = '{0}' AND workflow_state = 'Disetujui Direktur Operasi'""".format(sub_contract_hand_over), as_dict=1)
# 	if lpps:
# 		if lpps[0].termin:
# 			termin = lpps[0].termin
# 		if lpps[0].periode:
# 			periode = lpps[0].periode
# 	return termin+1, periode

# @frappe.whitelist()
# def get_detail(sub_contract_hand_over, termin):
# 	lpps = frappe.db.sql("""SELECT lppd.* FROM `tabLaporan Pengajuan Penagihan` lpp
# 					  INNER JOIN `tabLaporan Pengajuan Penagihan Detail` lppd ON lpp.name = lppd.parent
# 					  WHERE lpp.sub_contract_hand_over = '{0}' AND lpp.termin = '{1}'
# 					  ORDER BY lppd.idx ASC
# 					  """.format(sub_contract_hand_over, termin), as_dict=1)
# 	if lpps:
# 		return lpps
# 	else:
# 		lpps2 = frappe.db.sql("""SELECT 
# 							lppd.group,
# 							lppd.item_pekerjaan,
# 							lppd.uom,
# 							lppd.vol_kontrak,
# 							lppd.bobot,
# 							lppd.vol_terpasang_sd_saat_ini vol_terpasang_lalu,
# 							0 vol_terpasang_saat_ini,
# 							lppd.vol_terpasang_sd_saat_ini,
# 							lppd.bobot_terpasang_sd_saat_ini bobot_terpasang_lalu,
# 							0 bobot_terpasang_saat_ini,
# 							lppd.bobot_terpasang_sd_saat_ini
# 						 FROM `tabLaporan Pengajuan Penagihan` lpp
# 					  INNER JOIN `tabLaporan Pengajuan Penagihan Detail` lppd ON lpp.name = lppd.parent
# 					  WHERE lpp.sub_contract_hand_over = '{0}' AND lpp.termin = '{1}'
# 					  ORDER BY lppd.idx ASC
# 					  """.format(sub_contract_hand_over, int(termin)-1), as_dict=1)
# 		if lpps2:
# 			return lpps2
# 	return None

@frappe.whitelist()
def get_termin_pekerjaan(master_item_pekerjaan):
	termin = 0
	periode = ''
	lpps = frappe.db.sql("""SELECT MAX(termin) termin, periode FROM `tabLaporan Pengajuan Penagihan` WHERE master_item_pekerjaan = '{0}'""".format(master_item_pekerjaan), as_dict=1)
	if lpps:
		if lpps[0].termin:
			termin = lpps[0].termin
		if lpps[0].periode:
			periode = lpps[0].periode
	return termin+1, periode

@frappe.whitelist()
def get_detail_pekerjaan(master_item_pekerjaan, termin):
	lpps = frappe.db.sql("""SELECT lppd.* FROM `tabLaporan Pengajuan Penagihan` lpp
					  INNER JOIN `tabLaporan Pengajuan Penagihan Detail` lppd ON lpp.name = lppd.parent
					  WHERE lpp.master_item_pekerjaan = '{0}' AND lpp.termin = '{1}'
					  ORDER BY lppd.idx ASC
					  """.format(master_item_pekerjaan, termin), as_dict=1)
	if lpps:
		return lpps
	else:
		lpps2 = frappe.db.sql("""SELECT 
							mipd.group,
							mipd.item_pekerjaan,
							mipd.uom,
							mipd.vol_kontrak,
							mipd.bobot,
							lppd.vol_terpasang_sd_saat_ini vol_terpasang_lalu,
							0 vol_terpasang_saat_ini,
							lppd.vol_terpasang_sd_saat_ini,
							lppd.bobot_terpasang_sd_saat_ini bobot_terpasang_lalu,
							0 bobot_terpasang_saat_ini,
							lppd.bobot_terpasang_sd_saat_ini
						 FROM `tabLaporan Pengajuan Penagihan` lpp
					 INNER JOIN `tabMaster Item Pekerjaan Detail` mipd ON lpp.master_item_pekerjaan = mipd.parent
					  LEFT JOIN `tabLaporan Pengajuan Penagihan Detail` lppd ON lpp.name = lppd.parent AND lppd.item_pekerjaan = mipd.item_pekerjaan
					  WHERE lpp.master_item_pekerjaan = '{0}' AND lpp.termin = '{1}'
					  ORDER BY mipd.idx ASC
					  """.format(master_item_pekerjaan, int(termin)-1), as_dict=1)
		if lpps2:
			return lpps2
		else:
			return frappe.db.sql("""SELECT mipd.*, 0 vol_terpasang_lalu, 0 vol_terpasang_sd_saat_ini FROM `tabMaster Item Pekerjaan` mip
					  INNER JOIN `tabMaster Item Pekerjaan Detail` mipd ON mip.name = mipd.parent
					  WHERE mip.name = '{0}'
					  ORDER BY mipd.idx ASC
					  """.format(master_item_pekerjaan), as_dict=1)