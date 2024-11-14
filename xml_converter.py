import sys
import xml.etree.ElementTree as ET
import json

def create_root_reports(xml: str, manager_email: str):
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
            emp_dic = {
                'employee': {
                        "email": email,
                        "direct_reports": create_root_reports(xml, email) 
                    } 
                }
            reports.append(emp_dic) 
            xml.remove(employee)

    return reports  

def save_to_json_file(data: dict, json_file:str):
    output_file = json_file if json_file != None else "output_json.json"

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return (f"JSON data saved to {output_file}")              

def parseXmlToJson(xml_root: str, json_file: str):
    json_dic = {}
    email = None
    manager = None

    for employee in xml_root:
        for field in employee:
            if field.get('id') == 'email':
                email = field.text
            if field.get('id') == 'manager':
                manager = field.text
                if field.text == None:
                    break 
        if email and manager == None:
            json_dic['employee'] = {'email': email, 'direct_reports': [] }
            xml_root.remove(employee)
            break       

    dic_reps = create_root_reports(xml_root, email)
    json_dic['employee']['direct_reports'].extend(dic_reps)

    return save_to_json_file(json_dic, json_file)    

def main():
    usage = """
    Usage: *python xml_converter.py [xml_file.xml] [json_file.json]*

    Arguments:
    - `xml_converter.py`: Path to the python file.
    - `xml_file.xml`: Path to the xml file.
    - `json_file.json`: Path to the json file (optional)
"""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        return usage    

    xml_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        xml = ET.parse(xml_file)
        xml_root = xml.getroot()
    except ET.ParseError:
        return "Error with parsing."
    except Exception as error:
        return (f"Error: {error}") 
     
    return parseXmlToJson(xml_root, json_file)  
   
if __name__ == '__main__':
   print(main())
