import psycopg2
import psqlConfig as config
from collections import OrderedDict as od
from decimal import Decimal
import matplotlib.pyplot as plt


class BloodPressure:
    def __init__(self, database, user, password, host):
        '''
        Establishes a connection to the database with the following credentials:
        user - username, which is also the name of the database
        password - the password for this database on perlman

        Note: exits if a connection cannot be established.

        Also creates a list of all countries to check user input for country by selecting distinct country values and turning it into a list of strings
        '''
       
        try:
            self.prevalencethreshold = 0.35
            self.connection = psycopg2.connect(database=database, user=user, password=password, host=host)
            self.cursor = self.connection.cursor()
            
            
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def checkGenderInput(self, user_input):
        '''
        Checks input to see whether it matches gender in database(Men/Women)
        Parameters
            user_input - user input

        Returns:
            Gender if input is man or women, otherwise prompts user to enter gender in database

        '''
        
        while user_input != "Men" or not user_input != "Women":
            user_input = input("Please enter a gender in database: ")
            
        return user_input

    def checkCountryInput(self, user_input):
        '''
        Checks input to see whether it is a country in database
        Parameters
            user_input - user input

        Returns:
            String if input is a country and string or prompts user to enter country in database

        '''

        while user_input not in self.countriesList():
            user_input = input("Please enter a country in database: ")
        return user_input


    def checkIntInput(self, user_input):
        '''
        Checks input to see whether it is it is an integer and in database for years
        Parameters
            user_input - user input

        Returns:
            Year if input is int and falls in database year range 

        '''
        while type(user_input) != int or user_input < 1975 or user_input > 2015:
            user_input = input("Please enter a valid year: ")
        return user_input
    
    def countriesList(self):
        query = "SELECT DISTINCT Country FROM highBloodPressure"
        self.cursor.execute(query)
        country_list = list(self.cursor.fetchall())
        country_list = [str(result[0]) for result in country_list]
        return country_list

    def averageSystolicBP(self, country, gender):
        '''
        (1) Displays systolic blood pressure for demographic specified

        Parameters:
            country - country from database
            gender - Men or Women

        Returns:
            Systolic BP for specified demographic
        '''
        try:
            query = "SELECT Country, Sex, avgSystolicBP FROM highBloodPressure WHERE Year_ = 2015 AND Country = %s AND Sex = %s;"
            self.cursor.execute(query, (country, gender))
            return self.cursor.fetchall()


        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None



    def sortByCountry(self, country, year):
        '''
        (2) Displays susceptibility to high blood pressure for demographic specified

        Parameters:
            country - country - country from database
            year - year from database between 1975 - 2015
        
        Returns:
            Prevalence of high blood presure for specified demographic
        '''
        try:
            query = "SELECT SUM(prevalenceRaisedBP) * 100 FROM highBloodPressure WHERE Country = %s AND Year_ = %s;"
            self.cursor.execute(query, (country, year))
            return self.cursor.fetchall()
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None




    def sortByYear(self, year):
        '''
        (3) Displays prevalence of raised BP for demographic specified relative to other years (40 total)

        Parameters:
            year - year from database between 1975 - 2015
        
        Returns:
            Ranking of prevalence of raised BP for specified year in comparison to other years where 1 is the least prevalent year 
        '''
        try:
            sortedYearsList  = self.sortByYearHelper()
            queryResult = [item[0] for item in sortedYearsList], [item[1]*100 for item in sortedYearsList], list(od(sortedYearsList).keys()).index(year) + 1
            return self.parseTupleQuery(queryResult)
    
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def averageDiastolicBP(self, country, gender):
        '''
        (4) Displays diastolic blood pressure for demographic specified

        Parameters:
            country - country from database
            gender - Men or Women
                        
        Returns:
            Diastolic BP for specified demographic
        '''
        try:
            query = "SELECT Country, Sex, avgDiastolicBP FROM highBloodPressure WHERE Country = %s AND Sex = %s AND Year_ = 2015;"
            self.cursor.execute(query, (country, gender))
            return self.cursor.fetchall()
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None
    

    def countryContainsTop5(self, country, gender):
        '''(5) Displays whether prevalence of raised blood pressure of a demographics is in top 5 countries based on average raised blood pressure prevalence
        
        Parameters:
            country - country from database
            gender - Men or Women
        
        Returns:
            Whether a specific demographic is in the top 5 for most prevalent raised BP levels(thererfore determining whether this demographic looks like a typical patient likely to have high BP)
        '''
        try:
            if gender == "Men":
                sortedCountriesList = self.avgPrevalenceMenHelper()
                first_five_countries = sortedCountriesList[:5]
                if country in first_five_countries:
                    queryResult = [item[0] for item in sortedCountriesList], [item[1]*100 for item in sortedCountriesList], "In Top 5"
                    return self.parseTupleQuery(queryResult)
                else:
                    queryResult = [item[0] for item in sortedCountriesList], [item[1]*100 for item in sortedCountriesList], "Not In Top 5"
                    return self.parseTupleQuery(queryResult)
            if gender == "Women":
                sortedCountriesList = self.avgPrevalenceWomenHelper()
                first_five_countries = sortedCountriesList[:5]
                if country in first_five_countries:
                    queryResult = [item[0] for item in sortedCountriesList], [item[1]*100 for item in sortedCountriesList], "In Top 5"
                    return self.parseTupleQuery(queryResult)
                else:
                    queryResult = [item[0] for item in sortedCountriesList], [item[1]*100 for item in sortedCountriesList], "Not In Top 5"
                    return self.parseTupleQuery(queryResult)

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None
        
            


    def systolicAndDiastolicAverageBP(self, country, gender):
        '''(6) Determines BP metrics for demographic. Also determines whether specified demographic is considered at risk based on prevalence of raised BP.
            Allows user to be categorized as healthy or unhealthy where healthy is (systolic < 120 and diastolic < 80) and unhealthy is (systolic > 120 or diastolic > 80)
        
        Parameters:
            country - country from database
            gender - Men or Women
        
        Returns:
            BP measurements for a demographic and number of indicators that the demographic has of being at risk for high BP(indicator 1: individual BP, indicator 2: average prevalence of raisedBP for that demographic)
        '''
        try:
            systolic = self.averageSystolicBP(country, gender)
            diastolic = self.averageDiastolicBP(country, gender)
            healthMetric = self.systolicandDiastolicHelper(country, gender)
            if healthMetric > self.prevalencethreshold:
                if systolic[0][2] > 120 or diastolic[0][2] > 80:
                    queryResult = [systolic[0][2], diastolic[0][2], "You have two indicators that suggest being at risk"]
                    return self.parseQuery(queryResult)
                else:
                    queryResult = [systolic[0][2], diastolic[0][2], "Your demographic is an indicator of being at risk"]
                    return self.parseQuery(queryResult)
            else:
                if systolic[0][2] < 120 and diastolic[0][2] < 80:
                    queryResult = [systolic[0][2], diastolic[0][2], "No indicators of being at risk"]
                    return self.parseQuery(queryResult)
                else:
                    queryResult = [systolic[0][2], diastolic[0][2], "Your blood pressure is an indicator of being at risk"]
                    return self.parseQuery(queryResult)


        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None
    
    
    def systolicandDiastolicHelper(self, country, gender):
        """
        Helper function to get average raised BP prevalence for a specific demographic

        Parameters:
            country - country from database
            gender - Men or Women

        Returns:
            Average raised BP level for input 
        """

        query = "SELECT SUM(prevalenceRaisedBP)/40 FROM highBloodPressure WHERE Country = %s and Sex = %s"
        self.cursor.execute(query, (country, gender))
        queryResult = self.cursor.fetchone()
        return queryResult[0]

    def sortByYearHelper(self):
        """
        Helper function that sorts years by prevalence of raised blood pressure

        Returns:
            Sorted list of years based on their average raised BP prevalence 
        """
        query = "SELECT Year_, SUM(prevalenceRaisedBP)/400 FROM highBloodPressure GROUP BY Year_;"
        self.cursor.execute(query, ())
        data = self.cursor.fetchall()
        sortedYearsbyBP = sorted(data, key=lambda x:x[1])
        return sortedYearsbyBP

    def top5HelperMen(self, gender):
        """
        Helper function that makes a top 5 countries by prevalence of raised BP

        Parameters:
            gender - Men or Women from database

        Returns:
            Query for average prevalence of raised blood pressure based on country and gender(Men)
        """
        query = "SELECT Country, SUM(prevalenceRaisedBP)/40 FROM highBloodPressure WHERE Sex = %s GROUP BY Country;"
        self.cursor.execute(query, (gender,))
        return self.cursor.fetchall()        

    def top5HelperWomen(self, gender):
        """
        Helper function that makes a top 5 countries by prevalence of raised BP

        Parameters:
            gender - Men or Women from database

        Returns:
            Query for average prevalence of raised blood pressure based on country and gender(Women)
        """
        query = "SELECT Country, SUM(prevalenceRaisedBP)/40 FROM highBloodPressure WHERE Sex = %s GROUP BY Country;"
        self.cursor.execute(query, (gender,))
        return self.cursor.fetchall()        
    
    def avgPrevalenceMenHelper(self):
        """
        Helper function that sorts countries based on their average raised BP prevalence

        Returns:
            Sorted list of countries sorted by average raised BP prevalence for men 
        """
        data = self.top5HelperMen("Men")
        prevalenceList = sorted(data, key=lambda x: x[1], reverse=True)
        return prevalenceList
        
    def avgPrevalenceWomenHelper(self):
        """
        Helper function that sorts countries based on their average raised BP prevalence

        Returns:
            Sorted list of countries sorted by average raised BP prevalence for women 
        """
        data = self.top5HelperWomen("Women")
        prevalenceList = sorted(data, key=lambda x: x[1], reverse=True)
        return prevalenceList

    
    def parseQuery(self, queryResult):
        """The following helper method parses a query result of a list decimal objects."""
        result = [float(i) if isinstance(i, Decimal) else i for i in queryResult]
        return result
    
    def parseTupleQuery(self, queryResult):
        """The following helper method parses a query result of a tuple of decimal objects."""
        result = ([float(i) if isinstance(i, Decimal) else i for i in queryResult[0]], [float(i) if isinstance(i, Decimal) else i for i in queryResult[1]], queryResult[2])
        return result
    
    def plotAverageSystolicBP(self, country, gender):
        results = self.averageSystolicBP(country, gender)
        x_labels = country
        y_values = float(results[0][2])
        fig, ax = plt.subplots()
        ax.plot(x_labels, y_values, 'o-')
        plt.title("Average Systolic Blood Pressure for {} {}".format(country, gender))
        plt.ylabel("Average Systolic Blood Pressure (mmHg)")
        plt.savefig("systolic_bp.png")
    

    def plotSortByCountry(self, country, year):
        prevalence = self.sortByCountry(country, year)
        x_labels = country
        y_values = float(prevalence[0][0])
        fig, ax = plt.subplots()
        ax.plot(x_labels, y_values, 'o-')
        plt.title("Average prevalence of high blood pressure for {} in {}".format(country, year))
        plt.ylabel("Prevalence (%)")
        plt.savefig("susceptibility_to_highBP.png")

        
    def plotSortByYear(self, year):
        """The following helper method graphs the SortByYear query."""
        years, prevalences, ranking = self.sortByYear(year)
        plt.figure(figsize=(10, 6))
        plt.plot(years, prevalences, marker='o', markersize=8, color='blue')
        plt.plot(year, prevalences[years.index(year)], marker='o', markersize=12, color='red')
        plt.xticks(rotation=90, fontsize=12)
        plt.xlabel("Year", fontsize = 12)
        plt.ylabel("Prevalence (%)", fontsize=12)
        plt.title(f"Average prevalence of high blood pressure by Year ({year}): Prevalence Ranking({ranking})(1 being least prevalent out of 40 countries)", fontsize = 10)
        plt.savefig("prevalence_by_year.png")



    def plotAverageDiastolicBP(self, country, gender):
        """The following helper method graphs the 4th query."""
        results = self.averageDiastolicBP(country, gender)
        x_labels = country
        y_values = float(results[0][2])
        fig, ax = plt.subplots()
        ax.plot(x_labels, y_values, 'o-')
        plt.title("Average Diastolic Blood Pressure for {} in {}".format(country, gender))
        plt.ylabel("Average Diastolic Blood Pressure (mmHg)")
        plt.savefig("systolic_bp.png")

    def find10nearestcountries(self, country, gender):
        """The following helper methods graph the countryContainsTops5 query."""
        countries, prevalences, in_top_5 = self.countryContainsTop5(country, gender)
        country_index = countries.index(country)
        start_index = max(0, country_index-10)
        end_index = min(len(countries), country_index+10)
        countries_to_plot = countries[start_index:end_index]
        prevalences_to_plot = prevalences[start_index:end_index]
        return countries_to_plot, prevalences_to_plot
    
    def plotcountryContainsTop5(self, country, gender):
        countries_to_plot, prevalences_to_plot = self.find10nearestcountries(country, gender)
        colors = ['blue'] * len(countries_to_plot)
        country_index = countries_to_plot.index(country)
        colors[country_index] = 'red'
        plt.figure(figsize=(10, 6))
        for i, (country, prevalence) in enumerate(zip(countries_to_plot, prevalences_to_plot)):
            plt.plot(country, prevalence, marker='o', markersize=8, color=colors[i])
        plt.xticks(rotation=90, fontsize=12)
        plt.xlabel("Countries", fontsize=12)
        plt.ylabel("Prevalence (%)", fontsize=12)
        plt.title(f"Average prevalence of raised BP by country(+/- 10 countries with nearest prevalence %)", fontsize=12)
        
        plt.tight_layout()
        plt.savefig("countryprevalencenearest20.png", dpi=300)

    def plotSystolicAndDiastolicAverageBP(self, country, gender):
        self.plotAverageSystolicBP(country, gender)
        self.plotAverageDiastolicBP(country, gender)
        text = self.systolicAndDiastolicAverageBP(country, gender)
        text = text[2]
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, text, ha='center', va='center')
        plt.save("health_metric.png")







        
if __name__ == "__main__":
    
    bloodPressure = BloodPressure(database=config.database, user=config.user, password=config.password, host="localhost")
    
    
    results = bloodPressure.systolicAndDiastolicAverageBP("Algeria", "Men")
    
    # results2 = bloodPressure.sortByYear(2015)
    
    if results is not None:
        print("Query results: ", results)
    
    # if results2 is not None:
    #     print("Query results: ", results2)


   


        