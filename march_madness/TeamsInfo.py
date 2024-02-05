import pandas as pd


def map_full_names_to_school():
    # return {'Texas A&M-Corpus Christi': 'TAMU-CC',
    #         'Southeast Missouri State': 'SE Missouri State',
    #         'College of Charleston': 'Charleston',
    #         'North Carolina State': 'NC State',
    #         'UC Santa Barbara': 'UCSB',
    #         'Fairleigh Dickinson': 'FDU',
    #         'Florida Atlantic': 'FAU',
    #         'Louisiana-Lafayette': 'Louisiana',
    #         'Southern California': 'USC',
    #         'Miami (Fla.)': 'Miami',
    #         'Pittsburgh': 'Pitt',
    #         'Texas A&M': 'TAMU',
    #         'Saint Mary`s': "Saint Mary's",
    #         'Connecticut': 'UConn',
    school_mapping = {'Purdue Boilermakers': 'Purdue',
                      'Tennessee Volunteers': 'Tennessee',
                      'Alabama Crimson Tide': 'Alabama',
                      'Houston Cougars': 'Houston',
                      'UCLA Bruins': 'UCLA',
                      'Texas Longhorns': 'Texas',
                      'Kansas Jayhawks': 'Kansas',
                      'Arizona Wildcats': 'Arizona',
                      'Arizona State Sun Devils': 'Arizona State',
                      'Kansas State Wildcats': 'Kansas State',
                      'Virginia Cavaliers': 'Virginia',
                      'Gonzaga Bulldogs': 'Gonzaga',
                      'Marquette Golden Eagles': 'Marquette',
                      'Quinnipiac Bobcats': 'Quinnipiac',
                      'Xavier Musketeers': 'Xavier',
                      'Iowa State Cyclones': 'Iowa State',
                      'Baylor Bears': 'Baylor',
                      'TCU Horned Frogs': 'TCU',
                      'Duke Blue Devils': 'Duke',
                      'Connecticut Huskies': 'UConn',
                      'Central Connecticut Blue Devils': 'Central Connecticut',
                      'Indiana Hoosiers': 'Indiana',
                      'Illinois Fighting Illini': 'Illinois',
                      "Saint Mary`s Gaels": "Saint Mary's",
                      "Saint John`s Red Storm": "Saint John's",
                      'Providence Friars': 'Providence',
                      'Washington Huskies': 'Washington',
                      'Vanderbilt Commodores': 'Vanderbilt',
                      'San Diego State Aztecs': 'San Diego State',
                      'Rutgers Scarlet Knights': 'Rutgers',
                      'Miami (Fla.) Hurricanes': 'Miami',
                      'Missouri Tigers': 'Missouri',
                      'Creighton Bluejays': 'Creighton',
                      'Michigan State Spartans': 'Michigan State',
                      'Auburn Tigers': 'Auburn',
                      'Clemson Tigers': 'Clemson',
                      'Charlotte 49ers': 'Charlotte',
                      'North Carolina Tar Heels': 'North Carolina',
                      'North Carolina State Wolfpack': 'NC State',
                      'North Carolina Central Eagles': 'North Carolina Central',
                      'Southern California Trojans': 'USC',
                      'Florida Atlantic Owls': 'FAU',
                      'Northwestern Wildcats': 'Northwestern',
                      'Iowa Hawkeyes': 'Iowa',
                      'McNeese State Cowboys': 'McNeese State',
                      'New Mexico Lobos': 'New Mexico',
                      'Maryland Terrapins': 'Maryland',
                      'Toledo Rockets': 'Toledo',
                      'Grambling Tigers': 'Grambling',
                      'Arkansas Razorbacks': 'Arkansas',
                      'Boise State Broncos': 'Boise State',
                      'Pittsburgh Panthers': 'Pitt',
                      'Kentucky Wildcats': 'Kentucky',
                      'West Virginia Mountaineers': 'West Virginia',
                      'Memphis Tigers': 'Memphis',
                      'Oral Roberts Golden Eagles': 'Oral Roberts',
                      'Kent State Golden Flashes': 'Kent State',
                      'College of Charleston Cougars': 'Charleston',
                      'Liberty Flames': 'Liberty',
                      'Saint Louis Billikens': 'St. Louis',
                      'Louisiana-Lafayette Cajuns': 'Louisiana',
                      'UC Santa Barbara Gauchos': 'UCSB',
                      'Utah Utes': 'Utah',
                      'Utah Valley Wolverines': 'Utah Valley',
                      'Southern Illinois Salukis': 'Southern Illinois',
                      'Furman Paladins': 'Furman',
                      'Colgate Raiders': 'Colgate',
                      'Princeton Tigers': 'Princeton',
                      'Vermont Catamounts': 'Vermont',
                      'Eastern Washington Eagles': 'Eastern Washington',
                      'Siena Saints': 'Siena',
                      'UNC Asheville Bulldogs': 'UNC Asheville',
                      'Southeastern Louisiana Lions': 'SE Louisiana',
                      'Maryland-Eastern Shore Hawks': 'UMES',
                      'Southern Jaguars': 'Southern',
                      'Milwaukee Panthers': 'Milwaukee',
                      'Oklahoma Sooners': 'Oklahoma',
                      'Tennessee-Martin Skyhawks': 'UT-Martin',
                      'Virginia Commonwealth Rams': 'VCU',
                      'Seattle Redhawks': 'Seattle',
                      'UNC Greensboro Spartans': 'UNC Greensboro',
                      'Northern Kentucky Norse': 'Northern Kentucky',
                      'Eastern Kentucky Colonels': 'Eastern Kentucky',
                      'Wisconsin Badgers': 'Wisconsin',
                      'Penn State Nittany Lions': 'Penn State',
                      'Fairleigh Dickinson Knights': 'FDU',
                      'Hofstra Pride': 'Hofstra',
                      'Southeast Missouri State Redhawks': 'SE Missouri State',
                      'Nevada Wolf Pack': 'Nevada',
                      'Oklahoma State Cowboys': 'Oklahoma State',
                      'Alcorn State Braves': 'Alcorn State',
                      'Texas A&amp;M-Corpus Christi Islanders': 'TAMU-CC',
                      'Texas A&amp;M Aggies': 'TAMU',
                      'Drake Bulldogs': 'Drake',
                      'Bradley Braves': 'Bradley',
                      'Akron Zips': 'Akron',
                      'Cornell Big Red': 'Cornell',
                      'Youngstown State Penguins': 'Youngstown State',
                      'Morehead State Eagles': 'Morehead State',
                      'Rider Broncs': 'Rider',
                      'Yale Bulldogs': 'Yale',
                      'Nebraska Cornhuskers': 'Nebraska',
                      'Howard Bison': 'Howard',
                      'Georgia State Panthers': 'Georgia State',
                      'New Mexico State Aggies': 'New Mexico State',
                      'Mississippi State Bulldogs': 'Mississippi State',
                      'Mississippi Rebels': 'Mississippi',
                      'Indiana State Sycamores': 'Indiana State',
                      'Notre Dame Fightin` Irish': 'Notre Dame',
                      'Texas Tech Red Raiders': 'Texas Tech',
                      'Montana State Bobcats': 'Montana State',
                      'Davidson Wildcats': 'Davidson',
                      'Dayton Flyers': 'Dayton',
                      'UC Davis Aggies': 'UC Davis',
                      'Cal State Fullerton Titans': 'Cal State Fullerton',
                      'Norfolk State Spartans': 'Norfolk State',
                      'Virginia Tech Hokies': 'Virginia Tech',
                      'Chattanooga Mocs': 'Chattanooga',
                      'Longwood Lancers': 'Longwood',
                      'Michigan Wolverines': 'Michigan',
                      'High Point Panthers': 'High Point',
                      'Ohio State Buckeyes': 'Ohio State',
                      'Jacksonville State Gamecocks': 'Jacksonville State',
                      'Jackson State Tigers': 'Jackson State',
                      'Colorado State Rams': 'Colorado State',
                      'Loyola Chicago Ramblers': 'Loyola Chicago',
                      'Murray State Racers': 'Murray State',
                      'Wright State Raiders': 'Wright State',
                      'Delaware Blue Hens': 'Delaware',
                      'Delaware State Hornets': 'Delaware State',
                      'LSU Tigers': 'LSU',
                      'Villanova Wildcats': 'Villanova',
                      'Saint Peter`s Peacocks': "St. Peter's",
                      'San Francisco Dons': 'San Francisco',
                      'Richmond Spiders': 'Richmond',
                      'Texas Southern Tigers': 'Texas Southern',
                      'UAB Blazers': 'UAB',
                      'South Dakota State Jackrabbits': 'South Dakota State',
                      'South Carolina Gamecocks': 'South Carolina',
                      'Seton Hall Pirates': 'Seton Hall',
                      'Colorado Buffaloes': 'Colorado',
                      'Abilene Christian Wildcats': 'Abilene Christian',
                      'Oregon State Beavers': 'Oregon State',
                      'Hartford Hawks': 'Hartford',
                      'Georgetown Hoyas': 'Georgetown',
                      'Florida Gators': 'Florida',
                      'Ohio Bobcats': 'Ohio',
                      'Georgia Tech Yellow Jackets': 'Georgia Tech',
                      'Cleveland State Vikings': 'Cleveland State',
                      'Oregon Ducks': 'Oregon',
                      'Syracuse Orange': 'Syracuse',
                      'Grand Canyon Antelopes': 'Grand Canyon',
                      'Saint Bonaventure Bonnies': 'St. Bonaventure',
                      'North Texas Mean Green': 'North Texas',
                      'Drexel Dragons': 'Drexel',
                      'Winthrop Eagles': 'Winthrop',
                      'Appalachian State Mountaineers': 'Appalachian State',
                      'BYU Cougars': 'BYU',
                      'Iona Gaels': 'Iona',
                      'Green Bay Phoenix': 'Green Bay',
                      'Florida State Seminoles': 'Florida State',
                      'Utah State Aggies': 'Utah State',
                      'UC Irvine Anteaters': 'UC Irvine',
                      'Samford Bulldogs': 'Samford',
                      'Sam Houston State Bearkats': 'Sam Houston State',
                      'Kennesaw State Owls': 'Kennesaw State',
                      'Southern Mississippi Golden Eagles': 'Southern Mississippi'}
    return school_mapping


def map_schools_to_full_name():
    name_mapping = {v: k for k, v in map_full_names_to_school().items()}
    return name_mapping


def conference_mapping():
    confs_df = pd.read_csv('Projects/ncaam/march_madness/ncaamConfs.csv')

    conf_name_mapping = {'A-10': 'Atlantic 10',
                         'A-EAST': 'America East',
                         'A-SUN': 'ASUN',
                         # 'ACC': 'Atlantic Coast',
                         'AMER': 'American Athletic',
                         'BIG10': 'Big Ten',
                         'BIG12': 'Big 12',
                         'BIGEAST': 'Big East',
                         'BIGSKY': 'Big Sky',
                         'BIGSOUTH': 'Big South',
                         'BIGWEST': 'Big West',
                         'C-USA': 'Conference USA',
                         'CAA': 'Colonial Athletic Association',
                         'HL': 'Horizon League',
                         'IVY': 'Ivy League',
                         'MAAC': 'Metro Atlantic Athletic',
                         'MAC': 'Mid-American',
                         'MEAC': 'Mid-Eastern Athletic',
                         'MVC': 'Missouri Valley',
                         'MWC': 'Mountain West',
                         'NEC': 'Northeast',
                         'OVC': 'Ohio Valley',
                         'PAC-12': 'Pac-12',
                         'PL': 'Patriot League',
                         # 'SEC': 'Southeastern',
                         'SLC': 'Southland',
                         'SOCON': 'Southern',
                         'SUMMIT': 'Summit League',
                         'SUNBELT': 'Sun Belt',
                         'SWAC': 'Southwestern Athletic',
                         'WAC': 'Western Athletic',
                         'WCC': 'West Coast'}

    mapping = dict()
    for index, row in confs_df.iterrows():
        mapping[row['Team']] = conf_name_mapping.get(row['Conference'], row['Conference'])

    return mapping