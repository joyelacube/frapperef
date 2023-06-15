import frappe

def validate(doc,methods):

    doc.project=doc.project_id


def on_submit(doc,methods):
    if doc.project_id:
        
        protasks=frappe.get_list("Task",filters={"project": doc.project_id},order_by='name asc')
        for i in protasks:
            task=frappe.get_doc("Task",i)
            task.sales_invoice=doc.name
            # if task.doctypes_name=="Sales Invoice":
        
            #     task.d_id=doc.name
            task.save()
            print(task.sales_invoice)

    if doc.items:
        da=0
        journal=0
        for row in doc.items:
            if row.item_code:
                item=frappe.get_doc("Item",row.item_code)
                print(item)
                if item.scheme_name:
                    scheme=frappe.get_doc("Scheme",item.scheme_name)
                    print(scheme)

                    if scheme.subsidy_paid_to=="Installer":
                        rs=scheme.receivable_account
                        ia=scheme.income_account
                        print(scheme)
                        da=da+row.discount_amount
                        print(da)
                        journal=1
        if journal==1:
            je=frappe.new_doc("Journal Entry")
            je.append("accounts",{"account":rs,"party_type":"Customer","party":scheme.provided_by,"debit_in_account_currency":da})
            je.append("accounts",{"account":ia,"credit_in_account_currency":da})
            je.user_remark="Created against "+ doc.name
            je.save()
            je.submit()
            frappe.msgprint('Journal Entry ' f'<a href="/app/journal-entry/{je.name}" target="blank">{je.name} </a> Submitted Successfully ')
