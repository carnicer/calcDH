#!/bin/python3

import sys
import getopt
#import sympy


# default values
g_val_p = 199
g_val_g = 5
g_val_s = 0 # invalid value


def usage() :

    # TODO : have a self-usage from embedded script doc
    print("")
    print("Diffie-Hellman secret number generator")
    print("")
    print("Usage:")
    print("-h / --help: display this message")
    print("-p / --prime: set the prime number (optional)")
    print("-g / --generator: set the \'generator\' number (optional)")
    print("-s / --secret: set the secret number")
    print("The prime number must be prime (not checked by now), and quite high (>128) (default=199).")
    print("The generator number must be smaller than the prime number, and smaller than 100 (default=5).")
    print("Both the prime and generator numbers are public and known by everybody, and have to be agreed by you & your peer in advance.")
    print("Your secret number can not be shared, even with your peer. It shall also be smaller than 64 and larger than 10.")
    print("")

def parseInt(textNumber) :
    try: val = int(textNumber)
    except:
      usage()
      print("FATAL: %s is not an integer number" % textNumber)
      sys.exit(3)
    return val


def processOptions(cliArgsList) :

    textLongOptions = ["help", "prime=", "generator=", "secret="]
    selectors = 0
    print("processOptions, CLI args:", cliArgsList)
    try:
      opts, args = getopt.getopt(cliArgsList, "hp:g:s:", ["help", "prime=", "generator=", "secret="])
    except getopt.GetoptError as err:
      print("FATAL: %s" % err)  # will print something like "option -a not recognized"
      usage()
      sys.exit(2)

    global g_val_p, g_val_g, g_val_s
    for opt, arg in opts :
      if opt == "-h" or opt == textLongOptions[0] :
        usage()
        sys.exit(0)
      elif opt == "-p" or opt == textLongOptions[1][:-1] :
        g_val_p = parseInt(arg)
      elif opt == "-g" or opt == textLongOptions[2][:-1] :
        g_val_g = parseInt(arg)
      elif opt == "-s" or opt == textLongOptions[3][:-1] :
        g_val_s = parseInt(arg)
      else :
        print("FATAL: %s: wrong option, quitting" % opt)
        usage()
        sys.exit(1)

    return selectors


def checkSecretNumberIsSet() :

    global g_val_s
    if g_val_s == 0 : # not set by CLI params
      print("The secret number has not been set, please enter a value:")
      value = -1
      while value == -1 :
        textNumber = sys.stdin.readline()
        try: value = int(textNumber)
        except:
          print("Please enter a valid integer number")
      g_val_s = value


def checkProperValues() :

    global g_val_p, g_val_g, g_val_s

    print("Checking if the set values are appropiate ...")
    print("checking if the prime number (%d) is prime ... (not implemented yet)" % g_val_p)
    print("checking if the prime number (%d) is large enough (>128) ..." % g_val_p)
    if g_val_p <= 128 :
      print("No, it's not. Quitting ...")
      sys.exit(11)
    print("checking if the generator number (%d) is minor than 100 and less than the prime number ..." % g_val_g)
    if g_val_g >= 100 :
      print("No, it's not. Quitting ...")
      sys.exit(12)
    print("checking if the secret number (%d) is larger than 10 and less than 64 ..." % g_val_s)
    if g_val_s >= 64 or g_val_s <= 10 :
      print("No, it's not. Quitting ...")
      sys.exit(13)
      
    flowConfirm()


def flowConfirm() :

    print("OK?")
    sys.stdin.readline()


def calcDHfirstValue() :

    global g_val_p, g_val_g, g_val_s
    global g_val_1stPre, g_val_1st

    g_val_1stPre = g_val_g ** g_val_s
    g_val_1st = g_val_1stPre % g_val_p


def calcDHsecondValue() :

    global g_val_p, g_val_s
    global g_val_1st_peer
    global g_val_2stPre, g_val_2st

    g_val_2stPre = g_val_1st_peer ** g_val_s
    g_val_2st = g_val_2stPre % g_val_p


def flow() :

    global g_val_p, g_val_g, g_val_s

    print("prime number = %d" % g_val_p)
    print("generator number = %d" % g_val_g)
    print("secret number = %d" % g_val_s)
    flowConfirm()

    print("OK, then now calculate the modulus with the prime number of the generator (%d) powered to the secret number (%d)" % (g_val_g, g_val_s))
    flowConfirm()

    calcDHfirstValue()
    global g_val_1stPre, g_val_1st
    print("I've done it too, I get: %d (power = %d)" % (g_val_1st, g_val_1stPre))
    flowConfirm()

    print("Now give this value (%d) to your peer, and ask them what value they've got." % g_val_1st)
    flowConfirm()

    print("Please enter the 1st value they have calculated:")
    value = -1
    while value == -1 :
      textNumber = sys.stdin.readline()
      try: value = int(textNumber)
      except:
        print("Please enter a valid integer number")

    print("OK, then now calculate the modulus with the prime number of the number you have received (%d) powered to the secret number (%d)" % (value, g_val_s))
    flowConfirm()

    global g_val_1st_peer
    g_val_1st_peer = value
    calcDHsecondValue()
    global g_val_2stPre, g_val_2st
    print("I've done it too, I get: %d (power = %d)" % (g_val_2st, g_val_2stPre))
    flowConfirm()

    print("Now you and your peer have obtained a shared secret number (%d) that only you 2 know. Do you want to verify it? (if not, press ctrl-C)" % g_val_2st)
    flowConfirm()

    print("To verify that your shared secret numbers match, CONFIDENTIALLY give this value (%d) to your peer, and CONFIDENTIALLY ask them what 2nd value they've got." % g_val_2st)
    flowConfirm()

    print("Please enter the 2nd value they have calculated:")
    value = -1
    while value == -1 :
      textNumber = sys.stdin.readline()
      try: value = int(textNumber)
      except:
        print("Please enter a valid integer number")

    if value == g_val_2st :
      print("Congrats! You have successfully shared a secret number (%d) with your peer!" % g_val_2st)
    else :
      print("Oooops! So sorry, there must be a mistake or a misunderstanding with your peer. Please try again")



if __name__ == "__main__":

    processOptions(sys.argv[1:])

    checkSecretNumberIsSet()
    checkProperValues()

    flow()

