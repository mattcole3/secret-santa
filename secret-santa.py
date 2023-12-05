#!/usr/bin/env python3

import argparse as ap
import csv
import random
import smtplib, ssl, getpass
import yagmail

def secret_santa(participants, debug):
    # Shuffle the list of participants to randomly assign gift recipients
    names = list(participants.keys())
    recipients = list(participants.keys())

    random.shuffle(names)
    random.shuffle(recipients)

    # Assign gift recipients
    assignments = {}
    for i, name in enumerate(names):
        if debug:
            print("i is", i, "name is ", name, "recipient is", recipients[i] )
        assignments[name] = recipients[i]

    return assignments

def secret_santas_collide(secret_santa_assigns, year1, year2, debug):
    for name in secret_santa_assigns.keys():
        if debug:
            print(name, secret_santa_assigns[name])
        if name == secret_santa_assigns[name]:
            return True
        if secret_santa_assigns[name] == year1[name]:
            return True
        if secret_santa_assigns[name] == year2[name]:
            return True            
    return False
        
        

def main():
    debug = False
    secret_santa_assigns = {}
    last_year_assigns = {}
    other_year_assigns = {}

    parser = ap.ArgumentParser(prog='secret_santa.py', description='Secret Santa list randomizer and emailer. Provide a CSV with columns for "name" and "email" and it will pair two names randomly with no dupes or collisions, and then email all participants their assigned giftee.')
    parser.add_argument("-f", "--file", help="input file, names and emails")
    parser.add_argument("-o1", "--old1", required=False, help="last year's table")
    parser.add_argument("-o2", "--old2", required=False, help="table from 2 years ago")
    parser.add_argument("-d", "--debug", action="store_true", help="increase output verbosity; print list of gifters/recipients; send no emails")
    parser.add_argument("-e", "--email", help="email address to send secret santa notices from")
    parser.add_argument("-p", "--password", help="application-specific password for gmail SMTP access")
    args = parser.parse_args()

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
            print("2022:", last_year_assigns)

    if args.old2:
        with open(args.old2) as csvfile:
            reader2 = csv.DictReader(csvfile)
            for row in reader2:
                other_year_assigns[row['Name']] = row['Giftee']
            print("2021", other_year_assigns)

    iter_count = 0
    collisions = True
    while collisions:
        iter_count = iter_count+1
        print("Randomizing.... Attempt", iter_count)
        secret_santa_assigns = secret_santa(participants, args.debug)
        collisions = secret_santas_collide(secret_santa_assigns, last_year_assigns, other_year_assigns, args.debug)


    if args.debug:
        print("Your theoretical assignment list:")
        for name in secret_santa_assigns.keys():
            print(participants[name], name + ', your secret santa recipient is inside', "Your gift goes to: " + secret_santa_assigns[name])
        
    if not args.debug:
        yag = yagmail.SMTP(args.email, args.password)
        for name in secret_santa_assigns.keys():
            yag.send(participants[name], name + ', your secret santa recipient is inside', "Your gift goes to: " + secret_santa_assigns[name])

    return

if __name__ == "__main__":
    main()

