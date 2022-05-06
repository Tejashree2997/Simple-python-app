from errno import errorcode
import subprocess
import shlex

#try:
#    x = int(input("Please enter a number:\n"))
#    
#except ValueError:
#    print("Oops!  That was no valid number.  Try again...")
#
#else:
#    print("You entered number is", x)

try:
    #subprocess.check_output(shlex.split(f"./demo.sh"))
    me = subprocess.run(["demo.sh",
				"capture_output=True"], shell=True)
    print(me)
except:
    print("An error occured..!")

else:
    print("Script ran Successfull")
    