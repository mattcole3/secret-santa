# secret-santa

## Setup
GMail has deprecated password entry, so you must set up an application-specific password and be able to provide it on the command line in order to use yagmail to send the emails.

```
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
```

### ToDos
- [ ] Decouple the password requirement while running in debug (no-send) mode