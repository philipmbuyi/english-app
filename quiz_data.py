import json

def get_quiz_data(modules):
    """
    Returns a list of quiz data for each module.
    
    Args:
        modules (dict): Dictionary mapping module names to module IDs
        
    Returns:
        list: List of quiz data dictionaries
    """
    quizzes_data = []
    
    # Grammar quizzes
    quizzes_data.append({
        'module_id': modules['grammar'],
        'quiz_number': 1,
        'title': 'Parts of Speech Quiz',
        'description': 'Test your knowledge of nouns, verbs, adjectives, and more.',
        'questions': [
            {
                'question': 'Which of the following is a noun?',
                'options': json.dumps(['Running', 'Beautiful', 'Excitement', 'Quickly']),
                'answer': 'Excitement',
                'explanation': 'Excitement is a noun because it names a feeling or state of being.'
            },
            {
                'question': 'Identify the verb in this sentence: "She quickly walked to the store."',
                'options': json.dumps(['She', 'Quickly', 'Walked', 'Store']),
                'answer': 'Walked',
                'explanation': 'Walked is the verb because it describes the action being performed.'
            },
            {
                'question': 'Which word is an adjective in this sentence: "The red car stopped at the bright light."',
                'options': json.dumps(['Car', 'Red', 'Stopped', 'At']),
                'answer': 'Red',
                'explanation': 'Red is an adjective because it describes the car.'
            },
            {
                'question': 'Which of these is an adverb?',
                'options': json.dumps(['Slowly', 'Table', 'Garden', 'Happy']),
                'answer': 'Slowly',
                'explanation': 'Slowly is an adverb because it typically describes how an action is performed.'
            },
            {
                'question': 'Which part of speech connects words, phrases, or clauses?',
                'options': json.dumps(['Noun', 'Verb', 'Conjunction', 'Article']),
                'answer': 'Conjunction',
                'explanation': 'Conjunctions like "and," "but," and "or" connect words, phrases, or clauses.'
            }
        ]
    })
    
    quizzes_data.append({
        'module_id': modules['grammar'],
        'quiz_number': 2,
        'title': 'Sentence Structure Quiz',
        'description': 'Test your understanding of different sentence types and structures.',
        'questions': [
            {
                'question': 'Which is an example of a simple sentence?',
                'options': json.dumps([
                    'John ran, and Mary walked.',
                    'The cat slept on the mat.',
                    'Although it was raining, we went outside.',
                    'The dog barked when the mailman arrived.'
                ]),
                'answer': 'The cat slept on the mat.',
                'explanation': 'A simple sentence has one independent clause with a subject and predicate.'
            },
            {
                'question': 'What type of sentence is this: "Close the door!"',
                'options': json.dumps(['Declarative', 'Interrogative', 'Imperative', 'Exclamatory']),
                'answer': 'Imperative',
                'explanation': 'Imperative sentences give commands or make requests.'
            },
            {
                'question': 'In the sentence "The dog, which had brown fur, barked loudly," what is "which had brown fur"?',
                'options': json.dumps(['Independent clause', 'Dependent clause', 'Prepositional phrase', 'Gerund phrase']),
                'answer': 'Dependent clause',
                'explanation': 'This is a dependent clause that provides additional information about the dog.'
            },
            {
                'question': 'What is the subject in this sentence: "The tall, old tree fell during the storm."',
                'options': json.dumps(['Tall', 'Tree', 'Fell', 'Storm']),
                'answer': 'Tree',
                'explanation': 'The subject is the noun that performs the action in the sentence.'
            },
            {
                'question': 'Which of these is a compound sentence?',
                'options': json.dumps([
                    'I love to read books.',
                    'I love to read books, and my sister enjoys movies.',
                    'When I have time, I love to read books.',
                    'I love to read books that have adventure stories.'
                ]),
                'answer': 'I love to read books, and my sister enjoys movies.',
                'explanation': 'A compound sentence contains two independent clauses joined by a conjunction.'
            }
        ]
    })
    
    # Writing quizzes
    quizzes_data.append({
        'module_id': modules['writing'],
        'quiz_number': 1,
        'title': 'Essay Structure Quiz',
        'description': 'Test your knowledge of essay organization and structure.',
        'questions': [
            {
                'question': 'Which of the following is typically NOT included in an essay introduction?',
                'options': json.dumps(['Thesis statement', 'Hook', 'Background information', 'Detailed evidence']),
                'answer': 'Detailed evidence',
                'explanation': 'Detailed evidence is usually presented in the body paragraphs, not in the introduction.'
            },
            {
                'question': 'What is a thesis statement?',
                'options': json.dumps([
                    'A question that the essay will answer',
                    'A summary of the essay\'s main argument',
                    'A quote from an expert in the field',
                    'The first sentence of an essay'
                ]),
                'answer': 'A summary of the essay\'s main argument',
                'explanation': 'A thesis statement presents the main argument or point that the essay will develop.'
            },
            {
                'question': 'Which organization method arranges information from least important to most important?',
                'options': json.dumps(['Chronological', 'Spatial', 'Climactic', 'Compare and contrast']),
                'answer': 'Climactic',
                'explanation': 'Climactic organization builds toward the most important point at the end.'
            },
            {
                'question': 'What is the primary purpose of a conclusion paragraph?',
                'options': json.dumps([
                    'To introduce new evidence',
                    'To summarize main points and restate the thesis',
                    'To ask questions for further research',
                    'To include citations'
                ]),
                'answer': 'To summarize main points and restate the thesis',
                'explanation': 'Conclusions typically summarize the essay\'s main points and restate the thesis in a new way.'
            },
            {
                'question': 'Which of these transition words would best connect contrasting ideas?',
                'options': json.dumps(['Furthermore', 'Similarly', 'However', 'In addition']),
                'answer': 'However',
                'explanation': '"However" signals a contrast or change in direction between ideas.'
            }
        ]
    })
    
    # Pronunciation quizzes
    quizzes_data.append({
        'module_id': modules['pronunciation'],
        'quiz_number': 1,
        'title': 'Vowel Sounds Quiz',
        'description': 'Test your knowledge of English vowel sounds.',
        'questions': [
            {
                'question': 'Which word has a different vowel sound than the others?',
                'options': json.dumps(['Heat', 'Meet', 'Great', 'Seat']),
                'answer': 'Great',
                'explanation': '"Great" has the /eɪ/ sound, while the others have the /i:/ sound.'
            },
            {
                'question': 'How many syllables are in the word "comfortable"?',
                'options': json.dumps(['2', '3', '4', '5']),
                'answer': '3',
                'explanation': 'In common pronunciation, "comfortable" has three syllables: com-fort-ble.'
            },
            {
                'question': 'Which word has the same vowel sound as in "book"?',
                'options': json.dumps(['Food', 'Good', 'Moon', 'Boot']),
                'answer': 'Good',
                'explanation': '"Good" has the same short /ʊ/ sound as in "book".'
            },
            {
                'question': 'Which of these words contains a diphthong?',
                'options': json.dumps(['Bed', 'Price', 'Set', 'Met']),
                'answer': 'Price',
                'explanation': '"Price" contains the diphthong /aɪ/, which is a combination of two vowel sounds.'
            },
            {
                'question': 'In which word is the stressed syllable different?',
                'options': json.dumps(['Photograph', 'Photography', 'Photographer', 'Photographic']),
                'answer': 'Photography',
                'explanation': 'In "photography," the stress is on the second syllable, whereas in the others, it\'s on a different syllable.'
            }
        ]
    })
    
    # Conversation quizzes
    quizzes_data.append({
        'module_id': modules['conversation'],
        'quiz_number': 1,
        'title': 'Everyday Dialogues Quiz',
        'description': 'Test your understanding of common conversational expressions.',
        'questions': [
            {
                'question': 'What\'s the most appropriate response to "How do you do?"',
                'options': json.dumps([
                    'I\'m fine, thank you.',
                    'How do you do?',
                    'I\'m doing my homework.',
                    'Nothing much.'
                ]),
                'answer': 'How do you do?',
                'explanation': '"How do you do?" is a formal greeting, and the traditional response is to repeat the same phrase.'
            },
            {
                'question': 'Which phrase would you use to politely interrupt someone?',
                'options': json.dumps([
                    'Shut up for a moment.',
                    'Excuse me, may I say something?',
                    'I have something to say now.',
                    'Stop talking, please.'
                ]),
                'answer': 'Excuse me, may I say something?',
                'explanation': 'This is a polite way to interrupt someone in conversation.'
            },
            {
                'question': 'What does "I\'m afraid I can\'t make it" usually mean?',
                'options': json.dumps([
                    'I\'m scared to attend.',
                    'I won\'t be able to attend.',
                    'I don\'t know how to get there.',
                    'I\'m not sure if I want to go.'
                ]),
                'answer': 'I won\'t be able to attend.',
                'explanation': 'This is a polite way to decline an invitation.'
            },
            {
                'question': 'What\'s the meaning of the phrase "to break the ice"?',
                'options': json.dumps([
                    'To cool down a heated argument',
                    'To end a friendship',
                    'To start a conversation in a social situation',
                    'To solve a difficult problem'
                ]),
                'answer': 'To start a conversation in a social situation',
                'explanation': '"Breaking the ice" means making people feel more comfortable in a social situation by starting a conversation.'
            },
            {
                'question': 'Which response is appropriate when someone says "Thank you"?',
                'options': json.dumps([
                    'Thank you too.',
                    'You\'re welcome.',
                    'It\'s nothing.',
                    'All options are appropriate.'
                ]),
                'answer': 'All options are appropriate.',
                'explanation': 'All of these responses can be appropriate ways to respond to thanks, depending on the context.'
            }
        ]
    })
    
    # Reading quizzes
    quizzes_data.append({
        'module_id': modules['reading'],
        'quiz_number': 1,
        'title': 'Reading Strategies Quiz',
        'description': 'Test your knowledge of effective reading techniques.',
        'questions': [
            {
                'question': 'What is skimming?',
                'options': json.dumps([
                    'Reading only the first sentence of each paragraph',
                    'Looking for specific information in a text',
                    'Reading quickly to get the main idea',
                    'Reading every word carefully'
                ]),
                'answer': 'Reading quickly to get the main idea',
                'explanation': 'Skimming involves reading quickly to get a general overview or main idea of a text.'
            },
            {
                'question': 'Which of these is NOT a purpose for scanning a text?',
                'options': json.dumps([
                    'To find a specific date',
                    'To locate a name',
                    'To understand the overall argument',
                    'To look up a word in a dictionary'
                ]),
                'answer': 'To understand the overall argument',
                'explanation': 'Scanning is used to find specific information quickly, not to understand the overall argument.'
            },
            {
                'question': 'What should you do before starting to read a complex academic text?',
                'options': json.dumps([
                    'Read every word from beginning to end',
                    'Preview the text by looking at headings, images, and summaries',
                    'Look up every unfamiliar word in a dictionary',
                    'Take detailed notes on each paragraph'
                ]),
                'answer': 'Preview the text by looking at headings, images, and summaries',
                'explanation': 'Previewing gives you an overview of the text structure and main ideas before diving in.'
            },
            {
                'question': 'Which reading technique is best for studying for an exam?',
                'options': json.dumps([
                    'Skimming',
                    'Scanning',
                    'Intensive reading',
                    'Speed reading'
                ]),
                'answer': 'Intensive reading',
                'explanation': 'Intensive reading involves reading carefully for detailed understanding, which is important for exam preparation.'
            },
            {
                'question': 'What is the SQ3R reading method?',
                'options': json.dumps([
                    'Survey, Question, Read, Recite, Review',
                    'Scan, Question, Read, Remember, Revise',
                    'Study, Quiz, Read, Recall, Repeat',
                    'Skim, Question, Read, React, Respond'
                ]),
                'answer': 'Survey, Question, Read, Recite, Review',
                'explanation': 'SQ3R stands for Survey, Question, Read, Recite, and Review - a comprehensive reading strategy.'
            }
        ]
    })
    
    # Business English quizzes
    quizzes_data.append({
        'module_id': modules['business'],
        'quiz_number': 1,
        'title': 'Business Communication Quiz',
        'description': 'Test your knowledge of professional English communication.',
        'questions': [
            {
                'question': 'Which of these is the most appropriate way to begin a formal business email?',
                'options': json.dumps([
                    'Hey there,',
                    'Dear Sir/Madam,',
                    'Hi folks,',
                    'What\'s up?'
                ]),
                'answer': 'Dear Sir/Madam,',
                'explanation': 'In formal business correspondence, "Dear Sir/Madam" is appropriate when you don\'t know the recipient\'s name.'
            },
            {
                'question': 'Which phrase is LEAST appropriate in a business meeting?',
                'options': json.dumps([
                    'I\'d like to add something if I may.',
                    'Could we consider an alternative approach?',
                    'That\'s a stupid idea.',
                    'I respectfully disagree with that point.'
                ]),
                'answer': 'That\'s a stupid idea.',
                'explanation': 'Calling someone\'s idea "stupid" is unprofessional and disrespectful in a business context.'
            },
            {
                'question': 'What does ROI stand for in business?',
                'options': json.dumps([
                    'Rate Of Inflation',
                    'Return On Investment',
                    'Risk Of Insolvency',
                    'Range Of Interest'
                ]),
                'answer': 'Return On Investment',
                'explanation': 'ROI (Return On Investment) measures the profitability of an investment relative to its cost.'
            },
            {
                'question': 'Which of these is the most appropriate way to end a formal business letter?',
                'options': json.dumps([
                    'Cheers,',
                    'Love,',
                    'Yours sincerely,',
                    'See you soon,'
                ]),
                'answer': 'Yours sincerely,',
                'explanation': '"Yours sincerely" is a standard formal closing for business letters when you know the recipient\'s name.'
            },
            {
                'question': 'What is the purpose of a "call to action" in business communication?',
                'options': json.dumps([
                    'To summarize previous discussions',
                    'To encourage the recipient to take a specific step',
                    'To introduce yourself formally',
                    'To apologize for a mistake'
                ]),
                'answer': 'To encourage the recipient to take a specific step',
                'explanation': 'A call to action prompts the reader or listener to take a specific action, such as making a purchase or scheduling a meeting.'
            }
        ]
    })
    
    # Music quizzes
    quizzes_data.append({
        'module_id': modules['music'],
        'quiz_number': 1,
        'title': 'Understanding Song Lyrics Quiz',
        'description': 'Test your ability to interpret and analyze English song lyrics.',
        'questions': [
            {
                'question': 'What literary device is used when comparing two unlike things using "like" or "as"?',
                'options': json.dumps(['Metaphor', 'Simile', 'Alliteration', 'Hyperbole']),
                'answer': 'Simile',
                'explanation': 'A simile makes a comparison using "like" or "as," such as "My heart is like a river."'
            },
            {
                'question': 'What is a "chorus" in a song?',
                'options': json.dumps([
                    'The opening lines',
                    'A section that repeats with the same melody and lyrics',
                    'The instrumental section',
                    'The closing lines'
                ]),
                'answer': 'A section that repeats with the same melody and lyrics',
                'explanation': 'The chorus is a repeated section in a song that typically contains the main message or hook.'
            },
            {
                'question': 'If a song uses the phrase "a heart of stone," this is an example of:',
                'options': json.dumps(['Personification', 'Onomatopoeia', 'Metaphor', 'Irony']),
                'answer': 'Metaphor',
                'explanation': 'This is a metaphor comparing someone\'s heart to stone, suggesting they are unfeeling or cold.'
            },
            {
                'question': 'What does "reading between the lines" mean when analyzing lyrics?',
                'options': json.dumps([
                    'Looking up unfamiliar words',
                    'Understanding the implied meaning beyond the literal words',
                    'Reading very carefully',
                    'Looking at spacing between written lines'
                ]),
                'answer': 'Understanding the implied meaning beyond the literal words',
                'explanation': '"Reading between the lines" means finding the deeper or implied meaning that is not explicitly stated.'
            },
            {
                'question': 'What is the meaning of the idiom "to hit the road" in song lyrics?',
                'options': json.dumps([
                    'To drive recklessly',
                    'To start traveling or leave',
                    'To pave a new street',
                    'To dance on the street'
                ]),
                'answer': 'To start traveling or leave',
                'explanation': '"Hit the road" is an idiom meaning to leave or begin a journey.'
            }
        ]
    })
    
    # Cultural Studies quizzes
    quizzes_data.append({
        'module_id': modules['culture'],
        'quiz_number': 1,
        'title': 'English-Speaking Cultures Quiz',
        'description': 'Test your knowledge of cultural aspects in English-speaking countries.',
        'questions': [
            {
                'question': 'Which holiday is celebrated on October 31st in many English-speaking countries?',
                'options': json.dumps(['Christmas', 'Valentine\'s Day', 'Halloween', 'Easter']),
                'answer': 'Halloween',
                'explanation': 'Halloween is celebrated on October 31st with costumes, trick-or-treating, and spooky decorations.'
            },
            {
                'question': 'What does it mean to "keep a stiff upper lip"?',
                'options': json.dumps([
                    'To smile constantly',
                    'To stay calm and not show emotion during difficulty',
                    'To speak clearly',
                    'To maintain good posture'
                ]),
                'answer': 'To stay calm and not show emotion during difficulty',
                'explanation': 'This British expression refers to remaining stoic and not showing emotion during difficult situations.'
            },
            {
                'question': 'In the US, what would you typically say when answering the phone?',
                'options': json.dumps(['Speak to me!', 'Yes?', 'Hello?', 'I\'m listening!']),
                'answer': 'Hello?',
                'explanation': '"Hello?" is the standard greeting when answering the phone in the United States.'
            },
            {
                'question': 'In British English, what is a "fortnight"?',
                'options': json.dumps(['A castle', 'Two weeks', 'A sporting event', 'A traditional dance']),
                'answer': 'Two weeks',
                'explanation': 'A fortnight is a period of two weeks (fourteen nights), commonly used in British English.'
            },
            {
                'question': 'What is considered impolite in most English-speaking business cultures?',
                'options': json.dumps([
                    'Arriving on time for meetings',
                    'Making direct eye contact',
                    'Interrupting when others are speaking',
                    'Sending thank-you emails'
                ]),
                'answer': 'Interrupting when others are speaking',
                'explanation': 'Interrupting others while they are speaking is generally considered rude and impolite in business settings.'
            }
        ]
    })
    
    return quizzes_data