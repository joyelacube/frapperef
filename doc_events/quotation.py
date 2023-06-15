import frappe
from a3sola_solar_management.attach_document import attach_pdf


# def on_update(doc, methods):
#     if doc.pdf_url:
#         getfile=frappe.get_doc("File",{"file_url":doc.pdf_url})
#         res = getfile.name
#         print(res,"ghjklkjhgghjkkjhgghjkjhhjjhghjjhghjjhfk")
#         frappe.db.delete("File",res)
#         fallback_language = frappe.db.get_single_value("System Settings", "language") or "en"
#         args = {
#             "doctype": doc.doctype,
#             "name": doc.name,
#             "title": doc.get_title(),
#             "lang": getattr(doc, "language", fallback_language),
#             "show_progress": 0
#         }
#         fileurl = execute(**args)
#         doc.pdf_url = fileurl

#         attachments = frappe.get_all("File", filters={"attached_to_doctype":doc.doctype, "attached_to_name":doc.name}, fields=["name", "file_url"])
#         for attachment in attachments:
#             if attachment["file_url"] != fileurl:
#                 attach = get_doc("File", attachment["name"])
#                 attach.delete()



def on_submit(doc,methods):

    if doc.project_id:
        protasks=frappe.get_list("Task",filters={"project": doc.project_id},order_by='name asc')
        for i in protasks:
            task=frappe.get_doc("Task",i)
            task.quotation=doc.name
            if task.doctypes_name=="Quotation":
                task.d_id=doc.name
                task.status="Completed"

                frappe.msgprint('Quotation Task Completed" ' f'<a href="/app/task/{task.name}" target="blank">{task.name} </a> ')
            task.save()


            print(task.quotation)
            # attach_pdf(doc)




def after_insert(doc,methods):
    print("afterrrrrrrrrrr")
    fileurl,url=attach_pdf(doc)
    doc.pdf_doc=fileurl
    doc.attachment_url=url




    if not doc.quoation_print_specification:
        bundle=''
        for i in doc.items:
            item=frappe.get_doc("Item",i.item_code)
            if item.scheme_name:
                bundle=item.name
    

        if bundle:
            if frappe.db.exists("Quotation Print Specification",bundle):
                priqu=frappe.get_doc("Quotation Print Specification",bundle)
                doc.quoation_print_specification=priqu.name
               
                for i in priqu.system_specification:
                   
                    doc.append("system_specification",{"item":i.item,"specification":i.specification,"qty":i.qty,"make":i.make,"warranty_period":i.warranty_period})
                 
                for i in priqu.other_attachment:
                    doc.append("quotation_print_images",{"order_number":i.order_number,"attachment":i.attachment})

                produc_bundle=frappe.get_doc("Product Bundle",bundle)

                for i in produc_bundle.items:
                    if i.print_on_quotation:
                   
                        doc.append("system_specification",{"item":i.item_code,"specification":i.description,"qty":i.qty,"make":i.make,"warranty_period":i.warranty_period})
                 


                doc.save()




        
    doc.save()


def validate(doc,methods):
    pass
    # if not doc.quoation_print_specification:
    #     bundle=''
    #     for i in doc.items:
    #         item=frappe.get_doc("Item",i.item_code)
    #         if item.scheme_name:
    #             bundle=item.name
    

    #     if bundle:
    #         priqu=frappe.get_doc("Quoation Print Specification",bundle)
    #         doc.quoation_print_specification=priqu.name

    #     doc.save()



    


# @frappe.whitelist(allow_guest=True)
# def before(doc):
#     print("beforeeeeeeeeeeeeee")
   
#     doc=frappe.get_doc("Quotation",doc)
#     fileurl,url=attach_pdf(doc)
#     doc.pdf_doc=fileurl
#     doc.attachment_url=url
#     print(doc.pdf_doc,"pdf_doc")
#     doc.save()
   



# def onupdate(doc,methods):
  
#     on_update(doc,methods)



# To access externally




@frappe.whitelist(allow_guest=True)
def test(doc,pro):
    print(doc,"hiiiii++++++++++++++++++++++++++++++++++++++++++++++")
    print(pro)
    project = frappe.get_doc('Project',pro)


    d={'cadd':project.address,'customer':project.customer,'opp':project.oppertunity,'consno':project.consumer_number,'roof':project.type_of_roof,'consno:':project.consumer_number}

    # return frappe.db.sql(f"""SELECT *  FROM tabCustomer WHERE opportunity_name='CRM-OPP-2022-00002'""",as_dict=True)
    # print(d)
    return d