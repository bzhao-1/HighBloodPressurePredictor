import pandas as pd
import numpy as np
from collections import OrderedDict as od
import matplotlib.pyplot as plt

class BloodPressure:
    def __init__(self):
        '''
        Reads in and stores the data from the specified file as a list of dictionaries, for use by the rest of the functions in the class.
        
        PARAMETER
            filename - the name (and path, if not in the current working directory) of the data file
        '''
        data = pd.read_csv("HBPdata.csv")

        self.HBPdata = data

        countries_list = self.HBPdata['Country'].tolist()
        self.countriesList = countries_list
        self.totalCountries = 200
        self.lowerTop5 = 194
        self.upperTop5 = 199

    def stringInput(self, input):
        if input.isalpha():
            return input
        else:
            raise Exception("Please enter a string")

    def genderInput(self, input):
        # String matches choices here (Men, Women)
        gender = self.stringInput(input)
        if gender == "Men" or input == "Women":
            return input
        # Other word not accepted
        else:
            raise Exception("Not a gender in the database")

    def countryInput(self, input):
        # If the country is in the list (country appearing in list of the CSV file)
        country = self.stringInput(input)
        if country in self.countriesList:
            return country
        # If it isn't (Country that the CSV does not have data for and doesn't list)
        else:
            raise Exception("Not a valid country")

    def intInput(self, input):
        #If the input is a number and it is between 1975 and 2015 (1994, 2004, etc.)
        if type(input) == int and input >= 1975 and input <= 2015:
            return input
        # Negative numbers, 0, positive numbers outside the range, etc.
        else:
            raise Exception("Input not valid")

    def floatInput(input):
        # Input is a number with a decimal (43.6, 132.28, etc.)
        if type(input) == float:
            return input
        # Input is an integer or string (Name, whole number, etc.)
        else:
            raise Exception("Please enter a decimal")
        
    
    """(1) When given a country and gender, the function finds the country(string) and gender(string) to display systolic blood pressure from most recent year(2015)"""
    def averageSystolicBP(self, country, gender):
        df = self.HBPdata.loc[(self.HBPdata['Year'] == 2015) & (self.HBPdata['Country'] == country) & (self.HBPdata['Sex'] == gender)]
        return df.iloc[0]['Mean systolic blood pressure (mmHg)']

    """(2) When given a country(string) and year(int), the function determines the susceptibility of that country(String) to high blood pressure"""
    def sortByCountry(self, country, year):
        """Prevalence of raised blood pressure"""
        df = self.HBPdata.loc[(self.HBPdata['Country'] == country) & (self.HBPdata['Year'] == year)]
        totalSusceptibility = df['Prevalence of raised blood pressure'].sum()
        return (totalSusceptibility/2) * 100

    """(3) When given a year(int), the function determines the prevalnce of raised BP for that year relative to the other years"""
    def sortByYear(self, year):
        """Ranking of year in prevalance amongst 1975 to 2015"""
        sortedYearsList  = self.sortByYearHelper()
        return [item[0] for item in sortedYearsList], [item[1]*100 for item in sortedYearsList], list(od(sortedYearsList).keys()).index(year) + 1

    
    """(4) When given a country(string) and gender(string), the average diastolic blood pressure is displayed for the selected parameters from 2015(most recent year)."""
    def averageDiastolicBP(self, country, gender):
        df = self.HBPdata.loc[(self.HBPdata['Year'] == 2015) & (self.HBPdata['Country'] == country) & (self.HBPdata['Sex'] == gender)]
        return df.iloc[0]['Mean diastolic blood pressure (mmHg)']

    """(5) Given a gender(string) and country(string), the function will determine whether prevalence of raised blood pressure for these demographics is in top 5 based on average raised blood pressure prevalence"""
    def countryContainsTop5(self, country, gender):
        if gender == "Men":
            sortedCountriesList = self.top5HelperMen()
            countryRanking = list(od(sortedCountriesList).keys()).index(country)
            if self.lowerTop5 <= countryRanking <= self.upperTop5:
                return [item[0] for item in sortedCountriesList], [item[1]*100 for item in sortedCountriesList], "In Top 5"
            else:
                return [item[0] for item in sortedCountriesList], [item[1]*100 for item in sortedCountriesList], "Not In Top 5"
        if gender == "Women":
            sortedCountriesList = self.top5HelperWomen()
            countryRanking = list(od(sortedCountriesList).keys()).index(country)
            if self.lowerTop5 <= countryRanking <= self.upperTop5:
                return [item[0] for item in sortedCountriesList], [item[1]*100 for item in sortedCountriesList], "In Top 5"
            else:
                return [item[0] for item in sortedCountriesList], [item[1]*100 for item in sortedCountriesList], "Not In Top 5"

    """"(6) When given a country(string) and gender(string), the function retrieves the average BP for those demographics.
        It also determines if the user's BP is considered healthy or unhealthy.""" 
    def systolicAndDiastolicAverageBP(self, country, gender):
        systolic = self.averageSystolicBP(country, gender)
        diastolic = self.averageDiastolicBP(country, gender)
        if systolic > 120 or diastolic > 80:
            return [systolic, diastolic, "unhealthy"]
        else:
            return [systolic, diastolic, "healthy"]

    """Sorts years by prevalence of raised blood pressure"""
    def sortByYearHelper(self):
        Years = {}
        for i in range(1975, 2016):
            df = self.HBPdata.loc[self.HBPdata['Year'] == i]
            raisedBPbyYear = df['Prevalence of raised blood pressure'].sum()
            Years[i] = raisedBPbyYear / (self.totalCountries * 2)
        sortedYearsbyBP = sorted(Years.items(), key=lambda x:x[1])
        return sortedYearsbyBP

    """Makes a top 5 for countries by prevalence of raised blood pressure based on country and gender(Men)"""
    def top5HelperMen(self):
        top5Men = {}
        for country_name in set(self.countriesList):
            prevalence_Men = self.avgPrevalenceMenHelper(country_name)
            top5Men[country_name] = prevalence_Men
        sortedCountriesbyBP = sorted(top5Men.items(), key=lambda x:x[1])
        return sortedCountriesbyBP        

    """Makes a top 5 for countries by prevalence of raised blood pressure based on country and gender(Women)"""
    def top5HelperWomen(self):
        top5Women = {}
        for country_name in set(self.countriesList):
            prevalence_Women = self.avgPrevalenceMenHelper(country_name)
            top5Women[country_name] = prevalence_Women
        sortedCountriesbyBP = sorted(top5Women.items(), key=lambda x:x[1])
        return sortedCountriesbyBP        
    
    def avgPrevalenceMenHelper(self, country):
            df_Men = self.HBPdata.loc[(self.HBPdata['Country'] == country) & (self.HBPdata['Sex'] == "Men")]
            prevalence_Men = df_Men['Prevalence of raised blood pressure'].sum() / 40
            return prevalence_Men
        
    def  avgPrevalenceWomenHelper(self, country):
            df_Women = self.HBPdata.loc[(self.HBPdata['Country'] == country) & (self.HBPdata['Sex'] == "Women")]
            prevalence_Women = df_Women['Prevalence of raised blood pressure'].sum() / 40
            return prevalence_Women
  
    
   
    def createBarGraph(self, country, gender):
        systolic_bp = self.averageSystolicBP(country, gender)
        plt.bar(country, systolic_bp)
        plt.xlabel('Country')
        plt.ylabel('Systolic Blood Pressure (mmHg)')
        plt.title(f'Average Systolic Blood Pressure for {gender} in {country}')
        plt.show()
    
    def plot_average_systolic_bp(self, country, gender):
        bp = self.averageSystolicBP(country, gender)

        # Plot the graph
        x_labels = country
        y_values = bp
        fig, ax = plt.subplots()
        ax.plot(x_labels, y_values, 'o-')
        
        # Customize the x-axis
        # ax.set_xticks(range(len(x_labels)))
        # ax.set_xticklabels(x_labels)
        # ax.tick_params(axis='x', which='both', length=0)
        
        plt.title("Average Systolic Blood Pressure for {} {}".format(country, gender))
        plt.ylabel("Average Systolic Blood Pressure (mmHg)")
        plt.savefig("systolic_bp.png")

    def plot_average_diastolic_bp(self, country, gender):
        bp = self.averageDiastolicBP(country, gender)

        # Plot the graph
        x_labels = country
        y_values = bp
        fig, ax = plt.subplots()
        ax.plot(x_labels, y_values, 'o-')
        
        # Customize the x-axis
        # ax.set_xticks(range(len(x_labels)))
        # ax.set_xticklabels(x_labels)
        # ax.tick_params(axis='x', which='both', length=0)
        
        plt.title("Average Dia Blood Pressure for {} {}".format(country, gender))
        plt.ylabel("Average Dia Blood Pressure (mmHg)")
        plt.savefig("systolic_bp.png")


    
    def plotPrevalence(self, year):
        years, prevalences, ranking = self.sortByYear(year)
        plt.figure(figsize=(10, 6))
        plt.plot(years, prevalences, marker='o', markersize=8, color='blue')
        plt.plot(year, prevalences[years.index(year)], marker='o', markersize=12, color='red')
        plt.xticks(rotation=90, fontsize=12)
        plt.xlabel("Year", fontsize = 12)
        plt.ylabel("Prevalence (%)", fontsize=12)
        plt.title(f"Average prevalence of high blood pressure by Year ({year}): Prevalence Ranking({ranking})(1 being least prevalent out of 40 countries)", fontsize = 10)
        plt.subplots_adjust(bottom=0.2) 
        plt.savefig("prevalence_by_year.png")

    def plotsortByCountry(self, country, year):
        prevalence = self.sortByCountry(country, year)

        # Plot the graph
        x_labels = country
        y_values = prevalence
        fig, ax = plt.subplots()
        ax.plot(x_labels, y_values, 'o-')
        
      
        
        plt.title("Average prevalence of high blood pressure for {} in {}".format(country, year))
        plt.ylabel("Prevalence (%)")
        plt.show()
    
    def find10nearestcountries(self, country, gender):
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

  
       

            
if __name__ == "__main__":
    bloodPressure = BloodPressure()
    
    bloodPressure.plotsortByCountry("Algeria", 2015)
    
    

    