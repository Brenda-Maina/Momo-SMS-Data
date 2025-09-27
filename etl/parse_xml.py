import xml.etree.ElementTree as ET
import json
import os

def parse_sms_xml(xml_file_path='data/raw/momo.xml'):
    """
    Parse the existing momo.xml file from the raw data folder
    """
    # Check if file exists first
    if not os.path.exists(xml_file_path):
        print(f" Error: File '{xml_file_path}' not found!")
        return []
    
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        transactions = []
        
        # Try different possible XML structures
        for sms in root.findall('.//sms'):  # Look for sms elements anywhere in XML
            transaction = {
                'id': len(transactions) + 1,
                'address': sms.get('address', ''),
                'body': sms.get('body', ''),
                'date': sms.get('date', ''),
                'type': sms.get('type', ''),
                'readable_date': sms.get('readable_date', ''),
                'contact_name': sms.get('contact_name', '')
            }
            transactions.append(transaction)
        
        # If no transactions found, try alternative XML structure
        if len(transactions) == 0:
            print(" No SMS elements found. Trying alternative XML structure...")
            
            # Look for any elements that might contain transaction data
            for element in root.findall('.//*'):
                if element.attrib:  # If element has attributes
                    transaction = {
                        'id': len(transactions) + 1,
                        'element_tag': element.tag,
                        **element.attrib  # Include all attributes
                    }
                    transactions.append(transaction)
        
        # Save for API use
        with open('data/processed/api_transactions.json', 'w') as f:
            json.dump(transactions, f, indent=2)
            
        print(f"Successfully parsed {len(transactions)} items from momo.xml!")
        
        # Show a sample of what was parsed
        if transactions:
            print(" Sample transaction:")
            print(json.dumps(transactions[0], indent=2))
            
        return transactions
        
    except ET.ParseError as e:
        print(f" Error parsing XML: {e}")
        return []
    except Exception as e:
        print(f" Unexpected error: {e}")
        return []

if __name__ == "__main__":
    parse_sms_xml()