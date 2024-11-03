# recommendation-system

Final year project

Objective: Build a machine learning-powered movie recommendation system that suggests movies based on user interactions, such as moods (e.g., typing "happy" or "sad"). The system leverages Django for user interaction and machine learning algorithms to recommend personalized movies.

Key Features: User Registration and Profile Management: Users will sign up and create a profile. During registration, users can select their favorite genres and moods (optional), which helps the model in initial movie recommendations. User profiles will store viewing history, liked/disliked movies, and other interactions. Mood-Based Movie Recommendation: The system allows users to input their current mood (e.g., "happy" or "sad"). The machine learning model will analyze this mood input along with the user’s interaction history (watchlist, ratings, preferences) to recommend movies that fit the mood. User Interactions for Recommendations: The recommendation engine will learn from user interactions (e.g., ratings, likes, dislikes, mood-based requests) to improve predictions over time. Each time a user interacts with a movie (e.g., watches, rates, or skips), the system updates its recommendations.

Core Components: a. Django for User Interaction: User Authentication: Users can register, log in, and manage their profiles. Profile Management: Users can update their preferences (genres, favorite actors, etc.). Movie Search and Filtering: Users can search for movies and filter based on genres or mood. Mood Input: A simple input field for users to enter their current mood (happy, sad, etc.), triggering the recommendation model to provide relevant suggestions. b. Machine Learning for Recommendations: Collaborative Filtering/Content-Based Filtering: Collaborative Filtering will recommend movies based on similarities between users. Content-Based Filtering will recommend movies based on movie attributes (e.g., genres, actors, ratings). Mood Classification: The system will categorize movies based on mood types (e.g., "happy" movies may include comedies, feel-good dramas, etc.). When users type "happy" or "sad," the recommendation engine will use this as a feature for filtering relevant movies. c. User Interaction Logging: Every interaction (rating a movie, liking/disliking, typing mood) will be logged and used to refine future recommendations. The more users interact, the better the system will learn their preferences.

Steps in the Project: a. Data Collection and Preparation: Use the MovieLens dataset (or another dataset) to train the recommendation model. Data preprocessing: Clean the data, remove duplicates, and normalize movie features like genres, ratings, etc. b. Model Training: Train models using collaborative filtering or content-based filtering to predict movies based on user preferences. Integrate a basic Natural Language Processing (NLP) component to categorize movies based on moods (e.g., if a user types "happy", movies with high happiness ratings are recommended). c. Django Integration: Set up user authentication, profile management, and interactive elements (e.g., input fields for moods). Use Django’s ORM to interact with the recommendation system and serve personalized movie lists. d. Testing and Evaluation: Test the system with different users to evaluate how well the recommendation model responds to user moods and preferences. Evaluate model performance using metrics like Root Mean Square Error (RMSE) for collaborative filtering models.

Challenges and Considerations: Mood Classification: Defining clear categories for mood-based movie recommendations might be challenging, as moods can be subjective. User Behavior: Handling cold-start problems (e.g., when the system doesn't have enough data on a new user) is essential. You may need to implement fallback strategies like genre-based recommendations. Scalability: Consider how the system scales as the user base grows, both in terms of model performance and database handling.

Future Enhancements: Multi-modal Input: Allow users to specify more than just mood (e.g., "I feel happy and want a short movie"). Integration of Ratings: As users watch and rate more movies, the system will fine-tune recommendations. Hybrid Models: Combine collaborative filtering and content-based filtering for more accurate recommendations. This project will showcase your ability to blend machine learning techniques with user interaction systems, solving real-world problems like personalized movie recommendations based on mood and interaction data.

Movie Genre Preferences: During signup or in their profile, users can select their favorite genres (e.g., action, comedy, drama). The recommendation system can prioritize movies from these genres. Example Input:

"Select your favorite genres: Action, Comedy, Sci-Fi, Drama" 2. Favorite Actors/Directors: Users can specify their favorite actors or directors. Movies featuring these actors/directors can be prioritized in recommendations. Example Input:

"Select your favorite actors: Leonardo DiCaprio, Emma Stone" "Select your favorite directors: Christopher Nolan, Quentin Tarantino" 3. Rating-Based Recommendations: Ask users to rate a few movies they’ve seen during signup. The model can then find movies with similar ratings or preferences from other users who rated those movies similarly. Example Input:

"Rate these movies on a scale of 1 to 5" 4. Time Availability (Short vs. Long Movies): Users can specify how much time they have to watch a movie (e.g., less than 2 hours, more than 2 hours). Based on this, the model can recommend shorter or longer movies. Example Input:

"How much time do you have to watch a movie? Less than 2 hours / More than 2 hours" 5. Previous Movie Likes/Dislikes: Use data from the user’s interaction history, such as movies they liked or disliked in the past, to suggest similar or different kinds of movies. Example Input:

"Select movies you’ve liked or disliked in the past" 6. Trending or Popular Movies: Allow users to select if they prefer watching trending, newly released, or classic movies. This can trigger recommendations based on the latest popular or timeless films. Example Input:

"Do you prefer trending or classic movies?" 7. Recommended by Friends: If you have a social feature, users can get movie recommendations based on what their friends or people with similar tastes are watching. Example Input:

"Get recommendations based on your friends' favorites" 8. Movie Themes or Keywords: Instead of using broad moods, users can input themes or keywords that interest them (e.g., "adventure", "romance", "space"). Example Input:

"What type of movie are you in the mood for? Action, Romance, Adventure" Simplified Recommendation Triggers: Here’s how these simplified inputs can be mapped into triggers for your recommendation model:

Genre preferences → Suggest movies from similar genres. Favorite actors/directors → Suggest movies featuring those actors or directors. Rating-based suggestions → Suggest movies based on ratings or movies liked/disliked. Time availability → Suggest shorter or longer movies based on available time. Trending/classic movies → Suggest popular movies based on user preference. Summary of Possible Inputs: Genre preferences Favorite actors or directors Movie ratings Time availability Movie likes/dislikes Trending or classic preference Keywords or themes (e.g., "action", "romance")

Features:

Movie Rating System
Movie Watchlist
Favorite Genre(s) Selection
Movie Tags or Keywords Feature: Allow users to tag movies with keywords or select pre-defined tags (e.g., "funny," "exciting," "dark").
Movie Recommendations Based on Mood
Surveys for Initial Preferences
User Reviews and Comments
Recommendation Feedback
How Tags Work in the System: Tagging Functionality: Tags are typically used to categorize or label content. In this context, users can tag movies based on personal preferences, opinions, or attributes of the movie. These tags serve as an additional data layer to enhance personalization.

Feature Extraction for Machine Learning:

Tags can be treated as features for matrix factorization or collaborative filtering systems. For example, if many users tag a movie as “music” or “comedy,” this information can enhance the recommendation process by clustering movies with similar tags. Collaborative Filtering: Users with similar tagging behavior might receive similar recommendations. Matrix Factorization: Tags can be used as an additional feature to decompose user-movie interactions, which improves the latent feature space in the model. K-Means: Tags help in clustering movies or users based on common tags. Movies with similar tags will cluster together, helping recommend similar content to users. User Interaction:

Tagging Movies: Users can assign tags to movies they've watched. Browsing by Tags: Users may receive recommendations based on tags they've frequently interacted with or assigned to movies. Tag Influence on Recommendations: Tags help refine the recommendation system by improving the content-based filtering aspect of the system.

Use Links to Group Related Movies When creating collaborative filtering models, the links (e.g., sequels, prequels, or other related relationships) between movies can provide a basis for item similarity beyond user interactions. These relationships can be used in the following ways:

Enhancing Similarity Scores: When calculating the similarity between two movies (for example, using cosine similarity), you can adjust the similarity score between linked movies to be higher. For example, if two movies are linked as sequels, increase their similarity score.

Implicit User Preferences: If a user interacts with one movie in a linked set, you can use that information to recommend related movies from the same set. For example, if a user watches Movie 1 (with movieId 1), you might prioritize recommending its sequel (with movieId 2).

Metadata for Collaborative Filtering: When building your feature matrix for collaborative filtering, include information about the links as an additional feature. This will allow the model to understand connections between movies that users haven't interacted with yet.

Incorporate Linked Movies in Your Test You can add a test to ensure that your Link model works as expected. For example, if two movies are linked, the system should be able to retrieve the linked movie. Here is an example of how you might enhance your test_create_links function:

Resource Reference

Dataset Obtained from:  
F.Maxwell Harper And Joseph A. Konstan. 2015. The Movielens Dataset: History And Context. AMC Transactions on interactive intelligent systems (Tiis) 5, 4: 19:1-19:19 https://doi.org/10.1145/2827872

Literature Review: 
Khurana, A, Yadav, K., & Singh, R. (2021). Machine Learning model for movie recommendation system. International Journal of Engineering Research and Technology(IJERT),9(4). Retrieved from https://d1wqtxts1xzle7.cloudfront.net/87052435/machine-learning-model-for-movie-recommendation-system-IJERTV9IS040741-libre.pdf
![image](https://github.com/user-attachments/assets/f22130f2-59d0-4de0-abd3-535f366cca86)
