import frappe

def validate(doc,methods):
    marked_attendance=0

    att=frappe.get_list("Attendance",filters={'attendance_date': doc.date,'employee': doc.employee},order_by='name asc')
    for i in att:
        att=frappe.get_doc("Attendance",i)
        print(att.docstatus)
        if att.docstatus!=2: 
            marked_attendance=i

    if marked_attendance:
        attendance=frappe.get_doc("Attendance",marked_attendance)

        doc.attendance=attendance.name
     
        



