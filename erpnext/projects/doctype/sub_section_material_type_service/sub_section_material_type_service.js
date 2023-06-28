// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sub Section Material Type Service', {
	// refresh: function(frm) {

	// }
	setup: function(frm){
		frm.set_query('sub_project_sub_section', function(doc) {
			return {
				'filters': {
					'sub_section': doc.sub_section
				}
			};
		});
		
		frm.set_query('item_code', 'services', () => ({
			filters: {
				item_group: "Services"
			}
		}));
	}
});
