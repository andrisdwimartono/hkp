// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('BOQ', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("BOQ Detail", {
	document_of_type: function(frm, cdt, cdn) {
    	var d = locals[cdt][cdn];
		frappe.call({
			method: 'erpnext.projects.doctype.boq.boq.get_harga',
			args: {
				types: d.types,
				document_of_type: d.document_of_type
			},
			callback: function(r) {
				if(r.message){
					var vals = r.message;
					if(d.types == "Analisa Harga Satuan"){
						d.type = "";
						d.deskripsi = vals.nama_pekerjaan;

						d.pengadaan_material_harga_satuan = 0;

						d.transportasi_dan_asuransi_material_harga_satuan = 0;

						d.pemasangan_dan_instalasi_section_harga_satuan = vals.total;
						frm.refresh_field("boq_detail");
					}else{
						d.type = vals.type;
						d.deskripsi = vals.item_name;
						d.uom = vals.uom;

						d.pengadaan_material_harga_satuan = vals.price;

						d.transportasi_dan_asuransi_material_harga_satuan = vals.transport_price;

						d.pemasangan_dan_instalasi_section_harga_satuan = 0;
						frm.refresh_field("boq_detail");
					}
				}
			}
		});
	},
	qty: function(frm, cdt, cdn) {
    	var d = locals[cdt][cdn];
		d.pengadaan_material_harga_total = d.pengadaan_material_harga_satuan*d.qty*d.koefisien;

		d.transportasi_dan_asuransi_material_harga_total = d.transportasi_dan_asuransi_material_harga_satuan*d.qty*d.koefisien;

		d.pemasangan_dan_instalasi_section_harga_total = d.pemasangan_dan_instalasi_section_harga_satuan*d.qty*d.koefisien;

		d.total = d.pengadaan_material_harga_total+d.transportasi_dan_asuransi_material_harga_total+d.pemasangan_dan_instalasi_section_harga_total;
		frm.refresh_field("boq_detail");
	},
	pengadaan_material_harga_satuan: function(frm, cdt, cdn) {
    	var d = locals[cdt][cdn];
		d.pengadaan_material_harga_total = d.pengadaan_material_harga_satuan*d.qty*d.koefisien;

		d.transportasi_dan_asuransi_material_harga_total = d.transportasi_dan_asuransi_material_harga_satuan*d.qty*d.koefisien;

		d.pemasangan_dan_instalasi_section_harga_total = d.pemasangan_dan_instalasi_section_harga_satuan*d.qty*d.koefisien;

		d.total = d.pengadaan_material_harga_total+d.transportasi_dan_asuransi_material_harga_total+d.pemasangan_dan_instalasi_section_harga_total;
		frm.refresh_field("boq_detail");
	},
	transportasi_dan_asuransi_material_harga_satuan: function(frm, cdt, cdn) {
    	var d = locals[cdt][cdn];
		d.pengadaan_material_harga_total = d.pengadaan_material_harga_satuan*d.qty*d.koefisien;

		d.transportasi_dan_asuransi_material_harga_total = d.transportasi_dan_asuransi_material_harga_satuan*d.qty*d.koefisien;

		d.pemasangan_dan_instalasi_section_harga_total = d.pemasangan_dan_instalasi_section_harga_satuan*d.qty*d.koefisien;

		d.total = d.pengadaan_material_harga_total+d.transportasi_dan_asuransi_material_harga_total+d.pemasangan_dan_instalasi_section_harga_total;
		frm.refresh_field("boq_detail");
	},
	pemasangan_dan_instalasi_section_harga_satuan: function(frm, cdt, cdn) {
    	var d = locals[cdt][cdn];
		d.pengadaan_material_harga_total = d.pengadaan_material_harga_satuan*d.qty*d.koefisien;

		d.transportasi_dan_asuransi_material_harga_total = d.transportasi_dan_asuransi_material_harga_satuan*d.qty*d.koefisien;

		d.pemasangan_dan_instalasi_section_harga_total = d.pemasangan_dan_instalasi_section_harga_satuan*d.qty*d.koefisien;

		d.total = d.pengadaan_material_harga_total+d.transportasi_dan_asuransi_material_harga_total+d.pemasangan_dan_instalasi_section_harga_total;
		frm.refresh_field("boq_detail");
	},
	koefisien: function(frm, cdt, cdn) {
    	var d = locals[cdt][cdn];
		d.pengadaan_material_harga_total = d.pengadaan_material_harga_satuan*d.qty*d.koefisien;

		d.transportasi_dan_asuransi_material_harga_total = d.transportasi_dan_asuransi_material_harga_satuan*d.qty*d.koefisien;

		d.pemasangan_dan_instalasi_section_harga_total = d.pemasangan_dan_instalasi_section_harga_satuan*d.qty*d.koefisien;

		d.total = d.pengadaan_material_harga_total+d.transportasi_dan_asuransi_material_harga_total+d.pemasangan_dan_instalasi_section_harga_total;
		frm.refresh_field("boq_detail");
	},
});