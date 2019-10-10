from fuzzywuzzy import fuzz

# https://medium.com/@categitau/fuzzy-string-matching-in-python-68f240d910fe
# https://towardsdatascience.com/natural-language-processing-for-fuzzy-string-matching-with-python-6632b7824c49

print(fuzz.partial_ratio("the daily show with trevor noah", "the daily show"))
print(fuzz.ratio("the daily show", "the daily show with trevor noah"))
