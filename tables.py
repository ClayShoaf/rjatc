voltages = [120,208,240,277,347,415,480,600]
wye = [208,415,480,600]
volts = [120,240,277,347]
phases = [1,3]
# 240.6(A) and Table 240.6(A)
standard_ocpd = [1,3,6,10,15,20,25,30,35,40,45,50,60,70,80,90,100,110,125,150,175,200,225,250,300,350,400,450,500,600,700,800,1000,1200,1600,2000,2500,3000,4000,5000,6000]
# Table 310.16
thwn_amps = {
    '14': 20,
    '12': 25,
    '10': 35,
    '8': 50,
    '6': 65,
    '4': 85,
    '3': 100,
    '2': 115,
    '1': 130,
    '1/0': 150,
    '2/0': 175,
    '3/0': 200,
    '4/0': 230,
    '250': 255,
    '300': 285,
    '350': 310,
    '400': 335,
    '500': 380,
    '600': 420,
    '700': 460,
    '750': 475,
    '800': 490,
    '900': 520,
    '1000': 545,
    '1250': 590,
    '1500': 625,
    '1750': 650,
    '2000': 665,
}
# Table 450.3(B)
p_only = [1.25,1.67,3.,-1,-1]
p_and_s = [2.5,2.5,2.5,1.25,1.67]