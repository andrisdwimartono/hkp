# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from time import gmtime, strftime, strptime
from frappe.utils import today

class FormPaymentEntryProject(Document):
	def after_insert(self):
		assigner = []
		for d in self.pejabat:
			if x:
				assigner.append(d.user)
				self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user))
			notification_doc = {
				"type": "Alert",
				"document_type": self.doctype,
				"document_name": self.name,
				"subject": "Kas Bon Proyek baru {0}".format(self.name),
				"from_user": self.owner,
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)
	def validate(self):
		self.total_budget = 0
		for d in self.details:
			self.total_budget = self.total_budget+d.budget_amount
		if not self.total_budget_first:
			self.total_budget_first = self.total_budget
		if self.docstatus == 0:
			self.outstanding_amount = self.total_budget
	def on_submit(self):
		budget_approval_plan_doc = frappe.get_doc({
			"doctype" : "Budget Approval Plan",
			"posting_date": today()
			})
		budget_approval_plan_doc.append("budget_approval_plan_detail", {
			"peminta": self.owner,
			"total_budget": self.total_budget,
			"purpose": self.purpose,
			"form_payment_entry_project": self.name
		})
		budget_approval_plan_doc.save()
		frappe.db.sql("""UPDATE `tabForm Payment Entry Project` SET submitted_date = '{0}' WHERE name = '{1}'""".format(today(), self.name))
		frappe.db.commit()

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_pos_rap(doctype, txt, searchfield, start, page_len, filters):
    budget = filters["budget"]
    if budget:
        return frappe.db.sql("""
        SELECT DISTINCT pr.pos_rap FROM `tabBudget` b
        INNER JOIN `tabBudget Account` ba ON ba.parent = b.name
		INNER JOIN `tabPOS RAP` pr ON ba.pos_rap = pr.pos_rap
        WHERE b.name = '{0}' AND b.docstatus = 1 AND (pr.{1} LIKE "%{2}%")
        LIMIT {3}, {4}
        """.format(budget, searchfield, txt, start, page_len))
    else:
        return {}

@frappe.whitelist()
def check_budget(budget = None, pos_rap = None):
    if budget and pos_rap:
        return frappe.db.sql("""
        SELECT * FROM `tabBudget Account` ba 
        LEFT JOIN (SELECT br.pos_rap, SUM(br.volume) volume_realization FROM `tabForm Payment Entry Account` br INNER JOIN `tabForm Payment Entry Project` fpep ON fpep.name = br.parent WHERE fpep.budget = '{0}' AND br.pos_rap = '{1}' AND br.docstatus = 1) br ON br.pos_rap = ba.pos_rap
        WHERE ba.parent = '{0}' AND ba.pos_rap = '{1}' AND ba.docstatus = 1
        """.format(budget, pos_rap), as_dict=1)
    return None

@frappe.whitelist()
def get_details_hand_over_progress(hand_over_progress = None):
    if hand_over_progress:
        return frappe.db.sql("""
        SELECT hop.pos_rap, hop.total_cost unit_price, hop.total_cost budget_amount, hop.project, hop.progress_sequence, hop.job_name FROM `tabHand Over Progress` hop 
        WHERE hop.name = '{0}' AND hop.docstatus = 1
        """.format(hand_over_progress), as_dict=1)
    return None

@frappe.whitelist()
def get_details(budget = None):
    if budget:
        return frappe.db.sql("""
        SELECT ba.*, br.volume_realization FROM `tabBudget Account` ba 
        LEFT JOIN (SELECT br.pos_rap, SUM(br.volume) volume_realization FROM `tabForm Payment Entry Account` br INNER JOIN `tabForm Payment Entry Project` fpep ON fpep.name = br.parent WHERE fpep.budget = '{0}' AND br.docstatus = 1) br ON br.pos_rap = ba.pos_rap
        WHERE ba.parent = '{0}' AND ba.docstatus = 1
        """.format(budget), as_dict=1)
    return None

@frappe.whitelist()
def get_details_po(purchase_order = None):
    if purchase_order:
        return frappe.db.sql("""
        SELECT pr.name pos_rap, 1 duration, poi.qty volume, po.currency, poi.rate, poi.net_amount, poi.base_rate unit_price, poi.base_net_amount budget_amount, poi.expense_account account, poi.cost_center, poi.description FROM `tabPurchase Order Item` poi
        INNER JOIN `tabPurchase Order` po ON po.name = poi.parent
        LEFT JOIN `tabPOS RAP` pr ON pr.name = poi.item_code
        WHERE po.name = '{0}' AND po.docstatus = 1
        """.format(purchase_order), as_dict=1)
    return None

@frappe.whitelist()
def check_form_payment_entry_project(form_payment_entry_project = None):
    if form_payment_entry_project:
        return frappe.db.sql("""
        SELECT br.total_budget budget_amount, br.purpose FROM `tabForm Payment Entry Project` br
        WHERE br.name = '{0}' AND br.docstatus = 1
        """.format(form_payment_entry_project), as_dict=1)
    return None

@frappe.whitelist()
def check_form_payment_entry(form_payment_entry = None):
    if form_payment_entry:
        return frappe.db.sql("""
        SELECT br.total_budget budget_amount, br.purpose FROM `tabForm Payment Entry` br
        WHERE br.name = '{0}' AND br.docstatus = 1
        """.format(form_payment_entry), as_dict=1)
    return None

def get_permission_query_conditions(user):
	usr = frappe.db.sql("""SELECT * FROM `tabUser` where name = '{0}'""".format(frappe.session.user), as_dict=1)
	if usr and usr[0].role_profile_name == "Site Manager":
		return """(`tabForm Payment Entry Project`.project in (SELECT parent FROM `tabProject Team` WHERE user = '{0}'))""".format(frappe.session.user)
	else:
		return ""
      
@frappe.whitelist()
def get_detail(form_payment_entry_project):
      return frappe.db.sql("""SELECT * FROM `tabForm Payment Entry Account` WHERE parent = '{0}'""".format(form_payment_entry_project), as_dict=1)