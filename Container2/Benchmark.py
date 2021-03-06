import os
import stat

def prepare_exp(SSHHost, SSHPort, REMOTEROOT, optpt):
    f = open("config", 'w')
    f.write("Host benchmark\n")
    f.write("   Hostname %s\n" % SSHHost)
    f.write("   Port %d\n" % SSHPort)
    f.write("   User ubuntu\n")
    f.write("   IdentityFile ~/.ssh/sshcontainerkey\n")
    f.write("   StrictHostKeyChecking no\n")
    f.close()
    

    f = open("run-experiment.sh", 'w')
    f.write("#!/bin/bash\n")
    f.write("set -x\n\n")
    
    f.write("ssh -F config benchmark \"nohup memcached -u ubuntu -p 11211 -P memcached.pid > memcached.out 2> memcached.err &\"\n") # adjust this line to properly start memcached
    
    f.write("RESULT=`ssh -F config benchmark \"pidof memcached\"`\n")

    f.write("sleep 5\n")

    f.write("if [[ -z \"${RESULT// }\" ]]; then echo \"memcached process not running\"; CODE=1; else CODE=0; fi\n")
        
    f.write("mcperf --num-calls=%d --num-conns=%d --call-rate=%d -s %s &> stats.log\n\n" % ( optpt["noRequests"]*2, optpt["concurrency"],optpt["noRequests"], SSHHost)) #adjust this line to properly start the client
    
    f.write("RESPERSEC=`cat stats.log | head -11l | tail -1l | cut -d \" \" -f 3`\n")
    f.write("REQPERSEC=`cat stats.log | head -8l | tail -1l | cut -d \" \" -f 3`\n")
    f.write("LATENCY=`cat stats.log | head -13l | tail -1l | cut -d \" \" -f 5`\n")

    f.write("echo \"$LATENCY\"\n")

    f.write("ssh -F config benchmark \"sudo kill -9 $(cat memcached.pid)\"\n")

    f.write("echo \"requests latency responses\" > stats.csv\n")
    f.write("echo \"$REQPERSEC $LATENCY $RESPERSEC\" >> stats.csv\n")
    
    f.write("scp -F config benchmark:~/memcached.* .\n")

    f.write("if [[ $(wc -l <stats.csv) -le 1 ]]; then CODE=1; fi\n\n")
    
    f.write("exit $CODE\n")

    f.close()
    
    os.chmod("run-experiment.sh", stat.S_IRWXU)
