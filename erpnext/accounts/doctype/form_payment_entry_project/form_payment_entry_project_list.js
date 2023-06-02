frappe.listview_settings['Form Payment Entry Project'] = {
	add_fields: ["required_date", "outstanding_amount", "use_payment_entry"],
	get_indicator: function(doc) {
		if(doc.use_payment_entry){
			if(flt(doc.outstanding_amount)==0) {
				return [__("Paid"), "green", "outstanding_amount,<=,0"];
			} else if (flt(doc.outstanding_amount) > 0 && doc.required_date >= frappe.datetime.get_today()) {
				return [__("Belum Cair"), "orange", "outstanding_amount,>,0|required_date,>,Today"];
			} else if (flt(doc.outstanding_amount) > 0 && doc.required_date < frappe.datetime.get_today()) {
				return [__("Overdue"), "red", "outstanding_amount,>,0|required_date,<=,Today"];
			}
		}
	}
};
