##########################################
#
# this is admittedly brutal code, a total quickie....
#
# this reads two hardcoded DS18B20 1-wire sensors
# and the Pi motherboard temperatures
# and seeds a horrid web page on the local system
#
# to run, basically do something like:
#     python foo.py > /pathname/filename.html
# via cron every so often...
#
# FWIW, I call it every 5 minutes
#
##########################################

# most of this is copied/derived_from
# from https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/#step-four
#
from subprocess import *
from time import sleep, strftime
from datetime import datetime


print '<html><head><title="Pi temperatures"/></head><body><h2>Pi temperatures</h2><p/>'
print "<head4>"
print datetime.now().strftime('%b %d  %H:%M:%S\n')
print "</head4>"
print "<p>"
print "<dl><dd>"
print '<table>'
devices=["28-000005ab3d0c","28-000005bbe53e"]
for d in devices:
	filename="/sys/bus/w1/devices/" + d + "/w1_slave"
	tfile=open(filename)
	code=tfile.read()
	tfile.close()
	linetwo=code.split("\n")[1]
	tempdata=linetwo.split(" ")[9]
	temp=float(tempdata[2:])
	tempF=temp/1000 * 9/5 + 32
	print '<tr>'
	print ("<td>sensor %s</td>") % (d)
	print "<td>=</td>"
	print ("<td>%4.2f F</td>") % (tempF)
	print '</tr>'

#
# get the mobo temp
#
cmd="/opt/vc/bin/vcgencmd measure_temp"

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

mobotemp = run_cmd(cmd)
mobotemp=mobotemp.split("=")[1]
mobotemp=mobotemp.split("'")[0]
mobotemp=float(mobotemp)*9/5 + 32.00
print '<tr>'
print "<td>motherboard</td>"
print "<td>=</td>"
print ("<td>%4.2f F") % (mobotemp)
print '</tr>'
print '</table>'
print "</dd></dl>"

print '</body></html>'

