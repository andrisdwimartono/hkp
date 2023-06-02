frappe.listview_settings['Deposite'] = {
	add_fields: ["schedule_date", "status"],
	get_indicator: function(doc) {
		if (doc.status == "Taken") {
			return [__("Taken"), "green", "status,==,Taken"];
		} else if (doc.status == "Deposited" && doc.schedule_date >= frappe.datetime.get_today()) {
			return [__("Deposited"), "orange", "status,==,Deposited|schedule_date,>,Today"];
		} else if (doc.status == "Deposited" && doc.schedule_date < frappe.datetime.get_today()) {
			return [__("Overdue"), "red", "status,==,Deposited|schedule_date,<=,Today"];
		}
	}
};
