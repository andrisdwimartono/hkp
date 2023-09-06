// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Evaluasi Supplier Jasa', {
	refresh: function(frm) {
		// if (frm.doc.__unsaved == 1)	{
		// 	frm.clear_table("pejabat");
		// 	var x = ["Site Manager", "Manager Operasi", "Direktur Operasi"];
		// 	var y = ["SM", "M OPS", "DIR OPS"];
		// 	var z = ["Membuat", "Menyetujui", "Mengetahui"];

		// 	// var x = ["Site Manager", "Manager Operasi", "Manager Operasi 2", "Direktur Operasi"];
		// 	// var y = ["SM", "M OPS", "M OPS 2", "DIR OPS"];
		// 	// var z = ["Membuat", "Menyetujui", "Memeriksa", "Mengetahui"];

		// 	for(var i = 0; i < x.length; i++){
		// 		let d = frm.add_child("pejabat");
		// 		d.jabatan = x[i];
		// 		d.jabatan_abbr = y[i];
		// 		d.aksi = z[i];
		// 	}
			
		// 	frm.refresh_fields("pejabat");
		// 	frappe.db.get_value("Employee", {"user_id": cur_frm.doc.pejabat[0].user}, ["name", "user_id", "employee_name"]).then((value) => {
		// 		var vals = value.message;
		// 		var child = locals["Process Rule"][cur_frm.doc.pejabat[0].name];
		// 		child.user = vals.user_id;
		// 		child.employee = vals.name;
		// 		child.employee_name = vals.employee_name;
		// 		child.status = "Yes";
		// 		frm.refresh_fields("pejabat");
		// 	});
			
		// }else{
		// 	frappe.call({
		// 		method: 'erpnext.projects.utils.get_next_process_rule',
		// 		args: {
		// 			'doctype': frm.doc.doctype,
		// 			'docname': frm.doc.name
		// 		},
		// 		callback: function(r) {
		// 			if(r.message){
		// 				var vals = r.message;
		// 				frm.add_custom_button(vals.aksi, function () {
		// 					frappe.prompt([
		// 						{
		// 							label: 'Status',
		// 							fieldname: 'status',
		// 							fieldtype: 'Select',
		// 							options: !["Mengetahui", "Membuat"].includes(vals.aksi)?["Yes", "No"]: ["Yes"],
		// 							default: "Yes",
		// 							reqd: 1
		// 						},
		// 						{
		// 							label: __('Comment'),
		// 							fieldname: 'comment',
		// 							fieldtype: 'Small Text'
		// 						},
		// 						{
		// 							label: 'process_rule_name',
		// 							fieldname: 'process_rule_name',
		// 							fieldtype: 'Data',
		// 							hidden: 1,
		// 							default: vals.name
		// 						},
		// 					], (values) => {
		// 						frappe.call({
		// 							method: 'erpnext.projects.utils.save_process_rule',
		// 							args: {
		// 								'docname': values.process_rule_name,
		// 								'status': values.status,
		// 								'comment': values.comment
		// 							},
		// 							callback: function(r) {
		// 								if(r.message){
		// 									frm.reload_doc();
		// 								}
		// 							}
		// 						});
		// 					},
		// 						vals.jabatan+' '+vals.aksi,
		// 						'Simpan'
		// 					);
		// 				}).removeClass("btn-default").addClass("btn-info");
		// 			}
		// 		}
		// 	});
		// }

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
	onload: function(frm){
		frm.set_query('employee', 'pejabat', function() {
			return {
				filters: {
					user_id: ["!=", ""],
				},
			};
		});
	},
	kriteria_penilaian: function(frm){
		if (frm.doc.kriteria_penilaian) {
			cur_frm.clear_table("details")
			frappe.call({
				method: "erpnext.projects.doctype.evaluasi_supplier_jasa.evaluasi_supplier_jasa.get_details",
				args: {
					"kriteria_penilaian": frm.doc.kriteria_penilaian
				},
				callback: function(r) {
					if (r.message) {
						$.each(r.message, function(i, d) {
							var row = frappe.model.add_child(frm.doc, "Evaluasi Supplier Jasa Detail", "details");
							row.kriteria = d.kriteria;
							row.bobot = d.bobot;
						});
					}
					refresh_field("details");
				}
			});
			
			frappe.call({
				method: "erpnext.projects.doctype.evaluasi_supplier_jasa.evaluasi_supplier_jasa.get_panduan_penilaian",
				args: {
					"kriteria_penilaian": frm.doc.kriteria_penilaian
				},
				callback: function(r) {
					if (r.message) {
						for(var i = 0; i < r.message.length; i++){
							cur_frm.set_value("panduan_penilaian", r.message[i].panduan_penilaian);
						}
					}
					refresh_field("panduan_penilaian");
				}
			});
		}
	}
});
