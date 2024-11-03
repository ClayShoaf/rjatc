import streamlit as st
import functions as f

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

class xfmr():
    def __init__(self, phase=2, wye_prim=False, wye_sec=False, prim=0, sec=0, kva=0, secondary_protection=True, note_prim=False, note_sec=False):
        self.phase = phase
        self.note_prim = note_prim
        self.note_sec = note_sec
        self.wye_prim = wye_prim
        self.wye_sec = wye_sec
        self.prim = prim
        self.sec = sec
        self.kva = kva
        self.secondary_protection = secondary_protection

class outputs():
    def __init__(self, t_kva='', t_phase='', t_prim='', t_sec='', t_ocpd=''):
        self.t_kva = t_kva
        self.t_phase = t_phase
        self.t_prim = t_prim
        self.t_sec = t_sec
        self.t_ocpd = t_ocpd

if 'tranny' not in st.session_state:
    st.session_state.tranny = xfmr()
if 'o' not in st.session_state:
    st.session_state.o = outputs()

tranny = st.session_state.tranny
o = st.session_state.o

if st.button("Generate Transformer"):
    tranny.wye_prim = False
    tranny.wye_sec = False
    tranny = f.get_tranny(tranny)
    tranny.note_sec = False
    tranny.note_prim = False

    o.t_kva = f"{tranny.kva} kVA"

    if tranny.phase == 3:
        o.t_phase = "Three phase"

        if tranny.wye_prim:
            o.t_prim = f"Primary: {tranny.prim[0]}Y/{tranny.prim[1]}V"
        else:
            o.t_prim = f"Primary: {tranny.prim}V"

        if tranny.wye_sec:
            o.t_sec = f"Secondary: {tranny.sec[0]}Y/{tranny.sec[1]}V"
        else:
            o.t_sec = f"Secondary: {tranny.sec}V"

    elif tranny.phase == 1:
        o.t_phase = "Single phase"
        o.t_prim = f"Primary: {tranny.prim}V"
        o.t_sec = f"Secondary: {tranny.sec}V"

    if tranny.secondary_protection:
        o.t_ocpd = "Primary and secondary OCPD protection"
    else:
        o.t_ocpd = "Primary only OCPD protection"

st.write('# Transformer')
st.text(f"{o.t_kva}\n{o.t_phase}\n{o.t_prim}\n{o.t_sec}\n{o.t_ocpd}")

if st.button("Solve"):
    tranny, amps_p, amps_s, ocpd_p, ocpd_s = f.get_ocpd(tranny)
    wire_p, wire_s = f.get_wire(ocpd_p, ocpd_s)
    egc = f.get_egc(ocpd_p)
    ######### NEEDS TO BE FIXED! WE STILL NEED WIRES ON THE SECONDARY! ##############
    if tranny.secondary_protection:
        ssbj = f.get_ssbj(wire_s)
    else:
        ssbj = "N/A"
    pipe_p = ""
    pipe_s = ""

    output = f"\
Primary Amps: {amps_p}\n\
Secondary Amps: {amps_s}\n\
Primary OCPD: {ocpd_p}A\n\
Secondary OCPD: {ocpd_s}A\n\
Primary Wire: {wire_p}\n\
Secondary Wire: {wire_s}\n\
EGC: {egc}\n\
SSBJ: {ssbj}\n\
Primary Conduit: {pipe_p}\n\
Secondary Conduit: {pipe_s}\n"
    st.text(output)

    if tranny.note_prim:
        st.info("Note 1 applies to primary")
    if tranny.note_sec:
        st.info("Note 1 applies to secondary")
    

#st.write(tranny)
