import frappe
from a3sola_solar_management.attach_document import attach_pdf


def validate(doc,methods):
    if doc.project:
        doc.project_id=doc.project
        project = frappe.get_doc('Project',doc.project)
        doc.project_name=project.project_name
    if doc.project_id:
        if not doc.incentive_payable:
            if doc.payment_type=="Receive" and doc.party_type=='Customer':
                if doc.project:
                    todolist=frappe.get_all('ToDo',filters={'reference_name':doc.project,'reference_type':'Project','status':'Open'})

                    print(todolist)
                    print("tttt")
                    if todolist:
                        doc.incentive_payable.clear()
                        for i in todolist:
                            todo=frappe.db.get_value("ToDo", i['name'], "owner")
                            print(todo)
                            # todos=frappe.get_doc({"doctype":"ToDo",'name':i['name']})
                            # print(todos)
                            # print("^^^^^^^6")
                            # print(todos.name)
                            # print(todos.owner)
                            # print(todos.status)

                            doc.append("incentive_payable",{"user":todo})



    if doc.party_type=='Supplier':         
        supplier=frappe.get_doc('Supplier',doc.party)

       
        if supplier.is_installer:
            user=supplier.user
            doc.user=user

    if doc.party_type=='Customer':     
        customer=frappe.get_doc('Customer',doc.party)
 
        if customer.is_installer:
            user=customer.user
            doc.user=user

          



def on_submit(doc,methods):

    if doc.payment_type=="Pay":
        if doc.party_type=="Employee":
            employee=frappe.get_doc('Employee',doc.party)
            if employee.user:
                sharedoc = frappe.new_doc("DocShare")
                sharedoc.share_doctype='Payment Entry'
                sharedoc.share_name=doc.name
                    
                sharedoc.user=employee.user
                sharedoc.read=1
                sharedoc.write=0
                sharedoc.submit=0
                sharedoc.share=1
                sharedoc.notify=1
                sharedoc.save(ignore_permissions=True)


            
            


    if doc.project_id:
        if doc.incentive_payable and doc.payment_type=="Receive":
                doc.project_id=doc.project
                for i in doc.incentive_payable:
                    incentivelist=frappe.get_all('Track Incentive', filters={'Project_id': doc.project_id,'user':i.user})
                    print(incentivelist)


                    if incentivelist:

                        trackincentive=frappe.get_doc('Track Incentive', incentivelist[0]['name'])
                        trackincentive.allowed_incentive=trackincentive.allowed_incentive+i.incentive
                        trackincentive.unpaid=trackincentive.unpaid+i.incentive
                        inc="RS. "+str(i.incentive)+" Incentive Allowed"
                        trackincentive.append("log",{"date":frappe.utils.now(),"detail":inc})

                        trackincentive.save()


                    else:

                        trackincentive=frappe.new_doc("Track Incentive")
                        trackincentive.user=i.user
                        trackincentive.project_id=doc.project_id
                        trackincentive.allowed_incentive=i.incentive
                        trackincentive.unpaid=trackincentive.unpaid+i.incentive
                        inc="RS. "+str(i.incentive)+" Incentive Allowed"
                        trackincentive.append("log",{"date":frappe.utils.now(),"detail":inc})
                        trackincentive.save()


        if doc.payment_type=="Receive" and doc.party_type=='Customer':
            sales_orders=frappe.get_all('Sales Order', filters={'Project': doc.project,'docstatus':1})
            grand_total=0
            paid_amout=0
            if sales_orders:
                for i in sales_orders:
                    salesorder=frappe.get_doc('Sales Order',i['name'])
                    grand_total=grand_total+salesorder.rounded_total

            payment_entry=frappe.get_all('Payment Entry', filters={'Project': doc.project,'docstatus':1,'payment_type':'Receive','party_type':'Customer'})
            print(payment_entry)
            if payment_entry:
                 for i in payment_entry:
                    payment=frappe.get_doc('Payment Entry',i['name'])
                    paid_amout=paid_amout+payment.total_allocated_amount
            print(paid_amout)
            
            print("@@@@@@@@@@@@@@@@@@@@@@") 

            project = frappe.get_doc('Project',doc.project)

            if grand_total and paid_amout:
                half=grand_total/2
                print(half)
                
                if paid_amout==grand_total:
                    project.average_electricity_bill="Full Paid"
                elif paid_amout<half:
                    project.average_electricity_bill="Partially Paid"
                else:
                    project.average_electricity_bill="Half Paid"
            
                project.save()




        if doc.payment_type=="Pay" and doc.party_type=='Supplier':
            supplier=frappe.get_doc('Supplier',doc.party)
            if supplier.user:
                userid=supplier.user
                incentivelist=frappe.get_all('Track Incentive', filters={'Project_id': doc.project,'user':userid})
                if incentivelist:
                        trackincentive=frappe.get_doc('Track Incentive', incentivelist[0]['name'])


                        trackincentive.unpaid=trackincentive.unpaid-doc.paid_amount
                        trackincentive.paid=int(trackincentive.paid)+int(doc.paid_amount)
                        print(trackincentive.paid)
                        inc="RS. "+str(doc.paid_amount)+" Incentive Paid"
                        trackincentive.append("log",{"date":frappe.utils.now(),"detail":inc})
                        trackincentive.save()


                   
    if doc.party_type=='Supplier':         
        supplier=frappe.get_doc('Supplier',doc.party)

       
        if supplier.is_installer:
            if supplier.user:

                user_roles = frappe.get_roles(supplier.user)
                if user_roles:
                    for i in user_roles:
                        print(i)
                        if i=='Restricted':
                            user_permission = frappe.new_doc("User Permission")
                            user_permission.user=supplier.user
                            user_permission.allow='Payment Entry'
                            user_permission.for_value=doc.name
                            user_permission.save()

                sharedoc = frappe.new_doc("DocShare")
                sharedoc.share_doctype='Payment Entry'
                sharedoc.share_name=doc.name
                    
                sharedoc.user=supplier.user
                sharedoc.read=1
                sharedoc.write=0
                sharedoc.submit=0
                sharedoc.share=1
                sharedoc.notify=1

                sharedoc.save(ignore_permissions=True)
        

        if doc.party_type=='Customer':        
            customer=frappe.get_doc('customer',doc.party)

        
            if customer.is_installer:
                if customer.user:

                    user_roles = frappe.get_roles(customer.user)
                    if user_roles:
                        for i in user_roles:
                            print(i)
                            if i=='Restricted':
                                user_permission = frappe.new_doc("User Permission")
                                user_permission.user=supplier.user
                                user_permission.allow='Payment Entry'
                                user_permission.for_value=doc.name
                                user_permission.save()

                    sharedoc = frappe.new_doc("DocShare")
                    sharedoc.share_doctype='Payment Entry'
                    sharedoc.share_name=doc.name
                        
                    sharedoc.user=customer.user
                    sharedoc.read=1
                    sharedoc.write=0
                    sharedoc.submit=0
                    sharedoc.share=1
                    sharedoc.notify=1

                    sharedoc.save(ignore_permissions=True)





        if doc.payment_type=="Pay" and doc.party_type=='Customer':
            customer=frappe.get_doc('Customer',doc.party)
            if customer.is_installer:
                if customer.user:
                    userid=customer.user
                    incentivelist=frappe.get_all('Track Incentive', filters={'Project_id': doc.project,'user':userid})
                    if incentivelist:
                            trackincentive=frappe.get_doc('Track Incentive', incentivelist[0]['name'])


                            trackincentive.unpaid=trackincentive.unpaid-doc.paid_amount
                            trackincentive.paid=int(trackincentive.paid)+int(doc.paid_amount)
                            print(trackincentive.paid)
                            inc="RS. "+str(doc.paid_amount)+" Incentive Paid"
                            trackincentive.append("log",{"date":frappe.utils.now(),"detail":inc})
                            trackincentive.save()


def after_insert(doc,methods):
    print("afterrrrrrrrrrr")
    fileurl,url=attach_pdf(doc)
    doc.pdf_doc=fileurl
    doc.attachment_url=url
    doc.save()




@frappe.whitelist(allow_guest=True)
def before(doc):
    print("before")
    doc=frappe.get_doc("Payment Entry",doc)
    fileurl,url=attach_pdf(doc)
    doc.pdf_doc=fileurl
    doc.attachment_url=url
    print(doc.pdf_doc,"pdf_doc")
    doc.save()
   



@frappe.whitelist(allow_guest=True)
def incentive(pro,party,type):
        unpaid=0
        if type=="supplier":
            supplier=frappe.get_doc('Supplier',party)
            if supplier.user:
                userid=supplier.user

                print(userid)
                incentivelist=frappe.get_all('Track Incentive', filters={'Project_id': pro,'user':userid})
                if incentivelist:
                        trackincentive=frappe.get_doc('Track Incentive', incentivelist[0]['name'])

                        unpaid=trackincentive.unpaid


        
        if type=="customer":
            customer=frappe.get_doc('Customer',party)
            if customer.is_installer:
                if customer.user:
                    userid=customer.user

                
                    incentivelist=frappe.get_all('Track Incentive', filters={'Project_id': pro,'user':userid})
                    if incentivelist:
                            trackincentive=frappe.get_doc('Track Incentive', incentivelist[0]['name'])

                            unpaid=trackincentive.unpaid

        return unpaid
