frappe.query_reports['Daftar Hutang'] = {
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