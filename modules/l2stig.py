import re
from ciscoconfparse import CiscoConfParse
# CAT 1 VARs
# Network devices must be password protected, VulnID V-3012
NET0230 = ["V-3012", "login ."]
# Group accounts must not be configured for use on the network device. not possible on IOS device** -- Needs Attention
NET0460 = ["V-3056"]
# The network element must be configured to ensure passwords are not viewable when displaying configuration information. must use "show run all" on cisco devices to check
NET0600 = ["V-3062", "^service password-encryption"]
# Network devices must not have any default manufacturer passwords, Not possible on cisco devcies
NET0240 = ["V-3143", "password cisco"]
# the network devices must require authentication prior to establishing a management connection for administrative access.
NET1636 = ["V-3175", "login ."]
# The network device must use SNMP Version 3 Security Model with  FIPS 140-2 validated cryptography for any SNMP agent configured on the device.
NET1660 = ["V-3196", "sha", "aes"]
# The network device must not use the default or well-known SNMP community strings public and private.
NET1665 = ["V-3210", "snmp-server community public\n", "snmp-server community private\n"]
# The network device must require authentication for console acces
NET1623 = ["V-4582", "login authentication"]
# The switch must be configured to use 802.1x authentication on host facing access switch ports.
NET_NAC_009 = ["V-5626", "dot1x fallback", "dot1x host-mode", "dot1x port-control force-authorized"]
# The emergency administration account must be set to an appropriate authorization level to perform necessary administrative functions when the authentication server is not online.
NET0441 = ["V-15434", "username"]


# Subroutines for  STIG Checks


def check_net0230(parsed_obj, device_obj):
    # Subroutine to Validate Password protected vty and console access
    net0230_line_config = parsed_obj.find_parents_wo_child("^line", NET0230[1])
    if net0230_line_config:
        print("NET0230 Results: \"Network devices must be password protected\" \n" + (" fix " +
                                                                                      NET0230[0] + " in {1} \n" + " {0}").format(" {0}".format("  ".join(str(i) for i in net0230_line_config)), device_obj.hostname))
    else:
        print("NET0230:\n No violations detected")


def check_net0600(parsed_obj, device_obj):
    # Subroutine to Validate service password-encryption
    pattern = re.compile("no service password-encryption", re.I | re.M)

    net0600_config = parsed_obj.find_lines(pattern)

    if len(net0600_config) == 0:
        print("NET0600\n No violations detected")
    else:
        print("NET0600: " + NET0600[0] + " Results: \"passwords are viewable when displaying configuration information\" \n" + (
            " enable 'service password-encryption'" + " on" + " {1} \n").format(net0600_config, device_obj.hostname))


def check_net1636(parsed_obj, device_obj):
    # Subroutine to Validate Password protected vty and console access
    net1636_line_config = parsed_obj.find_parents_wo_child("^line", NET1636[1])

    if net1636_line_config:
        print("NET1636 Results: \"network devices must require authentication\" \n" + (" fix " +
                                                                                       NET1636[0] + " in {1} \n" + " {0}").format(" {0}".format("  ".join(str(i) for i in net1636_line_config)), device_obj.hostname))
    else:
        print("NET1636:\n No violations detected")


def check_net1660(device):
    # opening SNMP results file

    # REGEX to find violating config for SNMP

    # SNMP violation count
    COUNT_MD5 = AES_REG_A.count("MD5")
    COUNT_DES = AES_REG_A.count("DES")
    COUNT_3DES = AES_REG_A.count("3DES")
    NET1660_VIOLATION = COUNT_3DES + COUNT_MD5 + COUNT_DES

    # Looking for SNMP version 1 and 2c related configuration
    snmp_lines = parse.find_lines("(snmp-server.(user|group).*v(1|2))|(snmp-server community.*)")

    # Conditional to validate if device is using FIP-140-2 compliant SNMPv3 deployment and no SNMPv2 is being utilized
    if NET1660_VIOLATION > 0 or snmp_lines:
        print("NET1660 " + NET1660[0] + " Results: \"SNMPv3 must only Use SHA and AES\" \n" +
              " Execute 'show snmp user' on system")
        print(" ")
        print("NET1660 " + NET1660[0] + " Results: \"SNMPv1 and SNMPv2 must not be used\" \n " +
              "{0}").format(" ".join(str(i) for i in snmp_lines))
    else:
        print("NET1660:\n no violations detected")


def check_net1665(parsed_obj):
    # Extracts SNMP configuration, the re.complie, uses the re compile functon to create a REGEX pattern to be used with cisco conf parse
    snmp_pattern = re.compile("snmp-server.community.(public|private)", re.I | re.M)

    net1665_config_lines = parsed_obj.find_lines(snmp_pattern)

    # Stores Human Readable List in VAR
    net1665_config = "{0}".format("   ".join(str(i) for i in net1665_config_lines))

    # Conditional to test if  the private or public communty is there
    if len(net1665_config_lines) > 0:
        print("\nNET1665 Results: \"Device must not use the default or well-known SNMP community strings public and private.\" \n  Remidiation  for" +
              NET1665[0] + ": \n  Remove lines: \n   {0}").format(net1665_config)
    else:
        print("NET1665:\n No violations detected")


def check_net1623(PARSED_CONFIG):
    pattern = re.compile("(login.authentication..[a-z]?)", re.I | re.M)

    net1623_config_list = PARSED_CONFIG.find_parents_wo_child('^line con.[0-9]', pattern)

    # Stores Human Readable List in VAR
    net1623_config = "{0}".format("   ".join(str(i) for i in net1623_config_list))

    if len(net1623_config_list) > 0:
        print ("\nNET1623 Results: 'Network device must require authentication for console access' \n Please enable authentication for the following lines: \n   {}").format(net1623_config)
    else:
        print("NET1623:\n No violations detected")


def check_dot1x():
    pass


def parse_config(FILE):
    # opening Text File
    filename = "./" + FILE
    config = open(FILE, "r")
    # Creatting CiscoConfParse  obj.
    parse = CiscoConfParse(config)


def results(DEVICE):
        # Generates generic Results Method or Main Routine
    print("\t\tResults for {}").format(DEVICE.mgmt_ip)
