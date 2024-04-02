// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Form Payment Entry', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Form Payment Entry Non Project", "volume", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	get_budget(d);
});

frappe.ui.form.on("Form Payment Entry Non Project", "unit_price", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	get_budget(d);
});

function get_budget(d){
	var vol = d.unit_price?d.unit_price:0;
	var up = d.volume?d.volume:0;
	d.budget_amount = vol*up;
	cur_frm.refresh_field("details");
}

frappe.ui.form.on("Form Payment Entry Non Project", "budget_amount", function(frm, cdt, cdn) {
    var total_budget = 0;
	for(var i = 0; i < frm.doc.details.length; i++){
		var budget=frm.doc.details[i].budget_amount?frm.doc.details[i].budget_amount:0;
		total_budget = total_budget+budget;
	}
	frm.set_value("total_budget", total_budget);
	frm.refresh_field("total_budget");
});

// frappe.ui.form.on("Form Payment Entry Non Project", "approved_budget", function(frm, cdt, cdn) {
//     var total_budget = 0;
// 	var total_approved_budget = 0;
// 	for(var i = 0; i < frm.doc.details.length; i++){
// 		var budget=frm.doc.details[i].budget_amount?frm.doc.details[i].budget_amount:0;
// 		var approved_budget=frm.doc.details[i].approved_budget?frm.doc.details[i].approved_budget:0;
// 		total_budget = total_budget+budget;
// 		total_approved_budget = total_approved_budget+approved_budget;
// 	}
// 	frm.set_value("total_budget", total_budget);
// 	frm.set_value("total_approved_budget", total_approved_budget);
// 	frm.refresh_field("total_budget");
// 	frm.refresh_field("total_approved_budget");
// });