import frappe
from frappe.utils import now,add_to_date


def validate(doc,methods):
    if doc.reference_type=="Task":
        task=frappe.get_doc("Task",doc.reference_name)
        if task.project:
            project=frappe.get_doc("Project",task.project)
            if task.payment_dependence=='Fully Paid':
                if project.average_electricity_bill=='Fully Paid':
                    pass
                else:
                    frappe.throw("Project is not fully paid")
            elif task.payment_dependence=='Half Paid':
                if project.average_electricity_bill=='Half Paid' or project.average_electricity_bill=='Fully Paid':
                    pass
                else:
                    frappe.throw("Project is not half paid")
            elif task.payment_dependence=='Partially Paid':
                if project.average_electricity_bill=='Partially Paid' or project.average_electricity_bill=='Half Paid' or project.average_electricity_bill=='Fully Paid':
                    pass
                else:
                    frappe.throw("Project is not partially paid")
            else:
                pass
        
            
        

def after_insert(doc,methods):

    if doc.reference_type=="Lead":
        ld=frappe.get_doc("Lead",doc.reference_name)
        print(ld)
        ld.contact_by=doc.owner
        print(ld.contact_by)
        ld.save()

    


    if doc.reference_type=="Opportunity":
        opp=frappe.get_doc("Opportunity",doc.reference_name)
        print(opp)
        opp.contact_by=doc.owner


        print(opp.contact_by)
        toadydate=now()

        opp.contact_date=add_to_date(toadydate, years=0, months=0, weeks=0, days=3)
        opp.send_notification=1
        

     
        
        opp.save()


    if doc.reference_type!="Track Incentive":
        sharedoc = frappe.new_doc("DocShare")
        sharedoc.share_doctype=doc.reference_type
        sharedoc.share_name=doc.reference_name


        
        sharedoc.user=doc.owner
        sharedoc.read=1
        sharedoc.write=1
        sharedoc.submit=0
        sharedoc.share=1
        sharedoc.notify=1

        sharedoc.save(ignore_permissions=True)
    else:
        
        sharedoc = frappe.new_doc("DocShare")
        sharedoc.share_doctype=doc.reference_type
        sharedoc.share_name=doc.reference_name

        
        sharedoc.user=doc.owner
        sharedoc.read=1
        sharedoc.write=0
        sharedoc.submit=0
        sharedoc.share=1
        sharedoc.notify=1

        sharedoc.save(ignore_permissions=True)



    if doc.reference_type=="Project":
       
        user_roles = frappe.get_roles(doc.owner)
        if user_roles:
            for i in user_roles:
                print(i)
                if i=='Restricted':
                   user_permission = frappe.new_doc("User Permission")
                   user_permission.user=doc.owner
                   user_permission.allow='Project'
                   user_permission.for_value=doc.reference_name
                   user_permission.save()

    if doc.reference_type=="Task":
    
        user_roles = frappe.get_roles(doc.owner)
        if user_roles:
            for i in user_roles:
                print(i)
                if i=='Restricted':
                    user_permission = frappe.new_doc("User Permission")
                    user_permission.user=doc.owner
                    user_permission.allow='Task'
                    user_permission.for_value=doc.reference_name
                    user_permission.save()


    

         
