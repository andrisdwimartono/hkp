# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
import json

class SubContractWeeklyProgress(Document):
	def validate(self):
		lists = frappe.db.sql("""SELECT * FROM `tabSub Contract Weekly Progress` a
			WHERE a.week > '{0}' AND a.sub_contract_hand_over = '{1}'""".format(self.week, self.sub_contract_hand_over), as_dict=1)
		for li in lists:
			last_week = int(li.week or 0)-1
			dts = frappe.db.sql("""SELECT b.name, h.volume_cumulative_last_week FROM `tabSub Contract Weekly Progress` a
				INNER JOIN `tabSub Contract Weekly Progress Detail` b ON b.parent = a.name
				LEFT JOIN (SELECT g.job_detail, SUM(g.vol_this_week) volume_cumulative_last_week FROM `tabSub Contract Weekly Progress` f
					INNER JOIN `tabSub Contract Weekly Progress Detail` g ON g.parent = f.name
					WHERE f.week <= '{2}' AND f.sub_contract_hand_over = '{1}'
					GROUP BY g.job_detail
					) h ON h.job_detail = b.job_detail
				WHERE a.name = '{3}'""".format(li.week, li.sub_contract_hand_over, last_week, li.name), as_dict=1)
			for dt in dts:
				frappe.db.sql("""UPDATE `tabSub Contract Weekly Progress Detail` 
				SET volume_cumulative_last_week = '{1}'
				WHERE name = '{0}'""".format(dt.name, dt.volume_cumulative_last_week))
	
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

@frappe.whitelist()
def get_sub_contract_weekly_progress(week, sub_contract_hand_over):
	if sub_contract_hand_over and week:
		return frappe.db.sql("""
       	SELECT * FROM `tabSub Contract Weekly Progress` WHERE week = '{0}' AND sub_contract_hand_over = '{1}'
        """.format(week, sub_contract_hand_over), as_dict=1)
	return None

@frappe.whitelist()
def get_sub_contract_weekly_progress_detail(week, sub_contract_hand_over):
	if sub_contract_hand_over and week:
		last_week = int(week)-1
		a = frappe.db.sql("""
       	SELECT b.name, b.job_detail, b.uom, b.volume, b.weight, e.vol_next_week_plan volume_plan_from_last_week, b.vol_next_week_plan, h.volume_cumulative_last_week, b.vol_this_week, k.volume_cumulative_thist_week, 0 deviasi FROM `tabSub Contract Weekly Progress` a
		INNER JOIN `tabSub Contract Weekly Progress Detail` b ON b.parent = a.name
		LEFT JOIN (SELECT d.* FROM `tabSub Contract Weekly Progress` c
			INNER JOIN `tabSub Contract Weekly Progress Detail` d ON d.parent = c.name
			WHERE c.week = '{2}' AND c.sub_contract_hand_over = '{1}'
			GROUP BY d.job_detail
			) e ON e.job_detail = b.job_detail
		LEFT JOIN (SELECT g.job_detail, SUM(g.vol_this_week) volume_cumulative_last_week FROM `tabSub Contract Weekly Progress` f
			INNER JOIN `tabSub Contract Weekly Progress Detail` g ON g.parent = f.name
			WHERE f.week <= '{2}' AND f.sub_contract_hand_over = '{1}'
			GROUP BY g.job_detail
			) h ON h.job_detail = b.job_detail
		LEFT JOIN (SELECT j.job_detail, SUM(j.vol_this_week) volume_cumulative_thist_week FROM `tabSub Contract Weekly Progress` i
			INNER JOIN `tabSub Contract Weekly Progress Detail` j ON j.parent = i.name
			WHERE i.week <= '{0}' AND i.sub_contract_hand_over = '{1}'
			GROUP BY j.job_detail
			) k ON k.job_detail = b.job_detail
		WHERE a.week = '{0}' AND a.sub_contract_hand_over = '{1}'
        """.format(week, sub_contract_hand_over, last_week), as_dict=1)
		if a:
			return a
		else:
			return frappe.db.sql("""
			SELECT b.job_detail, b.uom, b.volume, b.weight, b.vol_next_week_plan volume_plan_from_last_week, 0 vol_next_week_plan, h.volume_cumulative_last_week, 0 vol_this_week, k.volume_cumulative_thist_week, 0 deviasi FROM `tabSub Contract Weekly Progress` a
			INNER JOIN `tabSub Contract Weekly Progress Detail` b ON b.parent = a.name
			LEFT JOIN (SELECT g.job_detail, SUM(g.vol_this_week) volume_cumulative_last_week FROM `tabSub Contract Weekly Progress` f
				INNER JOIN `tabSub Contract Weekly Progress Detail` g ON g.parent = f.name
				WHERE f.week <= '{2}' AND f.sub_contract_hand_over = '{1}'
				GROUP BY g.job_detail
				) h ON h.job_detail = b.job_detail
			LEFT JOIN (SELECT j.job_detail, SUM(j.vol_this_week) volume_cumulative_thist_week FROM `tabSub Contract Weekly Progress` i
				INNER JOIN `tabSub Contract Weekly Progress Detail` j ON j.parent = i.name
				WHERE i.week <= '{0}' AND i.sub_contract_hand_over = '{1}'
				GROUP BY j.job_detail
				) k ON k.job_detail = b.job_detail
			WHERE a.week = '{2}' AND a.sub_contract_hand_over = '{1}'
			""".format(week, sub_contract_hand_over, last_week), as_dict=1)
	return None

@frappe.whitelist()
def saving(name, sub_contract_hand_over, project, sub_contract, job_name, posting_date, week, contractor_name, project_name, pic_name, budget_amount, sub_contract_weekly_progress, sub_contract_weekly_progress_last_week, sub_contract_weekly_progress_detail):
	aaa = json.loads(sub_contract_weekly_progress_detail)
	nm = check_is_exist(name, sub_contract_hand_over, project, sub_contract, job_name, posting_date, week, contractor_name, project_name, pic_name, budget_amount, sub_contract_weekly_progress, sub_contract_weekly_progress_last_week, sub_contract_weekly_progress_detail)
	if nm:
		scwp = frappe.get_doc("Sub Contract Weekly Progress", nm)
		scwp.sub_contract_hand_over = sub_contract_hand_over
		scwp.project = project
		scwp.sub_contract = sub_contract
		scwp.job_name = job_name
		scwp.posting_date = posting_date
		scwp.week = week
		scwp.contractor_name = contractor_name
		scwp.project_name = project_name
		scwp.pic_name = pic_name
		scwp.budget_amount = budget_amount
		
		# for scwpd in scwp.sub_contract_weekly_progress_detail:
			# frappe.delete_doc("Sub Contract Weekly Progress Detail", scwpd.name)
		for n in aaa:
			if n["namex"] and 'new-sub-contract-weekly-progress-detail' not in n["namex"]:
				for xd in scwp.sub_contract_weekly_progress_detail:
					if xd.name == n["namex"]:
						xd.idx = n["idx"]
						xd.job_detail = n["job_detail"]
						xd.uom = n["uom"]
						xd.volume = n["volume"]
						xd.weight = n["weight"]
						xd.volume_plan_from_last_week = n["volume_plan_from_last_week"]
						xd.vol_next_week_plan = n["vol_next_week_plan"]
						xd.volume_cumulative_last_week = n["volume_cumulative_last_week"]
						xd.vol_this_week = n["vol_this_week"]
						xd.volume_cumulative_thist_week = n["volume_cumulative_thist_week"]
						xd.deviasi = n["deviasi"]
			else:
				scwp.append("sub_contract_weekly_progress_detail", {
					"idx": n["idx"],
					"job_detail": n["job_detail"],
					"uom": n["uom"],
					"volume": n["volume"],
					"weight": n["weight"],
					"volume_plan_from_last_week": n["volume_plan_from_last_week"],
					"vol_next_week_plan": n["vol_next_week_plan"],
					"volume_cumulative_last_week": n["volume_cumulative_last_week"],
					"vol_this_week": n["vol_this_week"],
					"volume_cumulative_thist_week": n["volume_cumulative_thist_week"],
					"deviasi": n["deviasi"]
				})
		scwp.save()

		return scwp.name
	else:
		scwp = frappe.get_doc({
			"doctype": "Sub Contract Weekly Progress",
			"sub_contract_hand_over": sub_contract_hand_over,
			"project": project,
			"sub_contract": sub_contract,
			"job_name": job_name,
			"posting_date": posting_date,
			"week": week,
			"contractor_name": contractor_name,
			"project_name": project_name,
			"pic_name": pic_name,
			"budget_amount": budget_amount,
		})
		
		for n in aaa:
			scwp.append("sub_contract_weekly_progress_detail", {
				"job_detail": n["job_detail"],
				"uom": n["uom"],
				"volume": n["volume"],
				"weight": n["weight"],
				"volume_plan_from_last_week": n["volume_plan_from_last_week"],
				"vol_next_week_plan": n["vol_next_week_plan"],
				"volume_cumulative_last_week": n["volume_cumulative_last_week"],
				"vol_this_week": n["vol_this_week"],
				"volume_cumulative_thist_week": n["volume_cumulative_thist_week"],
				"deviasi": n["deviasi"]
			})
		scwp.insert(ignore_permissions=True)
		return scwp.name

@frappe.whitelist()
def get_sub_contract_weekly_progress_detail2(week, sub_contract_hand_over):
	if sub_contract_hand_over and week:
		last_week = int(week)-1
		a = frappe.db.sql("""
       	SELECT b.name, b.job_detail, b.obstacle, b.analysis, b.resolve, b.pic, b.resolve_target, b.document FROM `tabSub Contract Weekly Progress` a
		INNER JOIN `tabSub Contract Weekly Progress Detail` b ON b.parent = a.name
		WHERE a.week = '{0}' AND a.sub_contract_hand_over = '{1}'
        """.format(week, sub_contract_hand_over, last_week), as_dict=1)
		if a:
			return a
		else:
			return frappe.db.sql("""
			SELECT b.job_detail, b.obstacle, b.analysis, b.resolve, b.pic, b.resolve_target, b.document FROM `tabSub Contract Weekly Progress` a
			INNER JOIN `tabSub Contract Weekly Progress Detail` b ON b.parent = a.name
			WHERE a.week = '{2}' AND a.sub_contract_hand_over = '{1}'
			""".format(week, sub_contract_hand_over, last_week), as_dict=1)
	return None

@frappe.whitelist()
def saving2(name, sub_contract_hand_over, project, sub_contract, job_name, posting_date, week, contractor_name, project_name, pic_name, budget_amount, sub_contract_weekly_progress, sub_contract_weekly_progress_last_week, sub_contract_weekly_progress_detail):
	aaa = json.loads(sub_contract_weekly_progress_detail)
	nm = check_is_exist(name, sub_contract_hand_over, project, sub_contract, job_name, posting_date, week, contractor_name, project_name, pic_name, budget_amount, sub_contract_weekly_progress, sub_contract_weekly_progress_last_week, sub_contract_weekly_progress_detail)
	if nm:
		scwp = frappe.get_doc("Sub Contract Weekly Progress", nm)
		scwp.sub_contract_hand_over = sub_contract_hand_over
		scwp.project = project
		scwp.sub_contract = sub_contract
		scwp.job_name = job_name
		scwp.posting_date = posting_date
		scwp.week = week
		scwp.contractor_name = contractor_name
		scwp.project_name = project_name
		scwp.pic_name = pic_name
		scwp.budget_amount = budget_amount
		
		# for scwpd in scwp.sub_contract_weekly_progress_detail:
		# 	frappe.delete_doc("Sub Contract Weekly Progress Detail", scwpd.name)
		for n in aaa:
			if n["namex"] and 'new-sub-contract-weekly-progress-detail' not in n["namex"]:
				for xd in scwp.sub_contract_weekly_progress_detail:
					if xd.name == n["namex"]:
						xd.idx = n["idx"]
						xd.job_detail = n["job_detail"]
						xd.obstacle = n["obstacle"]
						xd.analysis = n["analysis"]
						xd.resolve = n["resolve"]
						xd.pic = n["pic"]
						xd.resolve_target = n["resolve_target"]
						xd.document = n["document"]
			else:
				scwp.append("sub_contract_weekly_progress_detail", {
					"idx": n["idx"],
					"job_detail": n["job_detail"],
					"obstacle": n["obstacle"],
					"analysis": n["analysis"],
					"resolve": n["resolve"],
					"pic": n["pic"],
					"resolve_target": n["resolve_target"],
					"document": n["document"]
				})
		scwp.save()

		return scwp.name
	else:
		scwp = frappe.get_doc({
			"doctype": "Sub Contract Weekly Progress",
			"sub_contract_hand_over": sub_contract_hand_over,
			"project": project,
			"sub_contract": sub_contract,
			"job_name": job_name,
			"posting_date": posting_date,
			"week": week,
			"contractor_name": contractor_name,
			"project_name": project_name,
			"pic_name": pic_name,
			"budget_amount": budget_amount,
		})
		
		for n in aaa:
			scwp.append("sub_contract_weekly_progress_detail", {
				"job_detail": n["job_detail"],
				"obstacle": n["obstacle"],
				"analysis": n["analysis"],
				"resolve": n["resolve"],
				"pic": n["pic"],
				"resolve_target": n["resolve_target"],
				"document": n["document"]
			})
		scwp.insert(ignore_permissions=True)
		return scwp.name

def check_is_exist(name, sub_contract_hand_over, project, sub_contract, job_name, posting_date, week, contractor_name, project_name, pic_name, budget_amount, sub_contract_weekly_progress, sub_contract_weekly_progress_last_week, sub_contract_weekly_progress_detail):
	aa = frappe.db.sql("""
	SELECT * FROM `tabSub Contract Weekly Progress` a 
	WHERE a.week = '{0}' AND a.sub_contract_hand_over = '{1}'""".format(week, sub_contract_hand_over), as_dict=1)
	if aa:
		return aa[0].name
	else:
		return None
	