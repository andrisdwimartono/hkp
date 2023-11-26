# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	today,
)

class PengajuanPersonilLapangan(Document):
	def validate(self):
		if self.workflow_state == "Disetujui":
			for d in self.detail:
				if d.employee and self.project:
					project_doc = frappe.get_doc("Project", self.project)
					project_doc.append("project_team", {
						"designation": d.designation,
						"employee": d.employee,
						"employee_name": d.employee_name,
						"user": d.user
					})
					project_doc.save(ignore_permissions=True)

@frappe.whitelist()
def get_history(employee):
	es = frappe.db.sql("""
					SELECT pt.*, p.project_name FROM `tabProject Team` pt 
					  INNER JOIN `tabProject` p ON p.name = pt.parent
					  INNER JOIN `tabEmployee` e ON e.name = pt.employee
					  WHERE pt.employee = '{0}'
					ORDER BY p.name DESC""".format(employee), as_dict=1)
	if es:
		msg = """<h3>Pengalaman Proyek</h3>
				<table border=1 width="100%">
				  	<thead class="text-center">
				  	<tr>
				  		<td rowspan=2 width="6%">No</td>
				  		<td colspan=3 width="94%">Proyek</td>
				  	</tr>
				  	<tr>
				  		<td width="15%">Kode</td>
				  		<td width="59%">Nama</td>
				  		<td width="20%">Jabatan</td>
				  	</tr>
				  </thead>
				  <tbody style="padding-left: 2px !important; padding-right: 2px !important;">
			"""
		no = 0
		for e in es:
			no = no+1
			msg = msg+"""
					<tr>
				   		<td class="text-center">{0}</td>
						<td class="text-center">{1}</td>
						<td>{2}</td>
						<td class="text-center">{3}</td>
				   	</tr>
			""".format(no, e.parent, e.project_name, e.designation)
	if es:
		msg = msg+"""</tbody></table>"""
		frappe.msgprint(msg)
	
	es = frappe.db.sql("""
					SELECT pt.*, date_format(pt.date_end, "%d-%m-%Y") de FROM `tabEmployee Certificate` pt
					  INNER JOIN `tabEmployee` e ON e.name = pt.parent
					  WHERE e.name = '{0}' AND pt.date_end >= '{1}'
					ORDER BY pt.date_end DESC""".format(employee, today()), as_dict=1)
	if es:
		msg = """<h3>Sertifikat</h3>
				<table border=1 width="100%">
				  	<thead class="text-center">
				  	<tr>
				  		<td width="6%">No</td>
				  		<td width="20%">Institution</td>
				  		<td width="55%">Sertifikat</td>
				  		<td width="20%">Berlaku</td>
				  	</tr>
				  </thead>
				  <tbody style="padding-left: 2px !important; padding-right: 2px !important;">
			"""
		no = 0
		for e in es:
			no = no+1
			msg = msg+"""
					<tr>
				   		<td class="text-center">{0}</td>
						<td class="text-center">{1}</td>
						<td>{2}</td>
						<td class="text-right">{3}</td>
				   	</tr>
			""".format(no, e.institution, e.certificate, e.de)
	if es:
		msg = msg+"""</tbody></table>"""
		frappe.msgprint(msg)