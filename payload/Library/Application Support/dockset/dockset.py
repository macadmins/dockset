#/usr/bin/python

"""
This is like outset, but for docks.
"""

import plistlib
import os
import sys
import argparse
import subprocess

DOCKSET_DIR = '/Library/Application Support/dockset'

def find_dock_item(item, dockutil):
    """
    Finds an item in the dock. Returns a boolean.
    """
    if 'name' not in item:
        # Eventually we will try to guess the name from the path, but we're being quick and dirty here
        fail('name not in {}'.format(item))
    cmd = [
        dockutil,
        '--find',
        item['name']
    ]

    try:
        subprocess.check_output(cmd)
        return True
    except subprocess.CalledProcessError:
        print '{} not in dock'.format(item)
        return False

def add_item_to_dock(item, dockutil):
    """
    Adds an item to the dock
    """
    if 'path' not in item:
        fail('no path specified in {}'.format(item))
    cmd = [
        dockutil,
        '--add',
        item['path']
    ]

    if 'replacing' in item:
        cmd.append(['--replacing'], item['replacing'])

    if 'postition' in item:
        cmd.append(['--position', item['position']])

    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        fail('Failed to run {}'.format(cmd))

def remove_item_from_dock(item, dockutil):
    """
    Removes an item from the dock
    """
    if 'name' not in item:
        fail('no name specified in {}'.format(item))
    cmd = [
        dockutil,
        '--remove',
        item['name']
    ]

    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        fail('Failed to run {}'.format(cmd))

def process_dock_additions(dockutil):
    """
    Processes plists of items to add
    """
    if os.path.exists(os.path.join(DOCKSET_DIR, 'add-every')):
        for plist in os.listdir(os.path.join(DOCKSET_DIR, 'add-once')):
            plist = os.path.join(os.path.join(DOCKSET_DIR, 'add-once', plist))
            try:
                item = plistlib.readPlist(plist)
            except:
                fail('Could not parse {}', plist)
            add_item_to_dock(item, dockutil)
            os.remove(plist)

    if os.path.exists(os.path.join(DOCKSET_DIR, 'add-every')):
        for plist in os.listdir(os.path.join(DOCKSET_DIR, 'add-every')):
            plist = os.path.join(os.path.join(DOCKSET_DIR, 'add-every', plist))
            try:
                item = plistlib.readPlist(plist)
            except:
                fail('Could not parse {}', plist)
            if not find_dock_item(item, dockutil):
                add_item_to_dock(item, dockutil)

def process_dock_removals(dockutil):
    """
    Proceses plists of items to remove
    """
    if os.path.exists(os.path.join(DOCKSET_DIR, 'remove-once')):
        for plist in os.listdir(os.path.join(DOCKSET_DIR, 'remove-once')):
            plist = os.path.join(os.path.join(DOCKSET_DIR, 'remove-once', plist))
            try:
                item = plistlib.readPlist(plist)
            except:
                fail('Could not parse {}', plist)
            remove_item_from_dock(item, dockutil)
            os.remove(plist)

    if os.path.exists(os.path.join(DOCKSET_DIR, 'remove-every')):        
        for plist in os.listdir(os.path.join(DOCKSET_DIR, 'remove-every')):
            plist = os.path.join(os.path.join(DOCKSET_DIR, 'remove-every', plist))
            try:
                item = plistlib.readPlist(plist)
            except:
                fail('Could not parse {}', plist)
            if find_dock_item(item, dockutil):
                remove_item_from_dock(item, dockutil)

def fail(msg):
    """
    FAIL
    """
    print msg
    sys.exit(1)

def main():
    """
    Main main main
    """
    parser = argparse.ArgumentParser(
    description='Like outset, for docks')
    parser.add_argument(
        '--dockutil', help='Path to dockutil',
        default='/usr/local/bin/dockutil')
    
    args = parser.parse_args()
    dockutil = args.dockutil

    if not os.path.exists(dockutil):
        fail('dockutil not present')

    process_dock_additions(dockutil)
    process_dock_removals(dockutil)


if __name__ == '__main__':
    main()
