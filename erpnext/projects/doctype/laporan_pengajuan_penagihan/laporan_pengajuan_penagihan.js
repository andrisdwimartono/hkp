// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Laporan Pengajuan Penagihan', {
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			if(!frm.doc.process_rules){
				frm.clear_table("process_rules");
				frappe.call({
					method: 'erpnext.projects.utils.get_process_rules',
					args: {
						'doctype': frm.doc.doctype
					},
					callback: function(r) {
						if(r.message){
							var vals = r.message;
							for(var i = 0; i < vals.length; i++){
								var pr = frm.add_child("process_rules");
								pr.jabatan = vals[i].jabatan;
								pr.jabatan_abbr = vals[i].jabatan_abbr;
								pr.state = vals[i].state;
								pr.employee = vals[i].employee;
								pr.initial = vals[i].initial;
								pr.employee_name = vals[i].employee_name;
								pr.user = vals[i].user;
							}
							frm.refresh_field("process_rules");
						}
					}
				});
			}
		}else{
			
		}
		cur_frm.fields_dict['process_rules'].$wrapper.find('.grid-add-row').addClass('d-none');
	},
	rencana: function(frm){
		var deviasi = 0;
		if(frm.doc.realisasi){
			deviasi = frm.doc.rencana-frm.doc.realisasi;
		}
		frm.set_value("deviasi", deviasi);
	},
	realisasi: function(frm){
		var deviasi = 0;
		if(frm.doc.realisasi){
			deviasi = frm.doc.rencana-frm.doc.realisasi;
		}
		frm.set_value("deviasi", deviasi);
	},
	sub_contract_hand_over: function(frm){
		frappe.call({
			method: 'erpnext.projects.doctype.laporan_pengajuan_penagihan.laporan_pengajuan_penagihan.get_termin',
			args: {
				'sub_contract_hand_over': frm.doc.sub_contract_hand_over
			},
			callback: function(r) {
				if(r.message){
					var vals = r.message;
					frm.set_value("termin", vals[0]);
					frm.refresh_field("termin");
					frm.set_value("periode", vals[1]);
					frm.refresh_field("periode");

					frm.clear_table("detail");
					frm.refresh_field("detail");
					frappe.call({
						method: 'erpnext.projects.doctype.laporan_pengajuan_penagihan.laporan_pengajuan_penagihan.get_detail',
						args: {
							'sub_contract_hand_over': frm.doc.sub_contract_hand_over,
							'termin': vals[0]
						},
						callback: function(r) {
							var vals = r.message;
							if(r.message){
								for(var i = 0; i < vals.length; i++){
									var pr = frm.add_child("detail");
									pr.group = vals[i].group;
									pr.item_pekerjaan = vals[i].item_pekerjaan;
									pr.uom = vals[i].uom;
									pr.vol_kontrak = vals[i].vol_kontrak;
									pr.bobot = vals[i].bobot;
									pr.vol_terpasang_lalu = vals[i].vol_terpasang_lalu;
									pr.vol_terpasang_saat_ini = vals[i].vol_terpasang_saat_ini;
									pr.vol_terpasang_sd_saat_ini = vals[i].vol_terpasang_sd_saat_ini;
									pr.bobot_terpasang_lalu = vals[i].bobot_terpasang_lalu;
									pr.bobot_terpasang_saat_ini = vals[i].bobot_terpasang_saat_ini;
									pr.bobot_terpasang_sd_saat_ini = vals[i].bobot_terpasang_sd_saat_ini;
								}
								frm.refresh_field("detail");
							}
						}
					});
				}
			}
		});
	}
});

frappe.ui.form.on('Laporan Pengajuan Penagihan Detail', {
	vol_kontrak: function(frm, dt, dn){
		var d = locals[dt][dn];
		d.bobot_terpasang_lalu = d.bobot*d.vol_terpasang_lalu/d.vol_kontrak;
		d.bobot_terpasang_saat_ini = d.bobot*d.vol_terpasang_saat_ini/d.vol_kontrak;
		d.bobot_terpasang_sd_saat_ini = d.bobot*d.vol_terpasang_sd_saat_ini/d.vol_kontrak;
		frm.refresh_field("detail");
	},
	bobot: function(frm, dt, dn){
		var d = locals[dt][dn];
		d.bobot_terpasang_lalu = d.bobot*d.vol_terpasang_lalu/d.vol_kontrak;
		d.bobot_terpasang_saat_ini = d.bobot*d.vol_terpasang_saat_ini/d.vol_kontrak;
		d.bobot_terpasang_sd_saat_ini = d.bobot*d.vol_terpasang_sd_saat_ini/d.vol_kontrak;
		frm.refresh_field("detail");
	},
	vol_terpasang_lalu: function(frm, dt, dn){
		//set bobot
		var d = locals[dt][dn];
		d.bobot_terpasang_lalu = d.bobot*d.vol_terpasang_lalu/d.vol_kontrak;

		d.vol_terpasang_sd_saat_ini = d.vol_terpasang_lalu+d.vol_terpasang_saat_ini;
		d.bobot_terpasang_sd_saat_ini = d.bobot*d.vol_terpasang_sd_saat_ini/d.vol_kontrak;
		frm.refresh_field("detail");

		var realisasi = 0;
		for(var i = 0; i < frm.doc.detail.length; i++){
			if(frm.doc.detail[i].group != 1)
				realisasi = realisasi+frm.doc.detail[i].bobot_terpasang_sd_saat_ini;
		}
		frm.set_value("realisasi", realisasi);
	},
	vol_terpasang_saat_ini: function(frm, dt, dn){
		//set bobot
		var d = locals[dt][dn];
		d.bobot_terpasang_saat_ini = d.bobot*d.vol_terpasang_saat_ini/d.vol_kontrak;

		d.vol_terpasang_sd_saat_ini = d.vol_terpasang_lalu+d.vol_terpasang_saat_ini;
		d.bobot_terpasang_sd_saat_ini = d.bobot*d.vol_terpasang_sd_saat_ini/d.vol_kontrak;
		frm.refresh_field("detail");

		var realisasi = 0;
		for(var i = 0; i < frm.doc.detail.length; i++){
			if(frm.doc.detail[i].group != 1)
				realisasi = realisasi+frm.doc.detail[i].bobot_terpasang_sd_saat_ini;
		}
		frm.set_value("realisasi", realisasi);
	},
	vol_terpasang_sd_saat_ini: function(frm, dt, dn){
		//set bobot
		var d = locals[dt][dn];
		d.bobot_terpasang_sd_saat_ini = d.bobot*d.vol_terpasang_sd_saat_ini/d.vol_kontrak;
		frm.refresh_field("detail");

		var realisasi = 0;
		for(var i = 0; i < frm.doc.detail.length; i++){
			if(frm.doc.detail[i].group != 1)
				realisasi = realisasi+frm.doc.detail[i].bobot_terpasang_sd_saat_ini;
		}
		frm.set_value("realisasi", realisasi);
	},
});