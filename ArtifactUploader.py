import os, glob, subprocess, pathlib, shlex, zipfile, argparse, configparser

url='https://pkgs.dev.azure.com/organization/feedname/_packaging/feedname/maven/v1'
repoId = 'repo'

# Arg parsing 
argParser = argparse.ArgumentParser()
argParser.add_argument("file", help="Full file path and name")
inpArgs = argParser.parse_args()

# Script will not run without args because of argparse
warFile = inpArgs.file

with zipfile.ZipFile(warFile, 'r') as zip_ref:
    zip_ref.extractall('./EXTRACTED_WAR')
    
with open('./EXTRACTED_WAR/WEB-INF/classes/Configuration.properties') as f:
    file_content = '[General]\r\n' + f.read()

config_parser = configparser.RawConfigParser()
config_parser.read_string(file_content)

# Determine version from config properties file
version=config_parser.get('General', 'application.buildversion')
os.chdir('./EXTRACTED_WAR/WEB-INF/lib')

for fileName in glob.glob("*.jar"):
    lastDash = fileName.rfind('-')
    artifactId=fileName[:lastDash]
    
    versionId=fileName[lastDash+1:-4]
    currentDir = pathlib.Path().absolute()
    
    cmd = 'mvn deploy:deploy-file -DgroupId=com.adminserver -DartifactId=' + artifactId + ' -Dversion=' + version + ' -DgeneratePom=true -Dpackaging=jar -DrepositoryId=' + repoId + '  -Durl=' + url 
    fullName='-Dfile=' + str(currentDir) + "\\" + fileName
    
    
    if(versionId == version):
        print ("Uploading " + fullName + "... ")
        allCommands = shlex.split(cmd)
        allCommands.append(fullName)
        # print(allCommands)
        subprocess.run(allCommands, shell=True)
