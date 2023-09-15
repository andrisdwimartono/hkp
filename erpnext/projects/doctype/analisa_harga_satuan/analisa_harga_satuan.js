// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Analisa Harga Satuan', {
	// refresh: function(frm) {

	// },
	setup: function(frm) {
		frm.set_query("document_of_type", "material", function() {
			return {
				filters: {
					type: "Sub Section Material Type Materi"
				}
			};
		});

		frm.set_query("document_of_type", "tenaga", function() {
			return {
				filters: {
					type: ["in", ["Sub Section Material Type Service" ,"Sub Section Material Type Jasa Konstruksi"]]
				}
			};
		});

		frm.set_query("document_of_type", "peralatan_kerja", function() {
			return {
				filters: {
					type: "Sub Section Material Type Tool"
				}
			};
		});
	},
});

frappe.ui.form.on("Analisa Harga Satuan Material", "koefisien", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    d.total = d.price*d.koefisien;
	refresh_field("material");
	refresh_field("tenaga");
	refresh_field("peralatan_kerja");
	var total = 0;
	if(frm.doc.material)
		for(var i = 0; i < frm.doc.material.length; i++){
			total += frm.doc.material[i].total;
		}
	if(frm.doc.tenaga)
		for(var i = 0; i < frm.doc.tenaga.length; i++){
			total += frm.doc.tenaga[i].total;
		}
	if(frm.doc.peralatan_kerja)
		for(var i = 0; i < frm.doc.peralatan_kerja.length; i++){
			total += frm.doc.peralatan_kerja[i].total;
		}
	frm.set_value("total", total);
});

frappe.ui.form.on("Analisa Harga Satuan Material", "price", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    d.total = d.price*d.koefisien;
	refresh_field("material");
	refresh_field("tenaga");
	refresh_field("peralatan_kerja");
	var total = 0;
	if(frm.doc.material)
		for(var i = 0; i < frm.doc.material.length; i++){
			total += frm.doc.material[i].total;
		}
	if(frm.doc.tenaga)
		for(var i = 0; i < frm.doc.tenaga.length; i++){
			total += frm.doc.tenaga[i].total;
		}
	if(frm.doc.peralatan_kerja)
		for(var i = 0; i < frm.doc.peralatan_kerja.length; i++){
			total += frm.doc.peralatan_kerja[i].total;
		}
	frm.set_value("total", total);
});