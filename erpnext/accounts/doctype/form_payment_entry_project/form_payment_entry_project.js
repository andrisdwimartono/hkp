// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Form Payment Entry Project', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on("Form Payment Entry Project Detail", "budget", function(frm, cdt, cdn) {
    var total_budget = 0;
	var total_approved_budget = 0;
	for(var i = 0; i < frm.doc.details.length; i++){
		var budget=frm.doc.details[i].budget?frm.doc.details[i].budget:0;
		var approved_budget=frm.doc.details[i].approved_budget?frm.doc.details[i].approved_budget:0;
		total_budget = total_budget+budget;
		total_approved_budget = total_approved_budget+approved_budget;
	}
	frm.set_value("total_budget", total_budget);
	frm.set_value("total_approved_budget", total_approved_budget);
	frm.refresh_field("total_budget");
	frm.refresh_field("total_approved_budget");
});

frappe.ui.form.on("Form Payment Entry Project Detail", "approved_budget", function(frm, cdt, cdn) {
    var total_budget = 0;
	var total_approved_budget = 0;
	for(var i = 0; i < frm.doc.details.length; i++){
		var budget=frm.doc.details[i].budget?frm.doc.details[i].budget:0;
		var approved_budget=frm.doc.details[i].approved_budget?frm.doc.details[i].approved_budget:0;
		total_budget = total_budget+budget;
		total_approved_budget = total_approved_budget+approved_budget;
	}
	frm.set_value("total_budget", total_budget);
	frm.set_value("total_approved_budget", total_approved_budget);
	frm.refresh_field("total_budget");
	frm.refresh_field("total_approved_budget");
});