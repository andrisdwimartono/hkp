// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sub Section Material Type Materi', {
	// refresh: function(frm) {

	// },
	setup: function(frm){
		frm.set_query('sub_section', function(doc) {
			return {
				'filters': {
					'name': ["!=", "UMUM"]
				}
			};
		})

		frm.set_query('sub_project_sub_section', function(doc) {
			return {
				'filters': {
					'sub_section': doc.sub_section
				}
			};
		});
	}
});