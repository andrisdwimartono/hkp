// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Detail Design Drawing', {
	// refresh: function(frm) {

	// }
	setup: function(frm){
		frm.set_query("drawing", "details", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Drawing', 'sub_section', '=', d.sub_section]
				]
			};
		});
	}
});
