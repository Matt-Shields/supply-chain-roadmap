criteria = {
'Blade': {
'Area':80,
'Quayside': 120,
'Draft': 6,
'Bearing': 15,
'Air Draft': 25,
},
'Nacelle': {
'Area':40,
'Quayside': 500,
'Draft': 10,
'Bearing': 15,
'Air Draft': 25,
},
'Tower': {
'Area':45,
'Quayside': 150,
'Draft': 10,
'Bearing': 7.5,
'Air Draft': 25,
},
'Monopile': {
'Area':100,
'Quayside': 500,
'Draft': 8,
'Bearing': 12,
'Air Draft': 25,
},
'Jacket': {
'Area':80,
'Quayside': 150,
'Draft': 8,
'Bearing': 15,
'Air Draft': 60,
},
'GBF': {
'Area':10,
'Quayside': 500,
'Draft': 10,
'Bearing': 15,
'Air Draft': 250,
},
'Cable': {
'Area':45,
'Quayside': 150,
'Draft': 6,
'Bearing': 15,
'Air Draft': 50,
},
'Transition piece': {
'Area':50,
'Quayside': 500,
'Draft': 10,
'Bearing': 15,
'Air Draft': 40,
},
'Steel plate': {
'Area':300,
'Quayside': 500,
'Draft': 10,
'Bearing': 15,
'Air Draft': 25,
},
'Flange': {
'Area':50,
'Quayside': 150,
'Draft': 6,
'Bearing': 15,
'Air Draft': 25,
},
'Bedplate': {
'Area':50,
'Quayside': 150,
'Draft': 6,
'Bearing': 15,
'Air Draft': 25,
},
}

upgrade_costs = {
'permit_design': 100,
'laydown': 100,
'quayside': 50,
'dredge': 100,
'bearing': 50
}

upgrade_time = 3

exceptions = {
'Laydown': ['Arthur Kill Terminal']
}

scenario ={
'Portsmouth Marine Terminal': {'Component': 'Blade', 'Factory': 'SGRE'},
'General Cargo Terminal at Port of Wilmington': {'Component': 'Blade', 'Factory': 'Blade 1'},
'Newport News Marine Terminal' : {'Component': 'Blade', 'Factory': 'Blade 2'},
'New Jersey Wind Port' : {'Component': 'Blade', 'Factory': 'Blade 3'},
'New Jersey Wind Port' : {'Component': 'Nacelle', 'Factory': 'GE'},
'New Jersey Wind Port' : {'Component': 'Nacelle', 'Factory': 'Vestas'},
'New Jersey Wind Port' : {'Component': 'Nacelle', 'Factory': 'Nacelle 1'},
}
