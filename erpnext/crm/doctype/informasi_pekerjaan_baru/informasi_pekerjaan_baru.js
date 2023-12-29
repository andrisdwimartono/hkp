// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('INFORMASI PEKERJAAN BARU', {
	refresh: function(frm) {
		// if (frm.doc.__unsaved == 1)	{
		// 	if(!frm.doc.process_rules){
		// 		frm.clear_table("process_rules");
		// 		frappe.call({
		// 			method: 'erpnext.projects.utils.get_process_rules',
		// 			args: {
		// 				'doctype': frm.doc.doctype
		// 			},
		// 			callback: function(r) {
		// 				if(r.message){
		// 					var vals = r.message;
		// 					for(var i = 0; i < vals.length; i++){
		// 						var pr = frm.add_child("process_rules");
		// 						pr.jabatan = vals[i].jabatan;
		// 						pr.jabatan_abbr = vals[i].jabatan_abbr;
		// 						pr.state = vals[i].state;
		// 						pr.employee = vals[i].employee;
		// 						pr.initial = vals[i].initial;
		// 						pr.employee_name = vals[i].employee_name;
		// 						pr.user = vals[i].user;
		// 					}
		// 					frm.refresh_field("process_rules");
		// 				}
		// 			}
		// 		});
		// 	}
		// }else{
			
		// }
		// cur_frm.fields_dict['process_rules'].$wrapper.find('.grid-add-row').addClass('d-none');
		if (frm.doc.__unsaved == 1)	{
			frm.clear_table("pejabat");
			var x = ["Direktur Operasi", "Manager Engineering", "Manager Operasi", "Estimasi", "Pengendalian Konstruksi", "Manager Logistik", "Manager Keuangan", "Manager Akuntansi", "Direktur Utama"];
			var y = ["Direktur Operasi", "Manager Engineering", "Manager Operasi", "Estimasi", "Pengendalian Konstruksi", "Manager Logistik", "Manager Keuangan", "Manager Akuntansi", "Direktur Utama"];
			var z = ["Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui"];
			for(var i = 0; i < x.length; i++){
				let d = frm.add_child("pejabat");
				d.jabatan = x[i];
				d.jabatan_abbr = y[i];
				d.aksi = z[i];
			}
			frm.refresh_fields("pejabat");
		}else{
			frappe.call({
				method: 'erpnext.crm.doctype.informasi_pekerjaan_baru.informasi_pekerjaan_baru.view_doc',
				args: {
					'docname': frm.doc.name
				},
				callback: function(r) {
					
				}
			});
		}
	}
});
