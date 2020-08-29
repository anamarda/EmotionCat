from body.services.DecisionMaker import DecisionMaker
from body.services.Mover import Mover
from body.services.ControllerLimb import ControllerLimb
from body.persistence.FileRepository import FileRepository
from body.validation.AngleValidator import AngleValidator
from utils.Bus import Bus
from brain.Brain import Brain
from application.Application import Cat
from application.Controller import Controller
from application.validation.Validator import Validator
from gui.GUI import GUI

try:
    b = Bus()
    bus = b.get_bus()
    repo = FileRepository()
    val = AngleValidator()
    ctr = ControllerLimb(repo, bus, val)
    mover = Mover(ctr)
    decision_maker = DecisionMaker(mover)
    emotion_detector = Brain()
    cat = Cat(decision_maker, emotion_detector)
    val2 = Validator()
    ctr = Controller(val2, cat)
    gui = GUI(ctr)
    gui.show()
except Exception as e:
    print(e)
finally:
    decision_maker.mirror_emotion("Neutral")


