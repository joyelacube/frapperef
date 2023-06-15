
import email
import frappe
import re
# To access the method externally from javascript



 


@frappe.whitelist(allow_guest=True)
# when values of an existing document is updated,call update function with arguments(doc,val,with-items,qn) from client script.
def on_update(doc,val,with_items,qn):
    # Check whether opportunity created with current lead name.
    if not frappe.db.exists({"Opportunity",doc}):
        # Returns lead document
        ld=frappe.get_doc("Lead",doc)
        #Create new opportunity
        opp = frappe.new_doc("Opportunity")
        # Set the value opportunity_from to "Lead"
        opp.opportunity_from = "Lead"
        #Update lead field in opportunity with name of current lead.
        opp.lead = ld.name
        # Update contact_person field in opportunity with lead name.
        opp.contact_person=ld.lead_name
        #Update email id and party_name
        opp.contact_email=ld.email_id
        opp.taluk=ld.taluk
        opp.district=ld.district
        opp.source=ld.ld_source
        opp.taluk_name=ld.taluk_name
        opp.district_name=ld.district_name

        # address=""
        # if ld.address_title:
        #     address=address+ld.address_title+"\n"
        # if ld.address_line1:
        #     address=address+ld.address_line1+"\n"
        # if ld.address_line2:
        #     address=address+ld.address_line2+"\n"
        # if ld.city:
        #     address=address+"\n"+ld.city
        # if ld.state and ld.county:
        #     address=address+"\n"+ld.state+", "+ld.county
        #     print(address)
        # address=address+ld.address_title+"\n"+ld.address_line1+"\n"+ld.address_line2+"\n"+ld.city

        item=frappe.get_doc("Item",val)

        if item.scheme_name:
            scheme=frappe.get_doc("Scheme",item.scheme_name)
            print(scheme)

        if item.scheme_name:
            ld.scheme_name=item.scheme_name

            if scheme.provided_by:
                ld.board_name=scheme.provided_by
            if scheme.subsidy_percentage:
                ld.subsidy_percent=scheme.subsidy_percentage
            if scheme.category:
                ld.category=scheme.category
        ld.save()


        if ld.category:
            opp.category=ld.category

        if ld.address_title:
                opp.append("address_list",{"address":ld.address_title,"address_line_1":ld.address_line1,"address_line_2":ld.address_line2,"city":ld.city,"state":ld.state,"country":ld.country})

        elif ld.address_link:
            addr= frappe.get_doc("Address",ld.address_link)
            print(addr)
            opp.append("address_list",{"address":addr.address_title,"address_line_1":addr.address_line1,"address_line_2":addr.address_line2,"city":addr.city,"state":addr.state,"country":addr.country})
            print("he")

        if ld.number_to_be_contacted:
            if ld.email_id:

                opp.append("contact_list",{"contact_number":ld.number_to_be_contacted,"email_id":ld.email_id})


        opp.party_name=ld.name
        opp.from_lead=1
        if ld.whatsapp_number:
            opp.whatsapp_number=ld.whatsapp_number
        #Set the with_items field in opportunity to 1
        opp.with_items=int(with_items)
        #qn=1
       #Check whether with_items field is checked
        if opp.with_items==1:
        #print(val["Item"])
        # Fetch items from dialog box variable in client script and add to child table
            opp.append("items",{"item_code":val,"qty":qn})





        # item=frappe.get_doc("Item",val)
        # print(item,"212423563")
        # if item.scheme_name:
        #     scheme=frappe.get_doc("Scheme",item.scheme_name)
        #     print(scheme)
        #     opp.scheme_name=item.scheme_name
        #     print(opp.scheme_name)
        #     opp.board_name=scheme.provided_by
        #  Insert all fields before saving.
        opp.insert()

        frappe.msgprint('Opportunity ' f'<a href="/app/opportunity/{opp.name}" target="blank">{opp.name} </a> Created Successfully ')


    else:
        pass

def validate(doc,methods):
    # if not doc.email_id and not doc.number_to_be_contacted  and not doc.aadhaar_number:
    #     frappe.throw("Please Enter Your Email ID,Mobile Number and Aadhaar Number ")

    # crm= frappe.get_doc("CRM Settings")
    # frappe.msgprint(crm.aml)
    # frappe.throw("y")
    crm=frappe.get_doc("CRM Settings")
    if crm.notify_escalation_manager==1:
        if crm.escalation_mannager_for_lead:
            print(crm.escalation_mannager_for_lead,"#################")
            doc.escalation_manager=crm.escalation_mannager_for_lead
            doc.enot=1
    else:
        doc.enot=0
    if crm.send_customer_notiication==1:
        doc.cnot=1
    else:
        doc.cnot=0

    print("ray")
    print(crm.aml)

    if crm.consumer_number_mandatory==1:
        if not doc.consumer_number:
            frappe.throw("Please Fill Consumer Number ")
    if crm.aml==1:
        if not doc.aadhaar_number:
            frappe.throw("Please Fill Aadhaar Number ")

    if  doc.email_id:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, doc.email_id)):
            pass
        else:
            frappe.throw("Please Check Your Email ID")

    if crm.contact_number_validation==1:
        if doc.number_to_be_contacted:
            r=re.fullmatch('[6-9][0-9]{9}',doc.number_to_be_contacted)
            if r!=None:
                pass

            else:
                frappe.throw("Please Check Your Mobile Number ")
    if doc.consumer_number:
        c=re.fullmatch('[0-9]{13}',doc.consumer_number)
        if c!=None:
            pass
        else:
            frappe.throw("Please Check Your Consumer Number")
    if doc.aadhaar_number:
        a=re.fullmatch('[0-9]{12}',doc.aadhaar_number)
        if a!=None:
            pass
        else:
            frappe.throw("Please Check Your Aadhaar Number")
    

@frappe.whitelist(allow_guest=True)
def aftersavefetch(ld):
    ld=frappe.get_doc("Lead",ld)


    if ld.emi_customer:
         crm=frappe.get_doc("CRM Settings")
         if crm.emi_follow_up_user:

            
            if not frappe.db.exists({"doctype":"ToDo","owner": crm.emi_follow_up_user,"reference_type":"Lead","reference_name":ld.name,'Status':'Open'}):
                ld.follow_up_user=crm.emi_follow_up_user
                todo = frappe.new_doc("ToDo")
                todo.owner = crm.emi_follow_up_user
                todo.description = "Lead Assignment"
                todo.reference_type = "Lead"
                todo.reference_name = ld.name
                todo.assigned_by = frappe.session.user
                todo.save()
                
            

    else:
        crm=frappe.get_doc("CRM Settings")
        if crm.emi_follow_up_user:
             if not frappe.db.exists({"doctype":"ToDo","owner": crm.default_follow_up_user,"reference_type":"Lead","reference_name":ld.name,'Status':'Open'}):
                ld.follow_up_user=crm.default_follow_up_user
                todo = frappe.new_doc("ToDo")
                todo.owner = crm.default_follow_up_user
                todo.description = "Lead Assignment"
                todo.reference_type = "Lead"
                todo.reference_name = ld.name
                todo.assigned_by = frappe.session.user
                todo.save()


             


             

    
   

def before_insert(doc,methods):
    tp=''
    template_id=''
    smst=frappe.get_doc("SMS Template General")
    if smst:
        if smst.template_parameter:
            tp=smst.template_parameter
        if smst.sms_template:
            for i in smst.sms_template:
                if i.document=='Lead':
                    template_id=i.template_id


    if tp and template_id:
        
        sms=frappe.get_doc("SMS Settings")
        if sms:
            for i in sms.parameters:
                print(i)
                print(i.parameter)
                if i.parameter==tp:
                    i.value=template_id      
            sms.save()
   
    



@frappe.whitelist(allow_guest=True)
def call(doc,num):
#   frappe.msgprint("<a href=tel:frm.doc.number_to_be_contacted>frm.doc.number_to_be_contacted</a>")
  frappe.msgprint('Click the number to call ' f'<a href=tel:"{num}">{num} </a>')



# # Check whether opportunity created with current lead name.
# @frappe.whitelist(allow_guest=True)
# def create_opp(doc):
#     if not frappe.db.exists("Opportunity",doc):
#         # Get details of lead
#         ld=frappe.get_doc("Lead",doc)
#         #Create new opportunity
#         opp = frappe.new_doc("Opportunity")
#         # Update fields in opportunity
#         opp.opportunity_from = "Lead"
#         opp.lead = ld.name
#         if ld.lead_address:
#             for c in ld.lead_address:
#                 opp.append("address_list",{"address":c.address,"address_line_1":c.address_line_1,"address_line_2":c.address_line_2,"city":c.city,"state":c.state,"country":c.country,"is_primary":c.is_primary})

#         if ld.lead_contact:
#             for c in ld.lead_contact:
#                 opp.append("contact_list",{"contact_number":c.contact_number,"email_id":c.email_id,"is_primary":c.is_primary})
#         # opp.contact_person=ld.lead_name
#         opp.email_id=ld.email_id
#         opp.party_name=ld.name
#         opp.from_lead=1
#         opp.insert()

    # else:
    #     frappe.throw("Opportunity Already Exist")
# def after_insert(doc,events):

#     primary_add = []
#     if len(doc.lead_address)>0:
#         for con in doc.lead_address:
#             if con.is_primary == 1:
#                 if len(primary_add)>0:
#                     frappe.throw("You can only add one Primary Address.")
#                 else:
#                     primary_add.append(con)
#             con.save()
# def after_insert(doc,methods):
#     address=frappe.get_doc("Address",doc.name)
#     if address.links:
#         for lin in address.links:
#             lin.link_doctype="Lead"
#             lin.link_name=doc.lead_name
#     address.save()
# #     doc.contact_by=ld.owner
#     ld.save()
#     # pr_cn=[]
    #if len(doc.lead_contact)>0:
        # for co in doc.lead_contact:
        #     if co.is_primary==1:
        #         pr_cn.append(co)
        #         if len(pr_cn)>1:
        #             frappe.throw("You can Add Only One Primary Contact")
        #             print(pr_cn)
        #         else:
        #             contact=frappe.get_list("Contact")

    #for row in contact:

                # if con.links:
                        #     for lin in con.links:
                        #         if lin.link_doctype=="Lead" and lin.link_name==doc.name:
                        #             for c in doc.lead_contact:
                        #                 if c.email_id:
                        #                     con.append("email_ids",{"email_id":c.email_id})
                        #                 if c.contact_number:
                        #                     con.append("phone_nos",{"phone":c.contact_number})
                        #             con.insert()
                        #             con.reload()
                        #             frappe.msgprint("Primary Contact Added")



    # if doc.lead_contact:
    #     contact=frappe.get_list("Contact")
    #     for row in contact:
    #         con=frappe.get_doc("Contact",row)
    #         #print(con,"hellooo",contact)
    #         if con.links:
    #             for lin in con.links:
    #                 if lin.link_doctype=="Lead" and lin.link_name==doc.name:
    #                     for c in doc.lead_contact:
    #                         if c.email_id:
    #                             con.append("email_ids",{"email_id":c.email_id})
    #                         if c.contact_number:
    #                             con.append("phone_nos",{"phone":c.contact_number})
    #                         con.save()
    #                 frappe.msgprint(con,"Success")





    # if doc.lead_contact:
    #     contact=frappe.get_list("Contact")
    #     for row in contact:
    #         con=frappe.get_doc("Contact",row.doc)
    #         print(row.doc)
    #         for lin in con.links:
    #             if lin.link_doctype=="Lead" and lin.link_name==doc.name:
    #                     for c in doc.lead_contact:
    #                         con.append("phone_nos", {"phone": c.contact_number})
    #                         print(c.contact_number)
    #                         print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    #                     con.insert()
