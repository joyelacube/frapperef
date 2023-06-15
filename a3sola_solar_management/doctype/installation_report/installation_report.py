# Copyright (c) 2022, Acube Innovations and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document

class InstallationReport(Document):
	pass



@frappe.whitelist(allow_guest=True)
def test(doc,pro):

		project = frappe.get_doc('Project',pro)

		print(project.primary_address)
		print(project.customer)
		



		d={'cadd':project.address,'customer':project.customer,'consumer':project.consumer_number,'con':project.contact_number,'em':project.email,'item':project.item_name}
		if frappe.db.exists("Site Information",{"project_id":pro}):
			si=frappe.get_doc("Site Information",{"project_id":pro})
			if si.latitude:
				d['lat']=si.latitude
			else:
				d['lat']=""
			if si.longitude:
				d['lon']=si.longitude
			else:
				d['lon']=""
			if si.type_of_roof:
				d['roof']=si.type_of_roof
			else:
				d['roof']=""
		if frappe.db.exists("Schedule Installation",{"project_id":pro}):
					schedule=frappe.get_doc("Schedule Installation",{"project_id":pro})
					print("@@@@@@@@@@@@@@@@@@@@@@@",schedule)
					if schedule.installation_scheduled_on:
						
						d['in']=schedule.installation_scheduled_on
					else:
						d['in']=""
		# return frappe.db.sql(f"""SELECT *  FROM tabCustomer WHERE opportunity_name='CRM-OPP-2022-00002'""",as_dict=True)
		print(d)
		return d
