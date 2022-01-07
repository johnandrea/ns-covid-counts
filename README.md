# ns-covid-counts
Grab counts of COVID-19 hospitaliztion

The counts for hospitalization and ICU in Nova Scotia are not made available through the regular health data site of https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19/epidemiological-economic-research-data.html Instead the numbers are in daily reports, non-structured format, at https://novascotia.ca/news/search/?dept=180

This code, run daily, looks at the new reports, attempts to extract the counts, and prepares sql statements for insertion into my database at http://data19.johnandrea.ca. It will fail if the phrases used to describe the counts change, but the body of the unmatched reports will be left in the data directory.

A cleanup should be performed on the archive directory so that it doesn't build without limit. I'm using (also daily):
```
find canada-hospital/ns/archive/ -mtime +30 -type f -name "*txt" -print -delete
find canada-hospital/ns/archive/ -mtime +30 -type f -name "*sql" -print -delete

```

I'm still hunting for data from the other provinces.
