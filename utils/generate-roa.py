#!/usr/bin/python3

# Based in https://github.com/nuku97/dn42-bird-roa-generator

import sys
import os
import glob
from datetime import datetime, timezone

def parse_registry_file(filepath):
    data = {}
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            # Handle multi-value fields for origin
            if key == 'origin':
                if key not in data:
                    data[key] = []
                data[key].append(val)
            elif key not in data:
                data[key] = val
    
    route_key = 'route'
    
    if route_key not in data or 'origin' not in data:
        return None

    return data

def process_registry(registry_path, output_file):
    route_dir = 'route'
    search_path = os.path.join(registry_path, 'data', route_dir, '*')

    roas = []

    files = glob.glob(search_path)
    for filepath in files:
        if not os.path.isfile(filepath):
            continue

        entry = parse_registry_file(filepath)
        if not entry:
            continue

        prefix_str = entry.get('route')
        origins = entry.get('origin', [])

        for origin_str in origins:
            itad = origin_str.upper()
            if itad.startswith('ITAD'):
                itad = itad[4:]
            if not itad.isdigit():
                 continue

            roas.append((prefix_str, itad))

    # Write output
    with open(output_file, 'w') as f:
        # Header
        f.write('#\n')
        f.write('# TRIP Resurgence Network ROA Generator\n')
        f.write('# Format: TRIP Resurgence tripd\n')
        f.write(f'# Generated: {datetime.now(timezone.utc).isoformat()}\n')
        f.write('#\n')
        
        for prefix, itad in roas:
            f.write(f'route {prefix} itad {itad}\n')

def main():
    if len(sys.argv) < 2:
        print('usage: ' + sys.argv[0] + ' <registry path>')
        exit(1)

    registry_path = sys.argv[1]
    output_path = 'tripnet_roa_tripd.txt'

    if len(sys.argv) == 3:
        output_path = sys.argv[2]

    process_registry(sys.argv[1], output_path)

if __name__ == '__main__':
    main()

