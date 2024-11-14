import sys
import xml.etree.ElementTree as ET
import json

def create_root_reports(xml:str, manager_email:str):
    reports = []
    
    email = None
    emp_manager = None

    for employee in xml:
        for field in employee:
            if field.get('id') == 'email':
                email = field.text
            if field.get('id') == 'manager':
                emp_manager = field.text

        if emp_manager == manager_email:
            emp_dic = {'employee': {"email": email, "direct_reports": create_root_reports(xml, email) } }
            reports.append(emp_dic) 
            
            xml.remove(employee)

    return reports  

def save_to_json_file(data: dict):
    output_file = "output_json.json"
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"JSON data saved to {output_file}")              

def parseXmlToJson(xml:str):
    json_dic = {}

    email = None
    manager = None

    for employee in xml:
        for field in employee:
            if field.get('id') == 'email':
                email = field.text
            if field.get('id') == 'manager':
                manager = field.text
                if field.text == None:
                    break 
        if email and manager == None:
            json_dic['employee'] = {'email': email, 'direct_reports': [] }
            xml.remove(employee)
            break       

    dic_reps = create_root_reports(xml, email)
    json_dic['employee']['direct_reports'].extend(dic_reps)

    save_to_json_file(json_dic)    

def main():
    xml_file = sys.argv[1]
   
    xml = ET.parse(xml_file)
    xml_root = xml.getroot()
        
    parseXmlToJson(xml_root)  
   

if __name__ == '__main__':
    main()
