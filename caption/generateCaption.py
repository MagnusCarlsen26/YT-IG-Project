from dotenv import load_dotenv,dotenv_values
from utility.Gemini import AskGemini
from utility.toMarkdown import to_markdown


def generateCaption(script) :
    prompt = f'''
        This is my script :

        {script}

        I want you to generate a caption for my reel. Your response should be such that I can copy your entire response and paste the caption.
    '''
    caption = to_markdown(AskGemini(prompt))
    print(caption)

generateCaption(''' Hey guys, it's that time again, time to dive into history! Today, June 28th, marks some pretty significant events. 

First up, we have the landmark Supreme Court case Regents of the University of California v. Bakke.  In 1978, the court ruled that while affirmative action programs aiming to increase diversity were constitutional, quota systems in college admissions were not.  This decision was a major victory for racial equality and helped shape the way we approach college admissions today.

But it wasn't all legal battles and court rulings. On this day in 1969,  a police raid on the Stonewall Inn in New York City sparked a series of protests by members of the LGBTQ+ community. This was a pivotal moment in the fight for gay rights, marking the beginning of a movement that continues to fight for equality and justice for all.

Finally, on this day in 1942,  World War II took a dramatic turn as the Wehrmacht launched "Case Blue" - a massive German offensive aimed at capturing oil fields in the south of the Soviet Union. This operation, despite initial gains, ultimately proved costly for the Germans and played a crucial role in shifting the momentum of the war.

So there you have it, folks! Just a glimpse into the significant events that unfolded on this day in history. For more historical content, be sure to follow my channel!''')