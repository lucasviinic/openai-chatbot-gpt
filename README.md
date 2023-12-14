## Python e GPT: Creating a chatbot with AI

The project involves creating an AI-powered chatbot using Python and Flask in conjunction with GPT.

**Step 1:** Integrating API with front-end

- Connecting GPT to our chatbot's front-end by creating routes using the Flask microframework;
- Identifying the advantages of using Stream configuration in our chatbot, including real-time responses, continuous interaction, time savings, improved user experience, and the ability to halt response generation before completion, analyzing how we receive messages in our chatbot compared to ChatGPT;
- Configuring our project to accommodate the stream=True configuration for the bot, creating a function to handle the received response, and updating our front-end to display these changes in real-time.

**Step 2:** Working with Memory

- Include the e-commerce data in our system prompt to send the information with each request made to the GPT API;
- Create a conversation history and store this history in a file to add this information to the bot's system prompt.

**Step 3:** Managing Conversation History

- Count the number of tokens in the system prompt to switch the model used in the bot that makes requests to the OpenAI API if the maximum tokens for each model are exceeded;
- Create a partial history in which we calculate the token count for each line of the history and delete the oldest lines based on the specified maximum token limit;
- Clear the conversation history and initiate a new conversation;
- Organize our project to enhance the readability and maintainability of our code.

**Step 4:** Adding History Summarization

- Implement the strategy of creating a history summarizer to save all important conversation information succinctly for sending to the chatbot's API request bot;
- Configure the summarizer within the response handling that sends information to the bot;
- Test different GPT models in the summarizer project.

**Step 5:** Multiple Users

- Create a login screen to require users to log in before accessing the chatbot.
- Configure the project to create separate histories for each existing user using the 
