// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('CHECKLIST DOKUMEN TENDER', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('CHECKLIST DOKUMEN TENDER _ LIST', {
	ada: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.ada == 1){
			d.tidak_ada = 0;
		}else{
			d.tidak_ada = 1;
		}
		refresh_field("checklist");
	},
	tidak_ada: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.tidak_ada == 1){
			d.ada = 0;
		}else{
			d.ada = 1;
		}
		refresh_field("checklist");
	},
});