import json
import sys
from jinja2 import Template

# Check if an argument is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <InputFileName.json>")
    sys.exit(1)

input_file = sys.argv[1]

# Load and parse the JSON Schema
with open(input_file) as file:
    schema = json.load(file)

# Function to resolve references within the schema
def resolve_reference(schema, ref):
    parts = ref.split('/')
    for part in parts[1:]:  # Skip the first empty part
        schema = schema.get(part, {})
    return schema

def to_title_case(text):
    return text.replace('_', ' ').title()

# Define the mapping logic
def map_schema_to_xml(schema):
    xml_components = []
    xml_resources = []

    for field, properties in schema.get('properties', {}).items():
        if '$ref' in properties:
            # Resolve the reference
            properties = resolve_reference(schema, properties['$ref'])

        field_type = properties.get('type')
        enums = properties.get('enum')
        field_label = to_title_case(field)

        xml_components.append(f'''<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:layout_marginVertical="8dp"
    android:orientation="vertical">''')

        xml_components.append(f'''<TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginBottom="4dp"
            android:text="{field_label}" />''')

        if field_type == 'array':
            items = properties.get('items', {})
            if '$ref' in items:
                items = resolve_reference(schema, items['$ref'])
            item_enums = items.get('enum')

            if item_enums:
                # Handling array of enums as a series of CheckBoxes
                for enum_item in item_enums:
                    xml_components.append(f'<CheckBox android:id="@+id/{field}_{enum_item.replace(" ", "_")}" android:text="{enum_item}" android:layout_width="wrap_content" android:layout_height="wrap_content"/>')
            else:
                # General handling for arrays
                xml_components.append(f'<ListView android:id="@+id/{field}" android:layout_width="match_parent" android:layout_height="wrap_content"/>')


        elif enums:
            # Handling enum as a Spinner
            spinner_items = f'<string-array name="{field}">\n'
            spinner_items += '\n'.join([f'<item>{enum_item}</item>' for enum_item in enums])
            spinner_items += f"\n</string-array>"
            xml_resources.append(f'{spinner_items}')
            xml_components.append(f'<Spinner android:id="@+id/{field}" android:layout_width="match_parent" android:layout_height="wrap_content" android:entries="@array/{field}" />')

        elif field_type == 'string':
            xml_components.append(f'<EditText android:id="@+id/{field}" android:layout_width="match_parent" android:layout_height="wrap_content"/>')

        elif field_type in ['number', 'integer']:
            xml_components.append(f'<EditText android:id="@+id/{field}" android:inputType="number" android:layout_width="match_parent" android:layout_height="wrap_content"/>')

        elif field_type == 'boolean':
            xml_components.append(f'<CheckBox android:id="@+id/{field}" android:text="{field_label}" android:layout_width="wrap_content" android:layout_height="wrap_content"/>')

        elif field_type == 'array':
            xml_components.append(f'<ListView android:id="@+id/{field}" android:layout_width="match_parent" android:layout_height="wrap_content"/>')

        elif field_type == 'object':
            xml_components.append(f'<!-- Object type for {field} not fully implemented -->')

        xml_components.append(f'</LinearLayout>')

    xml_components.extend(xml_resources)
    return xml_components

# Generate XML layout
xml_layout = map_schema_to_xml(schema)

# XML template for the layout
template = Template('''<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp">
    <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
        {% for component in components %}
            {{ component }}
        {% endfor %}
            
    </LinearLayout>
</ScrollView>
''')

output_xml = template.render(components=xml_layout)

# Save the output
with open('translator-output/output_layout.xml', 'w') as file:
    file.write(output_xml)
