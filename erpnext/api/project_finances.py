import frappe
from frappe.utils import get_first_day, get_last_day, add_months, nowdate

@frappe.whitelist()
def get_project_income_progress(project=None):
    if project:
        project_overview = frappe.db.get_value("Project", project, ["name", "project_name", "percent_complete", "status", "customer", "contract_no", "is_active"], as_dict=True)
        
        project_sm = frappe.db.sql("""
            SELECT
                pt.employee,
                pt.employee_name
            FROM `tabProject Team` AS pt
            WHERE pt.parent = %(project)s AND pt.designation = 'Site Manager'
        """, {"project": project}, as_dict=True)

        income = frappe.db.sql("""
            SELECT
                lmrap.income_final_realization
            FROM `tabLaporan Monitoring RAP` AS lmrap
            WHERE lmrap.project = %(project)s
        """, {"project": project}, as_dict=True)

        expense = frappe.db.sql("""
            SELECT
                SUM(lmrapad.final_realization) AS expense_final_realization
            FROM `tabLaporan Monitoring RAP` AS lmrap
            INNER JOIN `tabLaporan Monitoring RAP Detail` AS lmrapad ON lmrapad.parent = lmrap.name AND lmrapad.parenttype = 'Laporan Monitoring RAP'
            WHERE lmrap.project = %(project)s
        """, {"project": project}, as_dict=True)

        work_progress = frappe.db.sql("""
            SELECT
                proj.percent_complete,
                proj.contract_value
            FROM `tabProject` AS proj
            WHERE proj.name = %(project)s
        """, {"project": project}, as_dict=True)
        
        # hitung progress
        income_progress = 0
        if work_progress and work_progress[0]["contract_value"] != 0 and income:
            income_progress = (income[0]["income_final_realization"] / work_progress[0]["contract_value"]) * 100

        value_rap = frappe.db.sql("""
            SELECT
                budget.total_budget_amount
            FROM `tabBudget` AS budget
            WHERE budget.project = %(project)s
        """, {"project": project}, as_dict=True)

        response = {
            "project_name": project_overview["project_name"],
            "customer": project_overview["customer"],
            "contract_no": project_overview["contract_no"],
            "status": project_overview["status"],
            "is_active": project_overview["is_active"],
            "site_manager": project_sm[0]["employee_name"] if project_sm else "",
            "income_progress": income_progress,
            "work_progress": work_progress[0]["percent_complete"] if work_progress else 0,
            "contract_value": work_progress[0]["contract_value"] if work_progress else 0,
            "income": income[0]["income_final_realization"] if income else 0,
            "expense": expense[0]["expense_final_realization"] if expense else 0,
            "rap_value": value_rap[0]["total_budget_amount"] if value_rap else 0,
        }

        return response
    return {
        "project_name": None,
        "customer": None,
        "contract_no": None,
        "status": None,
        "is_active": None,
        "site_manager": None,
        "income_progress": 0,
        "work_progress": 0,
        "contract_value": 0,
        "income": 0,
        "expense": 0,
        "rap_value": 0,
    }

@frappe.whitelist()
def get_expense_income_last_3_months(project=None):
    if project:
        today = nowdate()
        this_start = get_first_day(today)
        this_end = get_last_day(today)
        
        this_month_expense = frappe.db.sql("""
            SELECT
                SUM(gle.debit-gle.credit) AS total_expense
            FROM `tabLaporan Monitoring RAP` AS lmr
            INNER JOIN `tabLaporan Monitoring RAP Detail` AS lmrd ON lmrd.parent = lmr.name AND lmrd.parenttype = 'Laporan Monitoring RAP'
            INNER JOIN `tabGL Entry` AS gle ON (gle.account = lmrd.account OR gle.account = lmrd.account2) AND gle.docstatus = 1
            WHERE lmr.project = %(project)s
                AND gle.posting_date BETWEEN %(start_date)s AND %(end_date)s;
                    """, {"project": project, "start_date": this_start, "end_date": this_end}, as_dict=True)

        this_month_income = frappe.db.sql("""
            SELECT
                SUM(bs.amount) AS total_income
            FROM `tabBilling Schedule` AS bs
            WHERE bs.project = %(project)s
                AND bs.payout_date IS NOT NULL
                AND bs.payout_date BETWEEN %(start_date)s AND %(end_date)s;
                    """, {"project": project, "start_date": this_start, "end_date": this_end}, as_dict=True)

        this_month_billing_schedule = frappe.db.sql("""
            SELECT
                SUM(bs.amount) AS total_billing
            FROM `tabBilling Schedule` AS bs
            WHERE bs.project = %(project)s
                AND bs.status NOT IN ('Completed')
                AND bs.billing_date BETWEEN %(start_date)s AND %(end_date)s""", {"project": project, "start_date": this_start, "end_date": this_end}, as_dict=True)

        last_start = get_first_day(add_months(today, -1))
        last_end = get_last_day(add_months(today, -1))

        last_month_expense = frappe.db.sql("""
            SELECT
                SUM(gle.debit-gle.credit) AS total_expense
            FROM `tabLaporan Monitoring RAP` AS lmr
            INNER JOIN `tabLaporan Monitoring RAP Detail` AS lmrd ON lmrd.parent = lmr.name AND lmrd.parenttype = 'Laporan Monitoring RAP'
            INNER JOIN `tabGL Entry` AS gle ON (gle.account = lmrd.account OR gle.account = lmrd.account2) AND gle.docstatus = 1
            WHERE lmr.project = %(project)s
                AND gle.posting_date BETWEEN %(start_date)s AND %(end_date)s;
                    """, {"project": project, "start_date": last_start, "end_date": last_end}, as_dict=True)

        last_month_income = frappe.db.sql("""
            SELECT
                SUM(bs.amount) AS total_income
            FROM `tabBilling Schedule` AS bs
            WHERE bs.project = %(project)s
                AND bs.payout_date IS NOT NULL
                AND bs.payout_date BETWEEN %(start_date)s AND %(end_date)s;
                    """, {"project": project, "start_date": last_start, "end_date": last_end}, as_dict=True)

        last_month_billing_schedule = frappe.db.sql("""
            SELECT
                SUM(bs.amount) AS total_billing
            FROM `tabBilling Schedule` AS bs
            WHERE bs.project = %(project)s
                AND bs.status NOT IN ('Completed')
                AND bs.billing_date BETWEEN %(start_date)s AND %(end_date)s""", {"project": project, "start_date": last_start, "end_date": last_end}, as_dict=True)

        third_start = get_first_day(add_months(today, -2))
        third_end = get_last_day(add_months(today, -2))

        three_months_ago_expense = frappe.db.sql("""
            SELECT
                SUM(gle.debit-gle.credit) AS total_expense
            FROM `tabLaporan Monitoring RAP` AS lmr
            INNER JOIN `tabLaporan Monitoring RAP Detail` AS lmrd ON lmrd.parent = lmr.name AND lmrd.parenttype = 'Laporan Monitoring RAP'
            INNER JOIN `tabGL Entry` AS gle ON (gle.account = lmrd.account OR gle.account = lmrd.account2) AND gle.docstatus = 1
            WHERE lmr.project = %(project)s
                AND gle.posting_date BETWEEN %(start_date)s AND %(end_date)s;
                    """, {"project": project, "start_date": third_start, "end_date": third_end}, as_dict=True)

        three_months_ago_income = frappe.db.sql("""
            SELECT
                SUM(bs.amount) AS total_income
            FROM `tabBilling Schedule` AS bs
            WHERE bs.project = %(project)s
                AND bs.payout_date IS NOT NULL
                AND bs.payout_date BETWEEN %(start_date)s AND %(end_date)s;
                    """, {"project": project, "start_date": third_start, "end_date": third_end}, as_dict=True)
        
        three_months_ago_billing_schedule = frappe.db.sql("""
            SELECT
                SUM(bs.amount) AS total_billing
            FROM `tabBilling Schedule` AS bs
            WHERE bs.project = %(project)s
                AND bs.status NOT IN ('Completed')
                AND bs.billing_date BETWEEN %(start_date)s AND %(end_date)s""", {"project": project, "start_date": third_start, "end_date": third_end}, as_dict=True)

        return {
            "this_month_expense": this_month_expense[0]["total_expense"] if this_month_expense else 0,
            "last_month_expense": last_month_expense[0]["total_expense"] if last_month_expense else 0,
            "three_months_ago_expense": three_months_ago_expense[0]["total_expense"] if three_months_ago_expense else 0,
            "this_month_income": this_month_income[0]["total_income"] if this_month_income else 0,
            "last_month_income": last_month_income[0]["total_income"] if last_month_income else 0,
            "three_months_ago_income": three_months_ago_income[0]["total_income"] if three_months_ago_income else 0,
            "this_month_billing_schedule": this_month_billing_schedule[0]["total_billing"] if this_month_billing_schedule else 0,
            "last_month_billing_schedule": last_month_billing_schedule[0]["total_billing"] if last_month_billing_schedule else 0,
            "three_months_ago_billing_schedule": three_months_ago_billing_schedule[0]["total_billing"] if three_months_ago_billing_schedule else 0,
        }
    return {
        "this_month_expense": 0,
        "last_month_expense": 0,
        "three_months_ago_expense": 0,
        "this_month_income": 0,
        "last_month_income": 0,
        "three_months_ago_income": 0,
        "this_month_billing_schedule": 0,
        "last_month_billing_schedule": 0,
        "three_months_ago_billing_schedule": 0,
    }

@frappe.whitelist()
def get_billing_schedule_no_complete(project=None):
    if project:
        return frappe.db.sql("""
            SELECT
                bs.*,
                bs_dc.available_document_count,
                bs_dc.not_available_document_count,
                bs_dc.total_document_count,
                bs_dc.document_list
            FROM `tabBilling Schedule` AS bs
            LEFT JOIN (
        SELECT
            bs_dc.parent,
            SUM(CASE WHEN bs_dc.avaibility = 'Available' THEN 1 ELSE 0 END) AS available_document_count,
            SUM(CASE WHEN bs_dc.avaibility = 'Not Available' THEN 1 ELSE 0 END) AS not_available_document_count,
            COUNT(*) AS total_document_count,
            CONCAT(
                '[',
                GROUP_CONCAT(
                    JSON_OBJECT(
                        'document_name', bs_dc.document_name,
                        'avaibility', bs_dc.avaibility
                    )
                    SEPARATOR ','
                ),
                ']'
            ) AS document_list
        FROM `tabBilling Schedule Documents Checklist` AS bs_dc
        WHERE bs_dc.parenttype = 'Billing Schedule'
        GROUP BY bs_dc.parent
    ) AS bs_dc ON bs_dc.parent = bs.name
            WHERE bs.project = %(project)s
                AND bs.billing_date IS NOT NULL
        """, {"project": project}, as_dict=True)
    return []