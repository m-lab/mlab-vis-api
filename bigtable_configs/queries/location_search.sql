SELECT
  REPLACE(LOWER(CONCAT(
    IFNULL(location, ""), "",
    IFNULL(client_region_code, ""), "",
    IFNULL(client_country_code, ""), "",
    IFNULL(client_continent_code, "")
  )), " ", "") as location_key,
  location,
  type,
  client_region,
  client_country,
  client_continent,
  test_count,
  last_three_month_test_count
from

-- Cities
(select
  "city" as type,
  count(*) as test_count,
  threemonths.last_three_month_test_count,
  all.client_city as location,
  all.client_city as client_city,
  all.client_region as client_region,
  all.client_country as client_country,
  all.client_continent as client_continent,

  all.client_region_code as client_region_code,
  all.client_country_code as client_country_code,
  all.client_continent_code as client_continent_code

  FROM {0} all
  left join
  (SELECT
    count(*) as last_three_month_test_count,
    client_city,
    client_region,
    client_country,
    client_continent
    from {0}
    where test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -3, "MONTH")
    group by
      client_city,
      client_region,
      client_country,
      client_continent) threemonths on
        all.client_city = threemonths.client_city and
        all.client_region = threemonths.client_region and
        all.client_country = threemonths.client_country and
        all.client_continent = threemonths.client_continent
  GROUP BY location, client_city, client_region, client_region_code, client_country,
    client_country_code, client_continent, client_continent_code,
    threemonths.last_three_month_test_count
),

-- Regions
(select
  "region" as type,
  count(*) as test_count,
  threemonths.last_three_month_test_count,
  all.client_region as location,
  all.client_region as client_region,
  all.client_country as client_country,
  all.client_continent as client_continent,

  all.client_region_code as client_region_code,
  all.client_country_code as client_country_code,
  all.client_continent_code as client_continent_code

  FROM {0} all
  left join
  (SELECT
    count(*) as last_three_month_test_count,
    client_region,
    client_country,
    client_continent
    from {0}
    where test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -3, "MONTH")
    group by
      client_region,
      client_country,
      client_continent) threemonths on
        all.client_region = threemonths.client_region and
        all.client_country = threemonths.client_country and
        all.client_continent = threemonths.client_continent
  GROUP BY location, client_region, client_region_code, client_country,
    client_country_code, client_continent, client_continent_code,
    threemonths.last_three_month_test_count
),

-- Countries
(select
  "country" as type,
  count(*) as test_count,
  threemonths.last_three_month_test_count,
  all.client_country as location,
  all.client_country as client_country,
  all.client_continent as client_continent,

  all.client_country_code as client_country_code,
  all.client_continent_code as client_continent_code

  FROM {0} all
  left join
  (SELECT
    count(*) as last_three_month_test_count,
    client_country,
    client_continent
    from {0}
    where test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -3, "MONTH")
    group by
      client_country,
      client_continent) threemonths on
        all.client_country = threemonths.client_country and
        all.client_continent = threemonths.client_continent
  GROUP BY location, client_country,
    client_country_code, client_continent, client_continent_code,
    threemonths.last_three_month_test_count
),

-- Continents
(select
  "continent" as type,
  count(*) as test_count,
  threemonths.last_three_month_test_count,
  all.client_continent as location,
  all.client_continent as client_continent,

  all.client_continent_code as client_continent_code
  FROM {0} all
  left join
  (SELECT
    count(*) as last_three_month_test_count,
    client_continent
    from {0}
    where test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -3, "MONTH")
    group by
      client_continent) threemonths on
        all.client_continent = threemonths.client_continent
  GROUP BY location, client_continent, client_continent_code,
  threemonths.last_three_month_test_count
)
WHERE
  location IS NOT NULL;
