# Copyright (c) 2022, Acube Innovations and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WarrantyReport(Document):
	pass



@frappe.whitelist(allow_guest=True)
def test(doc,pro):

		project = frappe.get_doc('Project',pro)



		d={'customer':project.customer,'it':project.item_name}

		if frappe.db.exists("Sales Invoice",{"project":pro}):
			si=frappe.get_doc("Sales Invoice",{"project":pro})


			# return frappe.db.sql(f"""SELECT *  FROM tabCustomer WHERE opportunity_name='CRM-OPP-2022-00002'""",as_dict=True)
			print(d)
			print(si.name)

			d['si']=si.name
		else:
			d['si']=""



		return d
