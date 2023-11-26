// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report REKAPITULASI PENAWARAN SUPPLIER JASA', {
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
	project: function(frm){
		if(frm.doc.project && frm.doc.jenis_pekerjaan){
			frm.clear_table("detail");
			frappe.call({
				method: 'erpnext.projects.doctype.report_rekapitulasi_penawaran_supplier_jasa.report_rekapitulasi_penawaran_supplier_jasa.get_data',
				args: {
					'project': frm.doc.project,
					'jenis_pekerjaan': frm.doc.jenis_pekerjaan
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("detail");
							pr.penawaran = vals[i].penawaran;
							pr.bulan = vals[i].bulan;
							pr.tahun = vals[i].tahun;
							pr.jenis_pekerjaan = vals[i].jenis_pekerjaan;
							pr.harga_rap = vals[i].harga_rap;
							pr.total_nilai = vals[i].total_nilai;
							pr.peringkat = i+1;
						}
						frm.refresh_field("detail");
					}
				}
			});
		}
	},
	jenis_pekerjaan: function(frm){
		if(frm.doc.project && frm.doc.jenis_pekerjaan){
			frm.clear_table("detail");
			frappe.call({
				method: 'erpnext.projects.doctype.report_rekapitulasi_penawaran_supplier_jasa.report_rekapitulasi_penawaran_supplier_jasa.get_data',
				args: {
					'project': frm.doc.project,
					'jenis_pekerjaan': frm.doc.jenis_pekerjaan
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("detail");
							pr.penawaran = vals[i].penawaran;
							pr.bulan = vals[i].bulan;
							pr.tahun = vals[i].tahun;
							pr.jenis_pekerjaan = vals[i].jenis_pekerjaan;
							pr.harga_rap = vals[i].harga_rap;
							pr.total_nilai = vals[i].total_nilai;
							pr.peringkat = i+1;
						}
						frm.refresh_field("detail");
					}
				}
			});
		}
	}
});
