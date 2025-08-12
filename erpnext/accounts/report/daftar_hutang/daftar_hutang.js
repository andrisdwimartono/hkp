frappe.query_reports['Daftar Hutang'] = {
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
       }
    ]
}