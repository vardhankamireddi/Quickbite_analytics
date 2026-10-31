# SQL Query Results Summary (All 20 Queries)
## QuickBite Analytics | Team: Data Knights | CODEGNAN DA-07

> Complete empirical results for all 20 analytical queries defined in `sql/04_analysis_queries.sql`.
> Executed against the full 100,000-order QuickBite canonical dataset.

## Q01: Total Orders by City
*(Result count: 3 rows)*

| city          |   total_orders |   completed_orders |   cancelled_orders |   cancellation_rate_pct |   pct_of_total |
|:--------------|---------------:|-------------------:|-------------------:|------------------------:|---------------:|
| Hyderabad     |          55032 |              48359 |               6673 |                   12.13 |          55.03 |
| Visakhapatnam |          25311 |              22228 |               3083 |                   12.18 |          25.31 |
| Vijayawada    |          19657 |              17235 |               2422 |                   12.32 |          19.66 |

---

## Q02: Revenue by City
*(Result count: 3 rows)*

| city          |   total_orders |   gross_order_value_inr |   total_discounts_inr |   net_sales_inr |   avg_order_value_inr |   discount_rate_pct |
|:--------------|---------------:|------------------------:|----------------------:|----------------:|----------------------:|--------------------:|
| Hyderabad     |          48359 |             1.81146e+07 |           1.44103e+06 |     1.66736e+07 |                374.59 |                7.96 |
| Visakhapatnam |          22228 |             8.31919e+06 |      659342           |     7.65985e+06 |                374.27 |                7.93 |
| Vijayawada    |          17235 |             6.44498e+06 |      509770           |     5.93521e+06 |                373.95 |                7.91 |

---

## Q03: Top Restaurants by Orders
*(Result count: 20 rows)*

|   rank | restaurant_id   | restaurant_name              | cuisine       | city          | area           |   completed_orders |
|-------:|:----------------|:-----------------------------|:--------------|:--------------|:---------------|-------------------:|
|      1 | R1115           | Local Healthy Bites          | Healthy       | Visakhapatnam | Seethammadhara |                 42 |
|      2 | R3560           | Star Biryani Corner          | Biryani       | Hyderabad     | Dilsukhnagar   |                 41 |
|      3 | R1296           | Classic Rolls & Wraps Hub    | Rolls & Wraps | Hyderabad     | Miyapur        |                 39 |
|      4 | R3688           | Authentic Fast Food House    | Fast Food     | Hyderabad     | Gachibowli     |                 39 |
|      5 | R3545           | Spicy Burger Stop            | Burger        | Vijayawada    | Gunadala       |                 37 |
|      6 | R1712           | Royal Fast Food Station      | Fast Food     | Hyderabad     | Dilsukhnagar   |                 37 |
|      7 | R1647           | Quick South Indian Station   | South Indian  | Hyderabad     | Kukatpally     |                 37 |
|      8 | R2892           | Grand Chinese Express        | Chinese       | Visakhapatnam | Asilmetta      |                 37 |
|      9 | R0156           | Royal Thali Station          | Thali         | Hyderabad     | Secunderabad   |                 37 |
|     10 | R3109           | Authentic Fast Food Bites    | Fast Food     | Visakhapatnam | Dwaraka Nagar  |                 36 |
|     11 | R0059           | Fresh North Indian Station   | North Indian  | Hyderabad     | Kondapur       |                 36 |
|     12 | R1592           | Grand South Indian Cafe      | South Indian  | Vijayawada    | Gunadala       |                 36 |
|     13 | R0803           | Urban Burger Hub             | Burger        | Visakhapatnam | Jagadamba      |                 36 |
|     14 | R0057           | Quick Continental Station    | Continental   | Hyderabad     | Ameerpet       |                 36 |
|     15 | R1973           | Royal Fast Food House        | Fast Food     | Hyderabad     | Hitech City    |                 36 |
|     16 | R2088           | Fresh Healthy Diner          | Healthy       | Visakhapatnam | MVP Colony     |                 36 |
|     17 | R0962           | Premium North Indian Kitchen | North Indian  | Visakhapatnam | Dwaraka Nagar  |                 35 |
|     18 | R1174           | Authentic Thali Kitchen      | Thali         | Hyderabad     | Jubilee Hills  |                 35 |
|     19 | R1047           | Classic Healthy Express      | Healthy       | Hyderabad     | Banjara Hills  |                 35 |
|     20 | R1245           | Classic Seafood Kitchen      | Seafood       | Visakhapatnam | Jagadamba      |                 35 |

---

## Q04: Top Restaurants by Revenue
*(Result count: 20 rows)*

|   revenue_rank | restaurant_id   | restaurant_name             | cuisine       | city          |   total_orders |   total_revenue_inr |   avg_order_value_inr |
|---------------:|:----------------|:----------------------------|:--------------|:--------------|---------------:|--------------------:|----------------------:|
|              1 | R1115           | Local Healthy Bites         | Healthy       | Visakhapatnam |             42 |             16025.5 |                381.56 |
|              2 | R3560           | Star Biryani Corner         | Biryani       | Hyderabad     |             41 |             15813   |                385.68 |
|              3 | R0156           | Royal Thali Station         | Thali         | Hyderabad     |             37 |             14338   |                387.51 |
|              4 | R3376           | Local North Indian Express  | North Indian  | Visakhapatnam |             30 |             14235.2 |                474.51 |
|              5 | R3988           | Spicy Continental Point     | Continental   | Hyderabad     |             30 |             14089.9 |                469.66 |
|              6 | R3353           | Fresh Fast Food Express     | Fast Food     | Vijayawada    |             32 |             13692.8 |                427.9  |
|              7 | R1047           | Classic Healthy Express     | Healthy       | Hyderabad     |             35 |             13517.4 |                386.21 |
|              8 | R2823           | Spicy Rolls & Wraps Point   | Rolls & Wraps | Visakhapatnam |             33 |             13400.3 |                406.07 |
|              9 | R3967           | Grand Burger Place          | Burger        | Hyderabad     |             32 |             13378.3 |                418.07 |
|             10 | R1600           | Grand Rolls & Wraps Kitchen | Rolls & Wraps | Vijayawada    |             31 |             13321   |                429.71 |
|             11 | R1647           | Quick South Indian Station  | South Indian  | Hyderabad     |             37 |             13194.5 |                356.61 |
|             12 | R1483           | Quick Pizza Delight         | Pizza         | Hyderabad     |             32 |             13161.7 |                411.3  |
|             13 | R3736           | Premium Desserts Stop       | Desserts      | Hyderabad     |             34 |             13137.9 |                386.41 |
|             14 | R0956           | Royal Thali Bites           | Thali         | Hyderabad     |             34 |             13137.1 |                386.39 |
|             15 | R1296           | Classic Rolls & Wraps Hub   | Rolls & Wraps | Hyderabad     |             39 |             13107   |                336.08 |
|             16 | R3688           | Authentic Fast Food House   | Fast Food     | Hyderabad     |             39 |             13104.6 |                336.01 |
|             17 | R2039           | Star Thali Kitchen          | Thali         | Hyderabad     |             30 |             12962.4 |                432.08 |
|             18 | R1178           | Star Desserts Corner        | Desserts      | Hyderabad     |             34 |             12936.7 |                380.49 |
|             19 | R3122           | Classic Thali Bites         | Thali         | Hyderabad     |             32 |             12917.8 |                403.68 |
|             20 | R1243           | Fresh Seafood Stop          | Seafood       | Visakhapatnam |             29 |             12805.9 |                441.58 |

---

## Q05: Restaurant Ranking by Rating
*(Result count: 20 rows)*

|   rating_rank | restaurant_id   | restaurant_name             | cuisine       | city          |   platform_rating |   total_reviews |   avg_customer_rating |   pct_5_star |   pct_low_rating |
|--------------:|:----------------|:----------------------------|:--------------|:--------------|------------------:|----------------:|----------------------:|-------------:|-----------------:|
|             1 | R0684           | Royal North Indian Diner    | North Indian  | Visakhapatnam |               5   |              15 |                  5    |        100   |                0 |
|             2 | R2708           | Classic Fast Food Delight   | Fast Food     | Hyderabad     |               5   |              14 |                  5    |        100   |                0 |
|             3 | R2622           | Local Burger Hub            | Burger        | Vijayawada    |               5   |              12 |                  5    |        100   |                0 |
|             4 | R2029           | Local Burger Eatery         | Burger        | Hyderabad     |               5   |              19 |                  4.95 |         94.7 |                0 |
|             5 | R3607           | Premium Desserts Place      | Desserts      | Vijayawada    |               4.9 |              18 |                  4.94 |         94.4 |                0 |
|             6 | R1345           | Premium Seafood Eatery      | Seafood       | Visakhapatnam |               5   |              18 |                  4.94 |         94.4 |                0 |
|             7 | R0050           | Quick Burger Stop           | Burger        | Hyderabad     |               4.9 |              17 |                  4.94 |         94.1 |                0 |
|             8 | R2572           | Fresh North Indian Kitchen  | North Indian  | Vijayawada    |               5   |              17 |                  4.94 |         94.1 |                0 |
|             9 | R3414           | Urban Rolls & Wraps Express | Rolls & Wraps | Hyderabad     |               4.9 |              16 |                  4.94 |         93.8 |                0 |
|            10 | R2378           | Star Burger House           | Burger        | Visakhapatnam |               4.8 |              15 |                  4.93 |         93.3 |                0 |
|            11 | R3937           | Local Burger Place          | Burger        | Hyderabad     |               5   |              21 |                  4.9  |         90.5 |                0 |
|            12 | R3690           | Quick Healthy Eatery        | Healthy       | Hyderabad     |               4.7 |              19 |                  4.89 |         89.5 |                0 |
|            13 | R2454           | Local Thali Hub             | Thali         | Hyderabad     |               4.9 |              17 |                  4.88 |         88.2 |                0 |
|            14 | R1849           | Spicy Rolls & Wraps Eatery  | Rolls & Wraps | Vijayawada    |               5   |              17 |                  4.88 |         88.2 |                0 |
|            15 | R2430           | Home Fast Food Stop         | Fast Food     | Vijayawada    |               4.9 |              16 |                  4.88 |         87.5 |                0 |
|            16 | R2677           | Quick Burger Bites          | Burger        | Hyderabad     |               4.9 |              15 |                  4.87 |         86.7 |                0 |
|            17 | R1016           | Authentic Healthy Eatery    | Healthy       | Vijayawada    |               4.9 |              15 |                  4.87 |         86.7 |                0 |
|            18 | R1868           | Grand North Indian Eatery   | North Indian  | Hyderabad     |               5   |              15 |                  4.87 |         86.7 |                0 |
|            19 | R2407           | Quick Fast Food Cafe        | Fast Food     | Hyderabad     |               5   |              14 |                  4.86 |         85.7 |                0 |
|            20 | R3715           | Classic North Indian Point  | North Indian  | Vijayawada    |               4.9 |              21 |                  4.86 |         90.5 |                0 |

---

## Q06: Complaint Rate by Restaurant
*(Result count: 20 rows)*

| restaurant_id   | restaurant_name             | city          | cuisine       |   total_feedback |   total_complaints |   complaint_rate_pct | top_complaints                               |
|:----------------|:----------------------------|:--------------|:--------------|-----------------:|-------------------:|---------------------:|:---------------------------------------------|
| R1388           | Tasty Fast Food House       | Hyderabad     | Fast Food     |               13 |                 13 |                  100 | Quality Issue, Rude Rider, Poor Packaging    |
| R3964           | Quick South Indian Place    | Visakhapatnam | South Indian  |               21 |                 21 |                  100 | Wrong Item, Rude Rider, Overcharge           |
| R1462           | Authentic Burger Point      | Visakhapatnam | Burger        |               13 |                 13 |                  100 | Late Delivery, Quality Issue, Poor Packaging |
| R2950           | Fresh Desserts Stop         | Vijayawada    | Desserts      |               10 |                 10 |                  100 | Late Delivery, Poor Packaging, Rude Rider    |
| R2953           | Star Desserts Place         | Visakhapatnam | Desserts      |               20 |                 20 |                  100 | Late Delivery, Cold Food, Quality Issue      |
| R1886           | Royal Continental Eatery    | Hyderabad     | Continental   |               11 |                 11 |                  100 | Missing Item, Rude Rider, Cold Food          |
| R3861           | Urban Healthy Corner        | Vijayawada    | Healthy       |               13 |                 13 |                  100 | Overcharge, Cold Food, Late Delivery         |
| R1499           | Star Fast Food Place        | Hyderabad     | Fast Food     |               13 |                 13 |                  100 | Late Delivery, Quality Issue, Poor Packaging |
| R2969           | Authentic South Indian Stop | Vijayawada    | South Indian  |               13 |                 13 |                  100 | Missing Item, Rude Rider, Wrong Item         |
| R2982           | Quick Continental Bites     | Hyderabad     | Continental   |               13 |                 13 |                  100 | Cold Food, Poor Packaging, Late Delivery     |
| R2937           | Quick North Indian House    | Visakhapatnam | North Indian  |               15 |                 15 |                  100 | Poor Packaging, Cold Food, Late Delivery     |
| R2875           | Quick Chinese Bites         | Visakhapatnam | Chinese       |               12 |                 12 |                  100 | Overcharge, Wrong Item, Rude Rider           |
| R1087           | Home Biryani Station        | Visakhapatnam | Biryani       |               21 |                 21 |                  100 | Overcharge, Missing Item, Rude Rider         |
| R3083           | Authentic Thali Cafe        | Hyderabad     | Thali         |               15 |                 15 |                  100 | Quality Issue, Late Delivery, Wrong Item     |
| R0519           | Tasty Healthy Corner        | Vijayawada    | Healthy       |               19 |                 19 |                  100 | Wrong Item, Poor Packaging, Cold Food        |
| R3045           | Local Thali House           | Visakhapatnam | Thali         |               11 |                 11 |                  100 | Late Delivery, Poor Packaging, Missing Item  |
| R2853           | Home Rolls & Wraps Cafe     | Hyderabad     | Rolls & Wraps |                7 |                  7 |                  100 | Rude Rider, Overcharge, Missing Item         |
| R1851           | Grand Fast Food Point       | Hyderabad     | Fast Food     |               18 |                 18 |                  100 | Late Delivery, Poor Packaging, Missing Item  |
| R3098           | Fresh Desserts Station      | Hyderabad     | Desserts      |               18 |                 18 |                  100 | Wrong Item, Late Delivery, Quality Issue     |
| R3115           | Quick Burger Place          | Hyderabad     | Burger        |               14 |                 14 |                  100 | Overcharge, Quality Issue, Late Delivery     |

---

## Q07: Avg Delivery by City
*(Result count: 3 rows)*

| city          |   total_deliveries |   avg_delivery_time_min |   min_delivery_time_min |   max_delivery_time_min |   avg_delay_min |   avg_distance_km |   on_time_deliveries |   on_time_pct |
|:--------------|-------------------:|------------------------:|------------------------:|------------------------:|----------------:|------------------:|---------------------:|--------------:|
| Vijayawada    |              17235 |                   46.26 |                     6.6 |                   165.4 |            4.5  |              6.84 |                14277 |         82.84 |
| Hyderabad     |              48359 |                   46.42 |                     5.7 |                   177.1 |            4.71 |              6.83 |                40026 |         82.77 |
| Visakhapatnam |              22228 |                   46.49 |                     7.8 |                   179.9 |            4.67 |              6.84 |                18454 |         83.02 |

---

## Q08: Delivery by Area and Hour
*(Result count: 50 rows)*

| city          | area           |   order_hour |   total_deliveries |   avg_delivery_time_min |   avg_delay_min |   delay_rate_pct |
|:--------------|:---------------|-------------:|-------------------:|------------------------:|----------------:|-----------------:|
| Visakhapatnam | Gajuwaka       |            1 |                  9 |                    72.3 |            29.7 |             77.8 |
| Hyderabad     | Hitech City    |            1 |                  9 |                    78.2 |            23.2 |             44.4 |
| Visakhapatnam | Dwaraka Nagar  |            0 |                 12 |                    65.3 |            22.2 |             58.3 |
| Visakhapatnam | Seethammadhara |            0 |                 11 |                    65.7 |            21.4 |             63.6 |
| Hyderabad     | LB Nagar       |            5 |                 16 |                    62   |            20.8 |             62.5 |
| Hyderabad     | Dilsukhnagar   |            2 |                  9 |                    65.1 |            20.6 |             55.6 |
| Visakhapatnam | Kommadi        |            1 |                  6 |                    67.8 |            20   |             50   |
| Hyderabad     | Ameerpet       |            4 |                 14 |                    61.1 |            19.9 |             57.1 |
| Vijayawada    | Moghalrajpuram |            4 |                  6 |                    60.6 |            19   |             50   |
| Hyderabad     | Uppal          |            6 |                 29 |                    56.4 |            19   |             58.6 |
| Hyderabad     | Chandanagar    |            1 |                 11 |                    59.8 |            18.8 |             63.6 |
| Vijayawada    | Governorpet    |            6 |                 20 |                    58.3 |            18.5 |             55   |
| Hyderabad     | Uppal          |            3 |                  5 |                    66.3 |            18.3 |             60   |
| Vijayawada    | Auto Nagar     |            2 |                  5 |                    53.2 |            18.3 |             40   |
| Vijayawada    | Governorpet    |            0 |                 12 |                    59.3 |            18.3 |             50   |
| Hyderabad     | Miyapur        |            0 |                 25 |                    62   |            18.2 |             60   |
| Visakhapatnam | MVP Colony     |            5 |                 12 |                    64.4 |            18.2 |             50   |
| Hyderabad     | Kondapur       |            3 |                  6 |                    64.7 |            18.1 |             33.3 |
| Vijayawada    | Benz Circle    |            6 |                 12 |                    61.1 |            18   |             66.7 |
| Hyderabad     | Kondapur       |            1 |                 16 |                    63.4 |            18   |             56.2 |
| Hyderabad     | Ameerpet       |            0 |                 15 |                    60   |            17.6 |             40   |
| Hyderabad     | Dilsukhnagar   |            5 |                 19 |                    53.8 |            17.5 |             57.9 |
| Visakhapatnam | Kommadi        |            5 |                  7 |                    57.5 |            17.5 |             57.1 |
| Visakhapatnam | Jagadamba      |            0 |                 11 |                    55.4 |            17.4 |             45.5 |
| Visakhapatnam | Kommadi        |           23 |                 71 |                    56   |            17.3 |             54.9 |

*... showing top 25 of 50 rows. Full data in `sql/05_Q08_Delivery_by_Area_and_Hour.csv`.*

---

## Q09: Slow Delivery Areas
*(Result count: 35 rows)*

| city       | area           |   total_deliveries |   avg_delivery_time |   avg_delay |   delay_rate_pct |   time_above_city_avg |   area_delay_rank |
|:-----------|:---------------|-------------------:|--------------------:|------------:|-----------------:|----------------------:|------------------:|
| Hyderabad  | Chandanagar    |               3106 |                47.8 |         5.2 |            18.22 |                   1.4 |                 1 |
| Hyderabad  | Miyapur        |               3557 |                47.1 |         4.9 |            17.99 |                   0.7 |                 2 |
| Hyderabad  | Secunderabad   |               2968 |                47.2 |         4.8 |            17.79 |                   0.8 |                 3 |
| Hyderabad  | Jubilee Hills  |               3647 |                46.5 |         4.8 |            17.69 |                   0.1 |                 4 |
| Hyderabad  | Madhapur       |               3002 |                46.4 |         4.8 |            17.52 |                  -0   |                 5 |
| Hyderabad  | Gachibowli     |               2995 |                46.4 |         4.9 |            17.5  |                  -0   |                 6 |
| Hyderabad  | Kondapur       |               3810 |                47   |         4.7 |            17.38 |                   0.6 |                 7 |
| Hyderabad  | Hitech City    |               3322 |                46.2 |         4.7 |            17.22 |                  -0.2 |                 8 |
| Hyderabad  | Uppal          |               2827 |                44.7 |         4.5 |            17.16 |                  -1.7 |                 9 |
| Hyderabad  | Kukatpally     |               3031 |                46.3 |         4.9 |            17.12 |                  -0.1 |                10 |
| Hyderabad  | Dilsukhnagar   |               3208 |                46.3 |         4.7 |            16.96 |                  -0.1 |                11 |
| Hyderabad  | Banjara Hills  |               3298 |                46.2 |         4.4 |            16.65 |                  -0.2 |                12 |
| Hyderabad  | Ameerpet       |               3690 |                45.8 |         4.7 |            16.61 |                  -0.6 |                13 |
| Hyderabad  | Begumpet       |               2885 |                46.5 |         4.2 |            16.5  |                   0.1 |                14 |
| Hyderabad  | LB Nagar       |               3013 |                45.8 |         4.4 |            16.06 |                  -0.7 |                15 |
| Vijayawada | Moghalrajpuram |               1776 |                46.9 |         4.9 |            18.86 |                   0.7 |                 1 |
| Vijayawada | Machavaram     |               2119 |                46.1 |         4.6 |            17.98 |                  -0.1 |                 2 |
| Vijayawada | Governorpet    |               1925 |                46.3 |         4.8 |            17.82 |                   0.1 |                 3 |
| Vijayawada | Kanuru         |               1975 |                47   |         4.6 |            17.37 |                   0.8 |                 4 |
| Vijayawada | MG Road        |               1288 |                44.9 |         4.4 |            17.31 |                  -1.3 |                 5 |
| Vijayawada | Benz Circle    |               1467 |                46.1 |         4.7 |            17.18 |                  -0.1 |                 6 |
| Vijayawada | Gunadala       |               1739 |                46.5 |         4.3 |            16.91 |                   0.3 |                 7 |
| Vijayawada | Auto Nagar     |               1560 |                46.1 |         4.5 |            16.41 |                  -0.1 |                 8 |
| Vijayawada | Patamata       |               1569 |                45.3 |         4   |            15.81 |                  -0.9 |                 9 |
| Vijayawada | Ramavarappadu  |               1817 |                46.8 |         4.2 |            15.58 |                   0.6 |                10 |

*... showing top 25 of 35 rows. Full data in `sql/05_Q09_Slow_Delivery_Areas.csv`.*

---

## Q10: Cancellation Rate by Restaurant
*(Result count: 20 rows)*

|   rank | restaurant_id   | restaurant_name          | city          | cuisine       |   total_orders |   cancelled_orders |   cancellation_rate_pct |
|-------:|:----------------|:-------------------------|:--------------|:--------------|---------------:|-------------------:|------------------------:|
|      1 | R1170           | Golden Fast Food Delight | Hyderabad     | Fast Food     |             27 |                 10 |                   37.04 |
|      2 | R3096           | Grand Desserts Corner    | Visakhapatnam | Desserts      |             20 |                  7 |                   35    |
|      3 | R2828           | Classic Fast Food Eatery | Hyderabad     | Fast Food     |             23 |                  8 |                   34.78 |
|      4 | R2252           | Quick Rolls & Wraps Stop | Vijayawada    | Rolls & Wraps |             21 |                  7 |                   33.33 |
|      5 | R2652           | Authentic Biryani Stop   | Hyderabad     | Biryani       |             21 |                  7 |                   33.33 |
|      6 | R1157           | Authentic Chinese Point  | Hyderabad     | Chinese       |             21 |                  7 |                   33.33 |
|      7 | R0753           | Classic Fast Food Bites  | Visakhapatnam | Fast Food     |             33 |                 11 |                   33.33 |
|      8 | R3157           | Golden Desserts House    | Vijayawada    | Desserts      |             24 |                  8 |                   33.33 |
|      9 | R2972           | Grand Burger Kitchen     | Hyderabad     | Burger        |             28 |                  9 |                   32.14 |
|     10 | R2737           | Golden Fast Food House   | Vijayawada    | Fast Food     |             25 |                  8 |                   32    |
|     11 | R0679           | Local Pizza House        | Vijayawada    | Pizza         |             25 |                  8 |                   32    |
|     12 | R2060           | Home South Indian Stop   | Hyderabad     | South Indian  |             25 |                  8 |                   32    |
|     13 | R3860           | Local Pizza Place        | Vijayawada    | Pizza         |             25 |                  8 |                   32    |
|     14 | R3529           | Local Healthy Place      | Vijayawada    | Healthy       |             22 |                  7 |                   31.82 |
|     15 | R0793           | Home Thali Station       | Hyderabad     | Thali         |             22 |                  7 |                   31.82 |
|     16 | R3150           | Tasty Fast Food Place    | Hyderabad     | Fast Food     |             22 |                  7 |                   31.82 |
|     17 | R3437           | Grand Burger Point       | Hyderabad     | Burger        |             22 |                  7 |                   31.82 |
|     18 | R3649           | Royal Burger Eatery      | Visakhapatnam | Burger        |             29 |                  9 |                   31.03 |
|     19 | R0886           | Spicy Thali Cafe         | Hyderabad     | Thali         |             26 |                  8 |                   30.77 |
|     20 | R3029           | Home South Indian Diner  | Visakhapatnam | South Indian  |             26 |                  8 |                   30.77 |

---

## Q11: Cancellation Reasons
*(Result count: 8 rows)*

| cancellation_reason      |   total_cancellations |   pct_of_total |   avg_order_value_inr |
|:-------------------------|----------------------:|---------------:|----------------------:|
| Restaurant not accepting |                  1578 |          12.96 |                369.82 |
| Long wait time           |                  1570 |          12.89 |                365.28 |
| Payment failed           |                  1550 |          12.73 |                369.59 |
| Duplicate order          |                  1535 |          12.6  |                370.1  |
| No rider available       |                  1507 |          12.37 |                378.9  |
| Address issue            |                  1485 |          12.19 |                376.86 |
| Customer cancelled       |                  1485 |          12.19 |                380.57 |
| Item unavailable         |                  1468 |          12.05 |                372.67 |

---

## Q12: Repeat Customer Rate
*(Result count: 3 rows)*

| city          |   total_customers |   one_time_customers |   repeat_customers |   loyal_customers_5plus |   vip_customers_10plus |   avg_orders_per_customer |   repeat_rate_pct |
|:--------------|------------------:|---------------------:|-------------------:|------------------------:|-----------------------:|--------------------------:|------------------:|
| Visakhapatnam |              4718 |                  665 |               4053 |                    2113 |                    690 |                      5.36 |             85.91 |
| Hyderabad     |             10211 |                 1463 |               8748 |                    4638 |                   1527 |                      5.39 |             85.67 |
| Vijayawada    |              3683 |                  566 |               3117 |                    1599 |                    542 |                      5.34 |             84.63 |

---

## Q13: Customer Segment Revenue
*(Result count: 4 rows)*

| customer_segment       |   customer_count |   segment_revenue_inr |   avg_lifetime_value_inr |   avg_order_value_inr |   pct_of_total_revenue |
|:-----------------------|-----------------:|----------------------:|-------------------------:|----------------------:|-----------------------:|
| 1 - One-time Customer  |             3093 |           1.06853e+06 |                   345.47 |                345.47 |                   3.53 |
| 10+ Orders (Loyal/VIP) |             2121 |           9.90043e+06 |                  4667.81 |                343.61 |                  32.71 |
| 2-3 Orders             |             5808 |           4.90714e+06 |                   844.89 |                344.42 |                  16.21 |
| 4-9 Orders (Regular)   |             7214 |           1.43925e+07 |                  1995.08 |                345.4  |                  47.55 |

---

## Q14: Delivery Time vs Ratings
*(Result count: 6 rows)*

| delay_bucket                  |   feedback_count |   avg_rating |   avg_delay_min |   high_ratings |   low_ratings |   pct_high_rating |   pct_low_rating |
|:------------------------------|-----------------:|-------------:|----------------:|---------------:|--------------:|------------------:|-----------------:|
| Early (<=0 min)               |            29435 |         3.89 |            -2.5 |          21532 |           480 |              73.2 |              1.6 |
| On Time (1-5 min)             |            28813 |         3.82 |             2.5 |          19934 |           602 |              69.2 |              2.1 |
| Slight Delay (6-15 min)       |             3804 |         3.57 |            10.1 |           2059 |           181 |              54.1 |              4.8 |
| Moderate Delay (16-30 min)    |             4257 |         3.2  |            20.9 |           1375 |           605 |              32.3 |             14.2 |
| Significant Delay (31-60 min) |             2981 |         2.39 |            45.1 |            146 |          1654 |               4.9 |             55.5 |
| Severe Delay (>60 min)        |             1012 |         1.97 |            65.1 |              4 |           827 |               0.4 |             81.7 |

---

## Q15: Distance vs Delays
*(Result count: 5 rows)*

| distance_bucket     |   total_deliveries |   avg_delivery_time_min |   avg_delay_min |   delay_rate_pct |   avg_distance_km |
|:--------------------|-------------------:|------------------------:|----------------:|-----------------:|------------------:|
| 0-2 km (Very Close) |               1188 |                    28.4 |             4.8 |            17.76 |              1.7  |
| 2-5 km (Close)      |              29792 |                    35.6 |             4.7 |            17.42 |              3.77 |
| 5-8 km (Medium)     |              31592 |                    44.6 |             4.5 |            16.92 |              6.37 |
| 8-12 km (Far)       |              17794 |                    56.3 |             4.7 |            17.03 |              9.62 |
| 12+ km (Very Far)   |               7456 |                    76.4 |             4.8 |            17.31 |             15.2  |

---

## Q16: Peak Hours
*(Result count: 24 rows)*

|   hour_of_day | time_segment               |   total_orders |   cancelled_orders |   cancellation_rate_pct |   avg_order_value_inr |   pct_of_daily_orders |
|--------------:|:---------------------------|---------------:|-------------------:|------------------------:|----------------------:|----------------------:|
|             0 | Late Night / Early Morning |            562 |                 45 |                    8.01 |                337.53 |                  0.56 |
|             1 | Late Night / Early Morning |            341 |                 33 |                    9.68 |                357.7  |                  0.34 |
|             2 | Late Night / Early Morning |            212 |                 23 |                   10.85 |                357.02 |                  0.21 |
|             3 | Late Night / Early Morning |            220 |                 22 |                   10    |                343.43 |                  0.22 |
|             4 | Late Night / Early Morning |            349 |                 38 |                   10.89 |                354.28 |                  0.35 |
|             5 | Late Night / Early Morning |            593 |                 60 |                   10.12 |                329.94 |                  0.59 |
|             6 | Morning (6-11)             |            944 |                104 |                   11.02 |                337.68 |                  0.94 |
|             7 | Morning (6-11)             |           1742 |                168 |                    9.64 |                341.6  |                  1.74 |
|             8 | Morning (6-11)             |           2315 |                237 |                   10.24 |                341.68 |                  2.32 |
|             9 | Morning (6-11)             |           2787 |                280 |                   10.05 |                340.23 |                  2.79 |
|            10 | Morning (6-11)             |           3506 |                358 |                   10.21 |                343.88 |                  3.51 |
|            11 | Morning (6-11)             |           5100 |                539 |                   10.57 |                345.04 |                  5.1  |
|            12 | Lunch Peak (12-14)         |           8027 |                789 |                    9.83 |                343.97 |                  8.03 |
|            13 | Lunch Peak (12-14)         |           8498 |                851 |                   10.01 |                343.01 |                  8.5  |
|            14 | Lunch Peak (12-14)         |           5826 |                562 |                    9.65 |                343.15 |                  5.83 |
|            15 | Afternoon (15-17)          |           3989 |                405 |                   10.15 |                347.04 |                  3.99 |
|            16 | Afternoon (15-17)          |           3333 |                350 |                   10.5  |                342.48 |                  3.33 |
|            17 | Afternoon (15-17)          |           5022 |                500 |                    9.96 |                344.53 |                  5.02 |
|            18 | Dinner Peak (18-22)        |           7457 |                716 |                    9.6  |                346.37 |                  7.46 |
|            19 | Dinner Peak (18-22)        |           9717 |               1561 |                   16.06 |                343.61 |                  9.72 |
|            20 | Dinner Peak (18-22)        |          10271 |               1645 |                   16.02 |                346.81 |                 10.27 |
|            21 | Dinner Peak (18-22)        |           9069 |               1464 |                   16.14 |                345.28 |                  9.07 |
|            22 | Dinner Peak (18-22)        |           6696 |               1053 |                   15.73 |                346.3  |                  6.7  |
|            23 | Late Night / Early Morning |           3424 |                375 |                   10.95 |                344.92 |                  3.42 |

---

## Q17: Poor Performing Restaurants
*(Result count: 30 rows)*

| restaurant_id   | restaurant_name               | city          | cuisine      |   total_orders |   avg_rating |   cancel_rate_pct |   complaint_rate_pct |   avg_delivery_min |   total_refunds_inr |   poor_perf_flags | performance_status     |
|:----------------|:------------------------------|:--------------|:-------------|---------------:|-------------:|------------------:|---------------------:|-------------------:|--------------------:|------------------:|:-----------------------|
| R1995           | Fresh South Indian Diner      | Visakhapatnam | South Indian |             20 |         2    |             20    |                70    |              32.53 |              975.26 |                 3 | CRITICAL - All 3 flags |
| R2398           | Quick Chinese Delight         | Hyderabad     | Chinese      |             26 |         2.12 |             26.92 |                65.38 |              48.14 |             1043.5  |                 3 | CRITICAL - All 3 flags |
| R1285           | Authentic South Indian Corner | Hyderabad     | South Indian |             26 |         2.24 |             19.23 |                65.38 |              47.5  |              787.63 |                 3 | CRITICAL - All 3 flags |
| R2969           | Authentic South Indian Stop   | Vijayawada    | South Indian |             23 |         2.31 |             26.09 |                56.52 |              41.61 |              490.44 |                 3 | CRITICAL - All 3 flags |
| R2512           | Classic South Indian Station  | Vijayawada    | South Indian |             21 |         2.36 |             23.81 |                47.62 |              49.11 |              570.77 |                 3 | CRITICAL - All 3 flags |
| R3811           | Tasty South Indian Delight    | Visakhapatnam | South Indian |             21 |         2.43 |             19.05 |                61.9  |              56.64 |              617.03 |                 3 | CRITICAL - All 3 flags |
| R0789           | Classic Biryani Express       | Hyderabad     | Biryani      |             26 |         2.47 |             23.08 |                57.69 |              66.96 |              705.81 |                 3 | CRITICAL - All 3 flags |
| R1170           | Golden Fast Food Delight      | Hyderabad     | Fast Food    |             27 |         2.47 |             37.04 |                55.56 |              36.69 |              682.69 |                 3 | CRITICAL - All 3 flags |
| R0388           | Local Burger Place            | Hyderabad     | Burger       |             26 |         2.47 |             15.38 |                65.38 |              48.92 |              848.54 |                 3 | CRITICAL - All 3 flags |
| R2600           | Grand Thali Express           | Hyderabad     | Thali        |             25 |         2.47 |             24    |                68    |              47.75 |              832.49 |                 3 | CRITICAL - All 3 flags |
| R3675           | Home Chinese Express          | Visakhapatnam | Chinese      |             29 |         2.5  |             27.59 |                41.38 |              50.09 |              399.72 |                 3 | CRITICAL - All 3 flags |
| R1407           | Premium Chinese Bites         | Vijayawada    | Chinese      |             33 |         2.52 |             15.15 |                60.61 |              51.63 |              664.33 |                 3 | CRITICAL - All 3 flags |
| R0449           | Home Burger Eatery            | Hyderabad     | Burger       |             29 |         2.53 |             17.24 |                51.72 |              46.18 |              700.9  |                 3 | CRITICAL - All 3 flags |
| R1571           | Urban Biryani Cafe            | Visakhapatnam | Biryani      |             28 |         2.53 |             21.43 |                53.57 |              61.48 |              335.19 |                 3 | CRITICAL - All 3 flags |
| R0649           | Classic Burger Hub            | Visakhapatnam | Burger       |             25 |         2.56 |             16    |                64    |              43.06 |              428.57 |                 3 | CRITICAL - All 3 flags |
| R2411           | Spicy Continental Hub         | Visakhapatnam | Continental  |             27 |         2.59 |             22.22 |                55.56 |              43.96 |              841.63 |                 3 | CRITICAL - All 3 flags |
| R3635           | Royal Fast Food Cafe          | Hyderabad     | Fast Food    |             22 |         2.62 |             27.27 |                40.91 |              53.45 |              720.28 |                 3 | CRITICAL - All 3 flags |
| R2389           | Tasty Desserts Eatery         | Visakhapatnam | Desserts     |             27 |         2.62 |             18.52 |                59.26 |              56.64 |              524.28 |                 3 | CRITICAL - All 3 flags |
| R3245           | Quick South Indian Diner      | Visakhapatnam | South Indian |             29 |         2.63 |             20.69 |                65.52 |              48.08 |              676.13 |                 3 | CRITICAL - All 3 flags |
| R3695           | Authentic Pizza Place         | Hyderabad     | Pizza        |             31 |         2.65 |             19.35 |                54.84 |              50.18 |              407.76 |                 3 | CRITICAL - All 3 flags |
| R0207           | Home Pizza Point              | Hyderabad     | Pizza        |             34 |         2.65 |             17.65 |                55.88 |              61.35 |              706.8  |                 3 | CRITICAL - All 3 flags |
| R2809           | Spicy Continental House       | Hyderabad     | Continental  |             26 |         2.67 |             26.92 |                57.69 |              52.95 |              204.24 |                 3 | CRITICAL - All 3 flags |
| R2937           | Quick North Indian House      | Visakhapatnam | North Indian |             22 |         2.67 |             22.73 |                68.18 |              48.06 |              189.16 |                 3 | CRITICAL - All 3 flags |
| R3134           | Royal Desserts Cafe           | Hyderabad     | Desserts     |             31 |         2.67 |             16.13 |                64.52 |              37.88 |              837.95 |                 3 | CRITICAL - All 3 flags |
| R3281           | Quick Continental Station     | Hyderabad     | Continental  |             21 |         2.67 |             23.81 |                66.67 |              49.66 |              428.25 |                 3 | CRITICAL - All 3 flags |

*... showing top 25 of 30 rows. Full data in `sql/05_Q17_Poor_Performing_Restaurants.csv`.*

---

## Q18: Cuisine Performance
*(Result count: 13 rows)*

| cuisine       |   restaurant_count |   total_orders |   completed_orders |   total_revenue_inr |   avg_order_value_inr |   avg_customer_rating |   avg_prep_time_min |   cancellation_rate_pct |
|:--------------|-------------------:|---------------:|-------------------:|--------------------:|----------------------:|----------------------:|--------------------:|------------------------:|
| Thali         |                362 |           9032 |               7979 |         2.72586e+06 |                341.63 |                  3.68 |               19.51 |                   11.66 |
| Continental   |                336 |           8430 |               7373 |         2.5388e+06  |                344.34 |                  3.69 |               22.01 |                   12.54 |
| Healthy       |                329 |           8291 |               7303 |         2.53251e+06 |                346.78 |                  3.71 |               15.13 |                   11.92 |
| Biryani       |                326 |           8123 |               7116 |         2.44997e+06 |                344.29 |                  3.73 |               24.67 |                   12.4  |
| North Indian  |                308 |           7780 |               6807 |         2.33608e+06 |                343.19 |                  3.73 |               20.42 |                   12.51 |
| Chinese       |                297 |           7575 |               6701 |         2.31554e+06 |                345.55 |                  3.64 |               17.81 |                   11.54 |
| Burger        |                301 |           7615 |               6639 |         2.28832e+06 |                344.68 |                  3.73 |               11.84 |                   12.82 |
| Seafood       |                310 |           7511 |               6608 |         2.27987e+06 |                345.02 |                  3.72 |               24.94 |                   12.02 |
| Rolls & Wraps |                291 |           7302 |               6458 |         2.2288e+06  |                345.12 |                  3.72 |               12.36 |                   11.56 |
| Pizza         |                285 |           7121 |               6286 |         2.18937e+06 |                348.29 |                  3.73 |               19.79 |                   11.73 |
| Fast Food     |                293 |           7293 |               6397 |         2.1868e+06  |                341.85 |                  3.74 |                9.92 |                   12.29 |
| Desserts      |                287 |           7061 |               6168 |         2.13664e+06 |                346.41 |                  3.69 |               10.14 |                   12.65 |
| South Indian  |                275 |           6866 |               5987 |         2.0601e+06  |                344.1  |                  3.71 |               15.09 |                   12.8  |

---

## Q19: Refunds by City
*(Result count: 3 rows)*

| city          |   feedback_count |   refund_issued_count |   total_refund_inr |   avg_refund_when_issued_inr |   refund_rate_pct |
|:--------------|-----------------:|----------------------:|-------------------:|-----------------------------:|------------------:|
| Hyderabad     |            38794 |                  2390 |           196001   |                        82.01 |              6.16 |
| Visakhapatnam |            17752 |                  1107 |            84153.6 |                        76.02 |              6.24 |
| Vijayawada    |            13756 |                   851 |            60593.2 |                        71.2  |              6.19 |

---

## Q20: Restaurant Performance Report
*(Result count: 100 rows)*

| restaurant_id   | restaurant_name             | cuisine       | city          | area           |   total_orders |   completed_orders |   cancel_rate_pct |   total_revenue_inr |   avg_del_min |   on_time_pct |   avg_rating |   complaint_rate_pct |   total_refund_inr | performance_tier   |
|:----------------|:----------------------------|:--------------|:--------------|:---------------|---------------:|-------------------:|------------------:|--------------------:|--------------:|--------------:|-------------:|---------------------:|-------------------:|:-------------------|
| R1115           | Local Healthy Bites         | Healthy       | Visakhapatnam | Seethammadhara |             45 |                 42 |              6.67 |             16025.5 |         47.45 |         80    |         3.34 |                37.78 |             120.41 | NEEDS ATTENTION    |
| R3560           | Star Biryani Corner         | Biryani       | Hyderabad     | Dilsukhnagar   |             44 |                 41 |              6.82 |             15813   |         46.8  |         84.09 |         3.69 |                20.45 |              55.07 | AVERAGE            |
| R0156           | Royal Thali Station         | Thali         | Hyderabad     | Secunderabad   |             39 |                 37 |              5.13 |             14338   |         46.2  |         69.23 |         3.37 |                38.46 |             455.6  | NEEDS ATTENTION    |
| R3376           | Local North Indian Express  | North Indian  | Visakhapatnam | Rushikonda     |             33 |                 30 |              9.09 |             14235.2 |         45.26 |         75.76 |         4.54 |                 9.09 |               0    | AVERAGE            |
| R3988           | Spicy Continental Point     | Continental   | Hyderabad     | LB Nagar       |             31 |                 30 |              3.23 |             14089.9 |         63.11 |         70.97 |         3.84 |                29.03 |               0    | NEEDS ATTENTION    |
| R3353           | Fresh Fast Food Express     | Fast Food     | Vijayawada    | Moghalrajpuram |             34 |                 32 |              5.88 |             13692.8 |         34.67 |         67.65 |         3.96 |                14.71 |               0    | AVERAGE            |
| R1047           | Classic Healthy Express     | Healthy       | Hyderabad     | Banjara Hills  |             40 |                 35 |             12.5  |             13517.4 |         47.57 |         75    |         3.04 |                57.5  |             475.02 | NEEDS ATTENTION    |
| R2823           | Spicy Rolls & Wraps Point   | Rolls & Wraps | Visakhapatnam | MVP Colony     |             33 |                 33 |              0    |             13400.3 |         45.35 |         87.88 |         3.79 |                27.27 |             104.88 | NEEDS ATTENTION    |
| R3967           | Grand Burger Place          | Burger        | Hyderabad     | Madhapur       |             36 |                 32 |             11.11 |             13378.3 |         46.61 |         61.11 |         4.41 |                11.11 |               0    | AVERAGE            |
| R1600           | Grand Rolls & Wraps Kitchen | Rolls & Wraps | Vijayawada    | Benz Circle    |             32 |                 31 |              3.12 |             13321   |         42    |         78.12 |         3.6  |                28.12 |             276.56 | NEEDS ATTENTION    |
| R1647           | Quick South Indian Station  | South Indian  | Hyderabad     | Kukatpally     |             39 |                 37 |              5.13 |             13194.5 |         44.09 |         84.62 |         2.56 |                82.05 |            1044.79 | NEEDS ATTENTION    |
| R1483           | Quick Pizza Delight         | Pizza         | Hyderabad     | Madhapur       |             33 |                 32 |              3.03 |             13161.7 |         54.07 |         63.64 |         3.92 |                12.12 |               1.65 | AVERAGE            |
| R3736           | Premium Desserts Stop       | Desserts      | Hyderabad     | Kukatpally     |             38 |                 34 |             10.53 |             13137.9 |         41.65 |         68.42 |         3.04 |                47.37 |            1266.61 | NEEDS ATTENTION    |
| R0956           | Royal Thali Bites           | Thali         | Hyderabad     | Kondapur       |             37 |                 34 |              8.11 |             13137.1 |         41.57 |         83.78 |         3.85 |                16.22 |               0    | AVERAGE            |
| R1296           | Classic Rolls & Wraps Hub   | Rolls & Wraps | Hyderabad     | Miyapur        |             40 |                 39 |              2.5  |             13107   |         40.98 |         80    |         3.91 |                15    |             149.42 | AVERAGE            |
| R3688           | Authentic Fast Food House   | Fast Food     | Hyderabad     | Gachibowli     |             42 |                 39 |              7.14 |             13104.6 |         39.31 |         71.43 |         3.68 |                21.43 |              63.06 | AVERAGE            |
| R2039           | Star Thali Kitchen          | Thali         | Hyderabad     | Hitech City    |             33 |                 30 |              9.09 |             12962.4 |         62.68 |         69.7  |         3.52 |                21.21 |             574.86 | AVERAGE            |
| R1178           | Star Desserts Corner        | Desserts      | Hyderabad     | Dilsukhnagar   |             36 |                 34 |              5.56 |             12936.7 |         37.12 |         80.56 |         3.79 |                16.67 |             160.19 | AVERAGE            |
| R3122           | Classic Thali Bites         | Thali         | Hyderabad     | Jubilee Hills  |             35 |                 32 |              8.57 |             12917.8 |         48.28 |         74.29 |         2.92 |                65.71 |             346.76 | NEEDS ATTENTION    |
| R1243           | Fresh Seafood Stop          | Seafood       | Visakhapatnam | Maddilapalem   |             34 |                 29 |             14.71 |             12805.9 |         50.37 |         70.59 |         3.77 |                23.53 |               0    | AVERAGE            |
| R2341           | Classic Chinese Express     | Chinese       | Visakhapatnam | Seethammadhara |             33 |                 31 |              6.06 |             12662.2 |         38.13 |         81.82 |         4.28 |                 3.03 |               0    | TOP PERFORMER      |
| R0613           | Fresh South Indian Eatery   | South Indian  | Visakhapatnam | MVP Colony     |             33 |                 30 |              9.09 |             12622.8 |         47.35 |         75.76 |         3.78 |                18.18 |               0    | AVERAGE            |
| R3545           | Spicy Burger Stop           | Burger        | Vijayawada    | Gunadala       |             41 |                 37 |              9.76 |             12476.3 |         36.78 |         75.61 |         3.31 |                41.46 |             229.22 | NEEDS ATTENTION    |
| R1592           | Grand South Indian Cafe     | South Indian  | Vijayawada    | Gunadala       |             41 |                 36 |             12.2  |             12449.9 |         58.32 |         68.29 |         3.41 |                36.59 |              46.11 | NEEDS ATTENTION    |
| R1174           | Authentic Thali Kitchen     | Thali         | Hyderabad     | Jubilee Hills  |             37 |                 35 |              5.41 |             12447   |         43.47 |         67.57 |         4.21 |                21.62 |              26.19 | AVERAGE            |

*... showing top 25 of 100 rows. Full data in `sql/05_Q20_Restaurant_Performance_Report.csv`.*

---
