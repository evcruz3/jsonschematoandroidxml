# json-schema to Android XML Layout 

## Description
This Python script is designed to convert a JSON Schema into an Android XML layout. The script reads a JSON file that defines various properties of a UI schema (like field types, enumerations, and references) and translates this schema into a corresponding XML layout that can be used in Android app development.

## Key Features
1. **JSON Schema Parsing**: Loads a JSON Schema and parses its contents.
2. **Reference Resolution**: Resolves $ref references within the JSON Schema to handle nested definitions.
3. **Dynamic XML Generation**: Creates Android XML layout components based on the JSON Schema properties, supporting various field types such as strings, numbers, booleans, arrays, and objects.
4. **Support for Enums**: Handles enumerations in the JSON Schema by creating Spinner components in the XML layout.
5. **Title Case Conversion**: Converts field names to title case for better readability in the layout.
6. **Output Customization**: The XML layout is generated according to the structure defined in the JSON Schema, allowing for customized UI layouts based on different schemas.

## Requirements
Python 3
jinja2 library for Python

## Installation
Before running the script, ensure you have Python 3 installed on your system. You also need to install the jinja2 library, which can be done using pip:

``` 
pip install jinja2
```


## Usage
To use the script, provide the JSON Schema file as a command-line argument:

```
python3 translator.py [Input JSON File]
```

For example:

```
python3 translator.py IncidentDetails.json
``` 

### Sample JSON Schema

```
{
  "type": "object",
  "properties": {
    "user_name": {
      "type": "string"
    },
    "age": {
      "type": "number"
    },
    "is_active": {
      "type": "boolean"
    },
    "role": {
      "type": "string",
      "enum": ["admin", "user", "guest"]
    }
    // ... more fields ...
  }
}
```

## Output
The script will create an Android XML layout file with UI components corresponding to the fields defined in the JSON Schema. The output file will be saved in the translator-output directory as output_layout.xml.

## Limitations
The script currently has limited support for nested objects and complex JSON structures.
Array handling does not provide specific UI implementations and might require manual adjustments in the generated XML.
Contributions
Feel free to contribute to this project by suggesting improvements, reporting bugs, or submitting pull requests.