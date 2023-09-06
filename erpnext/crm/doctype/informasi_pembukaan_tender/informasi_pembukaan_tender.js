// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('INFORMASI PEMBUKAAN TENDER', {
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
	informasi_pembuatan_penawaran_terkait: function(frm){
		frm.clear_table("hasil_pembukaan_tender");
		frappe.call({
			method: 'erpnext.crm.doctype.informasi_pembukaan_tender.informasi_pembukaan_tender.get_peserta',
			args: {
				'informasi_pembuatan_penawaran_terkait': frm.doc.informasi_pembuatan_penawaran_terkait
			},
			callback: function(r) {
				if(r.message){
					var vals = r.message;
					for(var i = 0; i < vals.length; i++){
						var pr = frm.add_child("hasil_pembukaan_tender");
						pr.nama_peserta = vals[i].peserta;
						// pr.jabatan_abbr = vals[i].jabatan_abbr;
						// pr.state = vals[i].state;
						// pr.employee = vals[i].employee;
						// pr.employee_name = vals[i].employee_name;
						// pr.user = vals[i].user;
					}
					frm.refresh_field("hasil_pembukaan_tender");
				}
			}
		});
	}
});
