#!/usr/bin/env python

import plistlib
import os
import platform
import sys
# import pprint
import subprocess

print("---------------------------------")
print("  BT-Linkkeysync by DigitalBird")
print("---------------------------------")

# file where the registry info shall be stored
filename = 'btkeys.reg'

highSierraLoc = float(".".join(platform.mac_ver()[0].split(".")[:2])) >= 10.13

print("> get Bluetooth Link Keys from macOS and store it to blued.plist")
if not highSierraLoc:
    output = subprocess.check_output(
        "sudo defaults export /private/var/root/Library/Preferences/blued.plist ./blued.plist", shell=True)
else:
    output = subprocess.check_output(
        "sudo defaults export /private/var/root/Library/Preferences/com.apple.bluetoothd.plist ./blued.plist", shell=True)

print("> convert exported list from binary to xml")
output = subprocess.check_output(
    "sudo plutil -convert xml1 ./blued.plist", shell=True)

print("> parse the converted plist")

if sys.version_info[0] == 2:
    pl = plistlib.readPlist("./blued.plist")
else:
    with open("./blued.plist", 'rb') as fp:
        pl = plistlib.load(fp, fmt=None, use_builtin_types=False)


# print the content in a human readable forat
# pprint.pprint(pl)

# open the file where we write the registry information
f = open(filename, 'w')

# function which is used to do the byte swapping and insert commas


def toWinRep(d, splitStr=",", isReverse=True, padEnd=0):
    if sys.version_info[0] == 2:
        s = d.data.encode("hex")
    else:
        s = d.data.hex()
    if padEnd > 0:
        s = s.ljust(padEnd, '0')
    if padEnd < 0:
        s = s.rjust(0-padEnd, '0')
    if isReverse:
        mystr = splitStr.join(map(str.__add__, s[-2::-2], s[-1::-2]))
    else:
        mystr = splitStr.join(map(str.__add__, s[0::2], s[1::2]))
    return mystr


print("> Convert the Link Keys and store them to btkeys.reg")
# header for the registry file
f.write("Windows Registry Editor Version 5.00")


# loop over all avialable Bluetooth 2.0 adapters
if "LinkKeys" in pl:
    print("  Bluetooth 2.0:    " +
          str(len(pl["LinkKeys"].keys())) + " Links keys found")
    for adapter in pl["LinkKeys"].keys():
        f.write(
            '\r\n\r\n[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Keys\\'+adapter.replace("-", "")+"]")

    # loop over all available devices of this adapter
    for device in pl["LinkKeys"][adapter].keys():
        f.write('\r\n"'+device.replace("-", "")+'"=hex:' +
                toWinRep(pl["LinkKeys"][adapter][device], ""))
else:
    print("No Bluetooth 2.0 information available")


# loop over all Bluetooth 4.0 LE adapters
if "SMPDistributionKeys" in pl:
    print("  Bluetooth 4.0 LE: " +
          str(len(pl["SMPDistributionKeys"].keys())) + " Links keys found")
    for adapter in pl["SMPDistributionKeys"].keys():

        # loop over all available devices of this adapter
        for device in pl["SMPDistributionKeys"][adapter].keys():
            dev = '\r\n\r\n[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Keys\\' + \
                adapter.replace("-", "")+'\\'+device.replace("-", "") + "]"
            # Lonk-Term Key (LTK)
            # 128-bit key used to generate the session key for an encrypted connection.
            dev += '\r\n"LTK"=hex:' + \
                toWinRep(pl["SMPDistributionKeys"][adapter]
                         [device]["LTK"], isReverse=False)
            # dev += '\r"KeyLength"=dword:00000000' # Don't know why this is zero when i pair my BT LE Mouse with windows.
            dev += '\r\n"KeyLength"=dword:' + \
                toWinRep(pl["SMPDistributionKeys"][adapter]
                         [device]["LTKLength"], "", padEnd=8)
            # Random Number (RAND):
            # 64-bit stored value used to identify the LTK. A new RAND is generated each time a unique LTK is distributed.
            dev += '\r\n"ERand"=hex(b):' + toWinRep(
                pl["SMPDistributionKeys"][adapter][device]["RAND"], isReverse=False)
            # Encrypted Diversifier (EDIV)
            # 16-bit stored value used to identify the LTK. A new EDIV is generated each time a new LTK is distributed.
            dev += '\r\n"EDIV"=dword:' + toWinRep(
                pl["SMPDistributionKeys"][adapter][device]["EDIV"], "", padEnd=8,)
            # Identity Resolving Key (IRK)
            # 128-bit key used to generate and resolve random address.
            dev += '\r\n"IRK"=hex:' + \
                toWinRep(pl["SMPDistributionKeys"][adapter][device]["IRK"])
            # Device Address
            # 48-bit Address of the connected device
            dev += '\r\n"Address"=hex(b):' + toWinRep(
                pl["SMPDistributionKeys"][adapter][device]["Address"], padEnd=-16)
            # Don't know whats that, i'm using an Logitech MX Master, and this is written to the registry when i pair it to windows
            dev += '\r\n"AddressType"=dword:00000001'
            # Connection Signature Resolving Key (CSRK)
            # 128-bit key used to sign data and verify signatures on the receiving device.
            # Info: CSRK is not stored on the OSX side.
            # It seems to be a temporary key which is only needed during the first bundling of the devices. After that, only the LTK is used.
            f.write(dev)
else:
    print("No Bluetooth 4.0 information available")

f.close()
print("> Registry file generated and ready for import")
