import frappe
from frappe.utils import add_to_date
import datetime
from frappe.utils import add_days, flt, get_datetime, get_time, get_url, nowtime, today
from frappe import _
from erpnext.projects.doctype.project.project import Project
import random
import hashlib
import re
# def validate(doc,methods):
#     # settings=frappe.get_doc("Projects Settings")
#     # if settings.template_details:
#     #     for tem in settings.template_details:
#     #         if doc.expected_start_date:
#     #             (doc.expected_end_date)=tem.duration+getdate(doc.expected_start_date)
#     #         doc.save()
#     # customer=frappe.db.sql(f"""SELECT *  FROM tabCustomer WHERE opportunity_name='CRM-OPP-2022-00002'""",as_dict=True)
#     # customer = frappe.get_doc('Customer',{'opportunity_name':'CRM-OPP-2022-00002'})

#     customer = frappe.get_doc("Customer", {"opportunity_name": doc.opportunity})
#     print(customer)
#     print("$$$$$$$$$$$$$$4")
#     # print(type(customer))
#     # print(customer[0].customer_name)

#     doc.customer=customer.customer_name
#     doc.address=customer.customer_primary_address
#     doc.contact=customer.customer_primary_contact
#     # doc.insert()

class Projectc(Project):

#Override existing class
    def send_welcome_email(self):

        url = get_url("/project/?name={0}".format(self.name))
        messages = (
            _("Hey Dude! You have been invited to collaborate on the project: {0}").format(self.name),
            url,
            _("Join"),
        )

        content = """
        <p>{0}.</p>
        <p><a href="{1}">{2}</a></p>
        """

        for user in self.users:
            if user.welcome_email_sent == 0:
                frappe.sendmail(
                    user.user, subject=_("Project Collaboration Invitation"), content=content.format(*messages)
                )
                user.welcome_email_sent = 1


@frappe.whitelist(allow_guest=True)
def test(doc,op):
    oppo=frappe.get_doc("Opportunity",op)
    ad=""
    if oppo.aadhaar_number:
            ad=oppo.aadhaar_number
    print(doc)
    l=frappe.get_list("Project")
    if l:
        last=frappe.get_last_doc("Project")
    else:
        last=""
    # last=frappe.get_last_doc('Project')
    d={}

    print(last)
    if oppo.items:
        for row in oppo.items:
            itm=row.item_code
            print(itm)
            item=frappe.get_doc("Item",row.item_code)
            print(item)
            if item.scheme_name:
                scheme=frappe.get_doc("Scheme",item.scheme_name)
                sch=item.scheme_name
                brd=scheme.provided_by
                print(sch)
                print(brd)
                # if oppo.scheme_name==item.scheme_name:
                if scheme.project_template:
                    template=scheme.project_template


                if scheme.subsidy_percentage:
                    sub=scheme.subsidy_percentage
                
                if scheme.subsidy_amount:
                    sub=scheme.subsidy_amount


                if scheme.category:
                    cat=scheme.category


                    print(cat)
            else:
                template=""
                cat=""
                sub=""
                sch=""
                brd=""


    else:
        pass

    # settings=frappe.get_doc("Project Settings")
    # if settings.template_details:
    #         for tem in settings.template_details:
    #             if doc.expected_start_date:
    #                 print(doc)
    #                 end=add_to_date((doc.expected_start_date),days=tem.duration,as_string=True)

    customer = frappe.get_doc("Customer", oppo.customer)
    # customer = frappe.get_doc('Customer',{'opportunity_name':'CRM-OPP-2022-00002'})
    print(customer.customer_primary_address)
    address=""
    if customer.customer_primary_address:
        primaryaddress=frappe.get_doc("Address",customer.customer_primary_address )
        address=""
        address=address+str(primaryaddress.address_line1)+"\n"+str(primaryaddress.address_line2)
        if primaryaddress.city and primaryaddress.pincode:
            address=address+"\n"+str(primaryaddress.city)+", "+str(primaryaddress.pincode)
        print(address)
        if primaryaddress.state and primaryaddress.county:
            address=address+"\n"+str(primaryaddress.state)+", "+str(primaryaddress.county)
        # last=frappe.get_last_doc('Project')
    oppo=frappe.get_doc("Opportunity",op)
    if oppo.contact_number:
        ccon=oppo.contact_number
    else:
        ccon=""

    l=frappe.get_list("Project")
    if l:
        last=frappe.get_last_doc("Project")
    else:
        last=""
    if oppo.items:
        for row in oppo.items:
            itm=row.item_code
            print(itm)

    if last:
        projectname=last.project_name

        s=""
        for i in reversed(projectname):
            print(i)
            if i=="-":
                break
            else:
                s=s+i
        print(s)


        # splited=projectname.split('-')
        # number=splited[2]

        number=s[::-1]

        if number.isdigit():
            print(number)
            nextid=int(number)+1
            print("+++++++++++++++++++")
            print(nextid)
        else:
            nextid="1000"

    else:
        nextid="1000"
    print(customer.customer_name)
    pr=customer.customer_name+"-"+str(itm)+"-"+str(nextid)
    print(pr,"??????????????????????????????????????????")
    print(cat,"######################")

    d={'aad':ad,'ct':cat,'sp':sub,'pn':pr,'sc':sch,'bd':brd,'tm':template,'cadd':customer.customer_primary_address,'ccon':ccon,'customer':customer.customer_name,'padd':address,'email':customer.email_id}
    print(d)

    return d


@frappe.whitelist(allow_guest=True)
def enddate(scheme_name,sdate):
    print("^^^^^^^^^^^^^^^^^^^^^")
    print(sdate)
    print(type(sdate))
    curdate=datetime.date.today()




    sdate=datetime.datetime.strptime(sdate, '%Y-%m-%d').date()

    if sdate<curdate:
        frappe.throw("Expected Date Can not be In Past")

    print(type(sdate))
    end=""
    settings=frappe.get_doc("Project Settings")
    if settings.template_details:
            template_details=settings.template_details
            for tem in template_details:
                if tem.scheme:
                    if scheme_name:
                        if scheme_name==tem.scheme:
                            print(tem.duration)
                            template=frappe.get_doc("Project Template",tem.select_template)
                            dura=0
                            for i in template.tasks:
                                if i.starting_day:
                                    dura=i.starting_day


                            duration=max(int(tem.duration),int(dura))
                            print(duration)
                            print(tem.board)
                            end=add_to_date((sdate),days=duration,as_string=True)
                            print("Heloo")
                            print(end)
                else:
                    end=""

    return end



def after_insert(doc,methods):

    # range_start=10**(10-1)


    # range_end=(10**10)-1

    # ran=random.randint(range_start,range_end)

    # num=doc.name+str(ran)

    # result = hashlib.sha1(num.encode())

    # print(result.hexdigest())

    # tracking_id=result.hexdigest()

    # doc.tracking_id=tracking_id
    # url=frappe.utils.get_url()

    # url=str(url)+"/show?id="+str(tracking_id)
    # print(url,"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    # doc.url=url
    # doc.save()

    if doc.oppertunity:
        oppo=frappe.get_doc("Opportunity",doc.oppertunity)

        print(oppo.party_name)
        oppo.project_name=doc.project_name
        doc.url=oppo.url
        doc.tracking_id=oppo.tracking_id
        doc.shorten_url=oppo.shorten_url
        doc.save()
        oppo.project_id=doc.name
        oppo.date_of_converted=frappe.utils.nowdate()
        oppo.status="Converted"
        oppo.save()
        if frappe.db.exists("Quotation",{"party_name":oppo.party_name}):
            qua=frappe.get_doc("Quotation",{"party_name":oppo.party_name})
            print(qua)
            print(qua.docstatus)
            if qua.docstatus==0:

                qua.project_id=doc.name

            qua.save()

        if frappe.db.exists("Site Survey",{"opportunity":oppo.name}):
            ss=frappe.get_doc("Site Survey",{"opportunity":oppo.name})
            print(ss)
            print(ss.docstatus)
            
            ss.project_id=doc.name

            ss.save()

 


def before_insert(doc,methods):
    tp=''
    template_id=''
    smst=frappe.get_doc("SMS Template General")
    if smst:
        if smst.template_parameter:
            tp=smst.template_parameter
        if smst.sms_template:
            for i in smst.sms_template:
                if i.document=='Project':
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
   



def validate(doc,methods):

    if doc.oppertunity:
        oppo=frappe.get_doc("Opportunity",doc.oppertunity)
        print("%%%%%%%%%%%%%%%%")
        if oppo.aadhaar_number==None and oppo.consumer_number==None:
            frappe.throw("Please Enter Aadhaar Number and Consumer Number in Opportunity")
        elif oppo.aadhaar_number==None:
            frappe.throw("Please Enter Aadhaar Number in Opportunity")
        elif oppo.consumer_number== None:
            frappe.throw("Please Enter Consumer Number in Opportunity")


        

       
    if doc.base_document=="Completion Report":
        

        
        
        cr=frappe.get_doc("Completion Report",{"project_id":doc.name})
        # if cr.consumer_name:
           
        #     doc.consumer_name=cr.consumer_name
          
		
        if cr.installed_plant_capacity:
            
            
            panel_capacity=str(cr.installed_plant_capacity)
            doc.panel_capacity=int(re.search(r'\d+', panel_capacity).group())
            print(doc.panel_capacity)



        if cr.serial_no:
            
            doc.serial_no.clear()
            count=0
            for i in cr.serial_no:
                    print(count)
                    doc.append("serial_no",{"spv_module_make":i.spv_module_make,"each_module_watts":i.each_module_watts,"spv_module_type":i.spv_module_type,"spv_serial_no":i.spv_serial_no,"no_of_modules":i.no_of_modules})

                    if count==0:
                        
                        doc.capacity_in_watts=i.each_module_watts   
                        doc.panel_make=i.spv_module_make
                        doc.panel_type=i.spv_module_type

                    count=count+1
            print(count)   
            capacity_in_watts=str(doc.capacity_in_watts)

            capacity_in_watts=int(re.search(r'\d+', capacity_in_watts).group())
            doc.capacity_in_watts=capacity_in_watts
            doc.number_of_panels=count
            doc.total_capacity=count*int(doc.capacity_in_watts) 

        if cr.inverter_serial_no:
            count=0
            doc.inverter_serial_no.clear()
            for i in cr.inverter_serial_no:
                if count==0:
                    doc.inverter_capacity=int(re.search(r'\d+', i.capacity_of_inverter).group())
                doc.append("inverter_serial_no",{"make":i.make,"capacity_of_inverter":i.capacity_of_inverter,"inverter_serial_no":i.inverter_serial_no})
                count=count+1
    else:
            cr=frappe.db.exists("Completion Report",{"project_id":doc.name})
            if cr:        
                cr=frappe.get_doc("Completion Report",{"project_id":doc.name})
                cr.save()
 
 
    if doc.base_document=='Module Capacity':
       
        
        
        mc=frappe.get_doc('Module Capacity',{"project_id":doc.name})
        if mc.panel_capacity:
          
            panel_capacity=str(mc.panel_capacity)
            doc.panel_capacity=int(re.search(r'\d+', panel_capacity).group())
            print(doc.panel_capacity)
            

        if mc.serial_no:
            count=0
            doc.serial_no.clear()
            
            for i in mc.serial_no:
                if count==0:
                    doc.capacity_in_watts=i.each_module_watts   
                    doc.panel_make=i.spv_module_make
                    doc.panel_type=i.spv_module_type
                count=count+1
                  
                doc.append("serial_no",{"spv_module_make":i.spv_module_make,"each_module_watts":i.each_module_watts,"spv_module_type":i.spv_module_type,"spv_serial_no":i.spv_serial_no,"no_of_modules":i.no_of_modules})
            doc.number_of_panels=count
            capacity_in_watts=str(doc.capacity_in_watts)

            capacity_in_watts=int(re.search(r'\d+', capacity_in_watts).group())
            doc.capacity_in_watts=capacity_in_watts
            doc.total_capacity=count*int(doc.capacity_in_watts)      
        
        if mc.inverter_serial_no:
            count=0
            doc.inverter_serial_no.clear()
            for i in mc.inverter_serial_no:
                if count==0:
                    
                    doc.inverter_capacity=int(re.search(r'\d+', i.capacity_of_inverter).group())
                doc.append("inverter_serial_no",{"make":i.make,"capacity_of_inverter":i.capacity_of_inverter,"inverter_serial_no":i.inverter_serial_no})
                count=count+1
    else:
        print(doc.name)
        
        
        mc=frappe.db.exists("Module Capacity",{"project_id":doc.name})
     
        if mc: 
                 
            mc=frappe.get_doc("Module Capacity",{"project_id":doc.name})
          
            mc.save()

    dcr=frappe.db.exists("DCR Declaration",{"project_id":doc.name})
	
    if dcr:
        
        dc=frappe.get_doc("DCR Declaration",{"project_id":doc.name})
        dc.save()



    # if doc.base_document==None or doc.base_document=='' :
    
    #     completion_report=frappe.db.exists("Completion Report",{"project_id":doc.name})
        

    #     if completion_report:
    #         print(doc.name)
            


    #         cr=frappe.get_doc("Completion Report",{"project_id":doc.name})
            
    #         if cr.serial_no and cr.inverter_serial_no:
    #             doc.base_document='Completion Report'
    #             print("%%%%%%%%%%,doc.base_document","^^^66")
    #             print(doc.base_document)
                
             
            
                  

    #             # if doc.base_document=='':
    #             #      doc.base_document='Completion Report'

    #             # print(id(cr.serial_no))

    #             # print(id(doc.serial_no))
    #             # crs=[]
    #             # prs=[]
    #             # for i in cr.serial_no:
    #             #     crs=crs+[i.spv_module_make]+[i.each_module_watts]+[i.spv_module_type]+[i.spv_serial_no]+[i.no_of_modules]
    #             # for i in doc.serial_no:
    #             #     prs=prs+[i.spv_module_make]+[i.each_module_watts]+[i.spv_module_type]+[i.spv_serial_no]+[i.no_of_modules]
    #             # cri=[]
    #             # pri=[]
    #             # for i in cr.inverter_serial_no:
    #             #     cri=cri+[i.make]+[i.capacity_of_inverter]+[i.inverter_serial_no]
    #             # for i in doc.inverter_serial_no:
    #             #     pri=pri+[i.make]+[i.capacity_of_inverter]+[i.inverter_serial_no]

    #             # print(crs)
    #             # print(prs)
    #             # if crs==prs and cri==pri:
    #             #     pass
    #             # else:
    #             if cr.serial_no:
    #                 doc.serial_no.clear()
    #                 for i in cr.serial_no:
    #                         doc.append("serial_no",{"spv_module_make":i.spv_module_make,"each_module_watts":i.each_module_watts,"spv_module_type":i.spv_module_type,"spv_serial_no":i.spv_serial_no,"no_of_modules":i.no_of_modules})
    #             if cr.inverter_serial_no:
    #                 doc.inverter_serial_no.clear()
    #                 for i in cr.inverter_serial_no:
    #                     doc.append("inverter_serial_no",{"make":i.make,"capacity_of_inverter":i.capacity_of_inverter,"inverter_serial_no":i.inverter_serial_no})

        # else:
        #     cr.save()
        

    
    if doc.status=="Cancelled":
        protasks=frappe.get_list("Task",filters={"project": doc.name},order_by='name asc')
        print(protasks)
        complete=1
        for i in protasks:
           task=frappe.get_doc("Task",i)
           task.status="Cancelled"
           task.save()
    


    # doc.add_comment('Comment',text="Test Comment")
    print(type(doc.percent_complete))
    print(doc.percent_complete)

    if doc.percent_complete==100.00:
        doc.pstatus="Project Completed"


    set=frappe.get_doc("Project Settings")
    if set.automate_project_assignment==1:
        if set.project_users:
            doc.users.clear()
            for us in set.project_users:
                print(us.user,"*************")
                doc.append("users",{"user":us.user,"full_name":us.full_name,"view_attachments":us.view_attachments,"welcome_email_sent":us.welcome_email_sent,"email":us.email})



    if not doc.scheme_name and not doc.tracking_id:
        l=frappe.get_list("Project")
        if l:
            last=frappe.get_last_doc("Project")
        else:
            last=""

        if last:
            projectname=last.project_name

            s=""
            for i in reversed(projectname):
                print(i)
                if i=="-":
                    break
                else:
                    s=s+i
            print(s)


            # splited=projectname.split('-')
            # number=splited[2]

            number=s[::-1]

            if number.isdigit():
                print(number)
                nextid=int(number)+1

                print(nextid)
            else:
                nextid="1000"

        else:
            nextid="1000"

        doc.project_name=doc.project_name+"-"+str(nextid)
        print(doc.project_name)



@frappe.whitelist(allow_guest=True)
def aftersavefetch(pro):
    pass
    
    # pr=frappe.get_doc("Project",pro)
    # if pr.base_document=="Completion Report":
    #     pass
    # else:
        
#         cr=frappe.db.exists("Completion Report",{"project_id":pro})
#         if cr:        
#             cr=frappe.get_doc("Completion Report",{"project_id":pro})
#             cr.save()
#     if pr.base_document=="Module Capsity":
#         pass
#     else:

#         mc=frappe.db.exists("Module Capsity",{"project_id":pro})
#         if mc:        
#             mc=frappe.get_doc("Module Capsity",{"project_id":pro})
#             mc.save()

    # ModuleCapacity=frappe.db.exists("Module Capacity",{"project_id":pro})
    # if ModuleCapacity:
    #     mc=frappe.get_doc("Module Capacity",{"project_id":pro})
    #     mc.save()
    # dcr=frappe.db.exists("DCR Declaration",{"project_id":pro})
    # print(dcr)
    # if dcr:
    #     dc=frappe.get_doc("DCR Declaration",{"project_id":pro})
    #     dc.save()

    # d_of_work=frappe.db.exists("Details of Work",{"project_id":pro})
    # print(d_of_work)
    # if d_of_work:
    #     dw=frappe.get_doc("Details of Work",{"project_id":pro})
    #     dw.save()
    # print(pro)

   
    #     if cr.serial_no and cr.inverter_serial_no:
            
    #         print(id(cr.serial_no))
    #         print(id(pr.serial_no))
    #         crs=[]
    #         prs=[]
    #         for i in cr.serial_no:
    #             crs=crs+[i.spv_module_make]+[i.each_module_watts]+[i.spv_module_type]+[i.spv_serial_no]+[i.no_of_modules]
    #         for i in pr.serial_no:
    #             prs=prs+[i.spv_module_make]+[i.each_module_watts]+[i.spv_module_type]+[i.spv_serial_no]+[i.no_of_modules]
    #         cri=[]
    #         pri=[]
    #         for i in cr.inverter_serial_no:
    #             cri=cri+[i.make]+[i.capacity_of_inverter]+[i.inverter_serial_no]
    #         for i in pr.inverter_serial_no:
    #             pri=pri+[i.make]+[i.capacity_of_inverter]+[i.inverter_serial_no]

    #         print(crs)
    #         print(prs)
            
    #         if crs==prs and cri==pri:
    #             print("same")
    #             pass
    #         else:
    #              print("differnt")
    #              cr.save()
    #     else:
    #          cr.save()


		
	
		
	






# def validate(doc,methods):
#     print(doc)
#     if not doc.scheme:
#         if not doc.from_template:
#             frappe.throw("Please Choose a template")
    # else:
    #     last=frappe.get_last_doc('Project')
    #     if last:
    #         projectname=last.project_name
    #         splited=projectname.split('-')
    #         number=splited[1]
    #         nextid=int(number)+1
    #         print("+++++++++++++++++++")
    #         print(nextid)
    #     else:
    #         nextid="1000"
    #     pr=customer.customer_name+"-"+itm+str(nextid)
    #     d={'pn':pr,'sc':sch,'bd':brd,'tm':template,'cadd':'','ccon':'','customer':customer.customer_name,'padd':'','email':''}

    # return frappe.db.sql(f"""SELECT *  FROM tabCustomer WHERE opportunity_name='CRM-OPP-2022-00002'""",as_dict=True)


# frappe.msgprint('Project ' f'<a href="/app/project/{self.name}" target="blank">{self.name} </a> Created Successfully ')

