// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Penilaian Karyawan Kontrak', {
	// refresh: function(frm) {

	// },
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: {
					'employment_type': ['in', 'Contract,On Job Training']
				}
			};
		});
	}
});
