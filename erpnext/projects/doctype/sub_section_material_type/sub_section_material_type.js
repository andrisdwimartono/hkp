// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sub Section Material Type', {
	// refresh: function(frm) {

	// },
	setup: function(frm){
		frm.set_query('item_code', 'tools', () => ({
			filters: {
				item_group: "Tools"
			}
		}));

		frm.set_query('item_code', 'services', () => ({
			filters: {
				item_group: "Services"
			}
		}));
		
		frm.set_query('item_code', 'materials', () => ({
			filters: {
				item_group: ["not in", ["Tools", "Services"]]
			}
		}));
	}
});
