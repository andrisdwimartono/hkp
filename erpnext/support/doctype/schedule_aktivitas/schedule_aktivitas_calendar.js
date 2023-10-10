frappe.views.calendar["Schedule Aktivitas"] = {
	field_map: {
		"start": "tanggalwaktu",
		"end": "tanggalwaktu",
		"id": "name",
		//"allDay": "all_day",
		"title": "agenda",
		//"status": "event_type",
		"color": "color"
	},
	style_map: {
		"Public": "success",
		"Private": "info"
	},
	get_events_method: "erpnext.support.doctype.schedule_aktivitas.schedule_aktivitas.get_schedule_aktivitas"
}