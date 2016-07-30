import sys
import json
from pprint import pprint

data_mtype_fn = 'data_mtype.json'
data_ptype_fn = 'data_ptype.json'

with open(data_mtype_fn) as mfile:
  mdata = json.load(mfile)
with open(data_ptype_fn) as pfile:
  pdata = json.load(pfile)

if len(sys.argv) < 2:
  print "usage: " + sys.argv[0] + " fileout"
  sys.exit()
out_fn=sys.argv[1]
outfile = open(out_fn, 'w')

print("len(mdata):" + str(len(mdata)))

for pentry in pdata:
  #for mkey in pentry["Quick Attacks"]:
  for mkey in pentry["Quick Moves"]:
    for mentry in mdata:
      if mentry["ID"] == mkey and mentry.get("Power") and mentry.get("Duration (ms)"):
        pwr = mentry["Power"]
        dur = mentry["Duration (ms)"]/1000.0
        power_per_sec = pwr/dur
        multip = 1.0
        for ptype in pentry["Types"]:
          if ptype == mentry["Type"]:
            multip = 1.25
        power_per_sec = power_per_sec*multip

        att_goodness = pentry["Base Attack"]*power_per_sec/100.0
        def_goodness = pentry["Base Defense"]*pentry["Base Stamina"]/1000.0
        print(str(pentry["PkMn"]))
        print(str(pentry["Name"]))
        print(str(mentry["Name"]))
        print(str(att_goodness))
        print(str(def_goodness))
        lineOut = str(pentry["PkMn"]) + "," + str(pentry["Name"]) + "," + str(mentry["Name"]) + "," + str(att_goodness) + "," + str(def_goodness) + "\n"
        outfile.write(lineOut)

