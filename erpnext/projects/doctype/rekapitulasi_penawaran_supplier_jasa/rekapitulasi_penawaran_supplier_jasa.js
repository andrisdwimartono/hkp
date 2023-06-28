// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('REKAPITULASI PENAWARAN SUPPLIER JASA', {
	// refresh: function(frm) {

	// },
	kriteria_penilaian: function(frm){
		if (frm.doc.kriteria_penilaian) {
			cur_frm.clear_table("details")
			frappe.call({
				method: "erpnext.projects.doctype.evaluasi_supplier_jasa.evaluasi_supplier_jasa.get_details",
				args: {
					"kriteria_penilaian": frm.doc.kriteria_penilaian
				},
				callback: function(r) {
					if (r.message) {
						$.each(r.message, function(i, d) {
							var row = frappe.model.add_child(frm.doc, "Evaluasi Supplier Jasa Detail", "details");
							row.kriteria = d.kriteria;
							row.bobot = d.bobot;
						});
					}
					refresh_field("details");
				}
			});
			
			frappe.call({
				method: "erpnext.projects.doctype.evaluasi_supplier_jasa.evaluasi_supplier_jasa.get_panduan_penilaian",
				args: {
					"kriteria_penilaian": frm.doc.kriteria_penilaian
				},
				callback: function(r) {
					if (r.message) {
						for(var i = 0; i < r.message.length; i++){
							cur_frm.set_value("panduan_penilaian", r.message[i].panduan_penilaian);
						}
					}
					refresh_field("panduan_penilaian");
				}
			});
		}
	}
});
