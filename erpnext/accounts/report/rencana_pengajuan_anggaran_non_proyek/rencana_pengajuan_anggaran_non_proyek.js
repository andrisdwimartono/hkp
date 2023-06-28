frappe.query_reports['Rencana Pengajuan Anggaran Non Proyek'] = {
    "filters": [
       {
        "fieldname":"date_from",
        "label":__("Date From"),
        "fieldtype": "Date",
        "default": "Today"
       },
       {
        "fieldname":"date_to",
        "label":__("Date To"),
        "fieldtype": "Date",
        "default": "Today"
       }
    ]
}