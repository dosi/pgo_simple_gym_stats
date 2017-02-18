import sys
import json
from pprint import pprint

data_mtype_fn = 'data_mtype_new.json'
data_ptype_fn = 'data_ptype_new_and_last_legacy.json'

with open(data_mtype_fn) as mfile:
  mdata = json.load(mfile)
with open(data_ptype_fn) as pfile:
  pdata = json.load(pfile)

if len(sys.argv) < 2:
  print "usage: " + sys.argv[0] + " fileout [save defender data]"
  print "if the optional econd argument is 0, no defender data is written. By default, it is written"
  sys.exit()
out_fn=sys.argv[1]
outfile = open(out_fn, 'w')
write_defender_data = True
if len(sys.argv) > 2:
  if sys.argv[2] == "0":
    write_defender_data = False

print("len(mdata):" + str(len(mdata)))

lineOut = "PkMn, PokeName, Quick Move Name, Charge Move Name, Attack, Defense, Att*Def, Should use charge, Base Attack, Base Defense, Base Stamina, Quick Move PPS, Charge Move PPS, Charge PPS Active Fraction, Total PPS, IV10%, IV20%, IV30%, IV40%, IV50%, IV60%, IV70%, IV80%, IV90%, IV100%"
if write_defender_data:
  lineOut = lineOut + ", Defender Quick Move PPS, Defender Charge PPS Active Fraction, Defender Total PPS, D_IV0%, D_IV10%, D_IV20%, D_IV30%, D_IV40%, D_IV50%, D_IV60%, D_IV70%, D_IV80%, D_IV90%, D_IV100%"
lineOut = lineOut + "\n"
outfile.write(lineOut)

crit_in_game = False

for pentry in pdata:
  #for mkey in pentry["Quick Attacks"]:
  set_of_quick_moves = set(pentry["Quick Moves"])
  #for mkey in pentry["Quick Moves"]:
  for mkey in set_of_quick_moves:
    for mentry in mdata:
      if mentry["Name"] == mkey and mentry.get("Power") and mentry.get("Duration (ms)"):
        pwr = mentry["Power"]
        dur = mentry["Duration (ms)"]/1000.0
        defender_dur = dur + 2.0
        power_per_sec = pwr/dur
        defender_power_per_sec = pwr/defender_dur
        multip = 1.0
        for ptype in pentry["Types"]:
          if ptype == mentry["Type"]:
            multip = 1.25
        power_per_sec = power_per_sec*multip
        defender_power_per_sec = defender_power_per_sec*multip
        
        set_of_cinematic_moves = set(pentry["Cinematic Moves"])
        #for charge_key in pentry["Cinematic Moves"]:
        for charge_key in set_of_cinematic_moves:
          for charge_move_entry in mdata:
            if charge_move_entry["Name"] == charge_key and charge_move_entry.get("Power") and charge_move_entry.get("Duration (ms)"):
              charge_pwr = charge_move_entry["Power"]
              charge_dur = charge_move_entry["Duration (ms)"]/1000.0
              charge_power_per_sec = charge_pwr/charge_dur
              charge_multip = 1.0
              for ptype in pentry["Types"]:
                if ptype == charge_move_entry["Type"]:
                  charge_multip = 1.25
              charge_power_per_sec = charge_power_per_sec*charge_multip
              print(str(pentry["PkMn"]))
              print(str(pentry["Name"]))
              print(str(mentry["Name"]))
              print(str(charge_move_entry["Name"]))
              #crit_bonus_pps = 0.5*power_per_sec*charge_move_entry["Crit"]
              crit_bonus_pps =0 # no crit in new data, not in game either -> no worries for now
              if not crit_in_game:
                crit_bonus_pps = 0
              charge_power_per_sec = crit_bonus_pps+charge_power_per_sec
              total_power_per_sec = power_per_sec
              should_use_charge = 0
              if charge_power_per_sec > power_per_sec:
                should_use_charge = 1
                # now we need to calculate the fraction of having charge move active
                # that is, calculate the time that it takes to generate needed energy vs the time charge move takes 
                quick_move_energy_per_second = mentry["Energy Delta"]/dur
                quick_move_active = -1.0*(charge_move_entry["Energy Delta"]/quick_move_energy_per_second)
                
                charge_dps_active_fraction = charge_dur/(charge_dur + quick_move_active)
                print(str(charge_dps_active_fraction))
                total_power_per_sec = charge_dps_active_fraction*charge_power_per_sec + (1.0 - charge_dps_active_fraction)*power_per_sec

              # defensive charge move, comp will always use
              defender_quick_move_energy_per_second = mentry["Energy Delta"]/defender_dur
              defender_quick_move_active = -1.0*(charge_move_entry["Energy Delta"]/defender_quick_move_energy_per_second)
              defender_charge_dps_active_fraction = charge_dur/(charge_dur + defender_quick_move_active)
              defender_charge_dodge_multiplier = 0.7 # fraction of damage remaining on average with average player dodging
              defender_total_power_per_sec = defender_charge_dps_active_fraction*charge_power_per_sec*defender_charge_dodge_multiplier +  (1.0 - defender_charge_dps_active_fraction)*defender_power_per_sec


              att_goodness = [0.0]*11
              def_goodness = [0.0]*11
              defender_att_goodness = [0.0]*11
              goodness = [0.0]*11
              defender_goodness = [0.0]*11
              iv_bonus_per_i = 1.5
              for i in range(0,11):
                iv_bonus = iv_bonus_per_i*i
                att_goodness[i] = (pentry["Base Attack"]+iv_bonus)*total_power_per_sec/100.0
                def_goodness[i] = (pentry["Base Defense"]+iv_bonus)*(pentry["Base Stamina"]+iv_bonus)/1000.0
                goodness[i] = att_goodness[i]*def_goodness[i]
                defender_att_goodness[i] = (pentry["Base Attack"]+iv_bonus)*defender_total_power_per_sec/100.0
                defender_goodness[i] = defender_att_goodness[i]*def_goodness[i]

              print(str(att_goodness))
              print(str(def_goodness))
              print(str(defender_att_goodness))
              lineOut = str(pentry["PkMn"]) + "," + str(pentry["Name"]) + "," + str(mentry["Name"]) + "," + str(charge_move_entry["Name"]) + "," + str(att_goodness[0]) + "," + str(def_goodness[0]) + "," + str(goodness[0]) + "," + str(should_use_charge) + "," + str(pentry["Base Attack"]) + "," + str(pentry["Base Defense"]) + "," + str(pentry["Base Stamina"]) + "," + str(power_per_sec) + "," + str(charge_power_per_sec) + "," + str(charge_dps_active_fraction) + "," + str(total_power_per_sec)
              for i in range(1,11):
                lineOut = lineOut + "," + str(goodness[i])
              if write_defender_data:
                lineOut = lineOut + ", " + str(defender_power_per_sec) + ", " + str(defender_charge_dps_active_fraction) + ", " + str(defender_total_power_per_sec) 
                for i in range(0,11):
                  lineOut = lineOut + "," + str(defender_goodness[i])
              lineOut = lineOut + "\n"
              outfile.write(lineOut)

 
              
        











