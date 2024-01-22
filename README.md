# sqlalchemy-challenge

![honolulu-location-map](https://github.com/Pooja14n/sqlalchemy-challenge/assets/144713762/46b039f8-02ed-4c20-9ef4-0af8e8091da9)

In this challenge, we need to do a climate analysis about Honolulu, Hawaii. The following sections outline the steps that you need to take to accomplish this task. 

# Part 1: Analyze and Explore the Climate Data
In this section, we will use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, we will use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, we have to complete the following steps:

1. Note that the provided files (climate_starter.ipynb and hawaii.sqlite) are used to complete your climate analysis and data exploration.

2. Use the SQLAlchemy create_engine() function to connect to SQLite database.

3. Use the SQLAlchemy automap_base() function to reflect tables into classes, and then save references to the classes named station and measurement.

4. Link Python to the database by creating a SQLAlchemy session.

IMPORTANT
Close the session at the end of the notebook.

5. Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

# Precipitation Analysis
1. Find the most recent date in the dataset.
2. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
3. Select only the "date" and "prcp" values.
4. Load the query results into a Pandas DataFrame. Explicitly set the column names.
5. Sort the DataFrame values by "date".
6. Plot the results by using the DataFrame plot method, as the following image shows:
