# Copyright (c) 2022, Acube Innovations and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
import frappe
from frappe.utils import date_diff


class ScheduleInstallation(Document):
	def validate(doc):
		if doc.installation_scheduled_on:
			protasks=frappe.get_list("Task",{"project": doc.project_id,"doctypes_name":"Installation Report"})
			# if protasks:
			# 	tas=frappe.get_doc("Task",protasks[0])
			# 	tas.exp_start_date=doc.installation_scheduled_on
			# 	date1=datetime.strptime(tas.exp_start_date, "%Y/%m/%d")
			# 	date2=datetime.strptime(tas.exp_end_date, "%Y/%m/%d")
			#
			# 	print(tas.exp_start_date)
			# 	delta = (date2 - date1)
			# 	print(f'Difference is {delta.days} days')
			# 	date=delta.days
			# 	print(date)
			# 	frappe.throw("haii")
			#
			#
			# 	tas.save()
			# #



@frappe.whitelist(allow_guest=True)
def test(doc,pro):
		print(doc,"hiiiii++++++++++++++++++++++++++++++++++++++++++++++")
		print(pro)
		project = frappe.get_doc('Project',pro)

		print(project.primary_address)
		print(project.customer)
		protasks=frappe.get_list("Task",{"project": pro,"doctypes_name":"Installation Report"})
		if protasks:
			tas=frappe.get_doc("Task",protasks[0])
			print(tas)
			tas=tas.name





		d={'cadd':project.primary_address,'customer':project.customer,'item':project.item_name}

		# return frappe.db.sql(f"""SELECT *  FROM tabCustomer WHERE opportunity_name='CRM-OPP-2022-00002'""",as_dict=True)
		print(d)
		d['tas']=tas
		return d
