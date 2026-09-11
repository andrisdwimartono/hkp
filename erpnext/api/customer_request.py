import frappe
from frappe.utils import add_months

@frappe.whitelist()
def get_customer_request(project=None):

    query = """
        SELECT
            cr.name,
            cr.docstatus,
            cr.project,
            cr.project_name,
            cr.title,
            cr.date,
            crd.title AS detail_title,
            crd.description,
            crd.note
        FROM `tabCustomer Request` AS cr
        INNER JOIN `tabCustomer Request Detail` AS crd
            ON crd.parent = cr.name
            AND crd.parenttype = 'Customer Request'
        WHERE cr.docstatus < 2
    """

    values = {}

    if project:
        query += " AND cr.project = %(project)s"
        values["project"] = project

    query += """
        ORDER BY cr.date DESC, crd.idx
    """

    return frappe.db.sql(
        query,
        values,
        as_dict=True
    )
    
    
