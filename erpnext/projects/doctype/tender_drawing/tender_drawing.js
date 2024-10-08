// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tender Drawing', {
	// refresh: function(frm) {

	// },
	setup: function(frm){
		frm.set_query("drawing", "details", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Drawing', 'sub_section', '=', d.sub_section]
				]
			};
		});

		frm.set_query('sub_section', "details", function(doc) {
			return {
				'filters': {
					'name': ["!=", "UMUM"]
				}
			};
		})
	}
	
});
