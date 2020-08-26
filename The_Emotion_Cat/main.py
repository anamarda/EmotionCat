from body.DecisionMaker import DecisionMaker
from body.services.Mover import Mover
from body.services.ControllerLimb import ControllerLimb
from body.persistence.FileRepository import FileRepository
from body.validator.AngleValidator import AngleValidator
from utils.Bus import Bus
from brain.Brain import Brain
from application.Application import Cat

b = Bus()
bus = b.get_bus()
repo = FileRepository()
val = AngleValidator()
ctr = ControllerLimb(repo, bus, val)
mover = Mover(ctr)
decision_maker = DecisionMaker(mover)
emotion_detector = Brain()

cat = Cat(decision_maker, emotion_detector)

try:
    cat.start()
except Exception as e:
    print(e)
finally:
    decision_maker.mirror_emotion("Neutral")
