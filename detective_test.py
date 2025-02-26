from modules.new_model import Detective

question = "find last house on Franklin Ave"
context = """
{"user_inputs":["find last house on Franklin Ave"],"sql_queries":["SELECT * FROM person WHERE address_street_name = 'Franklin Ave'"],"query_results":["COLUMNS:id,name,license_id,address_number,address_street_name,ssn\n(12207, 'Wilmer Wolever', 509484, 139, 'Franklin Ave', 636825374)\n(16371, 'Annabel Miller', 490173, 103, 'Franklin Ave', 318771143)\n(17683, 'Johnnie Schee', 968887, 1277, 'Franklin Ave', 815977821)\n(18651, 'Carleen Etoll', 356746, 22, 'Franklin Ave', 193369255)\n(22636, 'Zachary Ybarbo', 768359, 785, 'Franklin Ave', 285346605)\n(24737, 'Gema Nantz', 273410, 3968, 'Franklin Ave', 180545802)\n(30654, 'Clarita Rickels', 418084, 2254, 'Franklin Ave', 714941023)\n(32264, 'Shelby Dezeeuw', 735415, 1391, 'Franklin Ave', 143197463)\n(33793, 'Amado Mattan', 161915, 99, 'Franklin Ave', 125205748)\n(34592, 'Cordell Lindamood', 592762, 3657, 'Franklin Ave', 509890333)\n(36328, 'Domenic Laun', 971080, 3809, 'Franklin Ave', 825329637)\n(36400, 'Noe Pancoast', 895755, 3443, 'Franklin Ave', 732212073)\n(37616, 'Katelyn Schwerin', 430143, 332, 'Franklin Ave', 392365033)\n(46827, 'Bev Billiter', 643591, 2316, 'Franklin Ave', 940192302)\n(52059, 'Jordan Pelton', 686854, 2786, 'Franklin Ave', 676224073)\n(52075, 'Ezra Phy', 928109, 384, 'Franklin Ave', 176404498)\n(52121, 'Yelena Whitler', 427830, 3185, 'Franklin Ave', 115106155)\n(54817, 'Guy Bustard', 213929, 591, 'Franklin Ave', 820850670)\n(54896, 'Patty Wamsley', 688488, 1097, 'Franklin Ave', 725272037)\n(56142, 'William Shiver', 741336, 1926, 'Franklin Ave', 219913461)\n(57051, 'Lavette Koehl', 137365, 2284, 'Franklin Ave', 776046786)\n(59746, 'Ronny Gumbert', 469722, 3197, 'Franklin Ave', 561067477)\n(60944, 'Ricki Bidding', 443364, 2072, 'Franklin Ave', 614976330)\n(61001, 'Laurine Bousman', 197150, 247, 'Franklin Ave', 431360364)\n(61437, 'Colette Hollomon', 661377, 453, 'Franklin Ave', 314956038)\n(62292, 'Isaiah Holsten', 913856, 747, 'Franklin Ave', 995368430)\n(62520, 'Mariah Lepetich', 450447, 3086, 'Franklin Ave', 797745632)\n(67292, 'Renita Roperto', 801041, 625, 'Franklin Ave', 894442480)\n(69719, 'Hope Arzabala', 311724, 841, 'Franklin Ave', 270289620)\n(70050, 'Whitney Herkenratt', 138462, 3445, 'Franklin Ave', 552518972)\n(75510, 'Sebastian Ramnarase', 333188, 1127, 'Franklin Ave', 315716580)\n(76128, 'Ressie Razze', 633497, 1199, 'Franklin Ave', 456366143)\n(78170, 'Graig Summy', 192325, 3387, 'Franklin Ave', 277793306)\n(78408, 'Dante Eschen', 218173, 3447, 'Franklin Ave', 135374633)\n(78658, 'Blake Chrones', 310242, 2014, 'Franklin Ave', 423048084)\n(78830, 'Candice Train', 814779, 3255, 'Franklin Ave', 717570815)\n(83003, 'Wilmer Casella', 672050, 3564, 'Franklin Ave', 569057540)\n(83754, 'Maria Walsh', 201334, 2716, 'Franklin Ave', 121282864)\n(84531, 'Edgar Mendieta', 315790, 3881, 'Franklin Ave', 458847132)\n(87521, 'Moses Ikerd', 638991, 2283, 'Franklin Ave', 797715435)\n(88966, 'Raul Eads', 570927, 2066, 'Franklin Ave', 764132739)\n(93947, 'Omer Andreoni', 605718, 13, 'Franklin Ave', 322594288)\n(95119, 'Hong Lisa', 825828, 375, 'Franklin Ave', 113438176)\n(97913, 'Cameron Dilick', 971988, 2954, 'Franklin Ave', 665147939)\n(98744, 'Jordan Myntti', 256116, 3104, 'Franklin Ave', 876030104)\n"],"detective_answers":[null],"detective_thinking":[null]}
"""

response = Detective(question, context)


print((response.full_response))
print("\nAnswer:\n", response.answer)
print("\nNext step:\n", response.next_step)
print("\nThinking:\n", response.thinking)
