# secret-santa
python3 secret-santa.py -h
usage: secret-santa.py [-h] [-f FILE] [-d] -e EMAIL -p PASSWORD

Secret Santa

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  input file, names and emails
  -d, --debug           increase output verbosity; print list of gifters/recipients; send no emails
  -e EMAIL, --email EMAIL
                        email address to send secret santa notices from
  -p PASSWORD, --password PASSWORD
                        application-specific password for gmail SMTP access
