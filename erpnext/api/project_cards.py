import frappe

@frappe.whitelist()
def get_projects(is_active=None, project_name=None):
    if is_active:
        if is_active == "active":
            is_active = "Yes"
        else:
            is_active = "No"
    query = """
        SELECT
            proj.name,
            proj.project_name,
            proj.percent_complete,
            proteam.employee_name AS pic,
            proj.expected_start_date,
            proj.expected_end_date,
            0 AS drawing_total,
            0 AS drawing_notyet,
            0 AS drawing_nen,
            0 AS drawing_en,
            0 AS drawing_fail,
            budget.total_budget_amount AS expense_planning,
            realisasi.total_realisasi AS expense_realization,
            0 AS cashflow_income,
            0 AS cashflow_outcome,
            proj.customer,
            cust.image AS logo,
            CASE proj.is_active
                WHEN 'Yes' THEN 'active'
                ELSE 'inactive'
                END AS is_active,
            proj.status
        FROM
            `tabProject` AS proj
        LEFT JOIN tabCustomer AS cust ON cust.name = proj.customer
        LEFT JOIN (
            SELECT
            pt.parent,
            pt.designation,
                pt.employee,
                em.employee_name
            FROM `tabProject Team` pt
            LEFT JOIN tabEmployee em ON em.name = pt.employee
            INNER JOIN (
                    SELECT
                            parent,
                            MIN(idx) AS min_idx
                    FROM `tabProject Team`
                    WHERE designation = 'Site Manager'
                    GROUP BY parent
            ) x
            ON pt.parent = x.parent
            AND pt.idx = x.min_idx) AS proteam ON proteam.parent = proj.name
        LEFT JOIN (SELECT
                project,
                total_budget_amount
            FROM (
                SELECT
                    project,
                    total_budget_amount,
                    ROW_NUMBER() OVER (
                        PARTITION BY project
                        ORDER BY creation DESC
                    ) AS rn
                FROM tabBudget
                WHERE docstatus != 2
            ) t
            WHERE rn = 1) AS budget ON budget.project = proj.name
        LEFT JOIN (
            SELECT
            rea.project,
            SUM(COALESCE(reade.budget_amount, 0)) AS total_realisasi
            FROM `tabRealisasi Anggaran Proyek` AS rea
            LEFT JOIN `tabForm Payment Entry Account Realisasi` AS reade ON reade.parent = rea.name = reade.parenttype = 'Realisasi Anggaran Proyek'
            WHERE rea.docstatus != 2
            GROUP BY rea.project) AS realisasi ON realisasi.project = proj.name
        WHERE
            proj.docstatus < 2
    """

    values = {}

    if is_active:
        query += " AND proj.is_active = %(is_active)s"
        values["is_active"] = is_active

    if project_name:
        query += " AND proj.project_name LIKE %(project_name)s"
        values["project_name"] = f"%{project_name}%"

    query += " ORDER BY proj.modified DESC"
    
    return frappe.db.sql(query, values, as_dict=True)