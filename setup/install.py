from __future__ import print_function, unicode_literals

import frappe
from erpnext.accounts.doctype.cash_flow_mapper.default_cash_flow_mapper import DEFAULT_MAPPERS

from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import add_all_roles_to
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

default_mail_footer = """<div style="padding: 7px; text-align: right; color: #888"><small>Sent via
	<a style="color: #888" href="http://erpnext.org">ERPNext</a></div>"""


def after_install():
    frappe.get_doc({'doctype': "Task Type", "name": "Site Survey"}).insert()
    frappe.get_doc({'doctype': "Task Type", "name": "Delivery Note"}).insert()
    tl=frappe.get_list("Task Type")
    print("Haii")
    for i in tl:
        tt=frappe.get_doc({'doctype': "Task Type", "name": i.name})
        
        taskname=tt.name
        if taskname=="Site Survey" or taskname=="Delivery Note":
            pass
        else:
            frappe.get_doc({'doctype': "Task Type", "name": taskname}).insert()



# tl=frappe.get_list("Task Type")
# for i in tl:
#     t=frappe.get_doc({'doctype': "Task Type", "name": i.name})
#     tname=t.name
#     print(t.name)

	