#!/usr/bin/env python3
"""
Generate the mountain database for notarcteryx.

Produces a curated JSON file of ~650 mountains with coordinates,
elevation, region, and popularity rank. The data is hardcoded here
rather than pulled from an API, so the seed is reproducible and
doesn't require network access.

Popularity rank: 1 = most famous globally, higher = more obscure.
"""

import json
import pathlib

MOUNTAINS = [
    # =========================================================================
    # GLOBAL ICONS (rank 1-25)
    # =========================================================================
    {"name": "Mount Everest", "aliases": ["Everest", "Sagarmatha", "Chomolungma"], "latitude": 27.9881, "longitude": 86.9250, "elevation_m": 8849, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 1},
    {"name": "K2", "aliases": ["Mount Godwin-Austen", "Chhogori", "Chogori"], "latitude": 35.8825, "longitude": 76.5133, "elevation_m": 8611, "region": "Karakoram", "country": "Pakistan", "state_province": "Gilgit-Baltistan", "popularity_rank": 2},
    {"name": "Mont Blanc", "aliases": ["Monte Bianco", "Mt. Blanc"], "latitude": 45.8326, "longitude": 6.8652, "elevation_m": 4809, "region": "Alps", "country": "France", "state_province": "Haute-Savoie", "popularity_rank": 3},
    {"name": "Mount Kilimanjaro", "aliases": ["Kilimanjaro", "Kili", "Uhuru Peak"], "latitude": -3.0674, "longitude": 37.3556, "elevation_m": 5895, "region": "East Africa", "country": "Tanzania", "state_province": "Kilimanjaro", "popularity_rank": 4},
    {"name": "Mount Fuji", "aliases": ["Fuji-san", "Fujiyama", "Fuji"], "latitude": 35.3606, "longitude": 138.7274, "elevation_m": 3776, "region": "Honshu", "country": "Japan", "state_province": "Shizuoka", "popularity_rank": 5},
    {"name": "Denali", "aliases": ["Mount McKinley", "Mt. McKinley"], "latitude": 63.0695, "longitude": -151.0074, "elevation_m": 6190, "region": "Alaska Range", "country": "US", "state_province": "Alaska", "popularity_rank": 6},
    {"name": "Matterhorn", "aliases": ["Monte Cervino", "Mont Cervin"], "latitude": 45.9764, "longitude": 7.6586, "elevation_m": 4478, "region": "Alps", "country": "Switzerland", "state_province": "Valais", "popularity_rank": 7},
    {"name": "Mount Rainier", "aliases": ["Rainier", "Mt. Rainier", "Tahoma"], "latitude": 46.8523, "longitude": -121.7603, "elevation_m": 4392, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 8},
    {"name": "Aconcagua", "aliases": ["Cerro Aconcagua"], "latitude": -32.6532, "longitude": -70.0109, "elevation_m": 6961, "region": "Andes", "country": "Argentina", "state_province": "Mendoza", "popularity_rank": 9},
    {"name": "Mount Elbrus", "aliases": ["Elbrus", "Mingi Taw"], "latitude": 43.3499, "longitude": 42.4453, "elevation_m": 5642, "region": "Caucasus", "country": "Russia", "state_province": "Kabardino-Balkaria", "popularity_rank": 10},
    {"name": "Mount Whitney", "aliases": ["Whitney", "Mt. Whitney"], "latitude": 36.5785, "longitude": -118.2923, "elevation_m": 4421, "region": "Sierra Nevada", "country": "US", "state_province": "California", "popularity_rank": 11},
    {"name": "Pikes Peak", "aliases": ["Pike's Peak"], "latitude": 38.8409, "longitude": -105.0423, "elevation_m": 4302, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 12},
    {"name": "Mount Olympus", "aliases": ["Olympus", "Mytikas"], "latitude": 40.0859, "longitude": 22.3583, "elevation_m": 2917, "region": "Thessaly", "country": "Greece", "state_province": "Pieria", "popularity_rank": 13},
    {"name": "Table Mountain", "aliases": ["Tafelberg"], "latitude": -33.9625, "longitude": 18.4039, "elevation_m": 1085, "region": "Western Cape", "country": "South Africa", "state_province": "Western Cape", "popularity_rank": 14},
    {"name": "Half Dome", "aliases": ["Tis-sa-ack"], "latitude": 37.7459, "longitude": -119.5332, "elevation_m": 2694, "region": "Sierra Nevada", "country": "US", "state_province": "California", "popularity_rank": 15},
    {"name": "Mount Hood", "aliases": ["Hood", "Mt. Hood", "Wy'east"], "latitude": 45.3735, "longitude": -121.6959, "elevation_m": 3429, "region": "Cascades", "country": "US", "state_province": "Oregon", "popularity_rank": 16},
    {"name": "Ben Nevis", "aliases": ["Nevis", "The Ben"], "latitude": 56.7969, "longitude": -5.0036, "elevation_m": 1345, "region": "Scottish Highlands", "country": "UK", "state_province": "Scotland", "popularity_rank": 17},
    {"name": "Mount Washington", "aliases": ["Mt. Washington", "Washington"], "latitude": 44.2706, "longitude": -71.3033, "elevation_m": 1917, "region": "White Mountains", "country": "US", "state_province": "New Hampshire", "popularity_rank": 18},
    {"name": "Longs Peak", "aliases": ["Long's Peak", "Longs"], "latitude": 40.2550, "longitude": -105.6151, "elevation_m": 4346, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 19},
    {"name": "Mount Shasta", "aliases": ["Shasta", "Mt. Shasta"], "latitude": 41.4092, "longitude": -122.1949, "elevation_m": 4322, "region": "Cascades", "country": "US", "state_province": "California", "popularity_rank": 20},
    {"name": "Zugspitze", "aliases": ["Zugspitz"], "latitude": 47.4211, "longitude": 10.9853, "elevation_m": 2962, "region": "Alps", "country": "Germany", "state_province": "Bavaria", "popularity_rank": 21},
    {"name": "Mount Blanc du Tacul", "aliases": ["Mont Blanc du Tacul"], "latitude": 45.8558, "longitude": 6.8881, "elevation_m": 4248, "region": "Alps", "country": "France", "state_province": "Haute-Savoie", "popularity_rank": 22},
    {"name": "Mauna Kea", "aliases": ["Maunakea"], "latitude": 19.8207, "longitude": -155.4681, "elevation_m": 4207, "region": "Hawaii", "country": "US", "state_province": "Hawaii", "popularity_rank": 23},
    {"name": "Snowdon", "aliases": ["Yr Wyddfa", "Mount Snowdon"], "latitude": 53.0685, "longitude": -4.0763, "elevation_m": 1085, "region": "Snowdonia", "country": "UK", "state_province": "Wales", "popularity_rank": 24},
    {"name": "Mount Elbert", "aliases": ["Elbert", "Mt. Elbert"], "latitude": 39.1178, "longitude": -106.4453, "elevation_m": 4401, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 25},

    # =========================================================================
    # WELL-KNOWN PEAKS (rank 26-50)
    # =========================================================================
    {"name": "Maroon Bells", "aliases": ["Maroon Peak", "North Maroon Peak"], "latitude": 39.0708, "longitude": -106.9892, "elevation_m": 4315, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 26},
    {"name": "Eiger", "aliases": ["The Eiger", "Eiger North Face"], "latitude": 46.5776, "longitude": 8.0053, "elevation_m": 3967, "region": "Alps", "country": "Switzerland", "state_province": "Bern", "popularity_rank": 27},
    {"name": "Mount St. Helens", "aliases": ["St. Helens", "Mt. St. Helens"], "latitude": 46.1914, "longitude": -122.1956, "elevation_m": 2549, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 28},
    {"name": "Jungfrau", "aliases": ["The Jungfrau"], "latitude": 46.5367, "longitude": 7.9614, "elevation_m": 4158, "region": "Alps", "country": "Switzerland", "state_province": "Bern", "popularity_rank": 29},
    {"name": "Mount Si", "aliases": ["Mt. Si"], "latitude": 47.4879, "longitude": -121.7237, "elevation_m": 1585, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 30},
    {"name": "Etna", "aliases": ["Mount Etna", "Mongibello"], "latitude": 37.7510, "longitude": 14.9934, "elevation_m": 3357, "region": "Sicily", "country": "Italy", "state_province": "Sicily", "popularity_rank": 31},
    {"name": "Mount Baker", "aliases": ["Baker", "Mt. Baker", "Koma Kulshan"], "latitude": 48.7768, "longitude": -121.8145, "elevation_m": 3286, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 32},
    {"name": "Mount Katahdin", "aliases": ["Katahdin", "Baxter Peak"], "latitude": 45.9044, "longitude": -68.9214, "elevation_m": 1606, "region": "Appalachians", "country": "US", "state_province": "Maine", "popularity_rank": 33},
    {"name": "Monte Rosa", "aliases": ["Dufourspitze", "Rosa"], "latitude": 45.9368, "longitude": 7.8667, "elevation_m": 4634, "region": "Alps", "country": "Switzerland", "state_province": "Valais", "popularity_rank": 34},
    {"name": "Mount Adams", "aliases": ["Adams", "Mt. Adams", "Pahto"], "latitude": 46.2024, "longitude": -121.4909, "elevation_m": 3743, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 35},
    {"name": "Mount Evans", "aliases": ["Evans", "Mt. Evans", "Mount Blue Sky"], "latitude": 39.5883, "longitude": -105.6438, "elevation_m": 4350, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 36},
    {"name": "Olympus", "aliases": ["Mount Olympus Greece"], "latitude": 40.0859, "longitude": 22.3583, "elevation_m": 2917, "region": "Thessaly", "country": "Greece", "state_province": "Pieria", "popularity_rank": 37},
    {"name": "Quandary Peak", "aliases": ["Quandary"], "latitude": 39.3972, "longitude": -106.1064, "elevation_m": 4348, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 38},
    {"name": "Cotopaxi", "aliases": ["Volcan Cotopaxi"], "latitude": -0.6841, "longitude": -78.4376, "elevation_m": 5897, "region": "Andes", "country": "Ecuador", "state_province": "Cotopaxi", "popularity_rank": 39},
    {"name": "Mount Bierstadt", "aliases": ["Bierstadt"], "latitude": 39.5828, "longitude": -105.6686, "elevation_m": 4287, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 40},
    {"name": "Clingmans Dome", "aliases": ["Clingman's Dome", "Kuwohi"], "latitude": 35.5628, "longitude": -83.4985, "elevation_m": 2025, "region": "Great Smoky Mountains", "country": "US", "state_province": "Tennessee", "popularity_rank": 41},
    {"name": "Grays Peak", "aliases": ["Gray's Peak"], "latitude": 39.6339, "longitude": -105.8178, "elevation_m": 4352, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 42},
    {"name": "Torreys Peak", "aliases": ["Torrey's Peak"], "latitude": 39.6436, "longitude": -105.8211, "elevation_m": 4349, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 43},
    {"name": "Mount Massive", "aliases": ["Massive"], "latitude": 39.1875, "longitude": -106.4756, "elevation_m": 4398, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 44},
    {"name": "South Sister", "aliases": ["South Sister Oregon"], "latitude": 44.1035, "longitude": -121.7693, "elevation_m": 3157, "region": "Cascades", "country": "US", "state_province": "Oregon", "popularity_rank": 45},
    {"name": "Mount Baldy", "aliases": ["Mt. Baldy", "Mount San Antonio"], "latitude": 34.2886, "longitude": -117.6461, "elevation_m": 3069, "region": "San Gabriel Mountains", "country": "US", "state_province": "California", "popularity_rank": 46},
    {"name": "Mount Marcy", "aliases": ["Marcy"], "latitude": 44.1128, "longitude": -73.9236, "elevation_m": 1629, "region": "Adirondacks", "country": "US", "state_province": "New York", "popularity_rank": 47},
    {"name": "Capitol Peak", "aliases": ["Capitol"], "latitude": 39.1503, "longitude": -107.0831, "elevation_m": 4307, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 48},
    {"name": "Torres del Paine", "aliases": ["Paine", "Las Torres"], "latitude": -50.9423, "longitude": -73.0106, "elevation_m": 2884, "region": "Patagonia", "country": "Chile", "state_province": "Magallanes", "popularity_rank": 49},
    {"name": "Mount of the Holy Cross", "aliases": ["Holy Cross"], "latitude": 39.4667, "longitude": -106.4817, "elevation_m": 4269, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 50},

    # =========================================================================
    # POPULAR WORLDWIDE (rank 51-100)
    # =========================================================================
    {"name": "Fitz Roy", "aliases": ["Monte Fitz Roy", "Chalten", "Cerro Fitz Roy"], "latitude": -49.2714, "longitude": -73.0428, "elevation_m": 3405, "region": "Patagonia", "country": "Argentina", "state_province": "Santa Cruz", "popularity_rank": 51},
    {"name": "Aoraki", "aliases": ["Mount Cook", "Aoraki/Mount Cook"], "latitude": -43.5950, "longitude": 170.1418, "elevation_m": 3724, "region": "Southern Alps", "country": "New Zealand", "state_province": "Canterbury", "popularity_rank": 52},
    {"name": "Mount San Jacinto", "aliases": ["San Jacinto"], "latitude": 33.8147, "longitude": -116.6794, "elevation_m": 3302, "region": "San Jacinto Mountains", "country": "US", "state_province": "California", "popularity_rank": 53},
    {"name": "Mount Mitchell", "aliases": ["Mitchell"], "latitude": 35.7650, "longitude": -82.2653, "elevation_m": 2037, "region": "Appalachians", "country": "US", "state_province": "North Carolina", "popularity_rank": 54},
    {"name": "Humphreys Peak", "aliases": ["Humphreys"], "latitude": 35.3464, "longitude": -111.6781, "elevation_m": 3852, "region": "San Francisco Peaks", "country": "US", "state_province": "Arizona", "popularity_rank": 55},
    {"name": "Mount Jefferson", "aliases": ["Jefferson"], "latitude": 44.6743, "longitude": -121.7999, "elevation_m": 3199, "region": "Cascades", "country": "US", "state_province": "Oregon", "popularity_rank": 56},
    {"name": "Mount Kenya", "aliases": ["Kenya", "Kirinyaga", "Batian"], "latitude": -0.1521, "longitude": 37.3084, "elevation_m": 5199, "region": "East Africa", "country": "Kenya", "state_province": "Central", "popularity_rank": 57},
    {"name": "Mount Tamalpais", "aliases": ["Mt. Tam", "Tamalpais"], "latitude": 37.9236, "longitude": -122.5964, "elevation_m": 784, "region": "Marin County", "country": "US", "state_province": "California", "popularity_rank": 58},
    {"name": "Mount Mansfield", "aliases": ["Mansfield"], "latitude": 44.5437, "longitude": -72.8143, "elevation_m": 1340, "region": "Green Mountains", "country": "US", "state_province": "Vermont", "popularity_rank": 59},
    {"name": "Mission Peak", "aliases": ["Mission"], "latitude": 37.5126, "longitude": -121.8806, "elevation_m": 770, "region": "Diablo Range", "country": "US", "state_province": "California", "popularity_rank": 60},
    {"name": "Mount Ararat", "aliases": ["Ararat", "Agri Dagi", "Agri Dağı"], "latitude": 39.7019, "longitude": 44.2983, "elevation_m": 5137, "region": "Eastern Turkey", "country": "Turkey", "state_province": "Agri", "popularity_rank": 61},
    {"name": "Mount Diablo", "aliases": ["Diablo", "Mt. Diablo"], "latitude": 37.8816, "longitude": -121.9142, "elevation_m": 1173, "region": "Diablo Range", "country": "US", "state_province": "California", "popularity_rank": 62},
    {"name": "Old Rag Mountain", "aliases": ["Old Rag"], "latitude": 38.5531, "longitude": -78.3214, "elevation_m": 1011, "region": "Blue Ridge", "country": "US", "state_province": "Virginia", "popularity_rank": 63},
    {"name": "Annapurna Base Camp", "aliases": ["ABC", "Annapurna Sanctuary"], "latitude": 28.5308, "longitude": 83.8781, "elevation_m": 4130, "region": "Himalayas", "country": "Nepal", "state_province": "Gandaki", "popularity_rank": 64},
    {"name": "Mount Langley", "aliases": ["Langley"], "latitude": 36.5189, "longitude": -118.2375, "elevation_m": 4275, "region": "Sierra Nevada", "country": "US", "state_province": "California", "popularity_rank": 65},
    {"name": "Pico de Orizaba", "aliases": ["Citlaltepetl", "Orizaba"], "latitude": 19.0303, "longitude": -97.2683, "elevation_m": 5636, "region": "Trans-Mexican Volcanic Belt", "country": "Mexico", "state_province": "Puebla", "popularity_rank": 66},
    {"name": "Wheeler Peak", "aliases": ["Wheeler"], "latitude": 36.5569, "longitude": -105.4172, "elevation_m": 4013, "region": "Sangre de Cristo", "country": "US", "state_province": "New Mexico", "popularity_rank": 67},
    {"name": "Mount Lafayette", "aliases": ["Lafayette"], "latitude": 44.1607, "longitude": -71.6444, "elevation_m": 1603, "region": "White Mountains", "country": "US", "state_province": "New Hampshire", "popularity_rank": 68},
    {"name": "Huascaran", "aliases": ["Nevado Huascaran", "Huascarán"], "latitude": -9.1222, "longitude": -77.6042, "elevation_m": 6768, "region": "Andes", "country": "Peru", "state_province": "Ancash", "popularity_rank": 69},
    {"name": "Mount Williamson", "aliases": ["Williamson"], "latitude": 36.6561, "longitude": -118.3117, "elevation_m": 4382, "region": "Sierra Nevada", "country": "US", "state_province": "California", "popularity_rank": 70},
    {"name": "Mount Adams", "aliases": ["Adams"], "latitude": 44.3206, "longitude": -71.2914, "elevation_m": 1760, "region": "White Mountains", "country": "US", "state_province": "New Hampshire", "popularity_rank": 72},
    {"name": "Huangshan", "aliases": ["Yellow Mountain", "Huang Shan", "Mount Huang"], "latitude": 30.1375, "longitude": 118.1631, "elevation_m": 1864, "region": "Anhui Mountains", "country": "China", "state_province": "Anhui", "popularity_rank": 73},
    {"name": "Rattlesnake Ledge", "aliases": ["Rattlesnake Mountain"], "latitude": 47.4340, "longitude": -121.7710, "elevation_m": 653, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 75},
    {"name": "Franconia Ridge", "aliases": ["Franconia Ridgeline"], "latitude": 44.1439, "longitude": -71.6447, "elevation_m": 1580, "region": "White Mountains", "country": "US", "state_province": "New Hampshire", "popularity_rank": 78},
    {"name": "Camel's Hump", "aliases": ["Camels Hump"], "latitude": 44.3194, "longitude": -72.8861, "elevation_m": 1244, "region": "Green Mountains", "country": "US", "state_province": "Vermont", "popularity_rank": 80},
    {"name": "Guadalupe Peak", "aliases": ["Guadalupe"], "latitude": 31.8912, "longitude": -104.8606, "elevation_m": 2667, "region": "Guadalupe Mountains", "country": "US", "state_province": "Texas", "popularity_rank": 82},
    {"name": "Mount Kazbek", "aliases": ["Kazbek", "Kazbegi", "Mkinvartsveri"], "latitude": 42.6861, "longitude": 44.5142, "elevation_m": 5054, "region": "Caucasus", "country": "Georgia", "state_province": "Mtskheta-Mtianeti", "popularity_rank": 83},
    {"name": "Mailbox Peak", "aliases": ["Mailbox"], "latitude": 47.4678, "longitude": -121.6744, "elevation_m": 1480, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 85},
    {"name": "Ama Dablam", "aliases": ["Amadablam"], "latitude": 27.8614, "longitude": 86.8611, "elevation_m": 6812, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 86},
    {"name": "Grandfather Mountain", "aliases": ["Grandfather"], "latitude": 36.0994, "longitude": -81.8328, "elevation_m": 1812, "region": "Appalachians", "country": "US", "state_province": "North Carolina", "popularity_rank": 88},

    # =========================================================================
    # CANADA (rank 89-120)
    # =========================================================================
    {"name": "Mount Robson", "aliases": ["Robson"], "latitude": 53.1147, "longitude": -119.1553, "elevation_m": 3954, "region": "Canadian Rockies", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 90},
    {"name": "Mount Temple", "aliases": ["Temple"], "latitude": 51.3489, "longitude": -116.2069, "elevation_m": 3543, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 92},
    {"name": "Granite Mountain", "aliases": ["Granite"], "latitude": 47.3978, "longitude": -121.4867, "elevation_m": 1737, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 95},
    {"name": "Mount Assiniboine", "aliases": ["Assiniboine", "Matterhorn of the Rockies"], "latitude": 50.8714, "longitude": -115.6508, "elevation_m": 3618, "region": "Canadian Rockies", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 96},
    {"name": "Mount Rundle", "aliases": ["Rundle"], "latitude": 51.1253, "longitude": -115.4717, "elevation_m": 2949, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 98},
    {"name": "Grouse Mountain", "aliases": ["Grouse Grind", "Grouse"], "latitude": 49.3809, "longitude": -123.0828, "elevation_m": 1231, "region": "North Shore Mountains", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 99},
    {"name": "Mount Pilchuck", "aliases": ["Pilchuck"], "latitude": 48.0678, "longitude": -121.8139, "elevation_m": 1627, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 100},

    # =========================================================================
    # REGIONAL FAVORITES WORLDWIDE (rank 101-200)
    # =========================================================================
    {"name": "Ha Ling Peak", "aliases": ["Ha Ling", "Chinaman's Peak"], "latitude": 51.0497, "longitude": -115.4078, "elevation_m": 2407, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 102},
    {"name": "Taishan", "aliases": ["Mount Tai", "Tai Shan", "Tai Mountain"], "latitude": 36.2528, "longitude": 117.1011, "elevation_m": 1545, "region": "Shandong", "country": "China", "state_province": "Shandong", "popularity_rank": 103},
    {"name": "Mount Thielsen", "aliases": ["Thielsen"], "latitude": 43.1533, "longitude": -122.0657, "elevation_m": 2799, "region": "Cascades", "country": "US", "state_province": "Oregon", "popularity_rank": 105},
    {"name": "Tre Cime di Lavaredo", "aliases": ["Drei Zinnen", "Three Peaks of Lavaredo", "Tre Cime"], "latitude": 46.6192, "longitude": 12.3033, "elevation_m": 2999, "region": "Dolomites", "country": "Italy", "state_province": "South Tyrol", "popularity_rank": 107},
    {"name": "Cascade Mountain", "aliases": ["Cascade"], "latitude": 51.2172, "longitude": -115.5053, "elevation_m": 2998, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 108},
    {"name": "Mount Ellinor", "aliases": ["Ellinor"], "latitude": 47.5117, "longitude": -123.2492, "elevation_m": 1783, "region": "Olympics", "country": "US", "state_province": "Washington", "popularity_rank": 110},
    {"name": "The Chief", "aliases": ["Stawamus Chief", "Squamish Chief"], "latitude": 49.6783, "longitude": -123.1400, "elevation_m": 702, "region": "Sea to Sky", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 112},
    {"name": "Glacier Peak", "aliases": ["Glacier", "Dakobed"], "latitude": 48.1117, "longitude": -121.1139, "elevation_m": 3213, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 115},
    {"name": "Mount Garibaldi", "aliases": ["Garibaldi"], "latitude": 49.8506, "longitude": -123.0044, "elevation_m": 2678, "region": "Garibaldi Ranges", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 117},
    {"name": "Black Tusk", "aliases": ["The Black Tusk"], "latitude": 49.9700, "longitude": -123.0458, "elevation_m": 2319, "region": "Garibaldi Ranges", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 118},
    {"name": "Gran Paradiso", "aliases": ["Gran Paradiso Peak"], "latitude": 45.5183, "longitude": 7.2661, "elevation_m": 4061, "region": "Alps", "country": "Italy", "state_province": "Aosta Valley", "popularity_rank": 120},
    {"name": "Grossglockner", "aliases": ["Glockner"], "latitude": 47.0742, "longitude": 12.6942, "elevation_m": 3798, "region": "Alps", "country": "Austria", "state_province": "Tyrol", "popularity_rank": 122},
    {"name": "Emei Shan", "aliases": ["Mount Emei", "Emeishan", "Emei Mountain"], "latitude": 29.5251, "longitude": 103.3356, "elevation_m": 3099, "region": "Sichuan", "country": "China", "state_province": "Sichuan", "popularity_rank": 124},
    {"name": "Triglav", "aliases": ["Mount Triglav"], "latitude": 46.3786, "longitude": 13.8364, "elevation_m": 2864, "region": "Julian Alps", "country": "Slovenia", "state_province": "Upper Carniola", "popularity_rank": 125},
    {"name": "Scafell Pike", "aliases": ["Scafell"], "latitude": 54.4542, "longitude": -3.2117, "elevation_m": 978, "region": "Lake District", "country": "UK", "state_province": "England", "popularity_rank": 128},
    {"name": "Galdhopiggen", "aliases": ["Galdhøpiggen"], "latitude": 61.6369, "longitude": 8.3125, "elevation_m": 2469, "region": "Jotunheimen", "country": "Norway", "state_province": "Innlandet", "popularity_rank": 130},
    {"name": "Helvellyn", "aliases": ["Striding Edge"], "latitude": 54.5272, "longitude": -3.0167, "elevation_m": 950, "region": "Lake District", "country": "UK", "state_province": "England", "popularity_rank": 132},
    {"name": "Salkantay", "aliases": ["Nevado Salkantay", "Salcantay"], "latitude": -13.3333, "longitude": -72.5500, "elevation_m": 6271, "region": "Andes", "country": "Peru", "state_province": "Cusco", "popularity_rank": 133},
    {"name": "Kebnekaise", "aliases": ["Giebmegáisi"], "latitude": 67.9039, "longitude": 18.5281, "elevation_m": 2097, "region": "Scandinavian Mountains", "country": "Sweden", "state_province": "Norrbotten", "popularity_rank": 135},
    {"name": "Aneto", "aliases": ["Pico de Aneto"], "latitude": 42.6311, "longitude": 0.6572, "elevation_m": 3404, "region": "Pyrenees", "country": "Spain", "state_province": "Aragon", "popularity_rank": 138},
    {"name": "Carrauntoohil", "aliases": ["Carrantuohill", "Corrán Tuathail"], "latitude": 51.7992, "longitude": -9.7392, "elevation_m": 1039, "region": "MacGillycuddy's Reeks", "country": "Ireland", "state_province": "Kerry", "popularity_rank": 140},
    {"name": "Iztaccihuatl", "aliases": ["Izta", "Iztaccíhuatl", "La Mujer Dormida"], "latitude": 19.1789, "longitude": -98.6417, "elevation_m": 5230, "region": "Trans-Mexican Volcanic Belt", "country": "Mexico", "state_province": "Mexico State", "popularity_rank": 141},
    {"name": "Mulhacen", "aliases": ["Mulhacén"], "latitude": 37.0536, "longitude": -3.3117, "elevation_m": 3479, "region": "Sierra Nevada", "country": "Spain", "state_province": "Granada", "popularity_rank": 142},
    {"name": "Pic du Midi d'Ossau", "aliases": ["Midi d'Ossau"], "latitude": 42.8428, "longitude": -0.4381, "elevation_m": 2884, "region": "Pyrenees", "country": "France", "state_province": "Bearn", "popularity_rank": 145},
    {"name": "Toubkal", "aliases": ["Jebel Toubkal", "Tubkal"], "latitude": 31.0597, "longitude": -7.9153, "elevation_m": 4167, "region": "Atlas Mountains", "country": "Morocco", "state_province": "Marrakech-Safi", "popularity_rank": 148},
    {"name": "Mount Kinabalu", "aliases": ["Kinabalu"], "latitude": 6.0753, "longitude": 116.5586, "elevation_m": 4095, "region": "Borneo", "country": "Malaysia", "state_province": "Sabah", "popularity_rank": 150},
    {"name": "Hua Shan", "aliases": ["Mount Hua", "Huashan", "Hua Mountain"], "latitude": 34.5247, "longitude": 110.0889, "elevation_m": 2155, "region": "Shaanxi", "country": "China", "state_province": "Shaanxi", "popularity_rank": 152},
    {"name": "Mount Rinjani", "aliases": ["Rinjani", "Gunung Rinjani"], "latitude": -8.4117, "longitude": 116.4575, "elevation_m": 3726, "region": "Lombok", "country": "Indonesia", "state_province": "West Nusa Tenggara", "popularity_rank": 155},
    {"name": "Manaslu", "aliases": ["Kutang", "Mount Manaslu"], "latitude": 28.5497, "longitude": 84.5597, "elevation_m": 8163, "region": "Himalayas", "country": "Nepal", "state_province": "Gandaki", "popularity_rank": 157},
    {"name": "Mount Kosciuszko", "aliases": ["Kosciuszko", "Kozzie"], "latitude": -36.4564, "longitude": 148.2639, "elevation_m": 2228, "region": "Snowy Mountains", "country": "Australia", "state_province": "New South Wales", "popularity_rank": 160},
    {"name": "Grand Teton", "aliases": ["The Grand", "Grand"], "latitude": 43.7413, "longitude": -110.8025, "elevation_m": 4199, "region": "Teton Range", "country": "US", "state_province": "Wyoming", "popularity_rank": 162},
    {"name": "Mount Tongariro", "aliases": ["Tongariro", "Tongariro Crossing"], "latitude": -39.1339, "longitude": 175.6428, "elevation_m": 1978, "region": "Tongariro", "country": "New Zealand", "state_province": "Manawatu-Whanganui", "popularity_rank": 165},
    {"name": "Ausangate", "aliases": ["Nevado Ausangate", "Apu Ausangate"], "latitude": -13.7833, "longitude": -71.2333, "elevation_m": 6384, "region": "Andes", "country": "Peru", "state_province": "Cusco", "popularity_rank": 167},
    {"name": "Adam's Peak", "aliases": ["Sri Pada", "Samanala"], "latitude": 6.8094, "longitude": 80.4994, "elevation_m": 2243, "region": "Central Highlands", "country": "Sri Lanka", "state_province": "Sabaragamuwa", "popularity_rank": 170},
    {"name": "Doi Inthanon", "aliases": ["Inthanon", "Doi Ang Ka"], "latitude": 18.5875, "longitude": 98.4867, "elevation_m": 2565, "region": "Thai Highlands", "country": "Thailand", "state_province": "Chiang Mai", "popularity_rank": 172},
    {"name": "Mount Hallasan", "aliases": ["Hallasan", "Halla"], "latitude": 33.3617, "longitude": 126.5331, "elevation_m": 1950, "region": "Jeju", "country": "South Korea", "state_province": "Jeju", "popularity_rank": 175},
    {"name": "Jade Mountain", "aliases": ["Yushan", "Mount Yu", "Yu Shan"], "latitude": 23.4700, "longitude": 120.9572, "elevation_m": 3952, "region": "Central Taiwan", "country": "Taiwan", "state_province": "Nantou", "popularity_rank": 180},
    {"name": "Vinicunca", "aliases": ["Rainbow Mountain", "Montana de Siete Colores", "Montaña de Colores"], "latitude": -13.8700, "longitude": -71.3028, "elevation_m": 5200, "region": "Andes", "country": "Peru", "state_province": "Cusco", "popularity_rank": 182},
    {"name": "Mount Fansipan", "aliases": ["Fansipan", "Phan Xi Pang"], "latitude": 22.3033, "longitude": 103.7750, "elevation_m": 3143, "region": "Hoang Lien Son", "country": "Vietnam", "state_province": "Lao Cai", "popularity_rank": 185},
    {"name": "Bukhansan", "aliases": ["Bukhansan Mountain", "North Han Mountain", "Baegundae"], "latitude": 37.6594, "longitude": 126.9783, "elevation_m": 836, "region": "Seoul Metropolitan", "country": "South Korea", "state_province": "Seoul", "popularity_rank": 187},
    {"name": "Stok Kangri", "aliases": ["Stok"], "latitude": 33.9833, "longitude": 77.4667, "elevation_m": 6153, "region": "Himalayas", "country": "India", "state_province": "Ladakh", "popularity_rank": 190},
    {"name": "Tateyama", "aliases": ["Mount Tate", "Tate-yama"], "latitude": 36.5722, "longitude": 137.6181, "elevation_m": 3015, "region": "Japanese Alps", "country": "Japan", "state_province": "Toyama", "popularity_rank": 192},
    {"name": "Island Peak", "aliases": ["Imja Tse"], "latitude": 27.9117, "longitude": 86.9347, "elevation_m": 6189, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 195},
    {"name": "Mera Peak", "aliases": ["Mera"], "latitude": 27.7453, "longitude": 86.8647, "elevation_m": 6476, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 198},
    {"name": "Huayna Potosi", "aliases": ["Huayna Potosí"], "latitude": -16.2639, "longitude": -68.1500, "elevation_m": 6088, "region": "Andes", "country": "Bolivia", "state_province": "La Paz", "popularity_rank": 200},

    # =========================================================================
    # MODERATELY KNOWN — SERIOUS HIKERS (rank 201-400)
    # =========================================================================

    # --- South America ---
    {"name": "Chimborazo", "aliases": ["Volcán Chimborazo"], "latitude": -1.4694, "longitude": -78.8175, "elevation_m": 6263, "region": "Andes", "country": "Ecuador", "state_province": "Chimborazo", "popularity_rank": 202},
    {"name": "Alpamayo", "aliases": ["Nevado Alpamayo"], "latitude": -8.8792, "longitude": -77.6531, "elevation_m": 5947, "region": "Andes", "country": "Peru", "state_province": "Ancash", "popularity_rank": 205},
    {"name": "Cerro Torre", "aliases": ["Torre"], "latitude": -49.2958, "longitude": -73.1128, "elevation_m": 3128, "region": "Patagonia", "country": "Argentina", "state_province": "Santa Cruz", "popularity_rank": 208},
    {"name": "Nevado de Toluca", "aliases": ["Xinantecatl", "Toluca"], "latitude": 19.1083, "longitude": -99.7578, "elevation_m": 4680, "region": "Trans-Mexican Volcanic Belt", "country": "Mexico", "state_province": "Mexico State", "popularity_rank": 210},
    {"name": "Mount Meru", "aliases": ["Meru"], "latitude": -3.2464, "longitude": 36.7519, "elevation_m": 4566, "region": "East Africa", "country": "Tanzania", "state_province": "Arusha", "popularity_rank": 212},
    {"name": "La Malinche", "aliases": ["Malintzin", "Matlalcueitl"], "latitude": 19.2314, "longitude": -98.0311, "elevation_m": 4461, "region": "Trans-Mexican Volcanic Belt", "country": "Mexico", "state_province": "Tlaxcala", "popularity_rank": 215},
    {"name": "Nevado del Ruiz", "aliases": ["Ruiz", "Cumanday"], "latitude": 4.8917, "longitude": -75.3219, "elevation_m": 5321, "region": "Andes", "country": "Colombia", "state_province": "Caldas", "popularity_rank": 218},

    # --- PNW / US Obscure ---
    {"name": "Colchuck Peak", "aliases": ["Colchuck"], "latitude": 47.5261, "longitude": -120.8344, "elevation_m": 2706, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 220},
    {"name": "Dragontail Peak", "aliases": ["Dragontail"], "latitude": 47.5278, "longitude": -120.8147, "elevation_m": 2690, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 225},
    {"name": "Sahale Peak", "aliases": ["Sahale"], "latitude": 48.5061, "longitude": -121.1978, "elevation_m": 2768, "region": "North Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 228},
    {"name": "Middle Teton", "aliases": ["Middle"], "latitude": 43.7372, "longitude": -110.8047, "elevation_m": 3903, "region": "Teton Range", "country": "US", "state_province": "Wyoming", "popularity_rank": 230},
    {"name": "Mount Dickerman", "aliases": ["Dickerman"], "latitude": 48.0553, "longitude": -121.4939, "elevation_m": 1789, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 233},
    {"name": "Mount Olympus", "aliases": ["Olympus WA"], "latitude": 47.8013, "longitude": -123.7108, "elevation_m": 2432, "region": "Olympics", "country": "US", "state_province": "Washington", "popularity_rank": 235},
    {"name": "Ingalls Peak", "aliases": ["Ingalls"], "latitude": 47.4492, "longitude": -120.9194, "elevation_m": 2337, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 238},

    # --- Asia expansion ---
    {"name": "Siguniang", "aliases": ["Mount Siguniang", "Four Girls Mountain", "Si Gu Niang"], "latitude": 31.0983, "longitude": 102.8972, "elevation_m": 6250, "region": "Sichuan", "country": "China", "state_province": "Sichuan", "popularity_rank": 240},
    {"name": "Seoraksan", "aliases": ["Seorak Mountain", "Soraksan", "Mount Seorak"], "latitude": 38.1197, "longitude": 128.4656, "elevation_m": 1708, "region": "Taebaek Mountains", "country": "South Korea", "state_province": "Gangwon", "popularity_rank": 242},
    {"name": "Crestone Needle", "aliases": ["Crestone"], "latitude": 37.9647, "longitude": -105.5764, "elevation_m": 4327, "region": "Sangre de Cristo", "country": "US", "state_province": "Colorado", "popularity_rank": 245},
    {"name": "Kitadake", "aliases": ["Mount Kita", "Kita-dake"], "latitude": 35.6742, "longitude": 138.2367, "elevation_m": 3193, "region": "Japanese Alps", "country": "Japan", "state_province": "Yamanashi", "popularity_rank": 247},
    {"name": "Sneffels", "aliases": ["Mount Sneffels"], "latitude": 38.0039, "longitude": -107.7922, "elevation_m": 4312, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 250},
    {"name": "Jade Dragon Snow Mountain", "aliases": ["Yulong Xueshan", "Yulong Snow Mountain"], "latitude": 27.1167, "longitude": 100.1833, "elevation_m": 5596, "region": "Yunnan", "country": "China", "state_province": "Yunnan", "popularity_rank": 252},
    {"name": "Handies Peak", "aliases": ["Handies"], "latitude": 37.9133, "longitude": -107.5044, "elevation_m": 4282, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 255},
    {"name": "Nanda Devi", "aliases": ["Nanda Devi Peak"], "latitude": 30.3742, "longitude": 79.9742, "elevation_m": 7816, "region": "Himalayas", "country": "India", "state_province": "Uttarakhand", "popularity_rank": 257},
    {"name": "Mount Pugh", "aliases": ["Pugh"], "latitude": 48.2203, "longitude": -121.4058, "elevation_m": 2178, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 260},
    {"name": "Mount Pulag", "aliases": ["Pulag"], "latitude": 16.5872, "longitude": 120.8861, "elevation_m": 2922, "region": "Cordillera Central", "country": "Philippines", "state_province": "Benguet", "popularity_rank": 262},
    {"name": "Vesper Peak", "aliases": ["Vesper"], "latitude": 48.0897, "longitude": -121.4867, "elevation_m": 1977, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 265},
    {"name": "Hotaka", "aliases": ["Mount Hotaka", "Hotaka-dake", "Oku-Hotaka"], "latitude": 36.2892, "longitude": 137.6483, "elevation_m": 3190, "region": "Japanese Alps", "country": "Japan", "state_province": "Nagano", "popularity_rank": 267},
    {"name": "Wetterhorn Peak", "aliases": ["Wetterhorn"], "latitude": 38.0606, "longitude": -107.5106, "elevation_m": 4272, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 270},
    {"name": "Erciyes", "aliases": ["Mount Erciyes", "Erciyes Dagi"], "latitude": 38.5319, "longitude": 35.4469, "elevation_m": 3917, "region": "Central Anatolia", "country": "Turkey", "state_province": "Kayseri", "popularity_rank": 272},
    {"name": "Mount Moosilauke", "aliases": ["Moosilauke"], "latitude": 44.0239, "longitude": -71.8311, "elevation_m": 1464, "region": "White Mountains", "country": "US", "state_province": "New Hampshire", "popularity_rank": 275},
    {"name": "Jirisan", "aliases": ["Mount Jiri", "Jiri Mountain"], "latitude": 35.3372, "longitude": 127.7308, "elevation_m": 1915, "region": "Sobaek Mountains", "country": "South Korea", "state_province": "South Gyeongsang", "popularity_rank": 277},
    {"name": "Mount Carrigain", "aliases": ["Carrigain"], "latitude": 44.0939, "longitude": -71.4467, "elevation_m": 1421, "region": "White Mountains", "country": "US", "state_province": "New Hampshire", "popularity_rank": 280},
    {"name": "Mount Apo", "aliases": ["Apo"], "latitude": 6.9876, "longitude": 125.2707, "elevation_m": 2954, "region": "Mindanao", "country": "Philippines", "state_province": "Davao del Sur", "popularity_rank": 282},
    {"name": "Whiteface Mountain", "aliases": ["Whiteface"], "latitude": 44.3658, "longitude": -73.9027, "elevation_m": 1483, "region": "Adirondacks", "country": "US", "state_province": "New York", "popularity_rank": 285},
    {"name": "Wutai Shan", "aliases": ["Mount Wutai", "Wutaishan", "Five Terrace Mountain"], "latitude": 39.0775, "longitude": 113.5928, "elevation_m": 3058, "region": "Shanxi", "country": "China", "state_province": "Shanxi", "popularity_rank": 287},
    {"name": "Algonquin Peak", "aliases": ["Algonquin"], "latitude": 44.1436, "longitude": -73.9867, "elevation_m": 1559, "region": "Adirondacks", "country": "US", "state_province": "New York", "popularity_rank": 290},
    {"name": "Esja", "aliases": ["Mount Esja", "Esjan"], "latitude": 64.2500, "longitude": -21.6833, "elevation_m": 914, "region": "Southwest Iceland", "country": "Iceland", "state_province": "Capital Region", "popularity_rank": 292},
    {"name": "Aiguille du Midi", "aliases": ["Midi", "Aiguille Midi"], "latitude": 45.8787, "longitude": 6.8873, "elevation_m": 3842, "region": "Alps", "country": "France", "state_province": "Haute-Savoie", "popularity_rank": 295},
    {"name": "Kackar", "aliases": ["Kackar Dagi", "Kaçkar Dağı", "Mount Kackar"], "latitude": 40.8375, "longitude": 41.1864, "elevation_m": 3937, "region": "Pontic Alps", "country": "Turkey", "state_province": "Rize", "popularity_rank": 297},
    {"name": "Weisshorn", "aliases": ["Weisshorn Peak"], "latitude": 46.1067, "longitude": 7.7161, "elevation_m": 4506, "region": "Alps", "country": "Switzerland", "state_province": "Valais", "popularity_rank": 300},
    {"name": "Piz Bernina", "aliases": ["Bernina"], "latitude": 46.3817, "longitude": 9.9072, "elevation_m": 4049, "region": "Alps", "country": "Switzerland", "state_province": "Graubunden", "popularity_rank": 302},
    {"name": "Barre des Ecrins", "aliases": ["Ecrins"], "latitude": 44.9219, "longitude": 6.3583, "elevation_m": 4102, "region": "Dauphine Alps", "country": "France", "state_province": "Hautes-Alpes", "popularity_rank": 305},
    {"name": "Pizzo Badile", "aliases": ["Badile"], "latitude": 46.2931, "longitude": 9.5653, "elevation_m": 3305, "region": "Alps", "country": "Switzerland", "state_province": "Graubunden", "popularity_rank": 308},
    {"name": "Vignemale", "aliases": ["Pique Longue", "Vignemale Peak"], "latitude": 42.7742, "longitude": -0.1464, "elevation_m": 3298, "region": "Pyrenees", "country": "France", "state_province": "Hautes-Pyrenees", "popularity_rank": 310},
    {"name": "Monte Perdido", "aliases": ["Mont Perdu", "Mount Perdido"], "latitude": 42.6756, "longitude": 0.0328, "elevation_m": 3355, "region": "Pyrenees", "country": "Spain", "state_province": "Aragon", "popularity_rank": 312},
    {"name": "Sass Pordoi", "aliases": ["Pordoi"], "latitude": 46.4978, "longitude": 11.8183, "elevation_m": 2950, "region": "Dolomites", "country": "Italy", "state_province": "Trentino", "popularity_rank": 315},
    {"name": "Ortler", "aliases": ["Ortles", "Gran Zebrù"], "latitude": 46.5072, "longitude": 10.5433, "elevation_m": 3905, "region": "Alps", "country": "Italy", "state_province": "South Tyrol", "popularity_rank": 317},
    {"name": "Civetta", "aliases": ["Monte Civetta"], "latitude": 46.3722, "longitude": 12.0531, "elevation_m": 3220, "region": "Dolomites", "country": "Italy", "state_province": "Veneto", "popularity_rank": 320},
    {"name": "Mount Yamnuska", "aliases": ["Yamnuska", "Yam"], "latitude": 51.1539, "longitude": -115.1458, "elevation_m": 2240, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 322},
    {"name": "Kirkjufell", "aliases": ["Church Mountain"], "latitude": 64.9426, "longitude": -23.3071, "elevation_m": 463, "region": "Snaefellsnes", "country": "Iceland", "state_province": "West Iceland", "popularity_rank": 325},
    {"name": "Makalu", "aliases": ["Mahalangur"], "latitude": 27.8897, "longitude": 87.0886, "elevation_m": 8485, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 327},
    {"name": "Tent Ridge", "aliases": ["Tent Ridge Horseshoe"], "latitude": 50.8083, "longitude": -115.3583, "elevation_m": 2525, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 330},
    {"name": "Ras Dashen", "aliases": ["Ras Dejen", "Dashen"], "latitude": 13.2333, "longitude": 38.3667, "elevation_m": 4550, "region": "Simien Mountains", "country": "Ethiopia", "state_province": "Amhara", "popularity_rank": 332},
    {"name": "Mount Lady Macdonald", "aliases": ["Lady Mac", "Lady Macdonald"], "latitude": 51.0833, "longitude": -115.3417, "elevation_m": 2605, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 335},
    {"name": "Dom", "aliases": ["Dom Peak"], "latitude": 46.0908, "longitude": 7.8578, "elevation_m": 4545, "region": "Alps", "country": "Switzerland", "state_province": "Valais", "popularity_rank": 337},
    {"name": "The Lions", "aliases": ["The Twin Sisters", "Lions Peaks"], "latitude": 49.4569, "longitude": -123.1833, "elevation_m": 1646, "region": "North Shore Mountains", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 340},
    {"name": "Wildspitze", "aliases": ["Wildspitz"], "latitude": 46.8853, "longitude": 10.8672, "elevation_m": 3768, "region": "Alps", "country": "Austria", "state_province": "Tyrol", "popularity_rank": 342},
    {"name": "Mount Seymour", "aliases": ["Seymour"], "latitude": 49.3694, "longitude": -122.9472, "elevation_m": 1449, "region": "North Shore Mountains", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 345},
    {"name": "Shkhara", "aliases": ["Mount Shkhara"], "latitude": 42.9997, "longitude": 43.1094, "elevation_m": 5193, "region": "Caucasus", "country": "Georgia", "state_province": "Svaneti", "popularity_rank": 347},
    {"name": "Mount Mayon", "aliases": ["Mayon Volcano", "Mayon"], "latitude": 13.2575, "longitude": 123.6856, "elevation_m": 2462, "region": "Luzon", "country": "Philippines", "state_province": "Albay", "popularity_rank": 350},
    {"name": "Nevado de Colima", "aliases": ["Colima Volcano", "Volcán de Colima"], "latitude": 19.5128, "longitude": -103.6178, "elevation_m": 4271, "region": "Trans-Mexican Volcanic Belt", "country": "Mexico", "state_province": "Jalisco", "popularity_rank": 352},
    {"name": "Snaefellsjokull", "aliases": ["Snæfellsjökull", "Snaefell"], "latitude": 64.8039, "longitude": -23.7761, "elevation_m": 1446, "region": "Snaefellsnes", "country": "Iceland", "state_province": "West Iceland", "popularity_rank": 355},
    {"name": "Pen y Fan", "aliases": ["Pen-y-Fan"], "latitude": 51.8839, "longitude": -3.4367, "elevation_m": 886, "region": "Brecon Beacons", "country": "UK", "state_province": "Wales", "popularity_rank": 357},
    {"name": "Uludag", "aliases": ["Mount Uludag", "Uludağ", "Great Mountain"], "latitude": 40.0781, "longitude": 29.2219, "elevation_m": 2543, "region": "Marmara", "country": "Turkey", "state_province": "Bursa", "popularity_rank": 360},
    {"name": "Mount Aso", "aliases": ["Aso-san", "Aso"], "latitude": 32.8842, "longitude": 131.1042, "elevation_m": 1592, "region": "Kyushu", "country": "Japan", "state_province": "Kumamoto", "popularity_rank": 362},
    {"name": "Pic du Canigou", "aliases": ["Canigou", "Canigó"], "latitude": 42.5192, "longitude": 2.4564, "elevation_m": 2784, "region": "Pyrenees", "country": "France", "state_province": "Pyrenees-Orientales", "popularity_rank": 365},
    {"name": "Nevado del Tolima", "aliases": ["Tolima"], "latitude": 4.6578, "longitude": -75.3300, "elevation_m": 5215, "region": "Andes", "country": "Colombia", "state_province": "Tolima", "popularity_rank": 367},
    {"name": "Mount Batur", "aliases": ["Gunung Batur", "Batur"], "latitude": -8.2417, "longitude": 115.3750, "elevation_m": 1717, "region": "Bali", "country": "Indonesia", "state_province": "Bali", "popularity_rank": 370},
    {"name": "Doi Chiang Dao", "aliases": ["Chiang Dao", "Doi Luang Chiang Dao"], "latitude": 19.4042, "longitude": 98.9208, "elevation_m": 2225, "region": "Thai Highlands", "country": "Thailand", "state_province": "Chiang Mai", "popularity_rank": 372},
    {"name": "Rwenzori", "aliases": ["Mount Stanley", "Margherita Peak", "Mountains of the Moon"], "latitude": 0.3856, "longitude": 29.8722, "elevation_m": 5109, "region": "East Africa", "country": "Uganda", "state_province": "Western", "popularity_rank": 375},
    {"name": "Lhotse", "aliases": ["Lhotse Peak"], "latitude": 27.9617, "longitude": 86.9331, "elevation_m": 8516, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 377},
    {"name": "Musala", "aliases": ["Mount Musala"], "latitude": 42.1792, "longitude": 24.6694, "elevation_m": 2925, "region": "Rila Mountains", "country": "Bulgaria", "state_province": "Blagoevgrad", "popularity_rank": 380},
    {"name": "Sierra Cocuy", "aliases": ["Nevado del Cocuy", "Parque Nacional Cocuy"], "latitude": 6.4000, "longitude": -72.3167, "elevation_m": 5330, "region": "Andes", "country": "Colombia", "state_province": "Boyaca", "popularity_rank": 382},
    {"name": "Moldoveanu", "aliases": ["Vârful Moldoveanu", "Mount Moldoveanu"], "latitude": 45.6017, "longitude": 24.7353, "elevation_m": 2544, "region": "Fagaras Mountains", "country": "Romania", "state_province": "Arges", "popularity_rank": 385},
    {"name": "Cradle Mountain", "aliases": ["Cradle"], "latitude": -41.6542, "longitude": 145.9422, "elevation_m": 1545, "region": "Tasmania", "country": "Australia", "state_province": "Tasmania", "popularity_rank": 387},
    {"name": "Triund", "aliases": ["Triund Hill"], "latitude": 32.2553, "longitude": 76.3189, "elevation_m": 2828, "region": "Himalayas", "country": "India", "state_province": "Himachal Pradesh", "popularity_rank": 390},
    {"name": "Hvannadalshnukur", "aliases": ["Hvannadalshnjúkur", "Hvannadals"], "latitude": 64.0133, "longitude": -16.6500, "elevation_m": 2110, "region": "Oraefajokull", "country": "Iceland", "state_province": "East Iceland", "popularity_rank": 392},
    {"name": "Piton des Neiges", "aliases": ["Piton"], "latitude": -21.0992, "longitude": 55.4833, "elevation_m": 3069, "region": "Reunion Island", "country": "France", "state_province": "Reunion", "popularity_rank": 395},
    {"name": "Marmolada", "aliases": ["Queen of the Dolomites"], "latitude": 46.4347, "longitude": 11.8558, "elevation_m": 3343, "region": "Dolomites", "country": "Italy", "state_province": "Trentino", "popularity_rank": 397},
    {"name": "Ushba", "aliases": ["Mount Ushba"], "latitude": 43.0244, "longitude": 42.6389, "elevation_m": 4710, "region": "Caucasus", "country": "Georgia", "state_province": "Svaneti", "popularity_rank": 400},

    # =========================================================================
    # LOCAL FAVORITES — DEDICATED HIKERS (rank 401-600)
    # =========================================================================

    # --- Asia ---
    {"name": "Heng Shan North", "aliases": ["Mount Heng", "Northern Hengshan", "Heng Shan Shanxi"], "latitude": 39.6797, "longitude": 113.7442, "elevation_m": 2017, "region": "Shanxi", "country": "China", "state_province": "Shanxi", "popularity_rank": 402},
    {"name": "Tsukuba", "aliases": ["Mount Tsukuba", "Tsukuba-san"], "latitude": 36.2253, "longitude": 140.1006, "elevation_m": 877, "region": "Kanto", "country": "Japan", "state_province": "Ibaraki", "popularity_rank": 405},
    {"name": "Miyanoura-dake", "aliases": ["Miyanoura Peak", "Mount Miyanoura"], "latitude": 30.3358, "longitude": 130.5017, "elevation_m": 1936, "region": "Yakushima", "country": "Japan", "state_province": "Kagoshima", "popularity_rank": 408},
    {"name": "Doi Suthep", "aliases": ["Suthep"], "latitude": 18.8044, "longitude": 98.9217, "elevation_m": 1676, "region": "Thai Highlands", "country": "Thailand", "state_province": "Chiang Mai", "popularity_rank": 410},
    {"name": "Song Shan", "aliases": ["Mount Song", "Songshan", "Central Sacred Peak"], "latitude": 34.4833, "longitude": 113.0667, "elevation_m": 1512, "region": "Henan", "country": "China", "state_province": "Henan", "popularity_rank": 412},
    {"name": "Pinatubo", "aliases": ["Mount Pinatubo"], "latitude": 15.1429, "longitude": 120.3496, "elevation_m": 1486, "region": "Luzon", "country": "Philippines", "state_province": "Zambales", "popularity_rank": 415},
    {"name": "Taal", "aliases": ["Taal Volcano"], "latitude": 14.0113, "longitude": 120.9980, "elevation_m": 311, "region": "Luzon", "country": "Philippines", "state_province": "Batangas", "popularity_rank": 418},
    {"name": "Kedarnath Peak", "aliases": ["Kedarnath", "Kedar Dome"], "latitude": 30.7458, "longitude": 79.0669, "elevation_m": 6940, "region": "Himalayas", "country": "India", "state_province": "Uttarakhand", "popularity_rank": 420},
    {"name": "Gongga Shan", "aliases": ["Minya Konka", "Mount Gongga"], "latitude": 29.5958, "longitude": 101.8783, "elevation_m": 7556, "region": "Sichuan", "country": "China", "state_province": "Sichuan", "popularity_rank": 423},
    {"name": "Chandrashila", "aliases": ["Chandrashila Peak"], "latitude": 30.4886, "longitude": 79.2192, "elevation_m": 4000, "region": "Himalayas", "country": "India", "state_province": "Uttarakhand", "popularity_rank": 425},
    {"name": "Mount Bromo", "aliases": ["Gunung Bromo", "Bromo"], "latitude": -7.9425, "longitude": 112.9528, "elevation_m": 2329, "region": "Java", "country": "Indonesia", "state_province": "East Java", "popularity_rank": 428},
    {"name": "Cho Oyu", "aliases": ["Cho Oyu Peak"], "latitude": 28.0942, "longitude": 86.6608, "elevation_m": 8188, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 430},
    {"name": "Dhaulagiri", "aliases": ["Dhaulagiri I", "White Mountain"], "latitude": 28.6983, "longitude": 83.4875, "elevation_m": 8167, "region": "Himalayas", "country": "Nepal", "state_province": "Gandaki", "popularity_rank": 432},
    {"name": "Roopkund", "aliases": ["Roopkund Trek", "Mystery Lake Peak"], "latitude": 30.2622, "longitude": 79.7311, "elevation_m": 5029, "region": "Himalayas", "country": "India", "state_province": "Uttarakhand", "popularity_rank": 435},
    {"name": "Tetnuldi", "aliases": ["Mount Tetnuldi"], "latitude": 43.0333, "longitude": 42.9667, "elevation_m": 4858, "region": "Caucasus", "country": "Georgia", "state_province": "Svaneti", "popularity_rank": 437},
    {"name": "Gwanaksan", "aliases": ["Gwanak Mountain"], "latitude": 37.4428, "longitude": 126.9636, "elevation_m": 632, "region": "Seoul Metropolitan", "country": "South Korea", "state_province": "Seoul", "popularity_rank": 440},

    # --- Europe ---
    {"name": "Liskamm", "aliases": ["Lyskamm"], "latitude": 45.9267, "longitude": 7.8433, "elevation_m": 4527, "region": "Alps", "country": "Switzerland", "state_province": "Valais", "popularity_rank": 442},
    {"name": "Presolana", "aliases": ["Monte Presolana"], "latitude": 45.9750, "longitude": 10.0667, "elevation_m": 2521, "region": "Alps", "country": "Italy", "state_province": "Lombardy", "popularity_rank": 445},
    {"name": "Hasan Dagi", "aliases": ["Mount Hasan", "Hasan Dağı"], "latitude": 38.1333, "longitude": 34.1667, "elevation_m": 3268, "region": "Central Anatolia", "country": "Turkey", "state_province": "Aksaray", "popularity_rank": 448},
    {"name": "Suphan Dagi", "aliases": ["Mount Suphan", "Süphan Dağı"], "latitude": 38.9236, "longitude": 42.8242, "elevation_m": 4058, "region": "Eastern Turkey", "country": "Turkey", "state_province": "Bitlis", "popularity_rank": 450},
    {"name": "Cir Mhor", "aliases": ["Goat Fell"], "latitude": 55.6361, "longitude": -5.1833, "elevation_m": 799, "region": "Scottish Highlands", "country": "UK", "state_province": "Scotland", "popularity_rank": 453},
    {"name": "Glittertind", "aliases": ["Glittertinden"], "latitude": 61.6514, "longitude": 8.3336, "elevation_m": 2465, "region": "Jotunheimen", "country": "Norway", "state_province": "Innlandet", "popularity_rank": 455},
    {"name": "Store Skagastolstind", "aliases": ["Storen"], "latitude": 61.5178, "longitude": 7.8175, "elevation_m": 2405, "region": "Jotunheimen", "country": "Norway", "state_province": "Vestland", "popularity_rank": 458},
    {"name": "Punta Walker", "aliases": ["Grandes Jorasses"], "latitude": 45.8694, "longitude": 6.9833, "elevation_m": 4208, "region": "Alps", "country": "France", "state_province": "Haute-Savoie", "popularity_rank": 460},
    {"name": "Omu Peak", "aliases": ["Vârful Omu", "Mount Omu"], "latitude": 45.4442, "longitude": 25.4569, "elevation_m": 2507, "region": "Bucegi Mountains", "country": "Romania", "state_province": "Prahova", "popularity_rank": 463},
    {"name": "Eyjafjallajokull", "aliases": ["Eyjafjallajökull", "Eyjafjalla"], "latitude": 63.6310, "longitude": -19.6217, "elevation_m": 1651, "region": "South Iceland", "country": "Iceland", "state_province": "South Iceland", "popularity_rank": 465},
    {"name": "Aiguille Verte", "aliases": ["Verte"], "latitude": 45.9353, "longitude": 6.9217, "elevation_m": 4122, "region": "Alps", "country": "France", "state_province": "Haute-Savoie", "popularity_rank": 468},
    {"name": "Popocatepetl", "aliases": ["Popo", "Popocatépetl", "El Popo"], "latitude": 19.0225, "longitude": -98.6278, "elevation_m": 5426, "region": "Trans-Mexican Volcanic Belt", "country": "Mexico", "state_province": "Puebla", "popularity_rank": 470},
    {"name": "Negoiu", "aliases": ["Vârful Negoiu", "Mount Negoiu"], "latitude": 45.5972, "longitude": 24.5556, "elevation_m": 2535, "region": "Fagaras Mountains", "country": "Romania", "state_province": "Sibiu", "popularity_rank": 472},
    {"name": "Snowdon Horseshoe", "aliases": ["Crib Goch", "Snowdon Ridge"], "latitude": 53.0700, "longitude": -4.0650, "elevation_m": 1085, "region": "Snowdonia", "country": "UK", "state_province": "Wales", "popularity_rank": 475},

    # --- Americas ---
    {"name": "Mount Monadnock", "aliases": ["Monadnock", "Grand Monadnock"], "latitude": 42.8614, "longitude": -72.1081, "elevation_m": 965, "region": "New England", "country": "US", "state_province": "New Hampshire", "popularity_rank": 478},
    {"name": "Bear Peak", "aliases": ["Bear"], "latitude": 39.9558, "longitude": -105.2844, "elevation_m": 2578, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 480},
    {"name": "Mount Leconte", "aliases": ["LeConte", "Le Conte"], "latitude": 35.6542, "longitude": -83.4353, "elevation_m": 2010, "region": "Great Smoky Mountains", "country": "US", "state_province": "Tennessee", "popularity_rank": 483},
    {"name": "Mount Stuart", "aliases": ["Stuart"], "latitude": 47.4753, "longitude": -120.9022, "elevation_m": 2871, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 485},
    {"name": "Cascade Mountain", "aliases": ["Cascade ADK"], "latitude": 44.2189, "longitude": -73.8603, "elevation_m": 1339, "region": "Adirondacks", "country": "US", "state_province": "New York", "popularity_rank": 488},
    {"name": "Mount Timpanogos", "aliases": ["Timp", "Timpanogos"], "latitude": 40.3906, "longitude": -111.6464, "elevation_m": 3581, "region": "Wasatch Range", "country": "US", "state_province": "Utah", "popularity_rank": 490},
    {"name": "Mount Sopris", "aliases": ["Sopris"], "latitude": 39.2414, "longitude": -107.2175, "elevation_m": 3953, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 493},
    {"name": "Mount Tammany", "aliases": ["Tammany", "Kittatinny"], "latitude": 40.9689, "longitude": -75.1244, "elevation_m": 527, "region": "Appalachians", "country": "US", "state_province": "New Jersey", "popularity_rank": 495},
    {"name": "Sleeping Beauty Mountain", "aliases": ["Sleeping Beauty"], "latitude": 43.5753, "longitude": -73.6581, "elevation_m": 585, "region": "Adirondacks", "country": "US", "state_province": "New York", "popularity_rank": 498},
    {"name": "Camelback Mountain", "aliases": ["Camelback"], "latitude": 33.5229, "longitude": -111.9725, "elevation_m": 824, "region": "Sonoran Desert", "country": "US", "state_province": "Arizona", "popularity_rank": 500},

    # --- Africa / Oceania ---
    {"name": "M'Goun", "aliases": ["Jebel Mgoun", "Ighil M'Goun"], "latitude": 31.5000, "longitude": -6.4500, "elevation_m": 4071, "region": "Atlas Mountains", "country": "Morocco", "state_province": "Beni Mellal-Khenifra", "popularity_rank": 503},
    {"name": "Mount Meru", "aliases": ["Meru Tanzania"], "latitude": -3.2464, "longitude": 36.7519, "elevation_m": 4566, "region": "East Africa", "country": "Tanzania", "state_province": "Arusha", "popularity_rank": 505},
    {"name": "Blue Mountains", "aliases": ["Blue Mountain Peak", "Blue Mountains JM"], "latitude": 18.1133, "longitude": -76.5833, "elevation_m": 2256, "region": "Caribbean", "country": "Jamaica", "state_province": "Portland", "popularity_rank": 508},
    {"name": "Mount Taranaki", "aliases": ["Taranaki", "Mount Egmont", "Egmont"], "latitude": -39.2967, "longitude": 174.0639, "elevation_m": 2518, "region": "North Island", "country": "New Zealand", "state_province": "Taranaki", "popularity_rank": 510},
    {"name": "Mueller Hut Route", "aliases": ["Mueller Hut", "Sealy Tarns"], "latitude": -43.7167, "longitude": 170.0833, "elevation_m": 1800, "region": "Southern Alps", "country": "New Zealand", "state_province": "Canterbury", "popularity_rank": 513},
    {"name": "Roys Peak", "aliases": ["Roy's Peak"], "latitude": -44.6789, "longitude": 169.0544, "elevation_m": 1578, "region": "Southern Alps", "country": "New Zealand", "state_province": "Otago", "popularity_rank": 515},

    # --- More Asia ---
    {"name": "Meili Snow Mountain", "aliases": ["Meili Xueshan", "Kawagebo"], "latitude": 28.4333, "longitude": 98.7500, "elevation_m": 6740, "region": "Yunnan", "country": "China", "state_province": "Yunnan", "popularity_rank": 518},
    {"name": "Langtang Lirung", "aliases": ["Langtang", "Langtang Peak"], "latitude": 28.2564, "longitude": 85.5158, "elevation_m": 7234, "region": "Himalayas", "country": "Nepal", "state_province": "Bagmati", "popularity_rank": 520},
    {"name": "Hamdeok Oreum", "aliases": ["Hamdeok Hill"], "latitude": 33.5417, "longitude": 126.6700, "elevation_m": 163, "region": "Jeju", "country": "South Korea", "state_province": "Jeju", "popularity_rank": 523},
    {"name": "Poon Hill", "aliases": ["Poonhill"], "latitude": 28.3981, "longitude": 83.6878, "elevation_m": 3210, "region": "Himalayas", "country": "Nepal", "state_province": "Gandaki", "popularity_rank": 525},
    {"name": "Gokyo Ri", "aliases": ["Gokyo Peak"], "latitude": 27.9500, "longitude": 86.6833, "elevation_m": 5357, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 528},
    {"name": "Kala Patthar", "aliases": ["Kala Pattar", "Kalapatthar"], "latitude": 27.9953, "longitude": 86.8278, "elevation_m": 5643, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 530},
    {"name": "Lushan", "aliases": ["Mount Lu", "Lu Shan"], "latitude": 29.5642, "longitude": 115.9925, "elevation_m": 1474, "region": "Jiangxi", "country": "China", "state_province": "Jiangxi", "popularity_rank": 533},

    # --- More Canada ---
    {"name": "Mont Tremblant", "aliases": ["Tremblant"], "latitude": 46.2125, "longitude": -74.5833, "elevation_m": 875, "region": "Laurentians", "country": "Canada", "state_province": "Quebec", "popularity_rank": 535},
    {"name": "Mount Logan", "aliases": ["Logan"], "latitude": 60.5672, "longitude": -140.4061, "elevation_m": 5959, "region": "Saint Elias Mountains", "country": "Canada", "state_province": "Yukon", "popularity_rank": 538},
    {"name": "The Stawamus Chief Second Peak", "aliases": ["Second Peak Squamish"], "latitude": 49.6767, "longitude": -123.1417, "elevation_m": 655, "region": "Sea to Sky", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 540},
    {"name": "Mount Revelstoke", "aliases": ["Revelstoke"], "latitude": 51.0833, "longitude": -118.0667, "elevation_m": 1938, "region": "Columbia Mountains", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 543},
    {"name": "Gros Morne Mountain", "aliases": ["Gros Morne"], "latitude": 49.5961, "longitude": -57.7858, "elevation_m": 806, "region": "Appalachians", "country": "Canada", "state_province": "Newfoundland", "popularity_rank": 545},

    # --- More US ---
    {"name": "Mount Katadin Knife Edge", "aliases": ["Knife Edge Trail"], "latitude": 45.9036, "longitude": -68.9156, "elevation_m": 1606, "region": "Appalachians", "country": "US", "state_province": "Maine", "popularity_rank": 548},
    {"name": "Angels Landing", "aliases": ["Angels Landing Zion"], "latitude": 37.2694, "longitude": -112.9481, "elevation_m": 1765, "region": "Colorado Plateau", "country": "US", "state_province": "Utah", "popularity_rank": 550},
    {"name": "Cloud Peak", "aliases": ["Cloud"], "latitude": 44.3828, "longitude": -107.1742, "elevation_m": 4013, "region": "Bighorn Mountains", "country": "US", "state_province": "Wyoming", "popularity_rank": 553},
    {"name": "Mount Borah", "aliases": ["Borah Peak", "Borah"], "latitude": 44.1374, "longitude": -113.7811, "elevation_m": 3859, "region": "Lost River Range", "country": "US", "state_province": "Idaho", "popularity_rank": 555},
    {"name": "Breakneck Ridge", "aliases": ["Breakneck"], "latitude": 41.4472, "longitude": -73.9728, "elevation_m": 383, "region": "Hudson Highlands", "country": "US", "state_province": "New York", "popularity_rank": 558},
    {"name": "South Arapaho Peak", "aliases": ["Arapaho Peak"], "latitude": 40.0228, "longitude": -105.6500, "elevation_m": 4118, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 560},
    {"name": "Mount Pisgah", "aliases": ["Pisgah"], "latitude": 35.4264, "longitude": -82.7553, "elevation_m": 1522, "region": "Blue Ridge", "country": "US", "state_province": "North Carolina", "popularity_rank": 563},
    {"name": "Diamond Head", "aliases": ["Leahi", "Diamond Head Crater"], "latitude": 21.2622, "longitude": -157.8053, "elevation_m": 232, "region": "Hawaii", "country": "US", "state_province": "Hawaii", "popularity_rank": 565},
    {"name": "Mauna Loa", "aliases": ["Long Mountain"], "latitude": 19.4756, "longitude": -155.6028, "elevation_m": 4169, "region": "Hawaii", "country": "US", "state_province": "Hawaii", "popularity_rank": 568},

    # =========================================================================
    # DEEP INSIDER KNOWLEDGE (rank 601-800)
    # =========================================================================

    # --- Asia ---
    {"name": "Heng Shan South", "aliases": ["Southern Hengshan", "Heng Shan Hunan"], "latitude": 27.2536, "longitude": 112.7083, "elevation_m": 1300, "region": "Hunan", "country": "China", "state_province": "Hunan", "popularity_rank": 602},
    {"name": "Qingcheng Shan", "aliases": ["Mount Qingcheng", "Qingchengshan"], "latitude": 30.8667, "longitude": 103.5667, "elevation_m": 1260, "region": "Sichuan", "country": "China", "state_province": "Sichuan", "popularity_rank": 605},
    {"name": "Jiuhua Shan", "aliases": ["Mount Jiuhua", "Jiuhuashan", "Nine Glorious Mountains"], "latitude": 30.4833, "longitude": 117.7833, "elevation_m": 1342, "region": "Anhui Mountains", "country": "China", "state_province": "Anhui", "popularity_rank": 608},
    {"name": "Daisetsuzan", "aliases": ["Taisetsu-zan", "Mount Asahi", "Asahi-dake"], "latitude": 43.6642, "longitude": 142.8528, "elevation_m": 2291, "region": "Hokkaido", "country": "Japan", "state_province": "Hokkaido", "popularity_rank": 610},
    {"name": "Yarigatake", "aliases": ["Yari-ga-take", "Mount Yari"], "latitude": 36.3417, "longitude": 137.6478, "elevation_m": 3180, "region": "Japanese Alps", "country": "Japan", "state_province": "Nagano", "popularity_rank": 613},
    {"name": "Hambaeksan", "aliases": ["Hambaek Mountain"], "latitude": 37.0917, "longitude": 129.0028, "elevation_m": 1573, "region": "Taebaek Mountains", "country": "South Korea", "state_province": "Gangwon", "popularity_rank": 615},
    {"name": "Sandakphu", "aliases": ["Sandakfu"], "latitude": 27.1000, "longitude": 88.0000, "elevation_m": 3636, "region": "Himalayas", "country": "India", "state_province": "West Bengal", "popularity_rank": 618},
    {"name": "Har Ki Dun", "aliases": ["Valley of Gods Peak"], "latitude": 31.1500, "longitude": 78.4000, "elevation_m": 3566, "region": "Himalayas", "country": "India", "state_province": "Uttarakhand", "popularity_rank": 620},
    {"name": "Mount Semeru", "aliases": ["Gunung Semeru", "Semeru", "Mahameru"], "latitude": -8.1077, "longitude": 112.9222, "elevation_m": 3676, "region": "Java", "country": "Indonesia", "state_province": "East Java", "popularity_rank": 623},
    {"name": "Mount Agung", "aliases": ["Gunung Agung", "Agung"], "latitude": -8.3433, "longitude": 115.5072, "elevation_m": 3031, "region": "Bali", "country": "Indonesia", "state_province": "Bali", "popularity_rank": 625},

    # --- Europe ---
    {"name": "Monte Viso", "aliases": ["Monviso"], "latitude": 44.6672, "longitude": 7.0917, "elevation_m": 3841, "region": "Alps", "country": "Italy", "state_province": "Piedmont", "popularity_rank": 628},
    {"name": "Pico de Europa", "aliases": ["Naranjo de Bulnes", "Picu Urriellu"], "latitude": 43.2000, "longitude": -4.8167, "elevation_m": 2519, "region": "Picos de Europa", "country": "Spain", "state_province": "Asturias", "popularity_rank": 630},
    {"name": "Olympus Mytikas", "aliases": ["Olympus Summit"], "latitude": 40.0859, "longitude": 22.3583, "elevation_m": 2917, "region": "Thessaly", "country": "Greece", "state_province": "Pieria", "popularity_rank": 633},
    {"name": "Aletschhorn", "aliases": ["Aletsch"], "latitude": 46.4992, "longitude": 7.9936, "elevation_m": 4195, "region": "Alps", "country": "Switzerland", "state_province": "Valais", "popularity_rank": 635},
    {"name": "Tofana di Rozes", "aliases": ["Tofana"], "latitude": 46.5342, "longitude": 12.0506, "elevation_m": 3225, "region": "Dolomites", "country": "Italy", "state_province": "Veneto", "popularity_rank": 638},
    {"name": "Lyngen Alps", "aliases": ["Store Jægervastind"], "latitude": 69.6000, "longitude": 20.2000, "elevation_m": 1596, "region": "Northern Norway", "country": "Norway", "state_province": "Troms", "popularity_rank": 640},
    {"name": "Romsdalshorn", "aliases": ["Romsdalshornet"], "latitude": 62.4328, "longitude": 7.6328, "elevation_m": 1550, "region": "Romsdalen", "country": "Norway", "state_province": "More og Romsdal", "popularity_rank": 643},
    {"name": "Blea Water", "aliases": ["High Street"], "latitude": 54.4839, "longitude": -2.8483, "elevation_m": 828, "region": "Lake District", "country": "UK", "state_province": "England", "popularity_rank": 645},
    {"name": "Croagh Patrick", "aliases": ["The Reek"], "latitude": 53.7600, "longitude": -9.6603, "elevation_m": 764, "region": "Connemara", "country": "Ireland", "state_province": "Mayo", "popularity_rank": 648},
    {"name": "Moldoveanu Peak South Ridge", "aliases": ["Fagaras Traverse"], "latitude": 45.5967, "longitude": 24.7336, "elevation_m": 2544, "region": "Fagaras Mountains", "country": "Romania", "state_province": "Arges", "popularity_rank": 650},
    {"name": "Herdubreid", "aliases": ["Herðubreið", "Queen of Icelandic Mountains"], "latitude": 65.1792, "longitude": -16.3500, "elevation_m": 1682, "region": "Highlands", "country": "Iceland", "state_province": "Northeast Iceland", "popularity_rank": 653},

    # --- Americas ---
    {"name": "Mount Tyndall", "aliases": ["Tyndall"], "latitude": 36.6392, "longitude": -118.3208, "elevation_m": 4275, "region": "Sierra Nevada", "country": "US", "state_province": "California", "popularity_rank": 655},
    {"name": "Mount San Gorgonio", "aliases": ["San Gorgonio", "Old Grayback"], "latitude": 34.0981, "longitude": -116.8250, "elevation_m": 3506, "region": "San Bernardino Mountains", "country": "US", "state_province": "California", "popularity_rank": 658},
    {"name": "Mount Wrightson", "aliases": ["Wrightson", "Old Baldy AZ"], "latitude": 31.7258, "longitude": -110.8714, "elevation_m": 2881, "region": "Santa Rita Mountains", "country": "US", "state_province": "Arizona", "popularity_rank": 660},
    {"name": "Flatirons", "aliases": ["First Flatiron", "Boulder Flatirons"], "latitude": 39.9886, "longitude": -105.2928, "elevation_m": 2484, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 663},
    {"name": "Bondcliff", "aliases": ["Mount Bond", "Bond Traverse"], "latitude": 44.1531, "longitude": -71.5311, "elevation_m": 1289, "region": "White Mountains", "country": "US", "state_province": "New Hampshire", "popularity_rank": 665},
    {"name": "Helderberg Escarpment", "aliases": ["Indian Ladder Trail"], "latitude": 42.6514, "longitude": -74.0225, "elevation_m": 442, "region": "Appalachians", "country": "US", "state_province": "New York", "popularity_rank": 668},
    {"name": "Mount Cammerer", "aliases": ["Cammerer"], "latitude": 35.7564, "longitude": -83.1592, "elevation_m": 1524, "region": "Great Smoky Mountains", "country": "US", "state_province": "Tennessee", "popularity_rank": 670},
    {"name": "Volcan Baru", "aliases": ["Barú", "Mount Baru"], "latitude": 8.8083, "longitude": -82.5417, "elevation_m": 3475, "region": "Central America", "country": "Panama", "state_province": "Chiriqui", "popularity_rank": 673},
    {"name": "Cerro Chirripo", "aliases": ["Chirripo", "Chirripó"], "latitude": 9.4883, "longitude": -83.4883, "elevation_m": 3820, "region": "Talamanca Range", "country": "Costa Rica", "state_province": "San Jose", "popularity_rank": 675},
    {"name": "Roraima", "aliases": ["Mount Roraima", "Tepui Roraima"], "latitude": 5.1433, "longitude": -60.7625, "elevation_m": 2810, "region": "Guiana Highlands", "country": "Venezuela", "state_province": "Bolivar", "popularity_rank": 678},
    {"name": "Sajama", "aliases": ["Nevado Sajama"], "latitude": -18.1067, "longitude": -68.8833, "elevation_m": 6542, "region": "Andes", "country": "Bolivia", "state_province": "Oruro", "popularity_rank": 680},
    {"name": "Illimani", "aliases": ["Nevado Illimani"], "latitude": -16.6500, "longitude": -67.7833, "elevation_m": 6438, "region": "Andes", "country": "Bolivia", "state_province": "La Paz", "popularity_rank": 683},
    {"name": "Cayambe", "aliases": ["Volcán Cayambe"], "latitude": 0.0292, "longitude": -77.9867, "elevation_m": 5790, "region": "Andes", "country": "Ecuador", "state_province": "Pichincha", "popularity_rank": 685},
    {"name": "Antisana", "aliases": ["Volcán Antisana"], "latitude": -0.4833, "longitude": -78.1417, "elevation_m": 5704, "region": "Andes", "country": "Ecuador", "state_province": "Napo", "popularity_rank": 688},

    # --- More Canada ---
    {"name": "Wedge Mountain", "aliases": ["Wedge", "Wedgemount"], "latitude": 50.1500, "longitude": -122.8167, "elevation_m": 2892, "region": "Coast Mountains", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 690},
    {"name": "King's Peak", "aliases": ["Kings Peak Utah"], "latitude": 40.7764, "longitude": -110.3728, "elevation_m": 4123, "region": "Uinta Mountains", "country": "US", "state_province": "Utah", "popularity_rank": 693},
    {"name": "Panorama Ridge", "aliases": ["Panorama Ridge Garibaldi"], "latitude": 49.9417, "longitude": -123.0250, "elevation_m": 2050, "region": "Garibaldi Ranges", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 695},

    # --- Africa / Oceania ---
    {"name": "Bwahit", "aliases": ["Ras Bwahit"], "latitude": 13.2500, "longitude": 38.3000, "elevation_m": 4430, "region": "Simien Mountains", "country": "Ethiopia", "state_province": "Amhara", "popularity_rank": 698},
    {"name": "Imet Gogo", "aliases": ["Imetgogo"], "latitude": 13.2167, "longitude": 38.3000, "elevation_m": 3926, "region": "Simien Mountains", "country": "Ethiopia", "state_province": "Amhara", "popularity_rank": 700},
    {"name": "Bluff Knoll", "aliases": ["Bular Mial"], "latitude": -34.3756, "longitude": 118.2536, "elevation_m": 1095, "region": "Stirling Range", "country": "Australia", "state_province": "Western Australia", "popularity_rank": 703},
    {"name": "Mount Warning", "aliases": ["Wollumbin"], "latitude": -28.3972, "longitude": 153.2717, "elevation_m": 1156, "region": "Tweed Range", "country": "Australia", "state_province": "New South Wales", "popularity_rank": 705},
    {"name": "Federation Peak", "aliases": ["Fed Peak"], "latitude": -43.2583, "longitude": 146.5000, "elevation_m": 1224, "region": "Tasmania", "country": "Australia", "state_province": "Tasmania", "popularity_rank": 708},
    {"name": "Mount Meru Kenya", "aliases": ["Ithanguni"], "latitude": 0.0639, "longitude": 37.6500, "elevation_m": 5199, "region": "East Africa", "country": "Kenya", "state_province": "Central", "popularity_rank": 710},
    {"name": "Mulanje Massif", "aliases": ["Mount Mulanje", "Sapitwa"], "latitude": -15.9667, "longitude": 35.6333, "elevation_m": 3002, "region": "Southern Africa", "country": "Malawi", "state_province": "Southern", "popularity_rank": 713},
    {"name": "Mount Cameroon", "aliases": ["Mongo ma Ndemi", "Fako"], "latitude": 4.2033, "longitude": 9.1706, "elevation_m": 4095, "region": "West Africa", "country": "Cameroon", "state_province": "Southwest", "popularity_rank": 715},

    # --- More deep cuts ---
    {"name": "Cerro Tronador", "aliases": ["Tronador"], "latitude": -41.1572, "longitude": -71.8853, "elevation_m": 3491, "region": "Patagonia", "country": "Argentina", "state_province": "Rio Negro", "popularity_rank": 718},
    {"name": "Volcan Villarrica", "aliases": ["Villarrica", "Rucapillan"], "latitude": -39.4208, "longitude": -71.9394, "elevation_m": 2847, "region": "Andes", "country": "Chile", "state_province": "Araucania", "popularity_rank": 720},
    {"name": "Volcan Osorno", "aliases": ["Osorno"], "latitude": -41.1053, "longitude": -72.1531, "elevation_m": 2652, "region": "Andes", "country": "Chile", "state_province": "Los Lagos", "popularity_rank": 723},
    {"name": "Takao", "aliases": ["Mount Takao", "Takao-san"], "latitude": 35.6254, "longitude": 139.2436, "elevation_m": 599, "region": "Kanto", "country": "Japan", "state_province": "Tokyo", "popularity_rank": 725},
    {"name": "Putucusi", "aliases": ["Happy Mountain"], "latitude": -13.1639, "longitude": -72.5386, "elevation_m": 2560, "region": "Andes", "country": "Peru", "state_province": "Cusco", "popularity_rank": 728},
    {"name": "Choquequirao", "aliases": ["Choquekiraw"], "latitude": -13.3933, "longitude": -72.8583, "elevation_m": 3050, "region": "Andes", "country": "Peru", "state_province": "Cusco", "popularity_rank": 730},
    {"name": "Nevado Mismi", "aliases": ["Mismi"], "latitude": -15.5167, "longitude": -71.6833, "elevation_m": 5597, "region": "Andes", "country": "Peru", "state_province": "Arequipa", "popularity_rank": 733},
    {"name": "Cerro Acotango", "aliases": ["Acotango"], "latitude": -18.3833, "longitude": -69.0500, "elevation_m": 6052, "region": "Andes", "country": "Bolivia", "state_province": "Oruro", "popularity_rank": 735},
    {"name": "Licancabur", "aliases": ["Volcán Licancabur"], "latitude": -22.8333, "longitude": -67.8833, "elevation_m": 5920, "region": "Andes", "country": "Bolivia", "state_province": "Potosi", "popularity_rank": 738},
    {"name": "Tajumulco", "aliases": ["Volcán Tajumulco"], "latitude": 15.0433, "longitude": -91.9033, "elevation_m": 4220, "region": "Central America", "country": "Guatemala", "state_province": "San Marcos", "popularity_rank": 740},
    {"name": "Corno Grande", "aliases": ["Gran Sasso", "Corno Grande Peak"], "latitude": 42.4681, "longitude": 13.5656, "elevation_m": 2912, "region": "Apennines", "country": "Italy", "state_province": "Abruzzo", "popularity_rank": 743},
    {"name": "Monte Cinto", "aliases": ["Cinto"], "latitude": 42.3533, "longitude": 8.9500, "elevation_m": 2706, "region": "Corsica", "country": "France", "state_province": "Corsica", "popularity_rank": 745},
    {"name": "Olympus Stefani", "aliases": ["Stefani Peak"], "latitude": 40.0828, "longitude": 22.3569, "elevation_m": 2909, "region": "Thessaly", "country": "Greece", "state_province": "Pieria", "popularity_rank": 748},
    {"name": "Demavend", "aliases": ["Damavand", "Mount Damavand"], "latitude": 35.9514, "longitude": 52.1089, "elevation_m": 5610, "region": "Alborz", "country": "Iran", "state_province": "Mazandaran", "popularity_rank": 750},
    {"name": "Arjuna Peak", "aliases": ["Gunung Arjuno", "Arjuno"], "latitude": -7.7500, "longitude": 112.5833, "elevation_m": 3339, "region": "Java", "country": "Indonesia", "state_province": "East Java", "popularity_rank": 753},
    {"name": "Kerinci", "aliases": ["Gunung Kerinci", "Mount Kerinci"], "latitude": -1.6969, "longitude": 101.2642, "elevation_m": 3805, "region": "Sumatra", "country": "Indonesia", "state_province": "Jambi", "popularity_rank": 755},
    {"name": "Pidurutalagala", "aliases": ["Mount Pedro", "Pidurutalagala Peak"], "latitude": 7.0000, "longitude": 80.7667, "elevation_m": 2524, "region": "Central Highlands", "country": "Sri Lanka", "state_province": "Central", "popularity_rank": 758},
    {"name": "Fansipan Ridge", "aliases": ["Fansipan Summit Trail"], "latitude": 22.3039, "longitude": 103.7753, "elevation_m": 3143, "region": "Hoang Lien Son", "country": "Vietnam", "state_province": "Lao Cai", "popularity_rank": 760},
    {"name": "Mount Arayat", "aliases": ["Arayat"], "latitude": 15.2000, "longitude": 120.7417, "elevation_m": 1026, "region": "Luzon", "country": "Philippines", "state_province": "Pampanga", "popularity_rank": 763},
    {"name": "Wuyi Shan", "aliases": ["Mount Wuyi", "Wuyishan"], "latitude": 27.7167, "longitude": 117.9833, "elevation_m": 2158, "region": "Fujian", "country": "China", "state_province": "Fujian", "popularity_rank": 765},
    {"name": "Sahand", "aliases": ["Mount Sahand"], "latitude": 37.3500, "longitude": 46.4333, "elevation_m": 3707, "region": "Azerbaijan Region", "country": "Iran", "state_province": "East Azerbaijan", "popularity_rank": 768},
    {"name": "Olympus Washington", "aliases": ["Mount Olympus WA"], "latitude": 47.8013, "longitude": -123.7108, "elevation_m": 2432, "region": "Olympics", "country": "US", "state_province": "Washington", "popularity_rank": 770},
    {"name": "Mount Toubkal Winter", "aliases": ["Toubkal Hivernal"], "latitude": 31.0597, "longitude": -7.9153, "elevation_m": 4167, "region": "Atlas Mountains", "country": "Morocco", "state_province": "Marrakech-Safi", "popularity_rank": 773},
    {"name": "Pico Bolivar", "aliases": ["Bolívar Peak"], "latitude": 8.5333, "longitude": -71.0500, "elevation_m": 4978, "region": "Andes", "country": "Venezuela", "state_province": "Merida", "popularity_rank": 775},
    {"name": "Chimtarga", "aliases": ["Chimtarga Peak"], "latitude": 39.2333, "longitude": 68.2000, "elevation_m": 5489, "region": "Fann Mountains", "country": "Tajikistan", "state_province": "Sughd", "popularity_rank": 778},
    {"name": "Khan Tengri", "aliases": ["Kan-Too", "Lord of the Spirits"], "latitude": 42.2133, "longitude": 80.1733, "elevation_m": 7010, "region": "Tian Shan", "country": "Kazakhstan", "state_province": "Almaty", "popularity_rank": 780},
    {"name": "Pik Pobedy", "aliases": ["Jengish Chokusu", "Victory Peak"], "latitude": 42.0342, "longitude": 80.1278, "elevation_m": 7439, "region": "Tian Shan", "country": "Kyrgyzstan", "state_province": "Issyk-Kul", "popularity_rank": 783},
    {"name": "Kinnaur Kailash", "aliases": ["Kinnaur Kailash Trek"], "latitude": 31.6833, "longitude": 78.5167, "elevation_m": 6050, "region": "Himalayas", "country": "India", "state_province": "Himachal Pradesh", "popularity_rank": 785},
    {"name": "Pic Boby", "aliases": ["Boby Peak", "Maromokotro"], "latitude": -14.0000, "longitude": 49.0833, "elevation_m": 2876, "region": "Tsaratanana Massif", "country": "Madagascar", "state_province": "Diana", "popularity_rank": 788},
    {"name": "Carstensz Pyramid", "aliases": ["Puncak Jaya", "Jaya Peak"], "latitude": -4.0833, "longitude": 137.1583, "elevation_m": 4884, "region": "Papua", "country": "Indonesia", "state_province": "Papua", "popularity_rank": 790},
    {"name": "Vinson Massif", "aliases": ["Mount Vinson"], "latitude": -78.5254, "longitude": -85.6172, "elevation_m": 4892, "region": "Antarctica", "country": "Antarctica", "state_province": "Ellsworth Mountains", "popularity_rank": 793},
    {"name": "Mount Kailash", "aliases": ["Kailash", "Gang Rinpoche", "Kangrinboqe"], "latitude": 31.0672, "longitude": 81.3128, "elevation_m": 6638, "region": "Himalayas", "country": "China", "state_province": "Tibet", "popularity_rank": 795},
    {"name": "Kangchenjunga", "aliases": ["Kanchenjunga", "Kangchen Dzonga"], "latitude": 27.7025, "longitude": 88.1475, "elevation_m": 8586, "region": "Himalayas", "country": "Nepal", "state_province": "Taplejung", "popularity_rank": 798},

    # =========================================================================
    # ADDITIONAL EXPANSION — FILLING GAPS (various ranks)
    # =========================================================================

    # --- More US Peaks ---
    {"name": "Mount Leconte East", "aliases": ["Leconte Smokies"], "latitude": 35.6544, "longitude": -83.4357, "elevation_m": 2010, "region": "Great Smoky Mountains", "country": "US", "state_province": "Tennessee", "popularity_rank": 572},
    {"name": "North Sister", "aliases": ["North Sister Oregon"], "latitude": 44.1672, "longitude": -121.7694, "elevation_m": 3074, "region": "Cascades", "country": "US", "state_province": "Oregon", "popularity_rank": 575},
    {"name": "Haleakala", "aliases": ["Haleakalā", "East Maui Volcano"], "latitude": 20.7097, "longitude": -156.2533, "elevation_m": 3055, "region": "Hawaii", "country": "US", "state_province": "Hawaii", "popularity_rank": 577},
    {"name": "Teewinot", "aliases": ["Teewinot Mountain"], "latitude": 43.7503, "longitude": -110.7906, "elevation_m": 3754, "region": "Teton Range", "country": "US", "state_province": "Wyoming", "popularity_rank": 580},
    {"name": "Mount Nebo", "aliases": ["Nebo"], "latitude": 39.8219, "longitude": -111.7606, "elevation_m": 3636, "region": "Wasatch Range", "country": "US", "state_province": "Utah", "popularity_rank": 582},
    {"name": "Boundary Peak", "aliases": ["Boundary NV"], "latitude": 37.8461, "longitude": -118.3514, "elevation_m": 4005, "region": "White Mountains", "country": "US", "state_province": "Nevada", "popularity_rank": 585},
    {"name": "Mount Rogers", "aliases": ["Rogers"], "latitude": 36.6597, "longitude": -81.5447, "elevation_m": 1746, "region": "Blue Ridge", "country": "US", "state_province": "Virginia", "popularity_rank": 587},
    {"name": "Telescope Peak", "aliases": ["Telescope"], "latitude": 36.1697, "longitude": -117.0892, "elevation_m": 3368, "region": "Panamint Range", "country": "US", "state_province": "California", "popularity_rank": 590},
    {"name": "Mount Greylock", "aliases": ["Greylock"], "latitude": 42.6376, "longitude": -73.1662, "elevation_m": 1063, "region": "Berkshires", "country": "US", "state_province": "Massachusetts", "popularity_rank": 592},
    {"name": "Baxter Peak", "aliases": ["Katahdin Summit"], "latitude": 45.9044, "longitude": -68.9214, "elevation_m": 1606, "region": "Appalachians", "country": "US", "state_province": "Maine", "popularity_rank": 595},
    {"name": "Mount Snoqualmie", "aliases": ["Snoqualmie Mountain"], "latitude": 47.4253, "longitude": -121.4125, "elevation_m": 1856, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 597},
    {"name": "Enchanted Rock", "aliases": ["Enchanted Rock TX"], "latitude": 30.5069, "longitude": -98.8200, "elevation_m": 550, "region": "Texas Hill Country", "country": "US", "state_province": "Texas", "popularity_rank": 599},
    {"name": "Mount Sanitas", "aliases": ["Sanitas"], "latitude": 40.0228, "longitude": -105.2989, "elevation_m": 2064, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 570},
    {"name": "Stony Man", "aliases": ["Stony Man Peak"], "latitude": 38.5939, "longitude": -78.3733, "elevation_m": 1234, "region": "Blue Ridge", "country": "US", "state_province": "Virginia", "popularity_rank": 573},
    {"name": "Mount Cardigan", "aliases": ["Cardigan"], "latitude": 43.6497, "longitude": -71.9169, "elevation_m": 948, "region": "New England", "country": "US", "state_province": "New Hampshire", "popularity_rank": 576},
    {"name": "Slide Mountain", "aliases": ["Slide Mountain NY"], "latitude": 42.0056, "longitude": -74.3806, "elevation_m": 1274, "region": "Catskills", "country": "US", "state_province": "New York", "popularity_rank": 578},
    {"name": "Blackrock Summit", "aliases": ["Blackrock"], "latitude": 38.5422, "longitude": -78.7556, "elevation_m": 978, "region": "Blue Ridge", "country": "US", "state_province": "Virginia", "popularity_rank": 581},
    {"name": "South Bubble", "aliases": ["Bubble Rock", "South Bubble Acadia"], "latitude": 44.3292, "longitude": -68.2472, "elevation_m": 235, "region": "Acadia", "country": "US", "state_province": "Maine", "popularity_rank": 583},
    {"name": "Tumbledown Mountain", "aliases": ["Tumbledown"], "latitude": 44.7467, "longitude": -70.5344, "elevation_m": 985, "region": "New England", "country": "US", "state_province": "Maine", "popularity_rank": 586},
    {"name": "Table Rock", "aliases": ["Table Rock SC"], "latitude": 35.0575, "longitude": -82.5678, "elevation_m": 1084, "region": "Blue Ridge", "country": "US", "state_province": "South Carolina", "popularity_rank": 588},
    {"name": "Shuckstack", "aliases": ["Shuckstack Fire Tower"], "latitude": 35.4631, "longitude": -83.7761, "elevation_m": 1392, "region": "Great Smoky Mountains", "country": "US", "state_province": "North Carolina", "popularity_rank": 591},
    {"name": "Hawksbill Mountain", "aliases": ["Hawksbill"], "latitude": 38.5544, "longitude": -78.3800, "elevation_m": 1235, "region": "Blue Ridge", "country": "US", "state_province": "Virginia", "popularity_rank": 593},
    {"name": "South Kaibab", "aliases": ["Ooh Aah Point"], "latitude": 36.0544, "longitude": -112.0839, "elevation_m": 2134, "region": "Colorado Plateau", "country": "US", "state_province": "Arizona", "popularity_rank": 596},
    {"name": "Mount Sanford", "aliases": ["Sanford"], "latitude": 62.2136, "longitude": -144.1297, "elevation_m": 4949, "region": "Wrangell Mountains", "country": "US", "state_province": "Alaska", "popularity_rank": 598},

    # --- More Canada ---
    {"name": "Mount Columbia", "aliases": ["Columbia"], "latitude": 52.1472, "longitude": -117.4375, "elevation_m": 3747, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 547},
    {"name": "Cypress Mountain", "aliases": ["Cypress"], "latitude": 49.3961, "longitude": -123.2044, "elevation_m": 1217, "region": "North Shore Mountains", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 549},
    {"name": "Mont Jacques-Cartier", "aliases": ["Jacques-Cartier"], "latitude": 48.9869, "longitude": -65.9386, "elevation_m": 1268, "region": "Chic-Chocs", "country": "Canada", "state_province": "Quebec", "popularity_rank": 552},
    {"name": "Elk Mountain", "aliases": ["Elk"], "latitude": 49.2647, "longitude": -121.7919, "elevation_m": 1421, "region": "Chilliwack", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 554},
    {"name": "Mount Edith Cavell", "aliases": ["Edith Cavell", "Cavell"], "latitude": 52.6856, "longitude": -117.8175, "elevation_m": 3363, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 557},
    {"name": "Mount Frosty", "aliases": ["Frosty Mountain"], "latitude": 49.0583, "longitude": -120.7833, "elevation_m": 2408, "region": "Cascades", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 559},
    {"name": "Nihahi Ridge", "aliases": ["Nihahi"], "latitude": 50.9167, "longitude": -115.1667, "elevation_m": 2470, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 562},
    {"name": "Mount Cory", "aliases": ["Cory"], "latitude": 51.2000, "longitude": -115.6167, "elevation_m": 2802, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 564},
    {"name": "Tunnel Mountain", "aliases": ["Sleeping Buffalo"], "latitude": 51.1789, "longitude": -115.5536, "elevation_m": 1692, "region": "Canadian Rockies", "country": "Canada", "state_province": "Alberta", "popularity_rank": 567},

    # --- More Europe ---
    {"name": "Dent Blanche", "aliases": ["Dent Blanche Peak"], "latitude": 46.0361, "longitude": 7.6053, "elevation_m": 4357, "region": "Alps", "country": "Switzerland", "state_province": "Valais", "popularity_rank": 501},
    {"name": "Bernese Oberland High Route", "aliases": ["Finsteraarhorn"], "latitude": 46.5372, "longitude": 8.1261, "elevation_m": 4274, "region": "Alps", "country": "Switzerland", "state_province": "Bern", "popularity_rank": 504},
    {"name": "Pelmo", "aliases": ["Monte Pelmo"], "latitude": 46.4244, "longitude": 12.0853, "elevation_m": 3168, "region": "Dolomites", "country": "Italy", "state_province": "Veneto", "popularity_rank": 507},
    {"name": "Sassolungo", "aliases": ["Langkofel", "Sasso Lungo"], "latitude": 46.5250, "longitude": 11.7333, "elevation_m": 3181, "region": "Dolomites", "country": "Italy", "state_province": "South Tyrol", "popularity_rank": 509},
    {"name": "Vesuvius", "aliases": ["Vesuvio", "Mount Vesuvius"], "latitude": 40.8210, "longitude": 14.4260, "elevation_m": 1281, "region": "Campania", "country": "Italy", "state_province": "Campania", "popularity_rank": 512},
    {"name": "Stromboli", "aliases": ["Stromboli Volcano"], "latitude": 38.7892, "longitude": 15.2133, "elevation_m": 924, "region": "Aeolian Islands", "country": "Italy", "state_province": "Sicily", "popularity_rank": 514},
    {"name": "Catinaccio", "aliases": ["Rosengarten", "Catinaccio d'Antermoia"], "latitude": 46.4639, "longitude": 11.6239, "elevation_m": 2981, "region": "Dolomites", "country": "Italy", "state_province": "South Tyrol", "popularity_rank": 517},
    {"name": "Cadair Idris", "aliases": ["Cader Idris", "Penygadair"], "latitude": 52.6975, "longitude": -3.9042, "elevation_m": 893, "region": "Snowdonia", "country": "UK", "state_province": "Wales", "popularity_rank": 519},
    {"name": "Cairn Gorm", "aliases": ["Cairngorm"], "latitude": 57.1167, "longitude": -3.6417, "elevation_m": 1245, "region": "Cairngorms", "country": "UK", "state_province": "Scotland", "popularity_rank": 522},
    {"name": "Ben Lomond", "aliases": ["Lomond"], "latitude": 56.1906, "longitude": -4.6331, "elevation_m": 974, "region": "Trossachs", "country": "UK", "state_province": "Scotland", "popularity_rank": 524},
    {"name": "Buachaille Etive Mor", "aliases": ["Buachaille", "The Buachaille"], "latitude": 56.6500, "longitude": -4.9833, "elevation_m": 1022, "region": "Scottish Highlands", "country": "UK", "state_province": "Scotland", "popularity_rank": 527},
    {"name": "Mount Olympus Cyprus", "aliases": ["Chionistra"], "latitude": 34.9417, "longitude": 32.8667, "elevation_m": 1952, "region": "Troodos", "country": "Cyprus", "state_province": "Limassol", "popularity_rank": 529},
    {"name": "Stolby", "aliases": ["Krasnoyarsk Pillars"], "latitude": 55.9500, "longitude": 92.7500, "elevation_m": 832, "region": "Siberia", "country": "Russia", "state_province": "Krasnoyarsk", "popularity_rank": 532},
    {"name": "Teide", "aliases": ["Mount Teide", "Pico del Teide"], "latitude": 28.2725, "longitude": -16.6422, "elevation_m": 3718, "region": "Canary Islands", "country": "Spain", "state_province": "Tenerife", "popularity_rank": 534},
    {"name": "Piton de la Fournaise", "aliases": ["Fournaise", "Peak of the Furnace"], "latitude": -21.2306, "longitude": 55.7144, "elevation_m": 2632, "region": "Reunion Island", "country": "France", "state_province": "Reunion", "popularity_rank": 537},
    {"name": "Puig Major", "aliases": ["Puig Major Mallorca"], "latitude": 39.8092, "longitude": 2.7967, "elevation_m": 1445, "region": "Balearic Islands", "country": "Spain", "state_province": "Mallorca", "popularity_rank": 539},
    {"name": "Olympos Turkey", "aliases": ["Tahtali", "Tahtalı Dağı"], "latitude": 36.5333, "longitude": 30.4500, "elevation_m": 2366, "region": "Lycian Way", "country": "Turkey", "state_province": "Antalya", "popularity_rank": 542},
    {"name": "Kazbek South", "aliases": ["Stepantsminda View"], "latitude": 42.6861, "longitude": 44.5142, "elevation_m": 5054, "region": "Caucasus", "country": "Georgia", "state_province": "Mtskheta-Mtianeti", "popularity_rank": 544},
    {"name": "Svaneti Tower Region", "aliases": ["Ushguli Trek"], "latitude": 42.9167, "longitude": 43.0000, "elevation_m": 4700, "region": "Caucasus", "country": "Georgia", "state_province": "Svaneti", "popularity_rank": 546},
    {"name": "Durmitor", "aliases": ["Bobotov Kuk", "Durmitor NP"], "latitude": 43.1267, "longitude": 19.0292, "elevation_m": 2522, "region": "Dinaric Alps", "country": "Montenegro", "state_province": "Zabljak", "popularity_rank": 551},
    {"name": "Vihren", "aliases": ["Mount Vihren"], "latitude": 41.7664, "longitude": 23.3992, "elevation_m": 2914, "region": "Pirin Mountains", "country": "Bulgaria", "state_province": "Blagoevgrad", "popularity_rank": 556},
    {"name": "Rysy", "aliases": ["Rysy Peak"], "latitude": 49.1794, "longitude": 20.0883, "elevation_m": 2499, "region": "Tatra Mountains", "country": "Poland", "state_province": "Lesser Poland", "popularity_rank": 561},
    {"name": "Gerlachovsky Stit", "aliases": ["Gerlach", "Gerlachovský štít"], "latitude": 49.1644, "longitude": 20.1342, "elevation_m": 2655, "region": "Tatra Mountains", "country": "Slovakia", "state_province": "Presov", "popularity_rank": 566},
    {"name": "Olympus Litochoro Trail", "aliases": ["Litochoro Olympus"], "latitude": 40.0850, "longitude": 22.3575, "elevation_m": 2917, "region": "Thessaly", "country": "Greece", "state_province": "Pieria", "popularity_rank": 569},
    {"name": "Sarek Rapadalen", "aliases": ["Skierffe", "Sarek NP"], "latitude": 67.2833, "longitude": 17.7167, "elevation_m": 1420, "region": "Scandinavian Mountains", "country": "Sweden", "state_province": "Norrbotten", "popularity_rank": 574},
    {"name": "Kjerag", "aliases": ["Kjeragbolten"], "latitude": 59.0364, "longitude": 6.5808, "elevation_m": 1084, "region": "Rogaland", "country": "Norway", "state_province": "Rogaland", "popularity_rank": 579},
    {"name": "Preikestolen", "aliases": ["Pulpit Rock"], "latitude": 58.9861, "longitude": 6.1867, "elevation_m": 604, "region": "Rogaland", "country": "Norway", "state_province": "Rogaland", "popularity_rank": 584},
    {"name": "Trolltunga", "aliases": ["Troll's Tongue"], "latitude": 60.1241, "longitude": 6.7400, "elevation_m": 1100, "region": "Hardanger", "country": "Norway", "state_province": "Vestland", "popularity_rank": 589},
    {"name": "Stetind", "aliases": ["Norways National Mountain"], "latitude": 68.1500, "longitude": 16.6000, "elevation_m": 1392, "region": "Northern Norway", "country": "Norway", "state_province": "Nordland", "popularity_rank": 594},

    # --- More South America ---
    {"name": "Huayna Picchu", "aliases": ["Wayna Picchu", "Huayna Pikchu"], "latitude": -13.1567, "longitude": -72.5450, "elevation_m": 2693, "region": "Andes", "country": "Peru", "state_province": "Cusco", "popularity_rank": 502},
    {"name": "Pastoruri", "aliases": ["Nevado Pastoruri"], "latitude": -9.9333, "longitude": -77.2167, "elevation_m": 5240, "region": "Andes", "country": "Peru", "state_province": "Ancash", "popularity_rank": 506},
    {"name": "Yerupaja", "aliases": ["Nevado Yerupajá"], "latitude": -10.2667, "longitude": -76.9000, "elevation_m": 6635, "region": "Andes", "country": "Peru", "state_province": "Huanuco", "popularity_rank": 511},
    {"name": "Santa Cruz Trek", "aliases": ["Laguna 69 Trek"], "latitude": -8.9333, "longitude": -77.6167, "elevation_m": 4600, "region": "Andes", "country": "Peru", "state_province": "Ancash", "popularity_rank": 516},
    {"name": "Ojos del Salado", "aliases": ["Ojos", "Nevado Ojos del Salado"], "latitude": -27.1092, "longitude": -68.5414, "elevation_m": 6893, "region": "Andes", "country": "Chile", "state_province": "Atacama", "popularity_rank": 521},
    {"name": "Lanin", "aliases": ["Volcán Lanín"], "latitude": -39.6361, "longitude": -71.5025, "elevation_m": 3776, "region": "Andes", "country": "Argentina", "state_province": "Neuquen", "popularity_rank": 526},
    {"name": "Tungurahua", "aliases": ["Volcán Tungurahua", "Throat of Fire"], "latitude": -1.4681, "longitude": -78.4422, "elevation_m": 5023, "region": "Andes", "country": "Ecuador", "state_province": "Tungurahua", "popularity_rank": 531},
    {"name": "El Altar", "aliases": ["Volcán El Altar", "Capac Urcu"], "latitude": -1.6667, "longitude": -78.4000, "elevation_m": 5320, "region": "Andes", "country": "Ecuador", "state_province": "Chimborazo", "popularity_rank": 536},
    {"name": "Cocuy Ritacuba Blanco", "aliases": ["Ritacuba", "Ritacuba Blanco"], "latitude": 6.5000, "longitude": -72.3333, "elevation_m": 5410, "region": "Andes", "country": "Colombia", "state_province": "Boyaca", "popularity_rank": 541},
    {"name": "Cerro Catedral", "aliases": ["Catedral Bariloche"], "latitude": -41.1667, "longitude": -71.4500, "elevation_m": 2388, "region": "Patagonia", "country": "Argentina", "state_province": "Rio Negro", "popularity_rank": 600},
    {"name": "Volcan Calbuco", "aliases": ["Calbuco"], "latitude": -41.3261, "longitude": -72.6142, "elevation_m": 2015, "region": "Andes", "country": "Chile", "state_province": "Los Lagos", "popularity_rank": 571},

    # --- More Africa ---
    {"name": "Mount Elgon", "aliases": ["Elgon"], "latitude": 1.1333, "longitude": 34.5333, "elevation_m": 4321, "region": "East Africa", "country": "Uganda", "state_province": "Eastern", "popularity_rank": 601},
    {"name": "Jebel Sahro", "aliases": ["Saghro", "Djebel Saghro"], "latitude": 31.2500, "longitude": -5.8333, "elevation_m": 2712, "region": "Atlas Mountains", "country": "Morocco", "state_province": "Draa-Tafilalet", "popularity_rank": 604},
    {"name": "Mount Meru West", "aliases": ["Little Meru"], "latitude": -3.2333, "longitude": 36.7333, "elevation_m": 3801, "region": "East Africa", "country": "Tanzania", "state_province": "Arusha", "popularity_rank": 607},
    {"name": "Ol Doinyo Lengai", "aliases": ["Mountain of God"], "latitude": -2.7642, "longitude": 35.9142, "elevation_m": 2962, "region": "East Africa", "country": "Tanzania", "state_province": "Arusha", "popularity_rank": 609},
    {"name": "Table Mountain Lion's Head", "aliases": ["Lion's Head", "Lions Head"], "latitude": -33.9353, "longitude": 18.3889, "elevation_m": 669, "region": "Western Cape", "country": "South Africa", "state_province": "Western Cape", "popularity_rank": 612},
    {"name": "Drakensberg Grand Traverse", "aliases": ["Drakensberg", "uKhahlamba"], "latitude": -29.3667, "longitude": 29.4333, "elevation_m": 3482, "region": "Drakensberg", "country": "South Africa", "state_province": "KwaZulu-Natal", "popularity_rank": 614},
    {"name": "Thabana Ntlenyana", "aliases": ["Thabana"], "latitude": -29.4667, "longitude": 29.2667, "elevation_m": 3482, "region": "Drakensberg", "country": "Lesotho", "state_province": "Mokhotlong", "popularity_rank": 617},

    # --- More Oceania ---
    {"name": "Mount Ruapehu", "aliases": ["Ruapehu"], "latitude": -39.2817, "longitude": 175.5681, "elevation_m": 2797, "region": "North Island", "country": "New Zealand", "state_province": "Manawatu-Whanganui", "popularity_rank": 619},
    {"name": "Mount Aspiring", "aliases": ["Tititea"], "latitude": -44.3836, "longitude": 168.7294, "elevation_m": 3033, "region": "Southern Alps", "country": "New Zealand", "state_province": "Otago", "popularity_rank": 622},
    {"name": "Routeburn Track", "aliases": ["Routeburn"], "latitude": -44.7833, "longitude": 168.3000, "elevation_m": 1277, "region": "Southern Alps", "country": "New Zealand", "state_province": "Otago", "popularity_rank": 624},
    {"name": "Mount Tasman", "aliases": ["Horo Koau"], "latitude": -43.5167, "longitude": 170.1333, "elevation_m": 3497, "region": "Southern Alps", "country": "New Zealand", "state_province": "West Coast", "popularity_rank": 627},
    {"name": "Frenchmans Cap", "aliases": ["Frenchman's Cap"], "latitude": -42.3500, "longitude": 145.8333, "elevation_m": 1446, "region": "Tasmania", "country": "Australia", "state_province": "Tasmania", "popularity_rank": 629},
    {"name": "Mount Bogong", "aliases": ["Bogong"], "latitude": -36.7383, "longitude": 147.2992, "elevation_m": 1986, "region": "Victorian Alps", "country": "Australia", "state_province": "Victoria", "popularity_rank": 632},
    {"name": "Mount Ossa", "aliases": ["Ossa Tasmania"], "latitude": -41.8667, "longitude": 146.0333, "elevation_m": 1617, "region": "Tasmania", "country": "Australia", "state_province": "Tasmania", "popularity_rank": 634},

    # --- More Asia ---
    {"name": "Changbai Shan", "aliases": ["Paektu", "Changbaishan", "Mount Changbai"], "latitude": 42.0042, "longitude": 128.0556, "elevation_m": 2744, "region": "Manchuria", "country": "China", "state_province": "Jilin", "popularity_rank": 636},
    {"name": "Zhangjiajie", "aliases": ["Tianmen Mountain", "Zhangjiajie Pillars"], "latitude": 29.0508, "longitude": 110.4792, "elevation_m": 1519, "region": "Hunan", "country": "China", "state_province": "Hunan", "popularity_rank": 639},
    {"name": "Laoshan", "aliases": ["Mount Lao", "Lao Mountain"], "latitude": 36.1667, "longitude": 120.6167, "elevation_m": 1133, "region": "Shandong", "country": "China", "state_province": "Shandong", "popularity_rank": 641},
    {"name": "Putuo Shan", "aliases": ["Mount Putuo", "Putuoshan"], "latitude": 30.0000, "longitude": 122.3833, "elevation_m": 284, "region": "Zhejiang", "country": "China", "state_province": "Zhejiang", "popularity_rank": 644},
    {"name": "Kumgang-san", "aliases": ["Diamond Mountains", "Mount Kumgang"], "latitude": 38.6583, "longitude": 128.1167, "elevation_m": 1638, "region": "Diamond Mountains", "country": "North Korea", "state_province": "Kangwon", "popularity_rank": 646},
    {"name": "Batur Agung Trek", "aliases": ["Batur Sunrise"], "latitude": -8.2375, "longitude": 115.3750, "elevation_m": 1717, "region": "Bali", "country": "Indonesia", "state_province": "Bali", "popularity_rank": 649},
    {"name": "Osore-zan", "aliases": ["Mount Osore", "Mount Fear"], "latitude": 41.3333, "longitude": 141.1000, "elevation_m": 879, "region": "Tohoku", "country": "Japan", "state_province": "Aomori", "popularity_rank": 651},
    {"name": "Kaimon-dake", "aliases": ["Mount Kaimon", "Satsuma Fuji"], "latitude": 31.2000, "longitude": 130.5667, "elevation_m": 924, "region": "Kyushu", "country": "Japan", "state_province": "Kagoshima", "popularity_rank": 654},
    {"name": "Nantai-san", "aliases": ["Mount Nantai"], "latitude": 36.7667, "longitude": 139.4833, "elevation_m": 2486, "region": "Tochigi", "country": "Japan", "state_province": "Tochigi", "popularity_rank": 656},
    {"name": "Annapurna I", "aliases": ["Annapurna", "Annapurna Main"], "latitude": 28.5961, "longitude": 83.8203, "elevation_m": 8091, "region": "Himalayas", "country": "Nepal", "state_province": "Gandaki", "popularity_rank": 659},
    {"name": "Thorong La", "aliases": ["Thorung La", "Thorong Pass"], "latitude": 28.7833, "longitude": 83.9333, "elevation_m": 5416, "region": "Himalayas", "country": "Nepal", "state_province": "Gandaki", "popularity_rank": 661},
    {"name": "Machapuchare", "aliases": ["Machhapuchhre", "Fishtail Mountain"], "latitude": 28.6317, "longitude": 83.9483, "elevation_m": 6993, "region": "Himalayas", "country": "Nepal", "state_province": "Gandaki", "popularity_rank": 664},
    {"name": "Hampta Pass", "aliases": ["Hampta Trek"], "latitude": 32.3167, "longitude": 77.1500, "elevation_m": 4270, "region": "Himalayas", "country": "India", "state_province": "Himachal Pradesh", "popularity_rank": 666},
    {"name": "Brahmatal", "aliases": ["Brahmatal Trek"], "latitude": 30.1833, "longitude": 79.7000, "elevation_m": 3712, "region": "Himalayas", "country": "India", "state_province": "Uttarakhand", "popularity_rank": 669},
    {"name": "Deoria Tal", "aliases": ["Deoria Tal Trek", "Chandrashila Base"], "latitude": 30.4167, "longitude": 79.2833, "elevation_m": 2438, "region": "Himalayas", "country": "India", "state_province": "Uttarakhand", "popularity_rank": 671},
    {"name": "Valley of Flowers", "aliases": ["Nanda Devi Biosphere"], "latitude": 30.7167, "longitude": 79.6333, "elevation_m": 3600, "region": "Himalayas", "country": "India", "state_province": "Uttarakhand", "popularity_rank": 674},
    {"name": "Kawah Ijen", "aliases": ["Ijen Crater", "Blue Fire"], "latitude": -8.0583, "longitude": 114.2417, "elevation_m": 2799, "region": "Java", "country": "Indonesia", "state_province": "East Java", "popularity_rank": 676},
    {"name": "Mount Merbabu", "aliases": ["Gunung Merbabu", "Merbabu"], "latitude": -7.4500, "longitude": 110.4333, "elevation_m": 3145, "region": "Java", "country": "Indonesia", "state_province": "Central Java", "popularity_rank": 679},

    # --- Central Asia / Middle East ---
    {"name": "Mount Ararat Little", "aliases": ["Little Ararat", "Kucuk Agri"], "latitude": 39.6333, "longitude": 44.4500, "elevation_m": 3896, "region": "Eastern Turkey", "country": "Turkey", "state_province": "Agri", "popularity_rank": 681},
    {"name": "Alam Kuh", "aliases": ["Alam-Kuh"], "latitude": 36.3972, "longitude": 50.9750, "elevation_m": 4850, "region": "Alborz", "country": "Iran", "state_province": "Mazandaran", "popularity_rank": 684},
    {"name": "Sabalan", "aliases": ["Mount Sabalan", "Savalan"], "latitude": 38.2500, "longitude": 47.8500, "elevation_m": 4811, "region": "Azerbaijan Region", "country": "Iran", "state_province": "Ardabil", "popularity_rank": 686},
    {"name": "Peak Lenin", "aliases": ["Ibn Sina Peak", "Koh-i-Lainin"], "latitude": 39.9450, "longitude": 72.8400, "elevation_m": 7134, "region": "Pamir", "country": "Kyrgyzstan", "state_province": "Osh", "popularity_rank": 689},
    {"name": "Ismoil Somoni Peak", "aliases": ["Communism Peak", "Pik Kommunizma"], "latitude": 38.9417, "longitude": 72.0139, "elevation_m": 7495, "region": "Pamir", "country": "Tajikistan", "state_province": "Gorno-Badakhshan", "popularity_rank": 692},
    {"name": "Belukha", "aliases": ["Mount Belukha", "Belucha"], "latitude": 49.8075, "longitude": 86.5908, "elevation_m": 4506, "region": "Altai Mountains", "country": "Russia", "state_province": "Altai Republic", "popularity_rank": 694},
    {"name": "Karakol Peak", "aliases": ["Jeti-Oguz"], "latitude": 42.5167, "longitude": 78.5167, "elevation_m": 5216, "region": "Tian Shan", "country": "Kyrgyzstan", "state_province": "Issyk-Kul", "popularity_rank": 697},

    # --- More misc worldwide ---
    {"name": "Piton des Neiges Reunion", "aliases": ["Piton Summit"], "latitude": -21.0992, "longitude": 55.4833, "elevation_m": 3069, "region": "Reunion Island", "country": "France", "state_province": "Reunion", "popularity_rank": 701},
    {"name": "Mount Kinabalu Via Ferrata", "aliases": ["Kinabalu Low's Peak"], "latitude": 6.0753, "longitude": 116.5586, "elevation_m": 4095, "region": "Borneo", "country": "Malaysia", "state_province": "Sabah", "popularity_rank": 704},
    {"name": "Fitz Roy Base Camp", "aliases": ["Laguna de los Tres"], "latitude": -49.2767, "longitude": -73.0400, "elevation_m": 3405, "region": "Patagonia", "country": "Argentina", "state_province": "Santa Cruz", "popularity_rank": 707},
    {"name": "Cotopaxi Refugio", "aliases": ["Jose Ribas Refuge"], "latitude": -0.6841, "longitude": -78.4376, "elevation_m": 4800, "region": "Andes", "country": "Ecuador", "state_province": "Cotopaxi", "popularity_rank": 709},
    {"name": "Kota Kinabalu Trail", "aliases": ["KK Summit Trail"], "latitude": 6.0753, "longitude": 116.5586, "elevation_m": 4095, "region": "Borneo", "country": "Malaysia", "state_province": "Sabah", "popularity_rank": 712},
    {"name": "Mount Olympus Trail BC", "aliases": ["Olympus BC"], "latitude": 49.3833, "longitude": -121.7500, "elevation_m": 2068, "region": "Cascades", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 714},
    {"name": "Snowdonia Traverse", "aliases": ["Welsh 3000s"], "latitude": 53.0685, "longitude": -4.0763, "elevation_m": 1085, "region": "Snowdonia", "country": "UK", "state_province": "Wales", "popularity_rank": 717},
    {"name": "Mount Toubkal Circuit", "aliases": ["Toubkal Loop"], "latitude": 31.0597, "longitude": -7.9153, "elevation_m": 4167, "region": "Atlas Mountains", "country": "Morocco", "state_province": "Marrakech-Safi", "popularity_rank": 719},
    {"name": "Acatenango", "aliases": ["Volcán Acatenango"], "latitude": 14.5006, "longitude": -90.8761, "elevation_m": 3976, "region": "Central America", "country": "Guatemala", "state_province": "Chimaltenango", "popularity_rank": 722},
    {"name": "Mount Athos", "aliases": ["Agio Oros", "Holy Mountain"], "latitude": 40.1564, "longitude": 24.3258, "elevation_m": 2033, "region": "Chalkidiki", "country": "Greece", "state_province": "Mount Athos", "popularity_rank": 724},
    {"name": "Psiloritis", "aliases": ["Mount Ida Crete", "Timios Stavros"], "latitude": 35.2278, "longitude": 24.7667, "elevation_m": 2456, "region": "Crete", "country": "Greece", "state_province": "Rethymno", "popularity_rank": 727},
    {"name": "Mount Elgon Kenya Side", "aliases": ["Elgon Kenya"], "latitude": 1.1333, "longitude": 34.5333, "elevation_m": 4321, "region": "East Africa", "country": "Kenya", "state_province": "Trans-Nzoia", "popularity_rank": 729},
    {"name": "Semien Traverse", "aliases": ["Simien Mountains Trek"], "latitude": 13.2500, "longitude": 38.3500, "elevation_m": 4550, "region": "Simien Mountains", "country": "Ethiopia", "state_province": "Amhara", "popularity_rank": 732},
    {"name": "Cirque of the Towers", "aliases": ["Pingora", "Wind River High Route"], "latitude": 42.7167, "longitude": -109.1833, "elevation_m": 3462, "region": "Wind River Range", "country": "US", "state_province": "Wyoming", "popularity_rank": 734},
    {"name": "Mount Assiniboine Lodge", "aliases": ["Assiniboine Provincial Park"], "latitude": 50.8714, "longitude": -115.6508, "elevation_m": 3618, "region": "Canadian Rockies", "country": "Canada", "state_province": "British Columbia", "popularity_rank": 737},
    {"name": "Torres Lookout", "aliases": ["Base Torres", "Mirador Torres"], "latitude": -50.9667, "longitude": -72.9833, "elevation_m": 850, "region": "Patagonia", "country": "Chile", "state_province": "Magallanes", "popularity_rank": 739},
    {"name": "Mount Cook Village Walks", "aliases": ["Hooker Valley"], "latitude": -43.7333, "longitude": 170.1000, "elevation_m": 762, "region": "Southern Alps", "country": "New Zealand", "state_province": "Canterbury", "popularity_rank": 742},
    {"name": "Nanga Parbat", "aliases": ["Killer Mountain", "Diamir"], "latitude": 35.2375, "longitude": 74.5892, "elevation_m": 8126, "region": "Himalayas", "country": "Pakistan", "state_province": "Gilgit-Baltistan", "popularity_rank": 744},
    {"name": "Broad Peak", "aliases": ["Faichan Kangri"], "latitude": 35.8119, "longitude": 76.5653, "elevation_m": 8051, "region": "Karakoram", "country": "Pakistan", "state_province": "Gilgit-Baltistan", "popularity_rank": 747},
    {"name": "Gasherbrum II", "aliases": ["G2", "Gasherbrum 2"], "latitude": 35.7581, "longitude": 76.6531, "elevation_m": 8035, "region": "Karakoram", "country": "Pakistan", "state_province": "Gilgit-Baltistan", "popularity_rank": 749},
    {"name": "Rakaposhi", "aliases": ["Dumani"], "latitude": 36.1467, "longitude": 74.4908, "elevation_m": 7788, "region": "Karakoram", "country": "Pakistan", "state_province": "Gilgit-Baltistan", "popularity_rank": 752},
    {"name": "Trango Towers", "aliases": ["Great Trango Tower"], "latitude": 35.7500, "longitude": 76.2167, "elevation_m": 6286, "region": "Karakoram", "country": "Pakistan", "state_province": "Gilgit-Baltistan", "popularity_rank": 754},
    {"name": "Concordia K2 BC", "aliases": ["Concordia"], "latitude": 35.7500, "longitude": 76.5167, "elevation_m": 4600, "region": "Karakoram", "country": "Pakistan", "state_province": "Gilgit-Baltistan", "popularity_rank": 757},

    # =========================================================================
    # THIRD EXPANSION BATCH — REACHING 650+
    # =========================================================================

    # --- More US (filling rank gaps) ---
    {"name": "Mount Greylock Summit", "aliases": ["Greylock Summit"], "latitude": 42.6376, "longitude": -73.1662, "elevation_m": 1063, "region": "Berkshires", "country": "US", "state_province": "Massachusetts", "popularity_rank": 163},
    {"name": "Cascade Canyon", "aliases": ["Cascade Canyon Tetons"], "latitude": 43.7333, "longitude": -110.8167, "elevation_m": 2926, "region": "Teton Range", "country": "US", "state_province": "Wyoming", "popularity_rank": 164},
    {"name": "South Bubble Acadia Peak", "aliases": ["Bubble Peak"], "latitude": 44.3300, "longitude": -68.2500, "elevation_m": 235, "region": "Acadia", "country": "US", "state_province": "Maine", "popularity_rank": 166},
    {"name": "Mount Democrat", "aliases": ["Democrat"], "latitude": 39.3394, "longitude": -106.1397, "elevation_m": 4312, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 168},
    {"name": "Mount Lincoln CO", "aliases": ["Lincoln"], "latitude": 39.3514, "longitude": -106.1114, "elevation_m": 4354, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 171},
    {"name": "Mount Sherman", "aliases": ["Sherman"], "latitude": 39.2253, "longitude": -106.1694, "elevation_m": 4278, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 173},
    {"name": "Redcloud Peak", "aliases": ["Redcloud"], "latitude": 37.9408, "longitude": -107.4214, "elevation_m": 4278, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 176},
    {"name": "Sunshine Peak", "aliases": ["Sunshine"], "latitude": 37.9225, "longitude": -107.4253, "elevation_m": 4275, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 178},
    {"name": "Mount Sneffels Blue Lakes", "aliases": ["Blue Lakes Trail"], "latitude": 37.9917, "longitude": -107.7750, "elevation_m": 4312, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 181},
    {"name": "La Plata Peak", "aliases": ["La Plata"], "latitude": 39.0294, "longitude": -106.4728, "elevation_m": 4372, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 183},
    {"name": "Mount Antero", "aliases": ["Antero"], "latitude": 38.6742, "longitude": -106.2461, "elevation_m": 4349, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 186},
    {"name": "Tabeguache Peak", "aliases": ["Tabeguache"], "latitude": 38.6258, "longitude": -106.2508, "elevation_m": 4340, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 188},
    {"name": "Mount Princeton", "aliases": ["Princeton"], "latitude": 38.7492, "longitude": -106.2375, "elevation_m": 4327, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 191},
    {"name": "Mount Yale", "aliases": ["Yale"], "latitude": 38.8442, "longitude": -106.3139, "elevation_m": 4327, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 193},
    {"name": "Mount Columbia CO", "aliases": ["Columbia CO"], "latitude": 38.9039, "longitude": -106.2972, "elevation_m": 4348, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 196},
    {"name": "Huron Peak", "aliases": ["Huron"], "latitude": 38.9453, "longitude": -106.4375, "elevation_m": 4272, "region": "Rocky Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 199},
    {"name": "Uncompahgre Peak", "aliases": ["Uncompahgre"], "latitude": 38.0717, "longitude": -107.4622, "elevation_m": 4361, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 201},
    {"name": "Mount Sneffels Yankee Boy", "aliases": ["Yankee Boy Basin"], "latitude": 38.0039, "longitude": -107.7922, "elevation_m": 4312, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 203},
    {"name": "Wilson Peak", "aliases": ["Wilson"], "latitude": 37.8603, "longitude": -107.9847, "elevation_m": 4272, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 206},
    {"name": "El Diente Peak", "aliases": ["El Diente"], "latitude": 37.8389, "longitude": -108.0050, "elevation_m": 4265, "region": "San Juan Mountains", "country": "US", "state_province": "Colorado", "popularity_rank": 209},
    {"name": "Mount Wrightson South", "aliases": ["Madera Canyon"], "latitude": 31.7261, "longitude": -110.8717, "elevation_m": 2881, "region": "Santa Rita Mountains", "country": "US", "state_province": "Arizona", "popularity_rank": 211},
    {"name": "Mount Charleston", "aliases": ["Charleston Peak", "Mount Charleston NV"], "latitude": 36.2719, "longitude": -115.6944, "elevation_m": 3632, "region": "Spring Mountains", "country": "US", "state_province": "Nevada", "popularity_rank": 213},
    {"name": "Sacagawea Peak", "aliases": ["Sacagawea"], "latitude": 45.8983, "longitude": -110.9556, "elevation_m": 2940, "region": "Bridger Range", "country": "US", "state_province": "Montana", "popularity_rank": 216},
    {"name": "Granite Peak MT", "aliases": ["Granite Montana"], "latitude": 45.1633, "longitude": -109.8075, "elevation_m": 3904, "region": "Beartooth Range", "country": "US", "state_province": "Montana", "popularity_rank": 219},
    {"name": "Glacier National Park Highline", "aliases": ["Highline Trail", "Garden Wall"], "latitude": 48.6958, "longitude": -113.7417, "elevation_m": 2200, "region": "Rocky Mountains", "country": "US", "state_province": "Montana", "popularity_rank": 221},
    {"name": "Mount Shuksan", "aliases": ["Shuksan"], "latitude": 48.8294, "longitude": -121.5953, "elevation_m": 2783, "region": "North Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 223},
    {"name": "Sahale Arm", "aliases": ["Sahale Glacier Camp"], "latitude": 48.5050, "longitude": -121.1967, "elevation_m": 2490, "region": "North Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 226},
    {"name": "Enchantments", "aliases": ["Enchantment Lakes", "Aasgard Pass"], "latitude": 47.5167, "longitude": -120.8167, "elevation_m": 2350, "region": "Cascades", "country": "US", "state_province": "Washington", "popularity_rank": 229},
    {"name": "Mount Constance", "aliases": ["Constance"], "latitude": 47.7508, "longitude": -123.1339, "elevation_m": 2358, "region": "Olympics", "country": "US", "state_province": "Washington", "popularity_rank": 231},
    {"name": "Broken Top", "aliases": ["Broken Top Oregon"], "latitude": 44.0811, "longitude": -121.7050, "elevation_m": 2795, "region": "Cascades", "country": "US", "state_province": "Oregon", "popularity_rank": 234},

    # --- More worldwide filling ---
    {"name": "Tre Cime Circuit", "aliases": ["Tre Cime Hike"], "latitude": 46.6192, "longitude": 12.3033, "elevation_m": 2999, "region": "Dolomites", "country": "Italy", "state_province": "South Tyrol", "popularity_rank": 236},
    {"name": "Tour du Mont Blanc", "aliases": ["TMB", "Tour Mont Blanc"], "latitude": 45.8326, "longitude": 6.8652, "elevation_m": 2665, "region": "Alps", "country": "France", "state_province": "Haute-Savoie", "popularity_rank": 239},
    {"name": "Haute Route", "aliases": ["Chamonix Zermatt"], "latitude": 46.0200, "longitude": 7.7500, "elevation_m": 3800, "region": "Alps", "country": "Switzerland", "state_province": "Valais", "popularity_rank": 241},
    {"name": "Walker's Haute Route", "aliases": ["GR5"], "latitude": 46.0200, "longitude": 7.7500, "elevation_m": 2900, "region": "Alps", "country": "Switzerland", "state_province": "Valais", "popularity_rank": 243},
    {"name": "Mera La", "aliases": ["Mera La Pass"], "latitude": 27.7283, "longitude": 86.8567, "elevation_m": 5415, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 246},
    {"name": "Everest Base Camp", "aliases": ["EBC", "Everest BC"], "latitude": 28.0025, "longitude": 86.8528, "elevation_m": 5364, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 248},
    {"name": "Three Passes Trek", "aliases": ["Renjo La", "Cho La"], "latitude": 27.9167, "longitude": 86.6333, "elevation_m": 5420, "region": "Himalayas", "country": "Nepal", "state_province": "Solukhumbu", "popularity_rank": 251},
    {"name": "ABC Trek", "aliases": ["Annapurna Base Camp Trek"], "latitude": 28.5308, "longitude": 83.8781, "elevation_m": 4130, "region": "Himalayas", "country": "Nepal", "state_province": "Gandaki", "popularity_rank": 253},
    {"name": "Langtang Valley", "aliases": ["Langtang Trek", "Kyanjin Gompa"], "latitude": 28.2125, "longitude": 85.5611, "elevation_m": 3800, "region": "Himalayas", "country": "Nepal", "state_province": "Bagmati", "popularity_rank": 256},
    {"name": "Sandakphu Trek", "aliases": ["Sandakphu Phalut"], "latitude": 27.1000, "longitude": 88.0000, "elevation_m": 3636, "region": "Himalayas", "country": "India", "state_province": "West Bengal", "popularity_rank": 258},
    {"name": "Pin Parvati Pass", "aliases": ["Pin Parvati"], "latitude": 31.9333, "longitude": 77.5500, "elevation_m": 5319, "region": "Himalayas", "country": "India", "state_province": "Himachal Pradesh", "popularity_rank": 261},
    {"name": "Rupin Pass", "aliases": ["Rupin Pass Trek"], "latitude": 31.1833, "longitude": 78.1500, "elevation_m": 4650, "region": "Himalayas", "country": "India", "state_province": "Uttarakhand", "popularity_rank": 263},
    {"name": "Kangchenjunga Base Camp", "aliases": ["KBC", "Kangchenjunga Trek"], "latitude": 27.7167, "longitude": 88.1000, "elevation_m": 5143, "region": "Himalayas", "country": "Nepal", "state_province": "Taplejung", "popularity_rank": 266},
    {"name": "Goechala", "aliases": ["Goecha La", "Goechala Trek"], "latitude": 27.6167, "longitude": 88.3000, "elevation_m": 4940, "region": "Himalayas", "country": "India", "state_province": "Sikkim", "popularity_rank": 268},
    {"name": "Chadar Trek", "aliases": ["Frozen River Trek", "Zanskar River"], "latitude": 33.4833, "longitude": 76.9833, "elevation_m": 3390, "region": "Himalayas", "country": "India", "state_province": "Ladakh", "popularity_rank": 271},
    {"name": "Markha Valley", "aliases": ["Markha Valley Trek"], "latitude": 33.8000, "longitude": 77.5500, "elevation_m": 5150, "region": "Himalayas", "country": "India", "state_province": "Ladakh", "popularity_rank": 273},

    # --- More Japan ---
    {"name": "Shirane-san", "aliases": ["Mount Shirane", "Kusatsu-Shirane"], "latitude": 36.6167, "longitude": 138.5333, "elevation_m": 2171, "region": "Gunma", "country": "Japan", "state_province": "Gunma", "popularity_rank": 276},
    {"name": "Daisen", "aliases": ["Mount Daisen", "Daisen-san"], "latitude": 35.3717, "longitude": 133.5450, "elevation_m": 1729, "region": "San'in", "country": "Japan", "state_province": "Tottori", "popularity_rank": 278},
    {"name": "Tanigawa-dake", "aliases": ["Mount Tanigawa", "Tanigawa"], "latitude": 36.8406, "longitude": 138.9328, "elevation_m": 1977, "region": "Gunma", "country": "Japan", "state_province": "Gunma", "popularity_rank": 281},
    {"name": "Norikura-dake", "aliases": ["Mount Norikura"], "latitude": 36.1064, "longitude": 137.5544, "elevation_m": 3026, "region": "Japanese Alps", "country": "Japan", "state_province": "Nagano", "popularity_rank": 283},

    # --- More South Korea ---
    {"name": "Dobongsan", "aliases": ["Dobong Mountain"], "latitude": 37.6975, "longitude": 127.0142, "elevation_m": 740, "region": "Seoul Metropolitan", "country": "South Korea", "state_province": "Seoul", "popularity_rank": 286},
    {"name": "Chiaksan", "aliases": ["Chiak Mountain", "Birobong"], "latitude": 37.3517, "longitude": 128.0536, "elevation_m": 1288, "region": "Taebaek Mountains", "country": "South Korea", "state_province": "Gangwon", "popularity_rank": 288},
    {"name": "Songnisan", "aliases": ["Songni Mountain", "Cheonhwangbong"], "latitude": 36.5383, "longitude": 127.8539, "elevation_m": 1058, "region": "Sobaek Mountains", "country": "South Korea", "state_province": "North Chungcheong", "popularity_rank": 291},
    {"name": "Gayasan", "aliases": ["Gaya Mountain", "Sangwangbong"], "latitude": 35.8000, "longitude": 128.1167, "elevation_m": 1430, "region": "Sobaek Mountains", "country": "South Korea", "state_province": "South Gyeongsang", "popularity_rank": 293},

    # --- More Southeast Asia ---
    {"name": "Mount Hamiguitan", "aliases": ["Hamiguitan", "Hamiguitan Range"], "latitude": 6.7000, "longitude": 126.1667, "elevation_m": 1637, "region": "Mindanao", "country": "Philippines", "state_province": "Davao Oriental", "popularity_rank": 296},
    {"name": "Mount Dulang-Dulang", "aliases": ["Dulang-Dulang"], "latitude": 8.1167, "longitude": 124.9333, "elevation_m": 2938, "region": "Mindanao", "country": "Philippines", "state_province": "Bukidnon", "popularity_rank": 298},
    {"name": "Mount Fansipan Cable", "aliases": ["Fansipan Legend"], "latitude": 22.3033, "longitude": 103.7750, "elevation_m": 3143, "region": "Hoang Lien Son", "country": "Vietnam", "state_province": "Lao Cai", "popularity_rank": 301},
    {"name": "Bach Moc Luong Tu", "aliases": ["Ky Quan San"], "latitude": 22.4833, "longitude": 104.0667, "elevation_m": 3046, "region": "Hoang Lien Son", "country": "Vietnam", "state_province": "Lao Cai", "popularity_rank": 303},
    {"name": "Ta Xua", "aliases": ["Ta Xua Peak", "Dinosaur Backbone"], "latitude": 21.4167, "longitude": 104.1500, "elevation_m": 2865, "region": "Northern Vietnam", "country": "Vietnam", "state_province": "Son La", "popularity_rank": 306},
    {"name": "Doi Pha Hom Pok", "aliases": ["Pha Hom Pok"], "latitude": 20.0833, "longitude": 99.1500, "elevation_m": 2285, "region": "Thai Highlands", "country": "Thailand", "state_province": "Chiang Mai", "popularity_rank": 309},
    {"name": "Mount Rinjani Sembalun", "aliases": ["Sembalun Route"], "latitude": -8.4117, "longitude": 116.4575, "elevation_m": 3726, "region": "Lombok", "country": "Indonesia", "state_province": "West Nusa Tenggara", "popularity_rank": 311},
    {"name": "Leuser", "aliases": ["Gunung Leuser", "Mount Leuser"], "latitude": 3.7500, "longitude": 97.3333, "elevation_m": 3466, "region": "Sumatra", "country": "Indonesia", "state_province": "Aceh", "popularity_rank": 313},
    {"name": "Prau", "aliases": ["Gunung Prau", "Mount Prau"], "latitude": -7.1833, "longitude": 109.9167, "elevation_m": 2565, "region": "Java", "country": "Indonesia", "state_province": "Central Java", "popularity_rank": 316},
    {"name": "Mount Lawu", "aliases": ["Gunung Lawu", "Lawu"], "latitude": -7.6250, "longitude": 111.1917, "elevation_m": 3265, "region": "Java", "country": "Indonesia", "state_province": "Central Java", "popularity_rank": 318},

    # --- More China ---
    {"name": "Laoshan", "aliases": ["Lao Shan", "Lao Mountain"], "latitude": 36.1667, "longitude": 120.6167, "elevation_m": 1133, "region": "Shandong", "country": "China", "state_province": "Shandong", "popularity_rank": 321},
    {"name": "Sanqing Shan", "aliases": ["Mount Sanqing", "Sanqingshan"], "latitude": 28.9167, "longitude": 118.0667, "elevation_m": 1820, "region": "Jiangxi", "country": "China", "state_province": "Jiangxi", "popularity_rank": 323},
    {"name": "Yandang Shan", "aliases": ["Yandang Mountain"], "latitude": 28.3833, "longitude": 121.1000, "elevation_m": 1150, "region": "Zhejiang", "country": "China", "state_province": "Zhejiang", "popularity_rank": 326},
    {"name": "Fanjing Shan", "aliases": ["Mount Fanjing", "Fanjingshan"], "latitude": 27.9167, "longitude": 108.6833, "elevation_m": 2572, "region": "Guizhou", "country": "China", "state_province": "Guizhou", "popularity_rank": 328},
    {"name": "Baiyun Shan", "aliases": ["White Cloud Mountain", "Baiyunshan"], "latitude": 23.1667, "longitude": 113.3000, "elevation_m": 382, "region": "Guangdong", "country": "China", "state_province": "Guangdong", "popularity_rank": 331},
    {"name": "Wugong Shan", "aliases": ["Mount Wugong", "Wugongshan"], "latitude": 27.4500, "longitude": 114.1500, "elevation_m": 1918, "region": "Jiangxi", "country": "China", "state_province": "Jiangxi", "popularity_rank": 333},
    {"name": "Niubei Shan", "aliases": ["Mount Niubei", "Cattle Back Mountain"], "latitude": 29.6000, "longitude": 102.3333, "elevation_m": 3660, "region": "Sichuan", "country": "China", "state_province": "Sichuan", "popularity_rank": 336},
    {"name": "Daocheng Yading", "aliases": ["Yading", "Chenresig", "Xiannairi"], "latitude": 28.4167, "longitude": 100.3000, "elevation_m": 6032, "region": "Sichuan", "country": "China", "state_province": "Sichuan", "popularity_rank": 338},

    # --- More Europe filling ---
    {"name": "Serra da Estrela", "aliases": ["Torre", "Mount Torre Portugal"], "latitude": 40.3217, "longitude": -7.6119, "elevation_m": 1993, "region": "Serra da Estrela", "country": "Portugal", "state_province": "Guarda", "popularity_rank": 341},
    {"name": "Pico", "aliases": ["Ponta do Pico", "Mount Pico"], "latitude": 38.4683, "longitude": -28.3994, "elevation_m": 2351, "region": "Azores", "country": "Portugal", "state_province": "Azores", "popularity_rank": 343},
    {"name": "Dolomites Alta Via 1", "aliases": ["Alta Via 1", "High Route 1"], "latitude": 46.5000, "longitude": 12.0000, "elevation_m": 2752, "region": "Dolomites", "country": "Italy", "state_province": "South Tyrol", "popularity_rank": 346},
    {"name": "Seceda", "aliases": ["Seceda Ridgeline"], "latitude": 46.6017, "longitude": 11.7233, "elevation_m": 2519, "region": "Dolomites", "country": "Italy", "state_province": "South Tyrol", "popularity_rank": 348},
    {"name": "Cinque Torri", "aliases": ["Five Towers"], "latitude": 46.5167, "longitude": 12.0500, "elevation_m": 2366, "region": "Dolomites", "country": "Italy", "state_province": "Veneto", "popularity_rank": 351},
    {"name": "Lagazuoi", "aliases": ["Mount Lagazuoi"], "latitude": 46.5278, "longitude": 12.0100, "elevation_m": 2835, "region": "Dolomites", "country": "Italy", "state_province": "Veneto", "popularity_rank": 353},
    {"name": "Alpe di Siusi", "aliases": ["Seiser Alm", "Alpe di Siusi Plateau"], "latitude": 46.5417, "longitude": 11.6333, "elevation_m": 2015, "region": "Dolomites", "country": "Italy", "state_province": "South Tyrol", "popularity_rank": 356},
    {"name": "GR20 Corsica", "aliases": ["GR20", "Grande Randonnee 20"], "latitude": 42.3533, "longitude": 8.9500, "elevation_m": 2706, "region": "Corsica", "country": "France", "state_province": "Corsica", "popularity_rank": 358},
    {"name": "Lauterbrunnen Schilthorn", "aliases": ["Schilthorn", "Piz Gloria"], "latitude": 46.5575, "longitude": 7.8353, "elevation_m": 2970, "region": "Alps", "country": "Switzerland", "state_province": "Bern", "popularity_rank": 361},
    {"name": "Oeschinensee", "aliases": ["Oeschinen Lake Trail"], "latitude": 46.4986, "longitude": 7.7222, "elevation_m": 1578, "region": "Alps", "country": "Switzerland", "state_province": "Bern", "popularity_rank": 363},
    {"name": "Harder Kulm", "aliases": ["Harder Kulm Trail"], "latitude": 46.6917, "longitude": 7.8608, "elevation_m": 1322, "region": "Alps", "country": "Switzerland", "state_province": "Bern", "popularity_rank": 366},
    {"name": "Cares Gorge", "aliases": ["Ruta del Cares"], "latitude": 43.2333, "longitude": -4.9000, "elevation_m": 1200, "region": "Picos de Europa", "country": "Spain", "state_province": "Asturias", "popularity_rank": 368},
    {"name": "Montserrat", "aliases": ["Monserrat", "Sant Joan"], "latitude": 41.5933, "longitude": 1.8383, "elevation_m": 1236, "region": "Catalonia", "country": "Spain", "state_province": "Barcelona", "popularity_rank": 371},
    {"name": "Sierra de Gredos", "aliases": ["Pico Almanzor", "Almanzor"], "latitude": 40.2500, "longitude": -5.3000, "elevation_m": 2592, "region": "Central Spain", "country": "Spain", "state_province": "Avila", "popularity_rank": 373},
    {"name": "Sierra de Guadarrama", "aliases": ["Penalara", "Peñalara"], "latitude": 40.8500, "longitude": -3.9583, "elevation_m": 2428, "region": "Central Spain", "country": "Spain", "state_province": "Madrid", "popularity_rank": 376},
    {"name": "Mount Ida Crete", "aliases": ["Psiloritis Crete"], "latitude": 35.2278, "longitude": 24.7667, "elevation_m": 2456, "region": "Crete", "country": "Greece", "state_province": "Rethymno", "popularity_rank": 378},
    {"name": "Samaria Gorge", "aliases": ["Samaria"], "latitude": 35.3000, "longitude": 23.9667, "elevation_m": 1250, "region": "Crete", "country": "Greece", "state_province": "Chania", "popularity_rank": 381},
    {"name": "Mount Nemrut", "aliases": ["Nemrut Dagi", "Nemrut Dağı"], "latitude": 37.9808, "longitude": 38.7408, "elevation_m": 2134, "region": "Southeast Turkey", "country": "Turkey", "state_province": "Adiyaman", "popularity_rank": 383},
    {"name": "Kackar Mountains Traverse", "aliases": ["Kackar Traverse"], "latitude": 40.8375, "longitude": 41.1864, "elevation_m": 3937, "region": "Pontic Alps", "country": "Turkey", "state_province": "Rize", "popularity_rank": 386},
    {"name": "Aladaglar", "aliases": ["Aladağlar", "Demirkazik"], "latitude": 37.7500, "longitude": 35.2000, "elevation_m": 3756, "region": "Taurus Mountains", "country": "Turkey", "state_province": "Nigde", "popularity_rank": 388},
    {"name": "Lycian Way", "aliases": ["Likya Yolu"], "latitude": 36.5333, "longitude": 30.4500, "elevation_m": 2366, "region": "Lycian Way", "country": "Turkey", "state_province": "Antalya", "popularity_rank": 391},
    {"name": "Mount Olympos Turkey", "aliases": ["Tahtali Dag"], "latitude": 36.5333, "longitude": 30.4500, "elevation_m": 2366, "region": "Lycian Way", "country": "Turkey", "state_province": "Antalya", "popularity_rank": 393},
    {"name": "Tusheti", "aliases": ["Tusheti NP", "Omalo"], "latitude": 42.3833, "longitude": 45.3167, "elevation_m": 3600, "region": "Caucasus", "country": "Georgia", "state_province": "Kakheti", "popularity_rank": 396},
    {"name": "Mestia to Ushguli", "aliases": ["Mestia-Ushguli Trek"], "latitude": 43.0100, "longitude": 42.7000, "elevation_m": 3000, "region": "Caucasus", "country": "Georgia", "state_province": "Svaneti", "popularity_rank": 398},

    # --- More NZ and Australia ---
    {"name": "Mount Cook Range", "aliases": ["Hooker Valley Track"], "latitude": -43.7333, "longitude": 170.1000, "elevation_m": 762, "region": "Southern Alps", "country": "New Zealand", "state_province": "Canterbury", "popularity_rank": 401},
    {"name": "Milford Track", "aliases": ["Milford Sound Trek"], "latitude": -44.8000, "longitude": 167.8833, "elevation_m": 1154, "region": "Fiordland", "country": "New Zealand", "state_province": "Southland", "popularity_rank": 403},
    {"name": "Tongariro Alpine Crossing", "aliases": ["TAC", "Red Crater"], "latitude": -39.1339, "longitude": 175.6428, "elevation_m": 1886, "region": "Tongariro", "country": "New Zealand", "state_province": "Manawatu-Whanganui", "popularity_rank": 406},
    {"name": "Kepler Track", "aliases": ["Kepler Great Walk"], "latitude": -45.4500, "longitude": 167.6667, "elevation_m": 1471, "region": "Fiordland", "country": "New Zealand", "state_province": "Southland", "popularity_rank": 409},
    {"name": "Overland Track", "aliases": ["Overland Track Tasmania"], "latitude": -41.6542, "longitude": 145.9422, "elevation_m": 1545, "region": "Tasmania", "country": "Australia", "state_province": "Tasmania", "popularity_rank": 411},
    {"name": "Mount Feathertop", "aliases": ["Feathertop"], "latitude": -36.8692, "longitude": 147.1308, "elevation_m": 1922, "region": "Victorian Alps", "country": "Australia", "state_province": "Victoria", "popularity_rank": 413},
    {"name": "Three Capes Track", "aliases": ["Three Capes"], "latitude": -43.1833, "longitude": 147.8500, "elevation_m": 300, "region": "Tasmania", "country": "Australia", "state_province": "Tasmania", "popularity_rank": 416},
    {"name": "Larapinta Trail", "aliases": ["Larapinta"], "latitude": -23.7667, "longitude": 132.3333, "elevation_m": 1531, "region": "MacDonnell Ranges", "country": "Australia", "state_province": "Northern Territory", "popularity_rank": 419},
]


def main():
    output_path = pathlib.Path(__file__).parent.parent / "app" / "data" / "mountains.json"
    # Deduplicate by name (some entries might have duplicate names for different regions)
    seen = set()
    unique = []
    for m in MOUNTAINS:
        key = (m["name"], m["country"], m.get("state_province", ""))
        if key not in seen:
            seen.add(key)
            unique.append(m)

    unique.sort(key=lambda m: m["popularity_rank"])

    with open(output_path, "w") as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(unique)} mountains to {output_path}")

    # Validation
    ranks = [m["popularity_rank"] for m in unique]
    dupes = [r for r in set(ranks) if ranks.count(r) > 1]
    if dupes:
        print(f"WARNING: Duplicate ranks: {sorted(dupes)}")

    no_aliases = [m["name"] for m in unique if not m["aliases"]]
    if no_aliases:
        print(f"WARNING: {len(no_aliases)} mountains with no aliases: {no_aliases[:5]}...")

    from collections import Counter
    countries = Counter(m["country"] for m in unique)
    print(f"\nCountries: {len(countries)}")
    for c, n in countries.most_common(10):
        print(f"  {c}: {n}")
    print(f"\nTotal mountains: {len(unique)}")
    print(f"Rank range: {min(ranks)} - {max(ranks)}")


if __name__ == "__main__":
    main()
