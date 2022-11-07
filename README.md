# DSC x Peak Datathon 2022
### Team Skynet: Diego Lopez, Alexa Tartaglia, Nghia Nim


**Recommendation System: The Machine Learning Challenge**
Goal: To enhance the shopping experience of customers, product recommenders are often used

-   They take transactional, user, and product data to provide personalised recommendations
-   These allow customers to be targeted with the products that they are most likely to purchase, increasing sales for the retailer

During this challenge, you will construct a product recommender

-   You will generate products that you think should be recommended to a list of customers based on the data available
-   You will then report your findings back, imagining that you are a data scientist presenting to a retailer that has hired you to do this work
-   This challenge will require great technical and communication skills, with each group constructing a recommender and also explaining what you have done to a non-technical audience

### The dataset

The dataset for the challenge can be found [here](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/).
 
## Product Recommender System

We implemented [this paper](https://arxiv.org/pdf/1507.08439.pdf) for our Product Recommender System.

> Three factors conspire to make recommendations challenging for us. Firstly, our system contains a very large number of items. This makes our data very sparse. Secondly, we deal in fashion: often, the most relevant items are those from newly released collections, allowing us only a short window to gather data and provide effective recommendations. Finally, a large proportion of our users are firsttime visitors: we would like to present them with compelling recommendations even with little data. This combination of user and item cold-start makes both pure collaborative and content-based methods unsuitable for us.

To solve this problem, We used a hybrid content-collaborative model, called LightFM which takes into account all three of the above factors. We developed an API using Flask to give recommendation based on a customer's id

## Demo
