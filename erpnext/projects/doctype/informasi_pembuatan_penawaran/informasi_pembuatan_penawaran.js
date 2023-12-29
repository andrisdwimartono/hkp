// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('INFORMASI PEMBUATAN PENAWARAN', {
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			frm.clear_table("pejabat");
			var x = ["Direktur Operasi", "Estimasi", "Manager Logistik", "Manager Sekretariat", "Manager Keuangan"];
			var y = ["DIR. OPS", "EST", "LOG", "SEK", "KEU"];
			var z = ["Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui"];
			for(var i = 0; i < x.length; i++){
				let d = frm.add_child("pejabat");
				d.jabatan = x[i];
				d.jabatan_abbr = y[i];
				d.aksi = z[i];
			}
			frm.refresh_fields("pejabat");

			frm.clear_table("aktivitas");
			var x = ["Pra-kualifikasi", "Pendaftaran", "Rencana Kerja dan Syarat - Syarat", "Gambar Tender", "Kantor", "Lapangan", "Finishing penawaran", "Pemasukan penawaran"];
			var y = ["", "", "Pengambilan Dokumen Tender", "Pengambilan Dokumen Tender", "Penjelasan", "Penjelasan", "", ""];
			for(var i = 0; i < x.length; i++){
				let d = frm.add_child("aktivitas");
				d.aktivitas = x[i];
				d.induk_aktivitas = y[i];
			}
			frm.refresh_fields("aktivitas");
		}else{
			frappe.call({
				method: 'erpnext.projects.doctype.informasi_pembuatan_penawaran.informasi_pembuatan_penawaran.view_doc',
				args: {
					'docname': frm.doc.name
				},
				callback: function(r) {
					
				}
			});
			// frm.disable_save();
			// frappe.call({
			// 	method: 'erpnext.projects.utils.get_next_process_rule',
			// 	args: {
			// 		'doctype': frm.doc.doctype,
			// 		'docname': frm.doc.name
			// 	},
			// 	callback: function(r) {
			// 		if(r.message){
			// 			var vals = r.message;
			// 			frm.add_custom_button(vals.aksi, function () {
			// 				frappe.prompt([
			// 					{
			// 						label: 'Status',
			// 						fieldname: 'status',
			// 						fieldtype: 'Select',
			// 						options: ["Yes", "No"],
			// 						default: "Yes",
			// 						reqd: 1
			// 					},
			// 					{
			// 						label: __('Comment'),
			// 						fieldname: 'comment',
			// 						fieldtype: 'Small Text'
			// 					},
			// 					{
			// 						label: 'process_rule_name',
			// 						fieldname: 'process_rule_name',
			// 						fieldtype: 'Data',
			// 						hidden: 1,
			// 						default: vals.name
			// 					},
			// 				], (values) => {
			// 					frappe.call({
			// 						method: 'erpnext.projects.utils.save_process_rule',
			// 						args: {
			// 							'docname': values.process_rule_name,
			// 							'status': values.status,
			// 							'comment': values.comment
			// 						},
			// 						callback: function(r) {
			// 							if(r.message){
			// 								frm.reload_doc();
			// 							}
			// 						}
			// 					});
			// 				},
			// 					vals.jabatan+' '+vals.aksi,
			// 					'Simpan'
			// 				);
			// 			}).removeClass("btn-default").addClass("btn-info");
			// 		}
			// 	}
			// });
		}
	},
	onload: function(frm){
		frm.set_query('employee', 'pejabat', function() {
			return {
				filters: {
					user_id: ["!=", ""],
				},
			};
		});
	}
});
