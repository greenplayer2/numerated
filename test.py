from unittest.mock import patch
from unittest import TestCase
import main

itinerary_1 = []
itinerary_2 = []
itinerary_3 = []

route_text = """Please select a route:

1: Red
2: Mattapan
3: Orange
4: Green-B
5: Green-C
6: Green-D
7: Green-E
8: Blue"""

itinerary_1.append(route_text)
itinerary_2.append(route_text)
itinerary_3.append(route_text)

itinerary_1.append("""

Please select your stop on the Orange line:
1: Oak Grove
2: Malden Center
3: Wellington
4: Assembly
5: Sullivan Square
6: Community College
7: North Station
8: Haymarket
9: State
10: Downtown Crossing
11: Chinatown
12: Tufts Medical Center
13: Back Bay
14: Massachusetts Avenue
15: Ruggles
16: Roxbury Crossing
17: Jackson Square
18: Stony Brook
19: Green Street
20: Forest Hills""")

itinerary_1.append("""

Please select a direction for the Orange route starting from Community College stop:
1: South toward Forest Hills
2: North toward Oak Grove""")

itinerary_1.append("""

You are taking the Orange line South toward Forest Hills from Community College.""")

itinerary_1.append("You need to be at Community College stop at ")

itinerary_2.append("""

Please select your stop on the Green-C line:
1: North Station
2: Haymarket
3: Government Center
4: Park Street
5: Boylston
6: Arlington
7: Copley
8: Hynes Convention Center
9: Kenmore
10: Saint Mary's Street
11: Hawes Street
12: Kent Street
13: Saint Paul Street
14: Coolidge Corner
15: Summit Avenue
16: Brandon Hall
17: Fairbanks Street
18: Washington Square
19: Tappan Street
20: Dean Road
21: Englewood Avenue
22: Cleveland Circle""")

itinerary_2.append("""

Please select a direction for the Green-C route starting from Kent Street stop:
1: West toward Cleveland Circle
2: East toward North Station""")

itinerary_2.append("""

You are taking the Green-C line West toward Cleveland Circle from Kent Street.""")

itinerary_2.append("You need to be at Kent Street stop at ")

itinerary_3.append("""

Please select your stop on the Red line:
1: Alewife
2: Davis
3: Porter
4: Harvard
5: Central
6: Kendall/MIT
7: Charles/MGH
8: Park Street
9: Downtown Crossing
10: South Station
11: Broadway
12: Andrew
13: JFK/UMass
14: Savin Hill
15: Fields Corner
16: Shawmut
17: Ashmont
18: North Quincy
19: Wollaston
20: Quincy Center
21: Quincy Adams
22: Braintree""")

itinerary_3.append("""

Please select a direction for the Red route starting from Alewife stop:
1: South toward Ashmont/Braintree
2: North toward Alewife""")

itinerary_3.append("""

You are taking the Red line North toward Alewife from Alewife.""")

itinerary_3.append("No schedule data could be determined for this route!")

class Test(TestCase):
    try:
        MBTA = main.MBTAScheduler()
    except Exception as e:
        print(str(e))
        quit()

    # Itinerary 1: Orange line from Community College stop South toward Forest Hills
    @patch('builtins.input', return_value='3')
    def test_1(self, mock_input):
        self.assertEqual(self.MBTA.get_routes(), itinerary_1[0])
        self.assertEqual(self.MBTA.select_route(), itinerary_1[1])

    @patch('builtins.input', return_value='6')
    def test_2(self, mock_input):
        self.assertEqual(self.MBTA.select_stop(), itinerary_1[2])

    @patch('builtins.input', return_value='1')
    def test_3(self, mock_input):
        self.assertEqual(self.MBTA.select_direction(), itinerary_1[3])
        self.assertEqual(self.MBTA.get_answer()[:-6], itinerary_1[4])

    # Itinerary 2: Green C line west toward Cleveland Circle from Kent Street
    @patch('builtins.input', return_value='5')
    def test_4(self, mock_input):
        self.assertEqual(self.MBTA.get_routes(), itinerary_2[0])
        self.assertEqual(self.MBTA.select_route(), itinerary_2[1])

    @patch('builtins.input', return_value='12')
    def test_5(self, mock_input):
        self.assertEqual(self.MBTA.select_stop(), itinerary_2[2])

    @patch('builtins.input', return_value='1')
    def test_6(self, mock_input):
        self.assertEqual(self.MBTA.select_direction(), itinerary_2[3])
        self.assertEqual(self.MBTA.get_answer()[:-6], itinerary_2[4])

    # Itinerary 3: Red Line from Alewife North toward Alewife
    @patch('builtins.input', return_value='1')
    def test_7(self, mock_input):
        self.assertEqual(self.MBTA.get_routes(), itinerary_3[0])
        self.assertEqual(self.MBTA.select_route(), itinerary_3[1])

    @patch('builtins.input', return_value='1')
    def test_8(self, mock_input):
        self.assertEqual(self.MBTA.select_stop(), itinerary_3[2])

    @patch('builtins.input', return_value='2')
    def test_9(self, mock_input):
        self.assertEqual(self.MBTA.select_direction(), itinerary_3[3])
        self.assertEqual(self.MBTA.get_answer(), itinerary_3[4])

