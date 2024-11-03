import tables as t
import random

def get_volts():
    if random.randint(0,1):
        zipped = []
        for i in zip(t.wye,t.volts):
            zipped.append(i)
        a,b = random.choice(zipped)
        return [a,b], True
    else:
        return random.choice(t.voltages), False

def get_tranny(tranny):
    #tranny.kva = round(random.randint(10,500), -1)
    tranny.kva = random.randint(1,31)
    tranny.phase = random.choice(t.phases)

    if tranny.phase == 3:
        tranny.prim, tranny.wye_prim = get_volts()
        tranny.sec, tranny.wye_sec = get_volts()
        while tranny.prim == tranny.sec:
            tranny.sec, tranny.wye_sec = get_volts()
    elif tranny.phase == 1:
        tranny.prim = random.choice(t.voltages)
        tranny.sec = random.choice(t.voltages)
        while tranny.prim == tranny.sec:
            tranny.sec = random.choice(t.voltages)

    if tranny.wye_prim or tranny.wye_sec:
        tranny.secondary_protection = True
    else:
        gacha = random.random()
        if gacha < 0.7:
            tranny.secondary_protection = False
        else:
            tranny.secondary_protection = True
    return tranny

def get_amps(volts, tranny):
    if tranny.phase == 3:
        amps = (tranny.kva * 1000)/(volts * 1.73)
    else:
        amps = (tranny.kva * 1000)/(volts)

    return amps
    
def picker(amps, up_down):
    if up_down == 'up':
        for idx,i in enumerate(t.standard_ocpd):
            if i > amps:
                return i
    if up_down == 'down':
        for idx,i in enumerate(t.standard_ocpd):
            if i > amps:
                return t.standard_ocpd[idx-1]

def choose_ocpd(amps, is_primary, tranny):
    if is_primary:
        if tranny.secondary_protection:
            if amps >= 9:
                amps = amps*t.p_and_s[0]
                ocpd = picker(amps, 'down')
            elif 9 > amps >= 2:
                amps = amps*t.p_and_s[1]
                ocpd = picker(amps, 'down')
            else:
                amps = amps*t.p_and_s[2]
                ocpd = picker(amps, 'down')
        else:
            if amps >= 9:
                amps = amps*t.p_only[0]
                ocpd = picker(amps, 'up')
                tranny.note_prim = True
            elif 9 > amps >= 2:
                amps = amps*t.p_only[1]
                ocpd = picker(amps, 'down')
            else:
                amps = amps*t.p_only[2]
                ocpd = picker(amps, 'down')
    else:
        if amps >= 9:
            amps = amps*t.p_and_s[3]
            ocpd = picker(amps, 'up')
            tranny.note_sec = True
        else:
            amps = amps*t.p_and_s[4]
            ocpd = picker(amps, 'down')
            tranny.note_sec = False
    return ocpd, tranny

def get_ocpd(tranny):
    if type(tranny.prim) == list:
        amps_p = get_amps(tranny.prim[0], tranny)
    else:
        amps_p = get_amps(tranny.prim, tranny)
    if type(tranny.sec) == list:
        amps_s = get_amps(tranny.sec[0], tranny)
    else:
        amps_s = get_amps(tranny.sec, tranny)

    if tranny.secondary_protection:
        ocpd_p, tranny = choose_ocpd(amps_p, True, tranny)
        ocpd_s, tranny = choose_ocpd(amps_s, False, tranny)
        return tranny, amps_p, amps_s, ocpd_p, ocpd_s
    else:
        ocpd_p, tranny = choose_ocpd(amps_p, True, tranny)
        return tranny, amps_p, "N/A", ocpd_p, "N/"

def get_wire(ocpd_p, ocpd_s):
    wire_p = ""
    wire_s = ""
    for i in t.thwn_amps.items():
        if i[1] >= ocpd_p:
            wire_p = i[0]
            break
    for i in t.thwn_amps.items():
        if ocpd_s == "N/":
            wire_s = "N/A"
            break
        if i[1] >= ocpd_s:
            wire_s = i[0]
            break
    return wire_p, wire_s

def get_egc(ocpd_p):
    for k,v in t.egc_size.items():
        if k >= ocpd_p:
            return v

def get_ssbj(wire_s):
    return t.ssbj_size[str(wire_s)]
