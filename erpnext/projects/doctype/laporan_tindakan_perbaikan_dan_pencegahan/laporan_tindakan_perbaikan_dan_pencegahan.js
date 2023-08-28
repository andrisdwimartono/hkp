// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('LAPORAN TINDAKAN PERBAIKAN DAN PENCEGAHAN', {
	refresh: function(frm) {
		frappe.prompt([
				{'fieldname': 'workflow_comment', 'fieldtype': 'Small Text', 'label': 'Komentar'}
			],
			function(values){
				show_alert(values.workflow_comment, 5);
			},
			'Persetujuan',
			'Simpan'
		);		
	}
});
