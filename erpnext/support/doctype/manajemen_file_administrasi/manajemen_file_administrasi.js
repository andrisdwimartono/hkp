// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manajemen File Administrasi', {
	setup: function(frm) {
		frm.set_query("parent_manajemen_file_administrasi", function() {
			return {
				filters: {
					'is_group': 1
				}
			};
		});
	}
});
