import json
from astroquery.jplhorizons import Horizons
from astropy.time import Time

def build_spacecraft_json(start_id=-1, end_id=-300, output_filename="spacecraft_horizons.json"):
    current_jd = Time.now().jd
    spacecraft_list = []
    failed_count = 0

    # Reference mapping dictionary for human annotators
    # @ sign indicates Barycentric rathern than physical centric
    reference_mappings = {
        "SSB": "@0",     #Solar System Barycentric
        "Sun": "@10",
        "Mercury": "@199",
        "Venus": "@299",
        "Earth": "@399",
        "Moon": "@301",
        "Mars": "@499",
        "Jupiter": "@599",
        "Saturn": "@699",
        "Uranus": "@799",
        "Neptune": "@899",
        "Pluto": "@999"
    }

    print(f"Querying JPL Horizons for IDs {start_id} to {end_id}...")

    # Loop through negative spacecraft IDs
    for target_id in range(start_id, end_id - 1, -1):
        try:
            # Query elements using astroquery
            query = Horizons(id=target_id, location='@0', epochs=current_jd)
            table = query.elements()
            row = table[0]

            # Raw target name usually comes back formatted like "Spacecraft Name (ID)"
            raw_name = str(row['targetname'])
            # Clean up the name (remove trailing ID in parentheses if present)
            clean_name = raw_name.split('(')[0].strip()

            sc_entry = {
                "id": target_id,
                "name": clean_name,
                "parent_id": "@0",          # Populate this during editing (e.g., 399 for Earth)
                "parent_id_name": "Sun"      # Populate this during editing (e.g., "Earth")
            }

            spacecraft_list.append(sc_entry)
            print(f"Found: ID {target_id} -> {clean_name}")

        except Exception:
            # Unassigned IDs or query failures trigger an exception in astroquery
            failed_count += 1

    # Package output data with instructions and reference mappings
    output_data = {
        "_instructions": "Annotate 'parent_id' and 'parent_id_name' using the horizons_reference_mappings dictionary below.",
        "horizons_reference_mappings": reference_mappings,
        "spacecraft": spacecraft_list
    }

    # Write to JSON file
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)

    print(f"\nDone! Saved {len(spacecraft_list)} registered spacecraft to '{output_filename}'.")
    print(f"Skipped {failed_count} unassigned or unreachable IDs.")

if __name__ == "__main__":
    # Adjust range as needed (e.g., -1 to -500)
    build_spacecraft_json(start_id=-1, end_id=-500)
