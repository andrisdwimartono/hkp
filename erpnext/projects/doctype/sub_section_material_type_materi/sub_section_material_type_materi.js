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


frappe.ui.form.on("Sub Section Material Type Materials", {
    item_code: function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
       	frappe.db.get_value("Item Price", {'item_code': d.item_code, 'buying': 1}, ["price_list_rate"], (r) => {
            frappe.model.set_value(cdt, cdn, "price", r.price_list_rate);
		});
 	}
});