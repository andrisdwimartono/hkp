// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rekapitulasi Anggaran Proyek', {
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
		if(frm.doc.project && frm.doc.start_date && frm.doc.finish_date){
			frm.clear_table("detail");
			frappe.call({
				method: 'erpnext.projects.doctype.rekapitulasi_anggaran_proyek.rekapitulasi_anggaran_proyek.get_rekap',
				args: {
					'project': frm.doc.project,
					'start_date': frm.doc.start_date,
					'finish_date': frm.doc.finish_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("detail");
							pr.project = vals[i].project;
							pr.project_name = vals[i].project_name;
							pr.uraian = vals[i].purpose;
							pr.tanggal_pengajuan = vals[i].posting_date;
							pr.total_budget_first = vals[i].total_budget_first;
							pr.tanggal_disetujui = vals[i].submitted_date;
							pr.total_budget = vals[i].total_budget;
							pr.tanggal_realisasi = vals[i].tanggal_realisasi;
							pr.paid_amount = vals[i].paid_amount;
							pr.keterangan = vals[i].keterangan;
						}
						frm.refresh_field("detail");
					}
				}
			});
		}
	},
	start_date: function(frm){
		if(frm.doc.project && frm.doc.start_date && frm.doc.finish_date){
			frm.clear_table("detail");
			frappe.call({
				method: 'erpnext.projects.doctype.rekapitulasi_anggaran_proyek.rekapitulasi_anggaran_proyek.get_rekap',
				args: {
					'project': frm.doc.project,
					'start_date': frm.doc.start_date,
					'finish_date': frm.doc.finish_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("detail");
							pr.project = vals[i].project;
							pr.project_name = vals[i].project_name;
							pr.uraian = vals[i].purpose;
							pr.tanggal_pengajuan = vals[i].posting_date;
							pr.total_budget_first = vals[i].total_budget_first;
							pr.tanggal_disetujui = vals[i].submitted_date;
							pr.total_budget = vals[i].total_budget;
							pr.tanggal_realisasi = vals[i].tanggal_realisasi;
							pr.paid_amount = vals[i].paid_amount;
							pr.keterangan = vals[i].keterangan;
						}
						frm.refresh_field("detail");
					}
				}
			});
		}
	},
	finish_date: function(frm){
		if(frm.doc.project && frm.doc.start_date && frm.doc.finish_date){
			frm.clear_table("detail");
			frappe.call({
				method: 'erpnext.projects.doctype.rekapitulasi_anggaran_proyek.rekapitulasi_anggaran_proyek.get_rekap',
				args: {
					'project': frm.doc.project,
					'start_date': frm.doc.start_date,
					'finish_date': frm.doc.finish_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("detail");
							pr.project = vals[i].project;
							pr.project_name = vals[i].project_name;
							pr.uraian = vals[i].purpose;
							pr.tanggal_pengajuan = vals[i].posting_date;
							pr.pengajuan = vals[i].total_budget_first;
							pr.tanggal_disetujui = vals[i].submitted_date;
							pr.disetujui = vals[i].total_budget;
							pr.tanggal_realisasi = vals[i].tanggal_realisasi;
							pr.realisasi = vals[i].paid_amount;
							pr.keterangan = vals[i].keterangan;
						}
						frm.refresh_field("detail");
					}
				}
			});
		}
	}
});

frappe.ui.form.on('Rekapitulasi Anggaran Proyek Detail', {
	// pengajuan: function(frm, dt, dn){
	// 	let d = locals[dt][dn];
	// 	if(d.pengajuan && d.realisasi){
	// 		d.saldo = d.pengajuan-d.realisasi;
	// 	}
	// 	frm.refresh_field("detail");
	// },
	// realisasi: function(frm, dt, dn){
	// 	let d = locals[dt][dn];
	// 	if(d.pengajuan && d.realisasi){
	// 		d.saldo = d.pengajuan-d.realisasi;
	// 	}
	// 	frm.refresh_field("detail");
	// }
});