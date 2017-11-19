import re

class PropertyCreator(type):
    
    def __new__(cls, name, bases, attrs):

        properties = dict()
        
        def add_property(pr_name, pr_type, pr_body):
            if (properties.get(pr_name) == None):
                properties[pr_name] = {}
            properties[pr_name][pr_type] = pr_body
        
        for attr_name, attr_body in attrs.items():
            if (callable(attr_body)):
                if (attr_name.startswith('get_') or attr_name.startswith('set_') or
                    attr_name.startswith('del_')):
                    add_property(attr_name[4:], attr_name[:3], attr_body)
                    
        for prop_name in properties:
            attrs[prop_name] = property(properties[prop_name].get('get'), properties[prop_name].get('set'), 
                                       properties[prop_name].get('del'))
            
        return super().__new__(cls, name, bases, attrs)