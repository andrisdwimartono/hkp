frappe.listview_settings['Payment Entry'] = {
	add_fields: ["mode_of_payment", "docstatus", "giro_mundur_date"],
	get_indicator: function(doc) {
		if(doc.docstatus == 1 && doc.mode_of_payment == "Giro Mundur"){
			var sys_date = new Date(frappe.datetime.get_today());
			sys_date.setDate(sys_date.getDate() - 1);

			var giro_mundur_date = new Date(doc.giro_mundur_date);
			giro_mundur_date.setDate(giro_mundur_date.getDate());
			if(giro_mundur_date.getDate() == sys_date.getDate() && giro_mundur_date.getMonth() == sys_date.getMonth() && giro_mundur_date.getFullYear() == sys_date.getFullYear()){
				return [__("Jatuh Tempo"), "yellow", "docstatus,==,1"];
			}
			
		}
		// if (doc.status == "Taken") {
		// 	return [__("Taken"), "green", "status,==,Taken"];
		// } else if (doc.status == "Deposited" && doc.schedule_date >= frappe.datetime.get_today()) {
		// 	return [__("Deposited"), "orange", "status,==,Deposited|schedule_date,>,Today"];
		// } else if (doc.status == "Deposited" && doc.schedule_date < frappe.datetime.get_today()) {
		// 	return [__("Overdue"), "red", "status,==,Deposited|schedule_date,<=,Today"];
		// }
	},
	onload: function(listview) {
		if (listview.page.fields_dict.party_type) {
			listview.page.fields_dict.party_type.get_query = function() {
				return {
					"filters": {
						"name": ["in", Object.keys(frappe.boot.party_account_types)],
					}
				};
			};
		}
	}
};

