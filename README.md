# ns-covid-counts
Grab counts of COVID-19 hospitaliztion

The counts for hospitalization and ICU in Nova Scotia are not made available through the regular health data site of https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19/epidemiological-economic-research-data.html Instead the numbers are in daily reports, non-structured format, at https://novascotia.ca/news/search/?dept=180

This code, run daily, looks at the new reports, attempts to extract the counts, and prepares sql statements for insertion into my database at http://data19.johnandrea.ca. It will fail if the phrases used to describe the counts change. The body of unmatched reports will be left in the data directory for human review.


## Matches ##

This code currently matches on these phrases (and more)
```
There are 48 people in hospital with nine in ICU.
Of those, 34 people are in hospital, including 4 in ICU.
```

Previously used phrases are not matched
```
No one is in hospital.
There are currently no hospitalizations.

One person is in hospital.
One person is currently in hospital, in ICU.

Of those, one person is in ICU.
Of those, one person is in a hospital COVID-19 unit.
Of those, four people are in hospital COVID-19 units.
Of those, three people are in hospital COVID-19 units, including one in ICU.

Two people are currently in hospital, in ICU.
Two people are currently in hospital. Of those, one is in ICU.
```

## Support ##

This code is provided with no support.
