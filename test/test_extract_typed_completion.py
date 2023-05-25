import jiggybase
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field, ValidationError, validator
from time import time

jb = jiggybase.JiggyBase()

gpt3_times =0 
gpt4_times = 0
count  = 0




# Define the pydantic model
class BookInformation(BaseModel):
    title: str = Field(description="The title of the book")
    author: str = Field(description="The name of the book's author")
    publication_year: Optional[int] = Field(description="The publication year of the book")
    genre: Optional[str] = Field(description="The genre of the book")
    characters: Optional[List[str]] = Field(description="A list of the main characters in the book")
    summary: Optional[str] = Field(min_length=10, description="A brief summary of the book's plot")

# Input unstructured text
unstructured_text = """
Pride and Prejudice is a novel by Jane Austen, published in 1813.
This classic novel follows the story of Elizabeth Bennet, the protagonist, as she navigates issues of manners, morality, education, and marriage in the society of the landed gentry of early 19th-century England.
The story revolves primarily around Elizabeth and her relationship with the haughty yet enigmatic Mr. Darcy.
The book is set in rural England, and it is notable for its wit and humor as well as its commentary on class distinctions, social norms, and values.
Some of the main characters in the novel include Elizabeth Bennet, Mr. Darcy, Jane Bennet, Mr. Bingley, Lydia Bennet, and Mr. Wickham.
Pride and Prejudice is considered a classic work of English literature and has been adapted numerous times for television, film, and stage.
It is often categorized as a romantic novel, but it also has elements of satire and social commentary.
"""

t0 = time()
model3 = jb.extract_typed_completion(unstructured_text, BookInformation, temperature=0, model='gpt-3.5-turbo')
gpt3_times += time() - t0
print(model3)

t0 = time()
model4 = jb.extract_typed_completion(unstructured_text, BookInformation, temperature=0, model='gpt-4')
gpt4_times += time() - t0
print(model4)
count += 1





class DocumentMetadata(BaseModel):
    title      : Optional[str] = Field(description='The title of the content')
    author     : Optional[str] = Field(description='The author of the content')
    created_at : Optional[str] = Field(description='The date in the format YYYY-MM-DD that the content was created if it appears in the content')
    language   : str           = Field(description='The 2 character ISO 639-1 language code of the primary language of the content')


unstructured_text = """Updated 24th March 2023
Generative AI - Chapter 1: Establishing the Investment Framework
BlackLake Equity Research
The advent of cloud computing paved the way for new investment opportunities by facilitating the provision of software as a service. Generative AI takes this a step further, offering additional tools to boost end-user productivity. While traditional AI has proven useful in predicting outcomes, Generative AI specializes in creating content such as text, video, images, or computer code - a feat previously unachievable. Large Language Models (LLMs) play a crucial role as enablers of GAI, displaying an unprecedented level of expertise and intelligence. AI holds the potential to give rise to new enterprises and furnish existing players with fresh growth opportunities by greatly enhancing end-user productivity."""



t0 = time()
model3 = jb.extract_typed_completion(unstructured_text, DocumentMetadata, temperature=0, model='gpt-3.5-turbo')
gpt3_times += time() - t0
print(model3)

t0 = time()
model4 = jb.extract_typed_completion(unstructured_text, DocumentMetadata, temperature=0, model='gpt-4')
gpt4_times += time() - t0
print(model4)
count += 1



# Define the pydantic models
class Course(BaseModel):
    title: str = Field(description="The title of the course")
    instructor: str = Field(description="The name of the course's instructor")
    duration_hours: Optional[int] = Field(description="The duration of the course in hours")

class Curriculum(BaseModel):
    curriculum_title: str = Field(description="The title of the curriculum")
    description: Optional[str] = Field(description="A brief description of the curriculum")
    courses: List[Course] = Field(description="A list of the courses included in the curriculum")

# Input unstructured text
unstructured_text = """
The Data Science Bootcamp is a comprehensive curriculum designed to provide students with the fundamental knowledge and practical skills required for a career in data science.
The bootcamp includes the following four courses:

1. Introduction to Python: This course, taught by John Doe, covers the basics of the Python programming language and its applications in data science. It lasts for 20 hours.

2. Data Wrangling and Visualization: Led by Jane Smith, this course teaches students how to clean, manipulate, and visualize data using popular Python libraries like pandas and Matplotlib. The course duration is 30 hours.

3. Machine Learning Foundations: In this 40-hour course, instructor Michael Brown introduces the core concepts and algorithms of machine learning, including supervised and unsupervised learning techniques.

4. Advanced Topics in Data Science: Taught by Sarah Johnson and lasting 35 hours, this course explores advanced data science techniques such as deep learning, natural language processing, and time series analysis.
"""

t0 = time()
model3 = jb.extract_typed_completion(unstructured_text, Curriculum, temperature=0, model='gpt-3.5-turbo')
gpt3_times += time() - t0
print(model3)

t0 = time()
model4 = jb.extract_typed_completion(unstructured_text, Curriculum, temperature=0, model='gpt-4')
gpt4_times += time() - t0
print(model4)
count += 1




# Define the pydantic model
class Event(BaseModel):
    event_name: str = Field(description="The name of the event")
    start_date: date = Field(description="The start date of the event")
    end_date: date = Field(description="The end date of the event")

    @validator('end_date')
    def start_date_must_be_prior_to_end_date(cls, end_date, values):
        start_date = values.get('start_date')
        if start_date and end_date <= start_date:
            raise ValidationError(f"End date ({end_date}) must be after start date ({start_date})")
        return end_date

class EventList(BaseModel):
    events: List[Event] = Field(description="A list of events")

# Input unstructured text
unstructured_text = """
Calendar Update
Tuesday, April 27, 2023
We have a series of exciting events happening over the next few weeks!

1. Next Monday, the Annual AI Conference will kick off, ending on Wednesday. The event will focus on the latest advancements in artificial intelligence and machine learning, with discussions led by industry experts.

2. In two weeks, the three-day Startup Showcase will take place, where new tech startups will demonstrate their innovative products and services. The event aims to foster collaboration and investment opportunities.

3. The following week, we are hosting a Blockchain Summit, running from Tuesday to Thursday. The summit will explore the potential applications of blockchain technology across various industries, featuring engaging panel discussions and presentations.

4. Finally, at the end of the month, a four-day Virtual Reality Festival will commence. This event celebrates the rapid progress of virtual and augmented reality technologies, with immersive exhibits and experiences available for all attendees.

Make sure to mark your calendars for these thrilling events and seize the opportunity to learn more about the ever-evolving world of technology!
"""

t0 = time()

model3 = jb.extract_typed_completion(unstructured_text, EventList, temperature=0, model='gpt-3.5-turbo')
gpt3_times += time() - t0
print(model3)

t0 = time()
model4 = jb.extract_typed_completion(unstructured_text, EventList, temperature=0, model='gpt-4')
gpt4_times += time() - t0
print(model4)
count += 1




# Define the pydantic model
class MovieInformation(BaseModel):
    title: str = Field(description="The title of the movie")
    director: str = Field(description="The name of the movie's director")
    release_year: Optional[int] = Field(description="The release year of the movie")
    cast: Optional[List[str]] = Field(description="A list of the main actors in the movie")
    genre: Optional[List[str]] = Field(description="The genres of the movie")
    duration_minutes: Optional[int] = Field(description="The duration of the movie in minutes")
    plot: Optional[str] = Field(min_length=10, description="A brief summary of the movie's plot")
    awards: Optional[List[str]] = Field(description="A list of the awards won by the movie")

# Input unstructured text
unstructured_text = """
The Godfather is a 1972 American crime film directed by Francis Ford Coppola, who co-wrote the screenplay with Mario Puzo, based on Puzo's best-selling 1969 novel of the same name.
The film stars Marlon Brando, Al Pacino, and James Caan, and tells the story of the powerful Italian-American crime family of Don Vito Corleone (played by Brando).
When an organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son, Michael Corleone (played by Pacino), a series of events unfold that threatens the stability of the family and the entire criminal underworld.
Set in New York City and spanning the years 1945 to 1955, The Godfather is notable for its realistic depiction of the Mafia and its exploration of themes such as power, loyalty, betrayal, and family dynamics.
The film was met with widespread critical acclaim upon release and is commonly regarded as one of the greatest films in world cinema.
It won three Academy Awards, including Best Picture, Best Actor (Marlon Brando), and Best Adapted Screenplay, and has been selected for preservation in the United States National Film Registry.
The Godfather is a crime drama film and is widely regarded as one of the most influential films in the gangster genre.
Its running time is approximately 175 minutes.
"""



t0 = time()
model3 = jb.extract_typed_completion(unstructured_text, MovieInformation, temperature=0, model='gpt-3.5-turbo')
gpt3_times += time() - t0
print(model3)

t0 = time()
model4 = jb.extract_typed_completion(unstructured_text, MovieInformation, temperature=0, model='gpt-4')
gpt4_times += time() - t0
print(model4)
count += 1



    
# The data class we wish to extract from the unstructured text
class UserDetails(BaseModel):
    name: str = Field(description="The name of the user")
    age: Optional[int] = Field(description="The age of the user")
    email: Optional[str] = Field(description="The email address of the user")
    country: str = Field(description="The country the user resides in")

# Example unstructured text from which to extract the UserDetails
unstructured_text = """
John Doe, a software engineer from San Francisco, California, started his career in the tech industry in the United States in 2010.
He initially worked for a small startup before joining a larger multinational company in 2014.
John, currently 30 years old, is passionate about programming and solving complex problems.
He has attended multiple conferences across the world and has collaborated with colleagues from various countries on numerous projects.
Despite his busy work life, John finds time for his hobbies, such as photography and hiking.
He enjoys traveling to different countries, and one of his favorite trips was to Japan in 2019.
Do you need to get in touch with John? Feel free to reach out to him at john.doe@example.com.
"""

t0 = time()
model3 = jb.extract_typed_completion(unstructured_text, UserDetails, temperature=0, model='gpt-3.5-turbo')
gpt3_times += time() - t0
print(model3)

t0 = time()
model4 = jb.extract_typed_completion(unstructured_text, UserDetails, temperature=0, model='gpt-4')
gpt4_times += time() - t0
print(model4)    
count += 1


print(f"GPT-3.5 Turbo: {gpt3_times/count} s")
print(f"GPT-4:         {gpt4_times/count} s")