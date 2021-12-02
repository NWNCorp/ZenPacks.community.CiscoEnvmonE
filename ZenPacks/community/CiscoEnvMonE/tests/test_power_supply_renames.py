import re


OTHER_EXAMPLES = [
    'Switch 1 Power Supply 4',
    'Switch 1 Power Supply 1',
    'Switch 1 Power Supply 2',
    'Switch 1 Power Supply 3',
    'Unknown',
    'Switch 7 - Power Supply B, Normal',
    'Switch 4 - Power Supply A, Shutdown',
    'Switch 6 - Power Supply B, Normal',
    'Switch 1 - Power Supply B, NotExist',
    'C2921/C2951 AC Power Supply',
    'Switch 1 - Power Supply A, Normal',
    'C2911 AC Power Supply',
    'VG3X0 AC Power Supply',
    '12V System PS',
    'chassis-2 Power Supply 2, C6880-',
    'C2921/C2951 DC Power Supply',
    'Switch 1 - Power Supply B, Normal',
    'Switch 5 - Power Supply B, NotExist',
    '3.3V  Supply',
    'Switch 2 - Power Supply B, Shutdown',
    'Switch 6 - Power Supply B, NotExist',
    'Power supply',
    'Switch 6 - Power Supply A, Normal',
    'Switch 3 - Power Supply B, NotExist',
    'Main Power Supply',
    'Switch 4 - Power Supply A, Normal',
    'Switch 2 - Power Supply B, NotExist',
    'Switch 8 - Power Supply B, Normal',
    '1.5V  Supply',
    'Switch 4 - Power Supply A, NotExist',
    'Switch 8 - Power Supply A, Normal',
    'C1941/C2901 AC Power Supply',
    'Switch 1 - Power Supply A, Shutdown',
    '0.75V Supply',
    'Switch 5 - Power Supply B, Normal',
    'Switch 2 - Power Supply B, Normal',
    '5V    Supply',
    '12AV  Supply',
    'chassis-1 Power Supply 2, C6880-',
    '1.8V  Supply',
    'Sw2, PS1 Normal',
    'Switch 7 - Power Supply A, Normal',
    'C3900 DC Power Supply 1',
    'Switch 3 - Power Supply A, Normal',
    'Switch 2 - Power Supply A, Normal',
    'Sw1, PS1 Normal',
    'C3900 Unknown Power Supply 2',
    'Switch 2 Power Supply Module 4',
    'Switch 2 Power Supply Module 1',
    'Switch 2 Power Supply Module 2',
    'Switch 2 Power Supply Module 3',
    'Switch 3 - Power Supply A, NotExist',
    'Switch 2 - Power Supply A, Shutdown',
    'Switch 1 Power Supply Module 3',
    'Switch 1 Power Supply Module 2',
    'Switch 1 Power Supply Module 1',
    'Switch 1 Power Supply Module 4',
    'Switch 1 - Power Supply B, Shutdown',
    'Switch 2 Power Supply 4',
    'Switch 2 Power Supply 1',
    'chassis-1 Power Supply 1, C6880-',
    'Switch 2 Power Supply 3',
    'Switch 2 Power Supply 2',
    'Switch 4 - Power Supply B, Normal',
    'Switch 3 - Power Supply B, Normal',
    '1.2V  Supply',
    'C3900 DC Power Supply 2',
    'chassis-2 Power Supply 1, C6880-',
    'C3900 AC Power Supply 1',
    'C3900 AC Power Supply 2',
    'Switch 3 - Power Supply A, Shutdown',
    'Switch 5 - Power Supply A, Normal',
    'Switch 1 - Power Supply A, NotExist',
    'AC Power Supply',
    '1.05V Supply',
    'Switch 2 - Power Supply A, NotExist',
    '1V    Supply',
    'Switch 4 - Power Supply B, NotExist',
    'Redundant Power Supply',
    '2.5V  Supply',
    'VG350 Unknown Power Supply 1',
    'Sw2, PS2 Normal',
    'VG350 AC Power Supply 1',
    'VG350 AC Power Supply 2',
    '48V System PS',
    'Sw1, PS2 Normal',
    'Unknown-(probable IOS bug)',
]

RPS_EXAMPLES = [
    'Sw5, PS1 Normal, RPS NotExist',
    'Sw3, PS1 Normal, RPS NotExist',
    'Switch#1, PowerSupply#1, Status is Normal, RPS Not Present',
    'Sw1, PS2 Normal, RPS NotExist',
    'Sw4, PS2 Normal, RPS NotExist',
    'Sw4, PS1 Normal, RPS NotExist',
    'Sw3, PS2 Normal, RPS NotExist',
    'Sw7, PS1 Normal, RPS NotExist',
    'Sw1, PS1 Normal, RPS NotExist',
    'Sw2, PS1 Normal, RPS NotExist',
    'Sw6, PS1 Normal, RPS NotExist',
    'Sw2, PS2 Normal, RPS NotExist',
]

RPS_RE = '(.*?),\s(PS\d|PowerSupply#\d).*'
PS_RE = '(.*?),\s(PS\d)'

_f = open('test_power_supply_results.txt', 'w')
_f.write("new\told\n")
RPS_EXAMPLES.extend(OTHER_EXAMPLES)

for name in RPS_EXAMPLES:
    old = name
    if name.count(',') > 1:
        m = re.search(RPS_RE, name)
        if m:
            name = ' - '.join(m.groups())
    else:
        m = re.search(PS_RE, name)
        if m:
            name = ' - '.join(m.groups())
        else:
            name = name.split(',')[0] if ',' in name else name
    _f.write("%s\t%s\n" % (name, old))

_f.close()