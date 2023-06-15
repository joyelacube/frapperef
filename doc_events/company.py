import frappe
import re
#validation for mobile number
def validate(doc,methods):
    if doc.phone:
        r=re.fullmatch('[6-9][0-9]{9}',doc.phone)
        if r!=None: 
            pass
        
        else:
            frappe.throw("Please Enter a Valid Phone number ")
    if  doc.support_mail_:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, doc.support_mail_)):
            pass
        else:
            frappe.throw("Please Check Your Email ID")
