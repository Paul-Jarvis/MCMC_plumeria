#  Script that reads plumeria output and extracts the inportant information

import sys

# Read command-line arguments
RunNumber         = int(sys.argv[1])
output_summaryfile=sys.argv[2]
#print 'Run number = ', RunNumber
#print 'Output summary file =', output_summaryfile

# Give parameters a default "missing number" value
diam           = -9999.0
H_t            = -9999.0
H_nbl          = -9999.0
m_g            = -9999.0
m_w            = -9999.0
mdot           = -9999.0
mdot_solids    = -9999.0
sound_speed    = -9999.0
T_m            = -9999.0
u_exit         = -9999.0
Vdot_nbl       = -9999.0
vent_elevation = -9999.0

#Open output file and read output
with open("output_file.txt","r") as f:
	searchlines = f.readlines()
for i, line in enumerate(searchlines):
	if "Vent diameter (m):" in line:
		string1 = searchlines[i]
		diam = float(string1[46:52])
	if "Maximum height =" in line:
		string1 = searchlines[i]
		H_t = float(string1[52:58])
	if "Neutral buoyancy height =" in line:
		string1 = searchlines[i]
		H_nbl = float(string1[52:58])
	if "Weight fraction gas:" in line:
		string1 = searchlines[i]
		m_g = float(string1[48:53])
	if "Mass fraction water added:" in line:
		string1 = searchlines[i]
		m_w = float(string1[48:53])
	if "Mass flux, (kg/s):" in line:
		string1 = searchlines[i]
		mdot = float(string1[47:56])
	if "mdot_solids =" in line:
		string1 = searchlines[i]
		mdot_solids = float(string1[53:63])
	if "Mixture sound speed (m/s):" in line:
		string1 = searchlines[i]
		sound_speed = float(string1[47:53])
	if "Magma temperature (C):" in line:
		string1 = searchlines[i]
		T_m = float(string1[48:53])
	if "Initial velocity (m/s):" in line:
		string1 = searchlines[i]
		u_exit = float(string1[47:53])
	if "Vdot at nbl" in line:
		string1 = searchlines[i]
		Vdot_nbl = float(string1[53:63])
	if "Vent elevation (m):" in line:
		string1 = searchlines[i]
		vent_elevation = float(string1[47:53])
f.close()

#print out results
#print 'diam = {:6.1f}'.format(diam)
#print 'H_t  = {:8.3f}'.format(H_t)
#print 'H_nbl = {:8.3f}'.format(H_nbl)
#print 'm_g = {:5.3f}'.format(m_g)
#print 'm_w = {:5.3f}'.format(m_w)
#print 'mdot = {:12.4e}'.format(mdot)
#print 'mdot_solids = {:12.4e}'.format(mdot_solids)
#print 'sound_speed = {:6.1f}'.format(sound_speed)
#print 'T_m = {:6.1f}'.format(T_m)
#print 'u_exit = {:6.1f}'.format(u_exit)
#print 'Vdot_nbl = {:12.4e}'.format(Vdot_nbl)
#print 'vent_elevation = {:6.1f}'.format(vent_elevation)

#print to output file
print('Printing to output file')

with open(output_summaryfile,"a") as f2:
	f2.write('{:05d}     {:12.4e}{:8.1f}{:10.1f}  {:7.2f}{:7.2f}{:7.1f}{:10.2f}{:15.1f}{:19.4e}{:9.3f}{:11.3f}{:14.4e}\n' \
        .format(RunNumber,mdot,diam,u_exit,m_w,m_g,T_m,sound_speed,vent_elevation,mdot_solids,H_t,H_nbl,Vdot_nbl))
f2.close()


