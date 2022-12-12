# Capstone Submission: Report
---

My project explores an area of sentiment analysis that the most Americans are at least somewhat concerned about: how reaction-inducing are their social media posts? In particular, how effective are they at posting _funny_ content?  

It's probably not wrong to say humor is subjective, so instead of trying to create a model that can produce Key & Peele levels of generalizable gag material, I focused on specific groups of people: my former batchmates when I was an associate at Revature and my data science colleagues at Brainstation. Being a member of both their Discord servers, I was able to compile message data that contained the following details:  

1. **Content** of the message
2. **Date and time** the content was submitted
3. Emotic **reactions** (if any)  

 My strategy was to employ Natural Language Processing techniques on this data to create a model that can predict if a message received either a 😂 or 🤣 reaction.  
 
 The value such a model would provide includes features for application development (e.g. as a user writes a post, inform the user in real-time that the post is likely to get a positive reaction) or for automation (e.g. a Discord bot that periodically reacts to messages in a manner that's expected by a human user).

## Process  

The means of obtaining my data was inspired by [a Medium article](https://hongchai.medium.com/scraping-discord-channels-d5de7ee87abe), where you visit the Discord channel like you normally would on your browser, and use the browser's developer tools to figure out where and how the browser makes a request to obtain the messages it renders to the user.  


![scraping discord messages](roffle-scrape.png "The data is all there!")  


I tried several methods to prepare the data for analysis and modeling. Originally I tried doing things programmatically in Python (e.g. creating Python classes to map JSON to the dataframe I want), but found a more streamlined way of data processing through [AWS Glue](https://aws.amazon.com/glue/) and [AWS Athena](https://aws.amazon.com/athena/). Glue takes my scraped JSON data in an AWS S3 bucket and converts it to a relational table. Athena allows me to make SQL queries on this table and generate the outputs of those queries as a CSV.  


![flowchart](roffle-flowchart.png)  


I use a simple Logistic Regression after tokenizing all the messages, and while the final model fails to identify many of the funny messages, the ones it does identify are more likely to have had funny emoji reactions than not (this is on a data set that is split roughly evenly between "funny" and "not funny").  

While this model would not perform particularly well in identifying repeated attempts to post a funny message, it could serve as a Discord bot that, because of it's relatively high precision, will react to messages that are actually meant to be funny.  

Another consideration that would supplement such a feature (the Discord bot) is determining if the chances of a funny message being posted increases significantly if a funny posting was made within a given timeframe. This is based on the assumption that a funny comment can lead to a "streak" of funny content being posted in response.  

To explore this, I divide the data into six annual quarters and for each day, compare the number of days until the next funny posting was made. The results are show below, where the horizontal axis represents the number of days since last funny posting, and the vertical axis are the days in chronological order.


![time series](roffle-time-series.png)  



The variation of the widths of the bars across time suggest that funny comments do in fact happen in "clusters" rather than regular intervals or with any consistency. For a Discord bot, this would mean increasing the likelihood of the bot reacting to the messages following a funny posting.  

## Final Remarks  

Since new Discord messages are posted almost every day, for my next sprint I would like to set up a system where this new data is fed to a pipeline that automatically updates my model. I would also want to make progress applying my model, whether it be Discord bot or otherwise.