#!/usr/bin/env python3

import pandas as pd
import numpy as np
import argparse as ap
import smtplib, ssl, getpass
import yagmail

def main():
    parser = ap.ArgumentParser(description='Secret Santa')
    parser.add_argument("-f", "--file", help="input file, names and emails", type=ap.FileType('r'))
    parser.add_argument("-v", "--verbosity", action="store_true", help="increase output verbosity")
    parser.add_argument("-e", "--email", help="email address to send secret santa notices from")
    args = parser.parse_args()
    #if args.verbosity:
    #    print(args.file.readlines())
    in_data = get_list(args)

    if args.verbosity:
        print("---")
        in_data.info()
        print("xxx")
        print(in_data.count())

    shuffled_list = in_data.sample(frac=1).reset_index(drop=True)
    recips = shuffled_list.iloc[:,0]
    length = recips.count()

    if args.verbosity:
        print("---")
        shuffled_list.info()
        print("***")
        print(recips)

    password = getpass.getpass(prompt='Password: ', stream=None)

    if args.verbosity:
        print("###")
        print(length)
        for idx, row in shuffled_list.iterrows():
            print(idx, row['Name'], row['Email'], recips[(idx+1)%length])

    if not args.verbosity:
        yag = yagmail.SMTP(args.email)
        for idx, row in shuffled_list.iterrows():

            yag.send(row['Email'], 'Your secret santa recipient is inside', "Your gift goes to: " + recips[(idx+1)%length])

    return

def get_list(args):
    df = pd.read_csv(args.file, header=0)
    dataset = (df[['Name', 'Email']])

    if args.verbosity:
        print("---")
        print(dataset)
    return(dataset)

if __name__ == "__main__":
    main()

