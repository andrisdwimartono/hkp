// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Laporan Ringkasan Aktivitas Proyek', {
	refresh: function(frm) {
		if(frm.doc.start_date){
			frappe.call({
				method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.check_week',
				args: {
					'posting_date': frm.doc.start_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						frm.set_value("week_periode", vals);
						frm.refresh_field("week_periode");
					}
				}
			});
		}
		
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
	project: function(frm){
		if(frm.doc.project && frm.doc.start_date){
			frm.clear_table("detail");
			frappe.call({
				method: 'erpnext.projects.doctype.laporan_ringkasan_aktivitas_proyek.laporan_ringkasan_aktivitas_proyek.get_detail',
				args: {
					'project': frm.doc.project,
					'start_date': frm.doc.start_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						var total_target = 0;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("detail");
							pr.uraian_aktivitas = vals[i].uraian_aktivitas;
							pr.target = vals[i].target_selanjutnya;
							total_target = total_target+vals[i].target_selanjutnya;
						}
						frm.refresh_field("detail");
						frm.set_value("rencana", total_target);
						frm.refresh_field("rencana");
					}
				}
			});
		}
	},
	start_date: function(frm){
		if(frm.doc.project && frm.doc.start_date){
			frm.clear_table("detail");
			frappe.call({
				method: 'erpnext.projects.doctype.laporan_ringkasan_aktivitas_proyek.laporan_ringkasan_aktivitas_proyek.get_detail',
				args: {
					'project': frm.doc.project,
					'start_date': frm.doc.start_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						var total_target = 0;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("detail");
							pr.uraian_aktivitas = vals[i].uraian_aktivitas;
							pr.target = vals[i].target_selanjutnya;
							total_target = total_target+vals[i].target_selanjutnya;
						}
						frm.refresh_field("detail");
						frm.set_value("rencana", total_target);
						frm.refresh_field("rencana");
					}
				}
			});
		}

		if(frm.doc.start_date){
			frappe.call({
				method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.check_week',
				args: {
					'posting_date': frm.doc.start_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						frm.set_value("week_periode", vals);
						frm.refresh_field("week_periode");
					}
				}
			});
		}
	},
	rencana: function(frm){
		var rencana = frm.doc.rencana;
		var realisasi = frm.doc.realisasi;
		frm.set_value("deviasi", realisasi-rencana);
		refresh_field("deviasi");
	},
	realisasi: function(frm){
		var rencana = frm.doc.rencana;
		var realisasi = frm.doc.realisasi;
		frm.set_value("deviasi", realisasi-rencana);
		refresh_field("deviasi");
	}
});

frappe.ui.form.on('Laporan Ringkasan Aktivitas Proyek Detail', {
	realisasi: function(frm, dt, dn){
		var d = locals[dt][dn];
		d.deviasi = d.realisasi+d.target;
		frm.refresh_field("detail");
		var total_target = 0;
		var total_realisasi = 0;
		var total_deviasi = 0;
		for(var i = 0; i < frm.doc.detail.length; i++){
			total_target = total_target+frm.doc.detail[i].target;
			total_realisasi = total_realisasi+frm.doc.detail[i].realisasi;
			total_deviasi = total_deviasi+frm.doc.detail[i].deviasi;
		}
		frm.set_value("rencana", total_target);
		frm.refresh_field("rencana");
		frm.set_value("realisasi", total_realisasi);
		frm.refresh_field("realisasi");
		frm.set_value("deviasi", total_deviasi);
		frm.refresh_field("deviasi");
	},
	target: function(frm, dt, dn){
		var d = locals[dt][dn];
		d.deviasi = d.realisasi+d.target;
		frm.refresh_field("detail");
		var total_target = 0;
		var total_realisasi = 0;
		var total_deviasi = 0;
		for(var i = 0; i < frm.doc.detail.length; i++){
			total_target = total_target+frm.doc.detail[i].target;
			total_realisasi = total_realisasi+frm.doc.detail[i].realisasi;
			total_deviasi = total_deviasi+frm.doc.detail[i].deviasi;
		}
		frm.set_value("rencana", total_target);
		frm.refresh_field("rencana");
		frm.set_value("realisasi", total_realisasi);
		frm.refresh_field("realisasi");
		frm.set_value("deviasi", total_deviasi);
		frm.refresh_field("deviasi");
	}
});