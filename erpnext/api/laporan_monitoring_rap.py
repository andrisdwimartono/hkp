import frappe
import time

def update_income_realization(docname, income_adjustment=0):
    doc = frappe.get_doc("Laporan Monitoring RAP", docname)

    income_realization = doc.get_income_realization()

    doc.db_set("income_realization", income_realization, update_modified=False)

    adjustment = income_adjustment or 0

    doc.db_set(
        "income_final_realization",
        income_realization + adjustment,
        update_modified=False
    )

    doc.db_set("is_synchronized", 1, update_modified=False)
    frappe.db.commit()

    send_progress(doc.name)

def update_cost_realization(docname, cost_adjustment=0):
    doc = frappe.get_doc("Laporan Monitoring RAP Detail", docname)

    pdp = doc.account
    cost = doc.account2

    # get total of pdp and cost
    total_cost = frappe.db.sql("""
        SELECT SUM(debit-credit) as amount FROM `tabGL Entry` WHERE account IN ('{0}','{1}') AND docstatus = 1
    """.format(pdp, cost), as_dict=True)

    # update detail realization
    doc.db_set("realization", total_cost[0].amount, update_modified=False)

    adjustment = cost_adjustment or 0

    doc.db_set(
        "final_realization",
        total_cost[0].amount + adjustment,
        update_modified=False
    )

    doc.db_set("is_synchronized", 1, update_modified=False)

    parent = frappe.db.get_value(
        "Laporan Monitoring RAP Detail",
        doc.name,
        "parent"
    )
    frappe.db.commit()
    
    send_progress(parent)

def send_progress(parent):
    total = frappe.db.count(
        "Laporan Monitoring RAP Detail",
        {"parent": parent}
    ) + 1

    completed = frappe.db.count(
        "Laporan Monitoring RAP Detail",
        {
            "parent": parent,
            "is_synchronized": 1
        }
    )

    if frappe.db.get_value(
        "Laporan Monitoring RAP",
        parent,
        "is_synchronized"
    ):
        completed += 1

    progress = round(completed / total * 100)

    frappe.db.commit()

    frappe.publish_realtime(
        "rap_sync_progress",
        {
            "docname": parent,
            "progress": progress,
            "completed": completed,
            "total": total
        }
    )

def update_realization_by_account(account):
    gles = frappe.db.sql("""
        SELECT
            gle.account,
            acc.root_type,
            SUM(COALESCE(gle.debit, 0)) AS total_debit,
            SUM(COALESCE(gle.credit, 0)) AS total_credit
        FROM `tabGL Entry` AS gle
        INNER JOIN tabAccount AS acc ON acc.name = gle.account
        WHERE gle.account = %s
        GROUP BY gle.account, acc.root_type
            """, (account), as_dict=True)
    
    if gles and gles[0]:
        amount = 0
        # if root_type IN Asset and Expense then total_debit-total_credit
        if gles[0].root_type in ['Asset', 'Expense']:
            amount = gles[0].total_debit - gles[0].total_credit
        # if root_type IN Liability and Income and Equity then total_credit-total_debit
        elif gles[0].root_type in ['Liability', 'Income', 'Equity']:
            amount = gles[0].total_credit - gles[0].total_debit

        if amount != 0:
            # Update All Laporan Monitoring RAP Detail that have same account OR account2 with the amount
            details = frappe.db.sql("""
                SELECT DISTINCT doc_name FROM (
                    SELECT parent AS doc_name FROM `tabLaporan Monitoring RAP Detail` WHERE account = %s OR account2 = %s
                    UNION
                    SELECT name AS doc_name FROM `tabLaporan Monitoring RAP` WHERE income = %s
                ) AS sub
            """, (account, account, account), as_dict=True)
            
            for detail in details:
                doc = frappe.get_doc("Laporan Monitoring RAP", detail.doc_name)
                doc.is_synchronized = 0
                doc.save()
            
            frappe.db.commit()
            
@frappe.whitelist()
def get_income_cost_realization_by_project(project=None):
    project_filter = "WHERE lpm.project = '{0}'".format(project) if project else ""
    return frappe.db.sql("""
        SELECT
                lpm.project,
                proj.project_name,
                proj.percent_complete,
                proj.expected_start_date,
                proj.expected_end_date,
                lpm.income_final_realization,
                SUM(lpmd.final_realization) AS cost_final_realization,
                COALESCE(bud.total_budget_amount, 0) AS total_budget_amount,
                CASE proj.is_active
                        WHEN 'Yes' THEN 'active'
                        ELSE 'inactive'
                        END AS is_active,
                proj.status
        FROM `tabLaporan Monitoring RAP` AS lpm
        INNER JOIN tabProject AS proj ON proj.name = lpm.project
        INNER JOIN `tabLaporan Monitoring RAP Detail` AS lpmd ON lpm.name = lpmd.parent AND lpmd.parenttype = 'Laporan Monitoring RAP'
        LEFT JOIN (
            SELECT
                bud.project,
                MAX(bud.name) AS name
            FROM tabBudget AS bud
            WHERE bud.budget_against = 'Project'
            AND bud.docstatus = 0
            GROUP BY bud.project) AS last_budget ON last_budget.project = proj.name
        LEFT JOIN tabBudget AS bud ON bud.name = last_budget.name
        {0}
        GROUP BY lpm.project, lpm.income_final_realization
    """.format(project_filter), as_dict=True)

# get income and cost per project
@frappe.whitelist()
def get_income_cost_by_project(project=None):
    project_filter = "WHERE lpm.project = '{0}'".format(project) if project else ""
    return frappe.db.sql("""
        SELECT
                lpm.project,
                proj.project_name,
                proj.percent_complete,
                proj.expected_start_date,
                proj.expected_end_date,
                lpm.income_final_realization,
                SUM(lpmd.final_realization) AS cost_final_realization,
                cust.image AS logo,
                CASE proj.is_active
                        WHEN 'Yes' THEN 'active'
                        ELSE 'inactive'
                        END AS is_active,
                proj.status
        FROM `tabLaporan Monitoring RAP` AS lpm
        INNER JOIN tabProject AS proj ON proj.name = lpm.project
        LEFT JOIN tabCustomer AS cust ON cust.name = proj.customer
        INNER JOIN `tabLaporan Monitoring RAP Detail` AS lpmd ON lpm.name = lpmd.parent AND lpmd.parenttype = 'Laporan Monitoring RAP'
        {0}
        GROUP BY lpm.project, lpm.income_final_realization
    """.format(project_filter), as_dict=True)