# Loyalty Lines

The European Parliament is the heart of politics within the European Union. Our application seeks to provide insight into the inter-party politics and dynamics between Members of the European Parliament (MEPs) and their parties through data visualizations, recommendations, and predictions. With our app, we hope to streamline MEP data by providing exploratory tools for our three user personas: a party leader, a political journalist, and a citizen. All of our app's features use real data to allow for real insights.

As a Party Leader, a user can receive recommendations for which MEPs they should recruit to their party, how aligned a party or multiple parties will be on certain types of votes, and create an MEP watchlist for MEPs of interest based on the results of the recommender model.

As a Political Journalist, a user can track how party loyalty levels have changed over time and compare two MEPs side by side.

As a Citizen, a user can learn about individual MEPs and learn which countries have MEPs whose priorities are aligned with theirs.


## Project Initialization 
1. Clone main branch of repository 
2. create .env file from template, choosing a good password
3. run ```docker compose up```
4. Navigate to http://localhost:8501/ to view the application!

## Using the application
Users can act as different personas and explore the features for each one. To log in, select a user from the dropdown menu of your desired persona and click the log in button.

Then, you can navigate to the different pages of the application using the buttons that appear on your user homepage or by using the sidebar. To return to the main homepage, click logout at the bottom of the sidebar.

## Team Members and Major Contributions
Alex Angione - data model (SQL DDL files, local and global ER diagrams) and API routes

Sienna Boos - logistic regression model, dissent over time page

Trayna Bui - watchlist, citizen country matching page

Emily Moy - cosine similarity recommender model


## Blog

Want to see a milestone by milestone view of our progress? 

Visit our Blog! --> [Blog](https://github.com/alexangione419/BelgianBloggers)!

