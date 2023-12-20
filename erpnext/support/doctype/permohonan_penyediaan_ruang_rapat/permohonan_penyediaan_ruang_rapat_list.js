// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.listview_settings['Permohonan Penyediaan Ruang Rapat'] = {
	add_fields: ["docstatus"],
	get_indicator: function(doc) {
		console.log(doc)
		if(doc.docstatus == 0) {
			return [__("Pengajuan"), "yellow", "docstatus,=,0"];
		} 
		if(doc.docstatus == 1) {
			return [__("Diterima"), "green", "docstatus,=,1"];
		} 
		if(doc.docstatus == 2) {
			return [__("Ditolak"), "red", "docstatus,=,2"];
		}
	}
};