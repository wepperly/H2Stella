import json
import sys
from astroquery.jplhorizons import Horizons
from astropy.time import Time

def generate_stellarium_ini(json_filename="spacecraft_horizons.json", ini_filename="ssystem_minor_update.ini"):
    """Reads spacecraft configuration from JSON, queries JPL Horizons, and generates a Stellarium INI file."""
    try:
        with open(json_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_filename} not found.", file=sys.stderr)
        return

    spacecraft_list = data.get("spacecraft", [])
    current_jd = Time.now().jd
    
    ini_lines = []
    ini_lines.append("# Stellarium Solar System Configuration File for Spacecraft")
    ini_lines.append("# Generated dynamically from JSON configuration\n")
    ini_lines.append("# Make a backup of the following file first!:")
    ini_lines.append("#   ssystem_minor.ini")
    ini_lines.append("# append this data to the end of the following file:")
    ini_lines.append(r"#   C:\Users\<YourUserName>\AppData\Roaming\Stellarium\data\ssystem_minor.ini" + "\n")


    success_count = 0
    fail_count = 0

    for sc in spacecraft_list:
        target_id = sc["id"]
        display_name = sc["name"]
        center_code = sc.get("parent_id", "@0")
        parent_name = sc.get("parent_id_name", "Sun")

        print(f"Querying Horizons for {display_name} (ID: {target_id}, Center: {center_code})...")

        try:
            # Query Horizons using the correct tracking center and target ID from JSON
            query = Horizons(id=target_id, location=center_code, epochs=current_jd)
            table = query.elements()
            row = table[0]
            
            # Format block matching the structure to support Stellarium minor solar system ini file
            block = f"""[{display_name}]
name = {display_name}
parent = {parent_name}
type = artificial
orbit_Epoch = {row['datetime_jd']:.6f}
orbit_TimeAtPericenter = {row['Tp_jd']:.6f}
orbit_PericenterDistance = {row['q']:.12f}
orbit_Eccentricity = {row['e']:.12f}
orbit_ArgOfPericenter = {row['w']:.6f}
orbit_AscendingNode = {row['Omega']:.6f}
orbit_Inclination = {row['incl']:.6f}
"""
            ini_lines.append(block)
            success_count += 1
        except Exception as e:
            print(f"  -> Failed to query ID {target_id} ({display_name}): {e}", file=sys.stderr)
            fail_count += 1

    with open(ini_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(ini_lines))

    print(f"\nDone! Successfully generated {ini_filename} with {success_count} spacecraft configs ({fail_count} failed/skipped).")

if __name__ == "__main__":
    generate_stellarium_ini()
