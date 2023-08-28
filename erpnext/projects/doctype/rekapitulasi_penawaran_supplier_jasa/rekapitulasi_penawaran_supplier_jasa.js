// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('REKAPITULASI PENAWARAN SUPPLIER JASA', {
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
	},
	// before_save: function(frm){
	// 	return new Promise(function (resolve, reject) {
	// 		show_alert();
	// 		// This will cancel save
	// 			// frappe.validated = false;
	// 			// reject();
			
	// 		// This will continue to save
	// 			// var negative = 'frappe.validated = false';
	// 			// resolve(negative);

	// 		// If you comment all of it
	// 		// Save button will be disabled (like it still processing)
	// 	})
	// },
	// before_workflow_action: async function(frm){
	// 	// let promise = new Promise((resolve, reject) => {
	// 	// 	frappe.confirm("anda yakin?",
	// 	// 		() => {
	// 	// 			frappe.msgprint("Oke");
	// 	// 		},
	// 	// 		() => reject()
	// 	// 	);
	// 	// });

	// 	// await promise.catch(() => frappe.throw("aaa"));
	// 	frappe.prompt([
	// 		{
	// 			label: 'Status',
	// 			fieldname: 'status',
	// 			fieldtype: 'Select',
	// 			options: ["Mengetahui", "Membuat"],
	// 			default: "Yes",
	// 			reqd: 1
	// 		},
	// 		{
	// 			label: __('Comment'),
	// 			fieldname: 'comment',
	// 			fieldtype: 'Small Text'
	// 		},
	// 		{
	// 			label: 'process_rule_name',
	// 			fieldname: 'process_rule_name',
	// 			fieldtype: 'Data',
	// 			hidden: 1,
	// 			default: 'aa'//vals.name
	// 		},
	// 	], (values) => {
	// 		// frappe.call({
	// 		// 	method: 'erpnext.projects.utils.save_process_rule',
	// 		// 	args: {
	// 		// 		'docname': values.process_rule_name,
	// 		// 		'status': values.status,
	// 		// 		'comment': values.comment
	// 		// 	},
	// 		// 	callback: function(r) {
	// 		// 		if(r.message){
	// 		// 			frm.reload_doc();
	// 		// 		}
	// 		// 	}
	// 		// });
	// 	},
	// 		"ABC",
	// 		'Simpan'
	// 	);
	// },
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
