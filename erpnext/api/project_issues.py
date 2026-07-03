import frappe

@frappe.whitelist()
def get_project_issues(status=None, kesesuaian=None, issue_name=None):
    query = """
        SELECT
            ltb.name,
            ltb.project,
            proj.project_name,
            proj.percent_complete,
            proj.expected_start_date,
            proj.expected_end_date,
            proj.is_active,
            ltb.jenis,
            ltb.uraian,
            ltb.creation,
            ltb.target_penyelesaian,
            pr.initial,
            pr.employee_name,
            ltb.workflow_state AS status,
            ltb.kesesuaian
        FROM `tabLAPORAN TINDAKAN PERBAIKAN DAN PENCEGAHAN` AS ltb
        LEFT JOIN tabProject AS proj ON proj.name = ltb.project
        LEFT JOIN `tabProcess Rules` AS pr ON pr.parent = ltb.name
            AND pr.parenttype = 'LAPORAN TINDAKAN PERBAIKAN DAN PENCEGAHAN'
            AND pr.jabatan = 'Pelapor'
        WHERE ltb.docstatus != 2
    """

    values = {}

    if status:
        query += " AND ltb.workflow_state = %(status)s"
        values["status"] = status
    
    if kesesuaian:
        query += " AND ltb.kesesuaian = %(kesesuaian)s"
        values["kesesuaian"] = kesesuaian

    if issue_name:
        query += " AND ltb.uraian LIKE %(issue_name)s"
        values["issue_name"] = f"%{issue_name}%"

    query += " ORDER BY ltb.modified DESC"
    
    return frappe.db.sql(query, values, as_dict=True)