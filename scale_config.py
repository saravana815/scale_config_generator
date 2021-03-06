#!/bin/env python2

import argparse
import re
import sys, os
from nested_dict import *

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='input config file', required=True)
parser.add_argument('-c', '--count', help='number of times to scale the configs', required=True, type=int)
parser.add_argument('-o', '--outfile', help='output file name for generated configs', required=False, default='configs_out.txt')
args = parser.parse_args()

def incr_ip(ip, incr_val):
    #print ip, incr_val
    #split ip bytes 1.2 to 1, 2
    #split ip bytes 1.2.3 to 1, 2, 3
    #split ip bytes 1.2.3.4 to 1, 2, 3, 4
    ip_bytes = ip.split('.')
    ip_bytes_len = len(ip_bytes)
    if ip_bytes_len == 2:
        ip_byte1 = int(ip_bytes[0])
        ip_byte2 = int(ip_bytes[1])

        #actual hex value
        ip_value = (ip_byte1 * 256) + ip_byte2
        ip_value_incr = ip_value + incr_val

        #print ip_value_incr
        ip_byte1 = ip_value_incr / 256
        ip_byte2 = ip_value_incr % 256

        return str(ip_byte1) + '.' + str(ip_byte2)

    elif ip_bytes_len == 3:
        ip_byte1 = int(ip_bytes[0])
        ip_byte2 = int(ip_bytes[1])
        ip_byte3 = int(ip_bytes[2])

        #actual hex value
        ip_value = (ip_byte1 * 65536) + (ip_byte2 * 256) + ip_byte3
        ip_value_incr = ip_value + incr_val

        #print ip_value_incr
        ip_byte1 = ip_value_incr / 65536
        ip_byte2_3 = ip_value_incr % 65536
        ip_byte2 = ip_byte2_3 / 256
        ip_byte3 = ip_byte2_3 % 256

        return str(ip_byte1) + '.' + str(ip_byte2) + '.' + str(ip_byte3)

    elif ip_bytes_len == 4:
        ip_byte1 = int(ip_bytes[0])
        ip_byte2 = int(ip_bytes[1])
        ip_byte3 = int(ip_bytes[2])
        ip_byte4 = int(ip_bytes[3])

        #actual hex value
        ip_value = (ip_byte1 * 16777216) + (ip_byte2 * 65536) + (ip_byte3 * 256) + ip_byte4
        ip_value_incr = ip_value + incr_val

        #print ip_value_incr
        ip_byte1 = ip_value_incr / 16777216
        ip_byte2_3_4 = ip_value_incr % 16777216
        ip_byte2 = ip_byte2_3_4 / 65536
        ip_byte3_4 = ip_byte2_3_4 % 65536
        ip_byte3 = ip_byte3_4 / 256
        ip_byte4 = ip_byte3_4 % 256

        return str(ip_byte1) + '.' + str(ip_byte2) + '.' + str(ip_byte3) + '.' + str(ip_byte4)


def incr_ipv6(ipv6, incr_val):
    #print ip, incr_val
    #split ip bytes 11AA:22BB to 11AA, 22BB
    ipv6_bytes = ipv6.split(':')
    ipv6_byte1 = int(ipv6_bytes[0], 16)
    ipv6_byte2 = int(ipv6_bytes[1], 16)

    #actual hex value
    ipv6_value = (ipv6_byte1 * 65536) + ipv6_byte2
    ipv6_value_incr = ipv6_value + incr_val

    #print ip_value_incr
    ipv6_byte1 = ipv6_value_incr / 65536
    ipv6_byte2 = ipv6_value_incr % 65536

    # return str(str(hex(ipv6_byte1)).replace('0x', '')).upper() + ':' + str(str(hex(ipv6_byte2)).replace('0x', '')).upper()
    return str(hex(ipv6_byte1)).replace('0x', '').upper() + ':' + str(hex(ipv6_byte2)).replace('0x', '').upper()

def incr_int(val, incr_val, incr_range, orig_val):
    #print val, incr_val, incr_range, orig_val
    if incr_range == '':
        return val + incr_val
    else:
        val_div = (val + incr_val) / incr_range
        val_mod = (val + incr_val) % incr_range
        if val_div == 1 and val_mod >= 1:
            return orig_val
        else:
            return (val + incr_val)


lines = []
#open file and parse lines
with open(args.file) as f:
    lines = f.readlines()
    # print lines

#parse the config lines surrounded by [] with value. ex [100], [0x64], [100,2]
#pat = re.compile(r'\[(0?x?[0-9A-Fa-f]+),?(\d+)?\]')
pat = re.compile(r'\[([0-9A-Fa-f\.x:]+),?(\d+)?,?(\d+)?\]')
lt = nested_dict()
tmp = 0
for line in lines:
    lt[tmp]['line'] = line
    #find all the pattern - dec and hex 0x
    match = pat.findall(line)
    if match:
        match_new = []
        match_incr_val = {}
        #Below match_dict used for int increment within a range
        match_range_val = {}
        match_orig_val = {}
        for num, x in enumerate(match):
            #hex match. Append hex value to list
            if ':' in x[0]:
                #match_new.append(hex(int(x[0][0],16)))
                match_new.append(x[0])
                if x[1] == '':
                    match_incr_val[num] = 1
                else:
                    match_incr_val[num] = int(x[1])
            #ip address match. Append ip address (part) to list
            elif '.' in x[0]:
                match_new.append(x[0])
                if x[1] == '':
                    match_incr_val[num] = 1
                else:
                    match_incr_val[num] = int(x[1])
            else:
                #decimal match. Append int value to list
                match_new.append(int(x[0]))
                if x[1] == '':
                    match_incr_val[num] = 1
                else:
                    match_incr_val[num] = int(x[1])

                if x[2] == '':
                    match_range_val[num] = ''
                else:
                    match_range_val[num] = int(x[2])

                match_orig_val[num] = int(x[0])

        #template line with python {}
        line_new = re.sub(r'\[[0-9A-Fa-f\.x:,]+]','{}',line)
        lt[tmp]['regsub'] = True
        lt[tmp]['line_format'] = line_new
        # print lt[tmp]['line_format']
        #replace list. Includes int and str(for hex, ip)
        lt[tmp]['substring'] = match_new
        # print lt[tmp]['substring']
        lt[tmp]['match_incr_val'] = match_incr_val
        lt[tmp]['match_range_val'] = match_range_val
        lt[tmp]['match_orig_val'] = match_orig_val

    else:
        lt[tmp]['regsub'] = False
        lt[tmp]['line_format'] = line

    tmp += 1

# #for keys_as_tuple, value in lt.iteritems_flat():
# #    print ("%-20s == %r" % (keys_as_tuple, value))

file_out = args.outfile
fout = open(file_out, 'w')
for i in range(args.count):
    for ln in range(len(lines)):
        if lt[ln]['regsub'] == True:
            #print line with value increment and replace 0x with ''
            print lt[ln]['line_format'].format(*lt[ln]['substring']).replace('0x',''),
            print >>fout, lt[ln]['line_format'].format(*lt[ln]['substring']).replace('0x',''),
            #increment the values for next iterataion
            lt[ln]['substring_new'] = []
            for num, x in enumerate(lt[ln]['substring']):
                if type(x) == int:
                    #lt[ln]['substring_new'].append(x + lt[ln]['match_incr_val'][num])
                    lt[ln]['substring_new'].append(incr_int(x, lt[ln]['match_incr_val'][num], \
                            lt[ln]['match_range_val'][num], lt[ln]['match_orig_val'][num]))
                elif ':' in x:
                    lt[ln]['substring_new'].append(incr_ipv6(x, lt[ln]['match_incr_val'][num]))
                elif '.' in x:
                    lt[ln]['substring_new'].append(incr_ip(x, lt[ln]['match_incr_val'][num]))

            lt[ln]['substring'] = lt[ln]['substring_new']
        else:
            print lt[ln]['line'],
            print >>fout, lt[ln]['line'],

fout.close()
