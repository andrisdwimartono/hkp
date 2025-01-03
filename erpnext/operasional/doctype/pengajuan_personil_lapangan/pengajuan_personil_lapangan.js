// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pengajuan Personil Lapangan', {
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
	onload: function(frm) {
		frm.set_query('informasi_pekerjaan_baru', function() {
			return {
				filters: {
					'project': frm.doc.project
				}
			};
		});
	}
});

frappe.ui.form.on('Pengajuan Personil Lapangan Personil', {
	employee: function(frm, dt, dn){
		var d = locals[dt][dn];
		frappe.call({
			method: 'erpnext.projects.doctype.pengajuan_personil_lapangan.pengajuan_personil_lapangan.get_history',
			args: {
				'employee': d.employee
			},
			callback: function(r) {
				
			}
		});
	},
	riwayat: function(frm, dt, dn){
		var d = locals[dt][dn];
		frappe.call({
			method: 'erpnext.projects.doctype.pengajuan_personil_lapangan.pengajuan_personil_lapangan.get_history',
			args: {
				'employee': d.employee
			},
			callback: function(r) {
				
			}
		});
	},
});