# secret-santa

{
usage: secret_santa.py [-h] [-f FILE] [-d] -e EMAIL -p PASSWORD

Secret Santa list randomizer and emailer. Provide a CSV with columns for "name" and "email" and it
will pair two names randomly with no dupes or collisions, and then email all participants their
assigned giftee.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  input file, names and emails
  -d, --debug           increase output verbosity; print list of gifters/recipients; send no emails
  -e EMAIL, --email EMAIL
                        email address to send secret santa notices from
  -p PASSWORD, --password PASSWORD
                        application-specific password for gmail SMTP access
}