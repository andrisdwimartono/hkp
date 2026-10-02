import frappe

@frappe.whitelist()
def get_daily_k3(project=None, from_date=None, to_date=None):
    if not project:
        frappe.throw("Project is required")
    if not from_date or not to_date:
        frappe.throw("From date and to date are required")
    elif from_date > to_date:
        frappe.throw("From date must be before to date")
    if project and from_date and to_date:
        return frappe.db.sql("""
			SELECT
			`tabDaily K3`.*,
			`tabProject`.customer,
			`tabProject`.project_address,
			`tabCustomer`.image,
			(
				CASE WHEN `tabDaily K3`.body_harness THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.pelindung_mata THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.masker THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.respirator THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.kedok_las THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.helm_safety THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.earmuff_earplug THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.sarung_tangan THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.sepatu_safety THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.sabuk_pengaman THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.pelampung THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.wearpack THEN 1 ELSE 0 END ) * 100.0 / 12 AS checklist_k3
		FROM `tabDaily K3`
		LEFT JOIN `tabProject` ON `tabDaily K3`.project = `tabProject`.name
		LEFT JOIN `tabCustomer` ON `tabProject`.customer = `tabCustomer`.name
		WHERE `tabDaily K3`.project = %s
		AND `tabDaily K3`.date BETWEEN %s AND %s
		ORDER BY `tabDaily K3`.date ASC
	""", (project, from_date, to_date), as_dict=1)