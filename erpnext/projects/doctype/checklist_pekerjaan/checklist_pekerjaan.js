// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Checklist Pekerjaan', {
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
	laporan_pengajuan_penagihan: function(frm){
		if(frm.doc.laporan_pengajuan_penagihan){
			frm.clear_table("detail");
			frappe.call({
				method: 'erpnext.projects.doctype.checklist_pekerjaan.checklist_pekerjaan.get_detail',
				args: {
					'laporan_pengajuan_penagihan': frm.doc.laporan_pengajuan_penagihan
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("detail");
							pr.obyek_pemeriksaan = vals[i].item_pekerjaan;
							pr.progress = vals[i].bobot_terpasang_sd_saat_ini;
						}
						frm.refresh_field("detail");
					}
				}
			});
		}
	}
});
