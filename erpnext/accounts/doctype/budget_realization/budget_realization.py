# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BudgetRealization(Document):
	pass

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_pos_rap(doctype, txt, searchfield, start, page_len, filters):
    budget = filters["budget"]
    if budget:
        return frappe.db.sql("""
        SELECT DISTINCT pr.pos_rap FROM `tabBudget` b
        INNER JOIN `tabBudget Account` ba ON ba.parent = b.name
		INNER JOIN `tabPOS RAP` pr ON ba.pos_rap = pr.pos_rap
        WHERE b.name = '{0}' AND (pr.{1} LIKE "%{2}%")
        LIMIT {3}, {4}
        """.format(budget, searchfield, txt, start, page_len))
    else:
        return {}

@frappe.whitelist()
def check_budget(budget = None, pos_rap = None):
    if budget and pos_rap:
        return frappe.db.sql("""
        SELECT * FROM `tabBudget Account` ba 
        LEFT JOIN (SELECT br.pos_rap, SUM(br.volume) volume_realization FROM `tabBudget Realization` br WHERE br.budget = '{0}' AND br.pos_rap = '{1}' AND br.docstatus = 1) br ON br.pos_rap = ba.pos_rap
        WHERE ba.parent = '{0}' AND ba.pos_rap = '{1}' AND ba.docstatus = 1
        """.format(budget, pos_rap), as_dict=1)
    return None

@frappe.whitelist()
def check_budget_realization(budget_realization = None):
    if budget_realization:
        return frappe.db.sql("""
        SELECT br.budget_amount FROM `tabBudget Realization` br
        WHERE br.name = '{0}' AND br.docstatus = 1
        """.format(budget_realization), as_dict=1)
    return None