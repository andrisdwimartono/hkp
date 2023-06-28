frappe.query_reports['Daftar Piutang'] = {
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
       },
       {
        "fieldname":"type",
        "label":__("Type"),
        "fieldtype": "Select",
        "options": "\nPiutang Afiliasi\nPiutang Hubungan Istimewa\nPiutang Karyawan\nPiutang Proyek",
        "default": "Piutang Afiliasi"
       }
    ]
}