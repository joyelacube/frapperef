# Copyright (c) 2022, Acube Innovations and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class EBInformation(Document):
	pass



@frappe.whitelist(allow_guest=True)
def test(doc,pro):
		print(doc,"hiiiii++++++++++++++++++++++++++++++++++++++++++++++")  
		print(pro)
		project = frappe.get_doc('Project',pro)

		print(project.primary_address)
		print(project.consumer_number)
		

		d={'cadd':project.primary_address,'customer':project.customer,'consno':project.consumer_number}

		
		print(d)
		return d
