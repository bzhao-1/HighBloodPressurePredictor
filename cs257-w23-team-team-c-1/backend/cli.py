from sqlapi import *
from decimal import Decimal
bp = BloodPressure(database=config.database, user=config.user, password=config.password, host="localhost")

def main():

    choice = 1

    print("Welcome to the High Blood Pressure Predictor! Please note that inputs should be entered with full country name, gender should be Men or Women, and year must be between 1975-2015(inclusive).")
    while choice != 0:
        valid_choice = False
        while not valid_choice:
            try:
                valid_choice = True
                print("Please select from the following choices: \n")
                print("(1) : Find the mean systolic blood pressure for a country and gender")
                print("(2) : Find the susceptibility of a specific country for raised blood pressure for a specific year")
                print("(3) : Find the prevalance(ranking among all years) of high blood pressure for a specific year")
                print("(4) : Find the average diastolic blood pressure for a country and gender")
                print("(5) : Find whether a given country is in the top 5 for prevalence of raised BP")
                print("(6) : Find the average BP for a specific country and gender and determine if these metrics are normal")
                print("(0) : Exit the program")

                choice = int(input("Make your selection: \n"))


                """ Mean systolic BP for country and gender in 2015 """
                if choice == 1:
                    inputCountry = bp.checkCountryInput(input("Select your country: \n"))
                    inputGender = bp.checkGenderInput(input("Select your gender: \n"))
                    prevalence = bp.averageSystolicBP(inputCountry, inputGender)
                    print("The mean systolic blood pressure for ", inputCountry, "and ", inputGender, " is ", float(prevalence[0][2]))
            
                """ Prevalence of raised BP for country and year """
                if choice == 2:
                    inputCountry = bp.checkCountryInput(input("Select your country: \n"))
                    inputYear = bp.checkIntInput(int(input("Select your year: \n")))
                    countrySusceptibility = bp.sortByCountry(inputCountry, inputYear)
                    print("The prevalence for high blood pressure for ", inputCountry, "in ", inputYear, "is", float(countrySusceptibility[0][0]), "%")

                """ Prevalence of high blood pressure by year(ranking amongst 1975 to 2015) """
                if choice == 3:
                    inputYear = bp.checkIntInput(int(input("Select your year: \n")))
                    outYear = bp.sortByYear(inputYear)
                    print(inputYear, "is ", outYear, "out of 50 for highest prevalence of raised blood pressure") 

                """ Average diastolic blood pressure for country and gender """
                if choice == 4:
                    inputCountry = bp.checkCountryInput(input("Select your country: \n"))
                    inputGender = bp.checkGenderInput(input("Select your gender: \n"))
                    outBP = bp.averageDiastolicBP(inputCountry, inputGender)
                    print("The mean diastolic blood pressure for ", inputCountry, "and ", inputGender, " is ", float(outBP[0][2]))
                
                """ Prevalence of cardiovascular disease for a specific gender and country """
                if choice == 5:
                    inputCountry = bp.checkCountryInput(input("Select your country: \n"))
                    inputGender = bp.checkGenderInput(input("Select your gender: \n"))
                    containsTop5 = bp.countryContainsTop5(inputCountry, inputGender)
                    print("The demographics ", inputCountry, "and ", inputGender, "are ", containsTop5, "for average raised blood pressure prevalence.")
                
                """ Average systolic and diastolic blood pressure for specific country and gender """
                if choice == 6:
                    inputCountry = bp.checkStringInput(input("Select your country: \n"))
                    inputGender = bp.checkGenderInput(input("Select your gender: \n"))
                    avgBP = bp.systolicAndDiastolicAverageBP(inputCountry, inputGender)
                    print("The average blood pressure for your demographics are: ", avgBP[0:2], avgBP[2])
                    
            except ValueError:
                print("Invalid input. Please enter a valid choice.")

    print("Thanks for using HBP predictor")
        

if __name__ == "__main__":
    main()
            
