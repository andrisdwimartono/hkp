// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Laporan Ringkasan Kebutuhan Proyek', {
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
		if(frm.doc.project && frm.doc.start_date && frm.doc.finish_date){
			frm.clear_table("realisasi_anggaran");
			frappe.call({
				method: 'erpnext.projects.doctype.laporan_ringkasan_kebutuhan_proyek.laporan_ringkasan_kebutuhan_proyek.get_rekap',
				args: {
					'project': frm.doc.project,
					'start_date': frm.doc.start_date,
					'finish_date': frm.doc.finish_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("realisasi_anggaran");
							pr.project = vals[i].project;
							pr.project_name = vals[i].project_name;
							pr.uraian = vals[i].purpose;
							pr.tanggal_pengajuan = vals[i].posting_date;
							pr.pengajuan = vals[i].total_budget_first;
							pr.tanggal_disetujui = vals[i].submitted_date;
							pr.disetujui = vals[i].total_budget;
							pr.tanggal_terbayar = vals[i].tanggal_terbayar;
							pr.terbayar = vals[i].paid_amount;
							pr.tanggal_realisasi = vals[i].tanggal_realisasi;
							pr.realisasi = vals[i].realisasi;
							pr.keterangan = vals[i].keterangan;
						}
						frm.refresh_field("realisasi_anggaran");
					}
				}
			});
		}
	},
	tanggal: function(frm){
		if(frm.doc.start_date && frm.doc.tanggal){
			var sisa_waktu = frappe.datetime.get_day_diff(frm.doc.tanggal,frm.doc.start_date);
			frm.set_value("sisa_waktu", sisa_waktu);
			frm.refresh_field("sisa_waktu");
		}
	},
	start_date: function(frm){
		if(frm.doc.start_date && frm.doc.tanggal){
			var sisa_waktu = frappe.datetime.get_day_diff(frm.doc.tanggal,frm.doc.start_date);
			frm.set_value("sisa_waktu", sisa_waktu);
			frm.refresh_field("sisa_waktu");
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
		if(frm.doc.project && frm.doc.start_date && frm.doc.finish_date){
			frm.clear_table("realisasi");
			frappe.call({
				method: 'erpnext.projects.doctype.laporan_ringkasan_kebutuhan_proyek.laporan_ringkasan_kebutuhan_proyek.get_rekap_materi',
				args: {
					'project': frm.doc.project,
					'start_date': frm.doc.start_date,
					'finish_date': frm.doc.finish_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("realisasi");
							pr.uraian_material = vals[i].uraian_material;
							pr.uom = vals[i].uom;
							pr.rencana = vals[i].rencana;
							pr.realisasi = vals[i].realisasi;
							pr.keterangan = vals[i].keterangan;
						}
						frm.refresh_field("realisasi");
					}
				}
			});
		}
		if(frm.doc.project && frm.doc.start_date && frm.doc.finish_date){
			frm.clear_table("realisasi_anggaran");
			frappe.call({
				method: 'erpnext.projects.doctype.laporan_ringkasan_kebutuhan_proyek.laporan_ringkasan_kebutuhan_proyek.get_rekap',
				args: {
					'project': frm.doc.project,
					'start_date': frm.doc.start_date,
					'finish_date': frm.doc.finish_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("realisasi_anggaran");
							pr.project = vals[i].project;
							pr.project_name = vals[i].project_name;
							pr.uraian = vals[i].purpose;
							pr.tanggal_pengajuan = vals[i].posting_date;
							pr.pengajuan = vals[i].total_budget_first;
							pr.tanggal_disetujui = vals[i].submitted_date;
							pr.disetujui = vals[i].total_budget;
							pr.tanggal_terbayar = vals[i].tanggal_terbayar;
							pr.terbayar = vals[i].paid_amount;
							pr.tanggal_realisasi = vals[i].tanggal_realisasi;
							pr.realisasi = vals[i].realisasi;
							pr.keterangan = vals[i].keterangan;
						}
						frm.refresh_field("realisasi_anggaran");
					}
				}
			});
		}
	},
	finish_date: function(frm){
		if(frm.doc.project && frm.doc.start_date && frm.doc.finish_date){
			frm.clear_table("realisasi_anggaran");
			frappe.call({
				method: 'erpnext.projects.doctype.laporan_ringkasan_kebutuhan_proyek.laporan_ringkasan_kebutuhan_proyek.get_rekap',
				args: {
					'project': frm.doc.project,
					'start_date': frm.doc.start_date,
					'finish_date': frm.doc.finish_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						for(var i = 0; i < vals.length; i++){
							var pr = frm.add_child("realisasi_anggaran");
							pr.project = vals[i].project;
							pr.project_name = vals[i].project_name;
							pr.uraian = vals[i].purpose;
							pr.tanggal_pengajuan = vals[i].posting_date;
							pr.pengajuan = vals[i].total_budget_first;
							pr.tanggal_disetujui = vals[i].submitted_date;
							pr.disetujui = vals[i].total_budget;
							pr.tanggal_terbayar = vals[i].tanggal_terbayar;
							pr.terbayar = vals[i].paid_amount;
							pr.tanggal_realisasi = vals[i].tanggal_realisasi;
							pr.realisasi = vals[i].realisasi;
							pr.keterangan = vals[i].keterangan;
						}
						frm.refresh_field("realisasi_anggaran");
					}
				}
			});
		}
	}
});
