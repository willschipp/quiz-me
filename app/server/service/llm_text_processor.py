# initial prompt to identify the beginning of a chapter in a text
prompt = 'You are an expert librarian. Read the following text, identify the first sentence of the first chapter, and return only it.  Text = TEXT'
# this can be used to start the parsing component
prompt_themes = 'You are an expert in literature. Read the following chapter and list the major themes, characters and locations using the JSON template provided. JSON={"majorThemes":[],"characters":[],"locations:[]} Text ='
# this can be used to generate a response
prompt_questions = 'You are a literature expert. Read the following text and create 5 questions about what the major themes are in the following text. Answer using the included JSON template. JSON_TEMPLATE=[{"question":question number,"question":question text}] TEXT='
# this is an example of an answer generation prompt
prompt_answer_generation = "You are a literature expert. Answer the following question about the following text. question=What is the significance of the ocean in the narrator's life, and how does it relate to his emotional well-being? text="
# prompt for character theme
prompt_character_theme = 'You are a literature expert. Summarize the following text identifying the major themes for all characters. Respond using the following JSON template. JSON=[{"character":character name,"major themes":major themes for the character"}] Text='
