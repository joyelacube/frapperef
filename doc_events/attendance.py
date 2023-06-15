import frappe
import re
from frappe.utils import today
from datetime import datetime,timedelta


#validation for mobile number
@frappe.whitelist(allow_guest=True)
def test(att):

    
    doc=frappe.get_doc("Attendance",att)


    today_checkin=frappe.get_list("Employee Checkin",filters={"employee":doc.employee,"date":today()},order_by='name asc')
    if len(today_checkin)>2:
        last_check_in= frappe.get_doc("Employee Checkin",today_checkin[-1])
        first_check_in= frappe.get_doc("Employee Checkin",today_checkin[0])

        in_time=str(first_check_in.time)
        in_time=in_time.split(" ")
        in_time=in_time[1]
        
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5")
        print(first_check_in.time)
        out_time=str(last_check_in.time)
        out_time=out_time.split(" ")
        out_time=out_time[1]
        print(in_time)
        print(out_time)
        return in_time,out_time
    else:
        return "no","no"
    
       
       