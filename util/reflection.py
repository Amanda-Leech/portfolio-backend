from flask import jsonify

def populate_object(obj, data_dictionary):
    fields = data_dictionary.keys()
    for field in fields:
        if hasattr(obj, field):
            setattr(obj, field, data_dictionary[field])
    return obj
