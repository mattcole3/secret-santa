# secret-santa

## Setup
GMail has deprecated password entry, so you must set up an application-specific password and be able to provide it on the command line in order to use yagmail to send the emails.

## Usage
```
usage: secret_santa.py [-h] [-f FILE] [-o1 OLD1] [-o2 OLD2] [-d] -e EMAIL -p PASSWORD

Secret Santa list randomizer and emailer. Provide a CSV with columns for "name" and "email" and it
will pair two names randomly with no dupes or collisions, and then email all participants their
assigned giftee.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  input file, names and emails
  -o1 OLD1, --old1 OLD1 last year's table
  -o2 OLD2, --old2 OLD2 table from 2 years ago
  -d, --debug           increase output verbosity; print list of gifters/recipients; send no emails
  -e EMAIL, --email EMAIL
                        email address to send secret santa notices from
  -p PASSWORD, --password PASSWORD
                        application-specific password for gmail SMTP access
                        
```

### ToDos
- [ ] Decouple the password requirement while running in debug (no-send) mode