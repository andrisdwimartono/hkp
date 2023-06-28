# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class SubContractWeeklyProgress(Document):
	pass
	
	# def validate(self):
	# 	d1 = datetime.strptime("{0}-01-01".format(datetime.now().year), "%Y-%m-%d")
	# 	d2 = datetime.strptime(self.posting_date, "%Y-%m-%d")
	# 	monday1 = (d1 - timedelta(days=d1.weekday()))
	# 	monday2 = (d2 - timedelta(days=d2.weekday()))

	# 	self.week = (monday2 - monday1).days / 7

@frappe.whitelist()
def check_week(posting_date = None):
	d1 = datetime.strptime("{0}-01-01".format(datetime.now().year), "%Y-%m-%d")
	d2 = datetime.strptime(posting_date, "%Y-%m-%d")
	monday1 = (d1 - timedelta(days=d1.weekday()))
	monday2 = (d2 - timedelta(days=d2.weekday()))

	week = (monday2 - monday1).days / 7
	return week

@frappe.whitelist()
def check_last_week(sub_contract_hand_over = None, week = None):
    if sub_contract_hand_over and week:
        return frappe.db.sql("""
       	SELECT b.*, e.tot_vol_this_week FROM `tabSub Contract Weekly Progress Detail` b
        INNER JOIN (SELECT * FROM `tabSub Contract Weekly Progress` a 
        WHERE a.sub_contract_hand_over = '{0}' AND a.week < '{1}'
        ORDER BY a.week desc
        LIMIT 1) c ON c.name = b.parent
        LEFT JOIN (SELECT  e.job_detail, SUM(e.vol_this_week) tot_vol_this_week FROM `tabSub Contract Weekly Progress Detail` e
			INNER JOIN (SELECT * FROM `tabSub Contract Weekly Progress` f 
			WHERE f.sub_contract_hand_over = '{0}' AND f.week <= '{1}') f ON f.name = e.parent
            GROUP BY e.job_detail) e ON e.job_detail = b.job_detail
        ORDER BY b.idx
        """.format(sub_contract_hand_over, week), as_dict=1)
    return None