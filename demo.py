import subprocess
import shlex

# If your shell script has shebang,
# you can omit shell=True argument.
me = subprocess.run(["demo.sh",
				"capture_output=True"], shell=True)

#me = subprocess.check_output(shlex.split(f"./demo.sh"))
print(me)