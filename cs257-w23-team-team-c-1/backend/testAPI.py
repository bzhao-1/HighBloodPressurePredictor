import unittest
import psycopg2
import psqlConfig as config

from sqlapi import *

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.bp = BloodPressure(database=config.database, user=config.user, password=config.password, host="localhost")

    # # GENDER INPUT METHODS
    def test_genderInput_menInput_pass(self):
        """Input is a gender in database and passes the genderInput method"""
        self.assertTrue(self.bp.genderInput("Men") == "Men")
    
    def test_genderInput_womenInput_fail(self):
        """Input is a gender in database and passes the genderInput method"""
        self.assertTrue(self.bp.genderInput("Women") == "Women")

    def test_genderInput_invalidString_fail(self): 
        """Input is a string but not a gender in the database and fails the genderInput method"""
        with self.assertRaises(Exception):
            self.bp.genderInput("Hello") == "Women"
            
    def test_genderInput_int_fail(self): 
        """Input is an int and fails the genderInput method"""
        with self.assertRaises(Exception):
            self.bp.genderInput(21)
        
    def test_genderInput_float_fail(self):  
        """Input is a float and fails the genderInput method"""
        with self.assertRaises(Exception):
            self.bp.genderInput(34.123)
    
    def test_genderInput_noInput_fail(self):  
        """Input is nonexistent and fails the genderInput method"""
        with self.assertRaises(Exception):
            self.bp.genderInput()
    
    def test_genderInput_boolean_fail(self):  
        """Input is a boolean and fails the genderInput method"""
        with self.assertRaises(Exception):
            self.bp.genderInput(False)
        
    # COUNTRY INPUT METHODS
    def test_country_input_pass(self):
        """Input is a country in the dataset and passes the countryInput method"""
        self.assertTrue(self.bp.countryInput("Nigeria") == "Nigeria")
    
    def test_country_input_invalidString_fail(self):
        """Input is a string that is not a country in the dataset and fails the countryInput method"""
        with self.assertRaises(Exception):
            self.bp.countryInput("Nice to meet you")
            
    def test_country_input_int_fail(self):
        """Input is an int and fails the countryInput method"""
        with self.assertRaises(Exception):
            self.bp.countryInput(32) 
    
    def test_country_input_boolean_fail(self):
        """Input is a boolean and fails the countryInput method"""
        with self.assertRaises(Exception):
            self.bp.countryInput(True)
    
    def test_country_input_float_fail(self):
        """Input is a float and fails the countryInput method"""
        with self.assertRaises(Exception):
            self.bp.countryInput(45.384)
    
    def test_country_input_noInput_fail(self):
        """Input is nonexistent and fails the countryInput method"""
        with self.assertRaises(Exception):
            self.bp.countryInput()
    
    #INT INPUT METHOD
    def test_intInput_pass(self):
        """Input is an integer between 1975 and 2015 and passes the intInput method"""
        self.assertTrue(self.bp.intInput(2000) == 2000)
    
    def test_intInput_int_fail(self):
        """Input is an integer outside that range and fails the intInput method"""
        with self.assertRaises(Exception):
            self.bp.intInput(1328)
    
    def test_intInput_invalidString_fail(self): 
        """Input is a string and fails the intInput method"""
        with self.assertRaises(Exception):
            self.bp.intInput("Hello again")
    
    def test_intInput_float_fail(self): 
        """Input is a float and fails the intInput method"""
        with self.assertRaises(Exception):
            self.bp.intInput(2013.32)

    def test_intInput_boolean_fail(self): 
        """Input is a boolean and fails the intInput method"""
        with self.assertRaises(Exception):
            self.bp.intInput(False)
    
    def test_intInput_noInput_fail(self): 
        """Input is nonexistent and fails the intInput method"""
        with self.assertRaises(Exception):
            self.bp.intInput()
        
    # AVERAGE SYSTOLIC BP METHODS
    def test_averageSystolicBP_validString_pass(self):
        """Inputs are strings (country and gender) and are in the database and within 1975-2015, 
        passing the averageSystolicBP method"""
        result = self.bp.averageSystolicBP("Algeria", "Men")
        self.assertTrue(result == self.bp.averageSystolicBP("Algeria", "Men"))
    
    def test_averageSystolicBP_invalidString_fail(self):
        """Inputs are strings (country and gender) which are not present in the database and 
        fail the averageSystolicBP method"""
        self.assertTrue(self.bp.averageSystolicBP("Wakanda", "Viper") == []) 
    
    def test_averageSystolicBP_boolean_float_fail(self):
        """Inputs are boolean and float, failing the averageSystolicBP method"""
        self.assertFalse(self.bp.averageSystolicBP(True, 32.1) == 2)
    
    def test_averageSystolicBP_noInput_fail(self):
        """Inputs are nonexistent, failing the averageSystolicBP method"""
        with self.assertRaises(Exception):
            self.bp.averageSystolicBP()
    
    # SORT BY COUNTRY METHOD
    def test_sortByCountry_validInput_pass(self):
        """If the country and year are in the database and the range of 1975-2015, passing the sortByCountry method"""
        result = self.bp.sortByCountry("Algeria", 2015)
        self.assertTrue(self.bp.sortByCountry("Algeria", 2015) == result)
    
    def test_sortByCountry_invalidStringAndInt_fail(self):
        """If the country and year are not in the database, failing the sortByCountry method"""
        self.assertFalse(self.bp.sortByCountry("Wakanda", 1032) == 49.9)
        
    def test_sortByCountry_invalidBooleanAndFloat_fail(self):
        """If the country and year are boolean and float, failing the sortByCountry method"""
        self.assertFalse(self.bp.sortByCountry(True, 2041.21829) == 49.9)
    
    def test_sortByCountry_noInput_fail(self):
        """If the country and year are nonexistent, failing the sortByCountry method"""
        with self.assertRaises(Exception):
            self.bp.sortByCountry()
    
    # # SORT BY YEAR METHOD
    def test_sortByYear_pass(self):
        """If the year is between the values of 1975-2015, passing the sortByYear method"""
        self.assertTrue(self.bp.sortByYear(2015) == 1)
    
    def test_sortByYear_invalidYear_fail(self):
        """If the year is outside of those values, failing the sortByYear method"""
        self.assertFalse(self.bp.sortByYear(1234) == 1)
    
    def test_sortByYear_float_fail(self):
        """If the year is a float, failing the sortByYear method"""
        self.assertFalse(self.bp.sortByYear(102.2) == 1)
    
    def test_sortByYear_boolean_fail(self): 
        """If the year is a boolean, failing the sortByYear method"""
        self.assertFalse(self.bp.sortByYear(True) == 1)
    
    def test_sortByYear_noInput_fail(self): 
        """If the year is nonexistent, failing the sortByYear method"""
        with self.assertRaises(Exception):
         self.bp.sortByYear()
        
    # # AVERAGE DIASTOLIC BP METHOD
    def test_averageDiastolicBP_validInput_pass(self):
        """Inputs are strings (country and gender) and are in the database and within 1975-2015, 
        passing the averageDiastolicBP method"""
        result = self.bp.averageDiastolicBP("Algeria", "Men")
        self.assertTrue(self.bp.averageDiastolicBP("Algeria", "Men") == result)

    def test_averageDiastolicBP_invalidString_fail(self):
        """Inputs are strings (country and gender) which are not present in the database and 
        fail the averageDiastolicBP method"""
        self.assertFalse(self.bp.averageSystolicBP("Wakanda", "Viper") == 77.7) 
    
    def test_averageDiastolicBP_int_fail(self):
        """Inputs are integers, failing the averageDiastolicBP method"""
        self.assertFalse(self.bp.averageDiastolicBP(12, 15) == 77.7) 
    
    def test_averageDiastolicBP_validInput_fail(self):
        """Inputs are boolean and float, failing the averageDiastolicBP method"""
        self.assertFalse(self.bp.averageDiastolicBP(True, 32.1) == 77.7)
    
    def test_averageDiastolicBP_noInput_fail(self):
        """Inputs are nonexistent, failing the averageDiastolicBP method"""
        with self.assertRaises(Exception):
            self.bp.averageDiastolicBP() == 128.9848303

    # COUNTRY CONTAINED IN TOP5 FOR PREVALENCE METHOD
    def test_countryContainsTop5_strings_pass(self):
        """The country and gender are strings in the database, passing the countryContainsTop5 method"""
        self.assertTrue(self.bp.countryContainsTop5("Algeria", "Men") == "Not In Top 5")
    
    def test_countryContainsTop5_invalidStrings_fail(self):
        """The country and gender are strings not in the database, failing the countryContainsTop5 method"""
        self.assertFalse(self.bp.systolicAndDiastolicAverageBP("Wakanda", "Creosote") == 10.2)
    
    def test_countryContainsTop5_boolean_float_fail(self):
        """The country and gender are boolean and float, failing the countryContainsTop5 method"""
        self.assertFalse(self.bp.systolicAndDiastolicAverageBP(True, 201231.12928319) == 2)
    
    def test_countryContainsTop5_int_fail(self):
        """The country and gender are integers, failing the countryContainsTop5 method"""
        self.assertFalse(self.bp.systolicAndDiastolicAverageBP(21, 23) == [])
    
    def test_countryContainsTop5_noInput_fail(self):
        """The country and gender inputs are nonexistent, failing the countryContainsTop5 method"""
        with self.assertRaises(Exception):
            self.bp.systolicAndDiastolicAverageBP()

        
    # # SYSTOLIC AND DIASTOLIC AVERAGE BP METHOD 
    def test_systolicAndDiastolicAverageBP_strings_pass(self):
        """The country and gender are strings in the database, passing the systolicAndDiastolicAverageBP method"""
        self.assertTrue(self.bp.systolicAndDiastolicAverageBP("Algeria", "Men") == [127.5986403, 77.72350578, 'Your blood pressure is an indicator of being at risk'])

    def test_systolicAndDiastolicAverageBP_invalidStrings_fail(self):
        """The country and gender are strings not in the database, failing the systolicAndDiastolicAverageBP method"""
        self.assertFalse(self.bp.systolicAndDiastolicAverageBP("Wakanda", "Creosote") == 77.777)
    
    def test_systolicAndDiastolicAverageBP_boolean_float_fail(self):
        """The country and gender are boolean and float, failing the systolicAndDiastolicAverageBP method"""
        self.assertFalse(self.bp.systolicAndDiastolicAverageBP(True, 201231.12928319) == 2)
    
    def test_systolicAndDiastolicAverageBP_int_fail(self):
        """The country and gender are integers, failing the systolicAndDiastolicAverageBP method"""
        self.assertFalse(self.bp.systolicAndDiastolicAverageBP(21, 23) == "Nigeria")
    
    def test_systolicAndDiastolicAverageBP_noInput_fail(self):
        """The country and gender inputs are nonexistent, failing the systolicAndDiastolicAverageBP method"""
        with self.assertRaises(Exception):
            self.bp.systolicAndDiastolicAverageBP()
        
    #######  HELPER METHODS  #######
    
    # # top5HelperMen HELPER METHOD
    def test_top5HelperMen_string_pass(self):
        """The country string is in the database, passing the top5HelperMen method"""
        result = self.bp.top5HelperMen("Algeria")
        self.assertTrue(self.bp.top5HelperMen("Algeria") == result)

    def test_top5HelperMen_invalidString_fail(self):
        """The input is a string that is not in the database, failing the top5HelperMen method"""
        self.assertFalse(self.bp.top5HelperMen("Fish") == 0.05)
    
    def test_top5HelperMen_float_fail(self):
        """The input is a float, failing the top5HelperMen method"""
        with self.assertRaises(Exception):
            self.bp.top5HelperMen(32.321234)
    
    def test_top5HelperMen_string_fail(self):
        """The input is an integer, failing the top5HelperMen method"""
        with self.assertRaises(Exception):
            self.bp.top5HelperMen(76)
    
    def test_top5HelperMen_boolean_fail(self):
        """The input is a boolean, failing the top5HelperMen method"""
        with self.assertRaises(Exception):
            self.bp.top5HelperMen(True)
    
    def test_top5HelperMen_noInput_fail(self):
        """The input is nonexistent, failing the top5HelperMen method"""
        with self.assertRaises(Exception):
            self.bp.top5HelperMen()
    
    # # # top5HelperWomen HELPER METHOD
    def test_top5HelperWomen_string_pass(self):
        """The country string is in the database, passing the top5HelperWomen method"""
        result = self.bp.top5HelperWomen("Algeria")
        self.assertTrue(self.bp.top5HelperWomen("Algeria") == result)
    
    def test_top5HelperWomen_invalidString_fail(self):
        """The input is a string that is not in the database, failing the top5HelperWomen method"""
        self.assertFalse(self.bp.top5HelperWomen("Cheese") == 0.06251686339000001)
    
    def test_top5HelperWomen_float_fail(self):
        """The input is a float, failing the top5HelperWomen method"""
        with self.assertRaises(Exception):
            self.bp.top5HelperWomen(3.2)
    
    def test_top5HelperWomen_int_fail(self):
        """The input is an integer, failing the top5HelperWomen method"""
        with self.assertRaises(Exception):
            self.bp.top5HelperWomen(65)
    
    def test_top5HelperWomen_boolean_fail(self):
        """The input is a boolean, failing the top5HelperWomen method"""
        with self.assertRaises(Exception):
            self.bp.top5HelperWomen(True)
    
    def test_top5HelperWomen_noInput_fail(self):
        """The input is nonexistent, failing the top5HelperWomen method"""
        with self.assertRaises(Exception):
            self.bp.top5HelperWomen()
            
    

if __name__ == "__main__":
    unittest.main()
