1. Add .babelrc for mocha test compile babel
run :  mocha --compilers js:babel-register --recursive
2 Errror : warning: LF will be replaced by CRLF 
run : git config core.autocrlf true
3. UNABLE_TO_VERIFY_LEAF_SIGNATURE (npm install)
run : npm config set strict-ssl false
4. install sublime3 on linux 
http://software-engineer.gatsbylee.com/how-to-install-sublime-3-on-centos-7-rhel-7/
5. can not pull on git (Peer's Certificate issuer is not recognized)
run: env GIT_SSL_NO_VERIFY=true git pull
6. Permission Directory on Linux
run: chmod -R 777 "Directory"
7. Add Path on linux
run : PATH=$PATH:/data/myscripts  / export PATH / echo $PATH
8. set API server (JS,Python)
- process.env.API_SERVER 
- import os, subprocess
os.environ['ATESTVARIABLE'] = 'value'
value = subprocess.check_output('echo $ATESTVARIABLE', shell=True)
assert 'value' in value
9. set env 
- linux : export API_SERVER=localhost:8989
- windows : set API_SERVER=localhost:8989
- MAC : API_SERVER=localhost:8989
10. jenkins (git push and triggered build)
- Jenkins set and github add plugin
11. get super user in linux
- su - then passwd
12. git push cancel
- git push -f origin +master
