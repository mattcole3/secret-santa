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

    if debug:
        print(names)
        print(recipients)
    random.shuffle(names)
    random.shuffle(recipients)

    # Assign gift recipients
    assignments = {}
    for i, name in enumerate(names):
        if debug:
            print("i is", i, "name is ", name, "recipient is", recipients[i] )
        assignments[name] = recipients[i]

    return assignments

def secret_santas_collide(secret_santa_assigns, debug):
    for name in secret_santa_assigns.keys():
        if debug:
            print(name, secret_santa_assigns[name])
        if name == secret_santa_assigns[name]:
            return True
    return False
        
        

def main():
    debug = False
    secret_santa_assigns = {}

    parser = ap.ArgumentParser(prog='secret_santa.py', description='Secret Santa list randomizer and emailer. Provide a CSV with columns for "name" and "email" and it will pair two names randomly with no dupes or collisions, and then email all participants their assigned giftee.')
    parser.add_argument("-f", "--file", help="input file, names and emails")
    parser.add_argument("-d", "--debug", action="store_true", help="increase output verbosity; print list of gifters/recipients; send no emails")
    parser.add_argument("-e", "--email", required=True, help="email address to send secret santa notices from")
    parser.add_argument("-p", "--password", required=True, help="application-specific password for gmail SMTP access")
    args = parser.parse_args()

    # Read the CSV file and store the name and email in a dictionary
    participants = {}
    with open(args.file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if args.debug:
                print("new row")
                print(row)
            participants[row['Name']] = row['Email']

    if debug:
        print("Participant list as read in")
        print(participants)

    iter_count = 0
    collisions = True
    while collisions:
        iter_count = iter_count+1
        print("Randomizing.... Attempt", iter_count)
        secret_santa_assigns = secret_santa(participants, args.debug)
        collisions = secret_santas_collide(secret_santa_assigns, args.debug)


    if args.debug:
        print("Here is the assignment dict")
        print(secret_santa_assigns)
        print("---")
        for name in secret_santa_assigns.keys():
            print(participants[name], name + ', your secret santa recipient is inside', "Your gift goes to: " + secret_santa_assigns[name])
        
    if not args.debug:
        yag = yagmail.SMTP(args.email, args.password)
        for name in secret_santa_assigns.keys():
            yag.send(participants[name], name + ', your secret santa recipient is inside', "Your gift goes to: " + secret_santa_assigns[name])

    return

if __name__ == "__main__":
    main()

