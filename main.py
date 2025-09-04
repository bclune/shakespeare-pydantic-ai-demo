import pprint
from enum import Enum
from typing import List

from pydantic import BaseModel
from pydantic_ai import Agent, DocumentUrl
from dotenv import load_dotenv

load_dotenv()

CORPUS_URL = "https://folger-main-site-assets.s3.amazonaws.com/uploads/2022/11/a-midsummer-nights-dream_PDF_FolgerShakespeare.pdf"


class Act(BaseModel):
    number: int


class Scene(BaseModel):
    act: Act
    description: str


class Character(BaseModel):
    name: str
    description: str
    motivation: str
    """ Why does the character act the way they do? What are they trying to do?"""


class ActionDirectionEnum(str, Enum):
    RISING = "rising"
    """ An action or plot beat that increases tension. """
    FALLING = "falling"
    """ An action or plot beat that decreases tension. """


class Action(BaseModel):
    scene: Scene
    action: str
    """ An action or plot beat. Expect multiple per scene. """
    characters: List[str]
    """ Characters involved in the action. """
    direction: ActionDirectionEnum
    """ Whether the action increases or decreases dramatic tension. """
    reason: str
    """ Why did the action happen from a character point of view? """
    emotions: List[str]
    """ What sentiments surround the action? """


class Relationship(BaseModel):
    left: Character
    right: Character
    description: str
    """ A description of the relationship between two characters. """


class ReviewFlashCard(BaseModel):
    """ A flashcard designed for study based on provided material. """
    question: str
    answer: str


if __name__ == "__main__":
    print = pprint.pp
    agent = Agent(
        'claude-3-5-haiku-latest',
        system_prompt='Brevity is the soul of wit, so be brief.',
    )

    result = agent.run_sync([
        """Who are the main characters in A Midsummer Nights Dream?""",
        DocumentUrl(url=CORPUS_URL)
    ],
        output_type=List[Character]
    )
    print(result.output)
    """
    [Character(name='Theseus', description='Duke of athens, who is to marry Hippolyta', motivation="To marry Hippolyta and oversee the resolution of the young lover's conflicts"),
     Character(name='Hippolyta', description='Queen of the Amazons, engaged to Theseus', motivation='To marry Theseus and observe the events unfolding around her'),
     Character(name='Lysander', description='One of the young male Athenian lover, in love with Hernia', motivation='To be with Hernia and overcome the obstacles preventing their marriage'),
     Character(name='Hernia', description='A young Athenian woman in love with Lysander', motivation="To marry Lysander despite her father's wishes and societal constraints"),
     Character(name='Demetrius', description='Another young Athenian male, originally intended to marry Hernia', motivation='Initially to marry Hernia, but later falls in love with Helena'),
     Character(name='Helena', description='A young Athenian woman who is in love with Demetrius', motivation="To win Demetrius's love and overcome her unrequited feelings"),
     Character(name='Oberon', description='King of the Fairies', motivation="To resolve his dispute with Titania and manipulate the human lover's relationships"),
     Character(name='Titania', description='Queen of the Fairies', motivation="To challenge Oberon's authority and maintain her independence"),
     Character(name='Puck (Rob in Goodfellow)', description='A mischievous fairy who serves Oberon', motivation="To carry out Oberon's orders and create magical chaos"),
     Character(name='Bottom', description='A weaver who is part of a group of amateur actors', motivation='To perform in a play and accidentally becomes enchanted by Titania')]
    """

    result = agent.run_sync([
        """What actions take place in Act 2 Scene 1?""",
        DocumentUrl(url=CORPUS_URL)
    ],
        output_type=List[Action],
    )
    print(result.output)
    """
    [Action(scene=Scene(act=Act(number=2), description='A scene in the woods'), action='The fairies discuss their conflicts and magical activities', characters=['Oberon', 'Titania', 'Fairy', 'Puck'], direction=<ActionDirectionEnum.RISING: 'rising'>, reason="Revealing the fairy kingdom's internal tensions and magical powers", emotions=['argumentative', 'mischievous', 'magical']),
     Action(scene=Scene(act=Act(number=2), description='A scene in the woods'), action="Oberon applies a magical flower juice to Titania's eyes, causing her to fall in love with Bottom (who has been transformed into a donkey)", characters=['Oberon', 'Titania', 'Bottom', 'Puck'], direction=<ActionDirectionEnum.RISING: 'rising'>, reason='To punish Titania for her defiance and take her changeling boy', emotions=['vengeful', 'playful', 'magical'])]
    """

    result = agent.run_sync([
        """What are the key relationships that drive the plot forward?""",
        DocumentUrl(url=CORPUS_URL)
    ],
        output_type=List[Relationship],
    )
    print(result.output)
    """
    [Relationship(left=Character(name='Lysander', description='Young Athenian lover of Hernia', motivation="To be with Hernia despite her father's opposition"), right=Character(name='Hernia', description='Young Athenian woman in love with Lysander', motivation='To marry Lysander instead of Demetrius'), description='Passionate romantic partners who defy parental and social constraints to be together'),
     Relationship(left=Character(name='Demetrius', description="Young Athenian suitor chosen by Hernia's father", motivation='To marry Hernia and gain social approval'), right=Character(name='Helena', description="Hernia's friend who is in love with Demetrius", motivation="To win Demetrius's love and affection"), description='Complex romantic tension where Helena pursues Demetrius, who initially rejects her'),
     Relationship(left=Character(name='Oberon', description='King of the Fairies', motivation='To manipulate and control the romantic interactions of others'), right=Character(name='Titania', description='Queen of the Fairies', motivation="To resist Oberon's manipulations and maintain her own agency"), description='Powerful fairy monarchs engaged in a complex power struggle and romantic dispute'),
     Relationship(left=Character(name='Bottom', description='Weaver and amateur actor', motivation='To perform in a play and experience fantastical adventures'), right=Character(name='Titania', description='Queen of the Fairies', motivation='To explore an enchanted love with Bottom'), description='Absurd and magical romantic encounter between a human and a fairy queen')]
    """

    result = agent.run_sync([
        """Generate between 20 and 40 review flash cards with questions that demonstrate understanding of the play.""",
        DocumentUrl(url=CORPUS_URL)
    ],
        output_type=List[ReviewFlashCard],
    )
    print(result.output)
    """
    [ReviewFlashCard(question='Who are the four main young Athenian characters in the play?', answer='Lysander, Demetrius, Hermiа, and Helena'),
     ReviewFlashCard(question='Who is the King of the Fairies?', answer='Oberon'),
     ReviewFlashCard(question='Who is the Queen of the Fairies?', answer='Titania'),
     ReviewFlashCard(question="What magical substance does Oberon use to manipulate the characters' love?", answer="A flower's love juice (also called 'love-in-idleness')"),
     ReviewFlashCard(question='Who are the main human characters planning a wedding at the beginning of the play?', answer='Theseus and Hippolyta'),
     ReviewFlashCard(question='What is the name of the play-within-a-play performed by the craftsmen?', answer='Pyramus and Thisbe'),
     ReviewFlashCard(question='Who plays the role of Pyramus in the play-within-a-play?', answer='Bottom'),
     ReviewFlashCard(question="What magical creature transforms Bottom by giving him an ass's head?", answer='Puck (also called Robert Goodfellow)'),
     ReviewFlashCard(question='What is the legal situation facing Hermiа at the beginning of the play?', answer='She must either marry Demetrius, become a nun, or be put to death according to Athenian law'),
     ReviewFlashCard(question='How do the fairies ultimately resolve the love complications?', answer='Puck uses the love juice to restore the original couples: Lysander with Hermiа, and Demetrius with Helena'),
     ReviewFlashCard(question='What blessing do the fairies give at the end of the play?', answer="They bless the marriages and promise that the couples' children will be free from physical defects"),
     ReviewFlashCard(question="What is the final message of Puck in the play's epilogue?", answer='If the play has offended, the audience should consider it merely a dream, and all will be forgiven'),
     ReviewFlashCard(question="What are the names of Titania's fairy attendants?", answer='Peaseblossom, Cobweb, Mote, and Mustardseed'),
     ReviewFlashCard(question='What metaphors does Theseus use to describe the imagination of poets, lunatics, and love?', answer="He describes them as creating fantastic visions that go beyond rational thought, comparing them to bodies forth shapes from 'airy nothing'"),
     ReviewFlashCard(question='Where do the main events of the play take place?', answer='A forest near athens'),
     ReviewFlashCard(question='How does Bottom react to being transformed into an ass?', answer='He remains largely unaware and continues to act confidently, even being attended to by Titania'),
     ReviewFlashCard(question='What role does Puck play in the chaos of the play?', answer='He creates mischief by mistakenly applying the love juice and transforming characters'),
     ReviewFlashCard(question='What time of year does the play primarily take place?', answer='Midsummer'),
     ReviewFlashCard(question='What is the symbolic meaning of the woodland setting?', answer='A realm of magic, transformation, and the blurring of reality and dream'),
     ReviewFlashCard(question='How does Shakespeare use the play-within-a-play to comment on theatrical performance?', answer="Through the amateur actors' comical performance, he satirizes and celebrates the nature of theatrical representation")]
    """