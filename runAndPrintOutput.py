import subprocess
def runAndPrintOutput(arrayCommand:list):
    result = subprocess.run(arrayCommand, shell=False, text=True, stderr=subprocess.STDOUT, check=False).stdout
    print(result)
