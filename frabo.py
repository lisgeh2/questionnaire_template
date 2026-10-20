PAGES = [
    {
        "title": "Question",
        "intro": "",
        "elements": [
            {
                "key": "name",
                "label": "What's your name?",
                "type": "textarea",
            },
            {
                "key": "lisa_knowledge",
                "label": "How well do you know Lisa? 1=not at all, 10=very well",
                "type": "slider",
                "min": 1,
                "max": 10,
                "default": 5,
            }, 
            {
                "key": "lisa_autistic",
                "label": "is lisa autistic?",
                "type": "radio",
                "options": ["yes", "no", "maybe"],
            },
            {
                "key": "open_answer",
                "label": "What are specific behaviours you've observed that are autistic / non-autistic?",
                "type": "textarea",
            },
        ],
    },
]