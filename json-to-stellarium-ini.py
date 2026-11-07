import json

def generate_ini_from_json(json_filename="spacecraft_horizons.json", ini_filename="spacecraft_sso.ini"):
    try:
        with open(json_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_filename} not found. Please run the fetch script first.")
        return

    spacecraft_list = data.get("spacecraft", [])
    
    ini_lines = []
    ini_lines.append("; Stellarium Solar System Configuration File for Spacecraft")
    ini_lines.append("; Automatically generated from annotated JSON data\n")

    exported_count = 0
    for sc in spacecraft_list:
        parent_name = sc.get("parent_id_name")
        parent_id = sc.get("parent_id")
        
        # Only process entries that have been annotated with valid parent information
        if parent_name and parent_id is not None:
            name = sc["name"]
            section_name = name.replace("=", "_").strip()
            
            ini_lines.append(f"[{section_name}]")
            ini_lines.append(f"name = {name}")
            ini_lines.append(f"parent = {parent_name}")
            ini_lines.append(f"radius = 1.0")
            ini_lines.append(f"oblateness = 0.0")
            ini_lines.append(f"albedo = 1.0")
            ini_lines.append(f"color = 1.0, 1.0, 1.0")
            ini_lines.append(f"lighting = true")
            ini_lines.append(f"orbit_type = ephemeris")
            ini_lines.append(f"horizon_class = artificial")
            ini_lines.append("")
            exported_count += 1

    with open(ini_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(ini_lines))

    print(f"Successfully generated {ini_filename} with {exported_count} configured spacecraft sections for Stellarium.")

if __name__ == "__main__":
    generate_ini_from_json()
