# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LaporanPengajuanPenagihan(Document):
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

@frappe.whitelist()
def get_termin(sub_contract_hand_over):
	termin = 0
	periode = ''
	lpps = frappe.db.sql("""SELECT MAX(termin) termin, periode FROM `tabLaporan Pengajuan Penagihan` WHERE sub_contract_hand_over = '{0}' AND workflow_state = 'Disetujui Direktur Operasi'""".format(sub_contract_hand_over), as_dict=1)
	if lpps:
		if lpps[0].termin:
			termin = lpps[0].termin
		if lpps[0].periode:
			periode = lpps[0].periode
	return termin+1, periode

@frappe.whitelist()
def get_detail(sub_contract_hand_over, termin):
	lpps = frappe.db.sql("""SELECT lppd.* FROM `tabLaporan Pengajuan Penagihan` lpp
					  INNER JOIN `tabLaporan Pengajuan Penagihan Detail` lppd ON lpp.name = lppd.parent
					  WHERE lpp.sub_contract_hand_over = '{0}' AND lpp.termin = '{1}'
					  ORDER BY lppd.idx ASC
					  """.format(sub_contract_hand_over, termin), as_dict=1)
	if lpps:
		return lpps
	else:
		lpps2 = frappe.db.sql("""SELECT 
							lppd.group,
							lppd.item_pekerjaan,
							lppd.uom,
							lppd.vol_kontrak,
							lppd.bobot,
							lppd.vol_terpasang_sd_saat_ini vol_terpasang_lalu,
							0 vol_terpasang_saat_ini,
							lppd.vol_terpasang_sd_saat_ini,
							lppd.bobot_terpasang_sd_saat_ini bobot_terpasang_lalu,
							0 bobot_terpasang_saat_ini,
							lppd.bobot_terpasang_sd_saat_ini
						 FROM `tabLaporan Pengajuan Penagihan` lpp
					  INNER JOIN `tabLaporan Pengajuan Penagihan Detail` lppd ON lpp.name = lppd.parent
					  WHERE lpp.sub_contract_hand_over = '{0}' AND lpp.termin = '{1}'
					  ORDER BY lppd.idx ASC
					  """.format(sub_contract_hand_over, int(termin)-1), as_dict=1)
		if lpps2:
			return lpps2
	return None