						************************************************************************************************************
																		CS 215 Project												
						************************************************************************************************************

Group 1:
--------------------------------------------------------------------------------------------------------------------------------------------------------
	Members				|	Roll Number	
	------------------------------------
	Chandra Maloo		|	130050009	
	Utkarsh Kumar		|	130050022
	Dibyendu Mondal		|	130050046	

--------------------------------------------------------------------------------------------------------------------------------------------------------

System Requirements:
-> Python 2.7

--------------------------------------------------------------------------------------------------------------------------------------------------------
How to run:
-> Go to the directory containing 'project.py' in the terminal.
-> Make sure the following files are present in the same directory:
	$	countries_id_map
	$	kb-facts-train_SI.tsv
	$	selected_indicators
	$	sentences.tsv
-> Run 'project.py' by "python project.py"
-> Output is generated in "output.csv"
--------------------------------------------------------------------------------------------------------------------------------------------------------

Working of our program:
-> We have defined classes 'Attribute', 'Country' and 'Sentence' along with their data members and data functions to help organise and simplify the code.

-> We also have defined three dictionaries (which are basically maps):
	# cc : A dictionary that maps a country code to the corresponding index number, in the order in which they are received the first time.
	# cn : A dictionary that maps a country name to the corresponding index number, in the order in which they are received the first time.
	# p  : A dictionary that maps an attribute to the corresponding index number, in the order in which they are received the first time.

-> On running the code, main function is called by default, which:
	# reads from "countries_id_map.txt" and populates 'country_array', which is a list of countries with their codes and list of names (different country names with the same country code). Here we have correctly assumed that country names with the same code appear one after the other.
	
	# reads from "selected_indicators" and populates "attributes_array_main", a list of the attributes with their attribute-codes, units etc, to be considered while analysing the sentences. Here we have assumed that there are 11 attributes to be considered per country.

	# runs a 'for' loop that adds this attribute-list to each of the countries already listed above.
	
	# reads from "kb-facts-train-SI.csv" and fills up the attribute-list for each country using this data.

	# calls regression() function for each of the countries, which:
		% finds the sample mean and variance for each attribute of the country
		% uses linear regression, assuming data points to correspond to years 1900 to 2010 with equal size intervals in an increasing order, and finds the regression coefficients

	# reads "sentences.tsv" and converts each row of input to a corresponding Sentence class object and calls the function doAll() on that Sentence object.
		
		% the doAll() function uses the country-name passed with the Sentence object and goes on removing the last letter until it finds a match with one of the countries in the country_array list (or the country-name becomes empty). This step is necessary so that words such as 'Indian' in the sentence can be identified.
		
		% if one of the numbers passed lies between 1500 and 2200, it is assumed to be the year under the consideration.

		% then, for each attribute for that country, it checks for the presence of atleast one of the key-words in the sentence. If not found, that attribute is ignored. But if it finds it, it calculates its Score with all the values present in the sentence by the member function Score of Sentence class.

		% if a year is not specified in the sentence, the score function returns 90 if the value lies between minimum and maximum of the given values of the attribute (since we do not have the year and hence it is a very elegible candidate). Else,
			$ if the value is greater than the largest of the given values of the attribute, u = maximum value.
			$ if the value is smaller than the smallest of the given values of the attribute, u = minimum value.

		% for calculation of score, the function uses the normlised exponential formula { score = 100 * exp( -(x-u)^2) / (2(s^2) ) / (sqrt(2*pi)*s) }, s being the standard deviation of the sample values of attribute in consideration.