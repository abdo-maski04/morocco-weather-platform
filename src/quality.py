# ce fichier set à controller les données douteuses avant de passer à dbt
# qui va faire le grand travail

from src.database import get_connection
import logging as log

logger = log.getLogger(__name__)  




def check_nulls():
    logger.info("checking nulls in the data for each city")
    with get_connection() as conn:
        with conn.cursor() as cursor:
                        query = """
                        select city, count(*) 
                        filter (where max_temp is null or min_temp is null or mean_temp is null or sum_precipitation is null or max_wind_speed is null) as nbr_null
                        from raw.weather_daily
                        group by city
                        """
                        cursor.execute(query)
                        results=cursor.fetchall()
                        nbr_nulls=0
                        for city,nbr_null in results:
                            if nbr_null>0:
                                logger.warning(f"City {city} has {nbr_null} null values in the data")
                                nbr_nulls+=nbr_null
                            else:
                                logger.info(f"City {city} has no null values in the data")
                        logger.info(f"Total number of null values in the data: {nbr_nulls}")
                        return nbr_nulls

def check_duplicates():
    logger.info("Checking duplicates in the data")

    with get_connection() as conn:
        with conn.cursor() as cursor:

            query = """
                SELECT
                    city,
                    date,
                    COUNT(*) AS nbr_duplicates
                FROM raw.weather_daily
                GROUP BY city, date
                HAVING COUNT(*) > 1;
            """

            cursor.execute(query)
            results = cursor.fetchall()

            nbr_duplicates = 0

            for city, date, nbr_duplicate in results:
                logger.error(
                    f"Duplicate key (city,date)=({city},{date}) "
                    f"appears {nbr_duplicate} times"
                )
                nbr_duplicates += 1
            logger.info(f"Total number of duplicate keys in the data: {nbr_duplicates}")
            return nbr_duplicates


def check_missing_dates():
     logger.info("Checking for missing dates in the data")

     with get_connection() as conn:
          with conn.cursor() as cursor:
               query="""
                select city,min(date) as minDate,max(date) as maxDate,count(*) as nbrDays
                from raw.weather_daily
                group by city
                """

               cursor.execute(query)
               results=cursor.fetchall()
               nbr_total_missing_days=0
               for city,minDate,maxDate,nbrDays in results:
                    if nbrDays!=(maxDate-minDate).days+1:
                         nbr_missing_days=(maxDate-minDate).days+1-nbrDays
                         nbr_total_missing_days+=nbr_missing_days
                         logger.warning(f"City {city} is missing {nbr_missing_days} days of data")
                    else:
                        logger.info(f"City {city} has no missing days of data")
               return nbr_total_missing_days
        
def check_outliers():
     logger.info("Checking for outliers in the data")
     with get_connection() as conn:
          with conn.cursor() as cursor:
               query="""
                select city,count(*)
                filter(
                where max_temp>50
                or max_temp<-20
                or min_temp>50
                or min_temp<-20
                or mean_temp not between -20 and 50
                or sum_precipitation<0
                or max_wind_speed<0
                ) as nbr_outliers
                from raw.weather_daily
                group by city"""
               cursor.execute(query)
               results=cursor.fetchall()
               nbr_total_outliers=0
               for city,nbr_outliers in results:
                    if nbr_outliers>0:
                         logger.warning(f"City {city} has {nbr_outliers} outliers in the data")
                         nbr_total_outliers += nbr_outliers
                    else:
                        logger.info(f"City {city} has no outliers in the data")
               logger.info(f"Total number of outliers in the data: {nbr_total_outliers}")
               return nbr_total_outliers

def run_quality_checks():
    nbr_duplicates = check_duplicates()
    nbr_outliers = check_outliers()
    check_nulls()            # avertissement seulement
    check_missing_dates()    # avertissement seulement
    if nbr_duplicates > 0 :
        raise ValueError(f"Quality checks failed: {nbr_duplicates} duplicates found.")  
    if nbr_outliers > 0:
        raise ValueError(f"Quality checks failed: {nbr_outliers} outliers found.")  # message avec les deux totaux
    logger.info("run quality_checks completed successfully with no duplicates or outliers found.")

   