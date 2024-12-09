variables = ""

def convert_type(param):
    elements_type = "any"

    if param['type'] == "array" and "defaultValue" in param:
        if all(isinstance(x,int) for x in param["defaultValue"]):
            elements_type = "number" 
        elif all(isinstance(x,str) for x in param["defaultValue"]):
            elements_type = "string"
        else:
            elements_type = "any"
            
    types = {
        "securestring" : "string",
        "string"       : "string",
        "int"          : "number",
        "bool"         : "bool",
        "array" : f"list({elements_type})"
    }

    return types[param['type']]


def defineValidation(content, nameOfVariable):
    condition = ""
    errorMessage = ""
    finalValidationBlock = ""

    def validation(condition, errorMessage):
        validation = ""
        validation = "validation { \n "  

        validation += "condition = " + condition + "\n"

        validation += f"error_message = {errorMessage}"+"\n"

        validation += "} \n"

        return validation



    if "allowedValues" in content:
        
        allowedValuesArray = "["
        for allowedValue in content["allowedValues"]:
            allowedValuesArray += "\""+f"{allowedValue}"+"\" ,"
        allowedValuesArray = allowedValuesArray[:-1]
        allowedValuesArray += "]"

        condition = f"contains({allowedValuesArray}, var.{nameOfVariable})"
        errorMessage = "\""+ f"{nameOfVariable} must one of these allowed values : "+f"{content['allowedValues']}" + "\""
        finalValidationBlock += validation(condition,errorMessage)

    if "minLength" in content or "maxLength" in content:
        if "maxLength" not in content:
            condition = f"length( var.{nameOfVariable} ) >= {content["minLength"]}"
            errorMessage = f"Minimum lenght of {nameOfVariable} must be {content['minLength']}"

        elif "minLength" not in content:
            condition = f"length( var.{nameOfVariable} ) <= {content["maxLength"]}"
            errorMessage = f"Max lenght of {nameOfVariable} must be {content['maxLength']}"
        
        else:
            condition = f"length( var.{nameOfVariable} ) <= {content["maxLength"]} & length( var.{nameOfVariable} ) >= {content["minLength"]}"
            errorMessage = f"{nameOfVariable} must be {content["minLength"]}-char min, {content['maxLength']}-char max"

    return finalValidationBlock

def extract_parameters(json_data):
    params = json_data["parameters"]
    for param in params:
        variable = f"variable {param} "+"{ \n"              # Start declaration

        # type declaration
        datatype = convert_type(params[param])              
        variable += f"type = {datatype} \n"    

        #sensitive 
        if "secure" in  params[param]['type'].lower():
            variable += f"sensitive = true \n"

        # setting description
        if "metadata" in params[param]:
            variable += f"description = \"{params[param]["metadata"]["description"]}\" \n"

        # setting validation
        variable += defineValidation(params[param],param)
        
        variable += "} \n"                                  # Closing variable
        print(variable)

    return variable

# def convert_parameters(json,)