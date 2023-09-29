# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.hr.apifacerecognition import get_transaction
from datetime import datetime
from frappe.utils import (
	time_diff_in_seconds,
)

class TarikDataAbsensi(Document):
	def validate(self):
		self.set("ringkasan_absensi_karyawan", [])
		if len(self.ringkasan_absensi_karyawan) <= 0:
			for e in frappe.db.sql("""SELECT * FROM `tabEmployee` e""", as_dict=1):
				self.append("ringkasan_absensi_karyawan", {
					"employee": e.name,
					"employee_name": e.employee_name,
					"emp_code": e.emp_code
				})
		map_emp_code = {}
		if len(self.ringkasan_absensi_karyawan) > 0:
			for d in self.ringkasan_absensi_karyawan:
				map_emp_code[d.emp_code] = [d.employee, d.employee_name]
		if self.start_date and self.end_date and len(self.ringkasan_absensi_karyawan) > 0:
			transactions = get_transaction(self.start_date, self.end_date)
			for t in transactions:
				emp = None
				if str(t["emp_code"]) in map_emp_code:
					emp = map_emp_code[str(t["emp_code"])]
					if t["punch_state"] == "Check In" and not frappe.db.sql("""SELECT * FROM `tabAttendance` WHERE emoloyee = '{0}' AND attendance_date = '{1}' AND docstatus != 2""".format(emp[0], t["att_date"]), as_dict=1):
						self.append("absences",{
							"employee": emp[0],
							"employee_name": emp[1],
							"attendance_date": t["att_date"],
							"attendance_time": t["punch_time"],
							"status": "Present"
						})
				self.append("detail_data_absensi", {
					"employee": emp[0] if emp else None,
					"employee_name": emp[1] if emp else None,
					"emp_code": t["emp_code"],
					"id": t["id"],
					"att_date": t["att_date"],
					"punch_time": t["punch_time"],
					"punch_state": t["punch_state"],
					"verify_type": t["verify_type"],
					"source": t["source"]
				})

		if len(self.absences) > 0 and len(self.detail_data_absensi) > 0:
			for d in self.absences:
				for k in self.ringkasan_absensi_karyawan:
					if k.employee == d.employee:
						k.total_kehadiran = k.total_kehadiran+1
				for e in self.detail_data_absensi:
					if e.punch_state == "Check Out" and d.employee == e.employee and d.attendance_date == e.att_date:
						d.leave_time = e.punch_time
						s1 = datetime.strptime(d.attendance_time, '%H:%M')
						s2 = datetime.strptime(d.leave_time, '%H:%M')
						delta = time_diff_in_seconds(d.leave_time, d.attendance_time)
						d.working_hours = float(delta/3600)
		
	def on_submit(self):
		for d in self.absences:
			attendance_doc = frappe.get_doc({
				"doctype": "Attendance",
				"employee": d.employee,
				"employee_name": d.employee_name,
				"working_hours": d.working_hours,
				"status": "Present",
				"attendance_date": d.attendance_date,
				"attendance_time": d.attendance_time,
				"leave_time": d.leave_time
			})
			attendance_doc.save()
			attendance_doc.submit()