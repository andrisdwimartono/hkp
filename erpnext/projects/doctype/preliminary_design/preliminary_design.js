// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Preliminary Design', {
	refresh: function(frm) {
		// $("div[data-fieldname='histories']>.field-area").attr("")
		// $("div[data-fieldname='histories']>.field-area").css({"display": "block"});

	},
	setup: function(frm){
		frm.set_query("drawing", "details", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Drawing', 'sub_section', '=', d.sub_section],
					['Drawing', 'project', '=', cur_frm.doc.project]
				]
			};
		});
	}
});

frappe.ui.form.on('Preliminary Design Detail', {
	// refresh: function(frm) {

	// }
	histories: function(frm, dt, dn){
		var d = locals[dt][dn];
		frappe.call({
			method: 'erpnext.projects.doctype.preliminary_design.preliminary_design.get_histories',
			args: {
				'docname': d.name
			},
			callback: function(r) {
				// if(r.message){
				// 	var vals = r.message;
				// 	for(var i = 0; i < vals.length; i++){
				// 		var pr = frm.add_child("process_rules");
				// 		pr.jabatan = vals[i].jabatan;
				// 		pr.jabatan_abbr = vals[i].jabatan_abbr;
				// 		pr.state = vals[i].state;
				// 		pr.employee = vals[i].employee;
				// 		pr.initial = vals[i].initial;
				// 		pr.employee_name = vals[i].employee_name;
				// 		pr.user = vals[i].user;
				// 	}
				// 	frm.refresh_field("process_rules");
				// }
			}
		});
	}
});
