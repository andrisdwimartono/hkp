frappe.query_reports['Rencana Pengajuan Anggaran Proyek'] = {
    "filters": [
       {
        "fieldname":"date_from",
        "label":__("Date From"),
        "fieldtype": "Date",
        "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
       },
       {
        "fieldname":"date_to",
        "label":__("Date To"),
        "fieldtype": "Date",
        "default": "Today"
       },
       {
        "fieldname":"status",
        "label":__("Status"),
        "fieldtype": "Select",
        "default": "Not Approved",
        "options": ["Not Approved", "Approved"]
       },
       {
        "fieldname": "type",
        "label":__("Type"),
        "fieldtype": "Select",
        "default": "All",
        "options": ["All", "Kas Bon Proyek", "Slip Pembayaran Supplier", "Slip Pembayaran Subkon"]
       },
    ]
}