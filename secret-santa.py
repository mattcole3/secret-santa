#!/usr/bin/env python3

import argparse as ap
import csv
import random
import smtplib, ssl, getpass
import yagmail
import time
from pprint import pprint

def secret_santa_shuffle(participants, preseed_assignments, debug):
    # Shuffle the list of participants to randomly assign gift recipients
    names = list(participants.keys())
    recipients = list(participants.keys())

    # Remove pre-seeded pairs from the lists
    for name, recipient in preseed_assignments.items():
        if name in names:
            names.remove(name)
        if recipient in recipients:
            recipients.remove(recipient)

    random.shuffle(names)
    random.shuffle(recipients)

    # Assign gift recipients
    assignments = preseed_assignments.copy()
    for i, name in enumerate(names):
        if debug:
            print("i is", i, "name is ", name, "recipient is", recipients[i] )
        assignments[name] = recipients[i]

    return assignments

def secret_santas_collide(secret_santa_assigns, year1, year2, year3, debug):
    for name in secret_santa_assigns.keys():
        if debug:
            print(name, secret_santa_assigns[name])
        if name == secret_santa_assigns[name]:
            return True
        if name in year1.keys() and secret_santa_assigns[name] == year1[name]:
            return True
        if name in year2.keys() and secret_santa_assigns[name] == year2[name]:
            return True
        if name in year3.keys() and secret_santa_assigns[name] == year3[name]:
            return True                    
    return False

def parse_preseed(preseed_str):
    preseed_assignments = {}
    pairs = preseed_str.split(',')
    for pair in pairs:
        name, recipient = pair.split(':')
        preseed_assignments[name.strip()] = recipient.strip()
    return preseed_assignments

def main():
    debug = False
    secret_santa_assigns = {}
    last_year_assigns = {}
    other_year_assigns = {}
    other_other_year_assigns = {}

    parser = ap.ArgumentParser(prog='secret_santa.py', description='Secret Santa list randomizer and emailer. Provide a CSV with columns for "name" and "email" and it will pair two names randomly with no dupes or collisions, and then email all participants their assigned giftee.')
    parser.add_argument("-f", "--file", help="input file, names and emails")
    parser.add_argument("-o1", "--old1", required=False, help="last year's table")
    parser.add_argument("-o2", "--old2", required=False, help="table from 2 years ago")
    parser.add_argument("-o3", "--old3", required=False, help="table from 3 years ago")
    parser.add_argument("-d", "--debug", action="store_true", help="increase output verbosity; print list of gifters/recipients; send no emails")
    parser.add_argument("-e", "--email", help="email address to send secret santa notices from")
    parser.add_argument("-p", "--password", help="application-specific password for gmail SMTP access")
    parser.add_argument("-s", "--preseed", required=False, help="pre-seeded name/recipient pairings in the format 'name1:recipient1,name2:recipient2,...'")

    args = parser.parse_args()

    if args.debug:
        debug = True

    if args.preseed:
        print("Naughty Santa Mode engaged")
        secret_santa_preseed = parse_preseed(args.preseed)
        if debug:
            print("Pre-seeded assignments:", secret_santa_preseed)

    # Seed the random number generator
    random.seed(time.time())

    # Read the CSV file and store the name and email in a dictionary
    participants = {}
    with open(args.file) as csvfile:
        reader0 = csv.DictReader(csvfile)
        for row in reader0:
            participants[row['Name']] = row['Email']

    if args.old1:
        with open(args.old1) as csvfile:
            reader1 = csv.DictReader(csvfile)
            for row in reader1:
                last_year_assigns[row['Name']] = row['Giftee']
            print("last year:", last_year_assigns)

    if args.old2:
        with open(args.old2) as csvfile:
            reader2 = csv.DictReader(csvfile)
            for row in reader2:
                other_year_assigns[row['Name']] = row['Giftee']
            print("two years ago:", other_year_assigns)

    if args.old3:
        with open(args.old3) as csvfile:
            reader3 = csv.DictReader(csvfile)
            for row in reader3:
                other_other_year_assigns[row['Name']] = row['Giftee']
            print("three years ago:", other_other_year_assigns)

    iter_count = 0
    collisions = True
    while collisions:
        iter_count = iter_count+1
        print("Randomizing.... Attempt", iter_count)
        secret_santa_assigns = secret_santa_shuffle(participants, secret_santa_preseed, args.debug)
        collisions = secret_santas_collide(secret_santa_assigns, last_year_assigns, other_year_assigns, other_other_year_assigns, args.debug)
    
    if args.debug:
        print("Your theoretical assignment list:")
        for name in secret_santa_assigns.keys():
            print(participants[name], name + ', your secret santa recipient is inside', "Your gift goes to: " + secret_santa_assigns[name])

    if not args.debug:
        yag = yagmail.SMTP(args.email, args.password)
        for name in secret_santa_assigns.keys():
            yag.send(participants[name], name + ', your secret santa recipient is inside', "Your gift goes to: " + secret_santa_assigns[name])

    if args.debug:
        print("Final assignments:")
        pprint(secret_santa_assigns)

if __name__ == "__main__":
    main()

