// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Permohonan Penyediaan Ruang Rapat', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 0)
			frm.add_custom_button(__('Tolak'), function () {
				frappe.call({
					method: 'erpnext.support.doctype.permohonan_penyediaan_ruang_rapat.permohonan_penyediaan_ruang_rapat.tolak_pengajuan',
					args: {
						'docname': frm.doc.name
					},
					callback: function(r) {
						location.reload();
					}
				});
			});
	}
});
