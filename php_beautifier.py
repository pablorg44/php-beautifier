#!/usr/bin/env python
import re
import base64
import optparse

def deobfuscate_b64(deob_data, d_file):
    with open(d_file, 'w') as fw:
        cnt = 1
        for line in deob_data:
            #print(line)
            if "base64_decode" in line:
                result = re.findall("base64_decode\([^\)]*", line)
                new_line = ""
                for b64 in result:
                    b64 = re.split("(\"|\')", b64)[2]
                    #b64 = b64.split("'")[1]
                    decoded = base64.b64decode(b64).decode('utf-8', 'ignore')
                    if new_line == "":
                        new_line = re.sub("base64_decode\((\'|\")"+b64+"(\'|\")\)",'"'+decoded+'"', line)
                    else:
                        new_line = re.sub("base64_decode\((\'|\")"+b64+"(\'|\")\)",'"'+decoded+'"', new_line)
                    #print(new_line)
                fw.write(new_line+'\n')
                #print(result)
            else:
                fw.write(line+'\n')
            cnt += 1

def beautify(filename):
    with open(filename, 'r') as fp:
        data = fp.read()
        #print(data)
        counter = 0
        counter_parenthesis = 0
        index = 0
        new_data = ""
        for c in data:
            if c == '{':
                if data[index-1] == ")":
                    counter = counter + 1
                    tabs = "\t"*(counter)
                    new_data += "{\n"+tabs
                elif index > 5:
                    if data[index-1] == 'e' and data[index-2] == 's' and data[index-3] == 'l' and data[index-4] == 'e':
                        counter = counter + 1
                        tabs = "\t"*(counter)
                        new_data += "{\n"+tabs
                    else:
                        new_data += c
                else:
                    new_data += c
            elif c == '}':
                tabs = "\t"*(counter - 1)
                new_data += '\n' + tabs + '}\n' + tabs
                counter -= 1
            elif c == '(':
                counter_parenthesis += 1
                new_data += c
            elif c == ')':
                counter_parenthesis -= 1
                new_data += c
            elif c == ';' and counter_parenthesis == 0:
                tabs = "\t" * counter
                new_data += ";\n" + tabs
            else:
                new_data += c
            index += 1
        deob_data = new_data.split('\n')
        return deob_data



if __name__ == "__main__":
    oParser = optparse.OptionParser(usage='usage: python3 php_beautifier.py -f FILE_TO_BEAUTIFY')
    oParser.add_option('-f', '--file', dest='filename', action='store', default='', help='File to beautify')
    oParser.add_option('-d', '--destinationfile', dest='d_file', action='store', default='php_beautify.php', help='Destination file (optional, by default = php_beautify.php)')
    (options, args) = oParser.parse_args()
    if not options.filename:
        oParser.error("-f option needed")
        exit(255)
    first_step = beautify(options.filename)
    deobfuscate_b64(first_step, options.d_file)
