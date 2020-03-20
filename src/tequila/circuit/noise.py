import typing
from tequila.tools import list_assignement
from tequila.utils import TequilaException
import copy


names_dict={
    'x':'x',
    'y':'y',
    'z':'z',
    'h':'h',
    'rx':'r',
    'ry':'r',
    'rz':'r',
    'r':'r',
    'phase':'r',
    'single':'single',
    'swap':'control',
    'cx':'control',
    'cy':'control',
    'cz':'control',
    'crx':'control',
    'cry':'control',
    'crz':'control',
    'control':'control',
    'cnot':'control',
    'ccnot':'multicontrol',
    'multicontrol':'multicontrol'
}

class Noise():
    prob_length={
        'bit flip':1,
        'phase flip':1,
        'phase damp':1,
        'amplitude damp':1,
        'phase-amplitude damp':2,
        'depolarizing':1
    }
    @property
    def name(self):
        return self._name

    @property
    def gate(self):
        return self._gate

    def __init__(self,name:str,probs:typing.List[float],gate:str,form: str='kraus'):
        probs=list_assignement(probs)
        self._name=name
        self._gate=names_dict[gate.lower()]
        assert len(probs) is self.prob_length[name]
        if form is 'kraus':
            assert sum(probs)<=1.
        if form is 'depolarizing':
            assert sum(probs)<=1.
        self.probs=list_assignement(probs)

    def __str__(self):
        back=self.name
        back+=' on ' + self.gate
        back+=', probs = ' +str(self.probs)
        return back

    @staticmethod
    def from_dict(d):
        if type(d) is dict:
            return Noise(**d)
        elif type(d) is Noise:
            return d
        else:
            raise TequilaException('who the fuck do you think you are?')

class NoiseModel():

    def __init__(self,noises: typing.List[typing.Union[dict,Noise]]=None):
        if noises is None:
            self.noises=[]
        else:
            self.noises=[Noise.from_dict(d) for d in list_assignement(noises)]


    def __str__(self):
        back=''
        for noise in self.noises:
            back += str(noise)
            back += ',\n'
        return back

    def __add__(self, other):
        new=NoiseModel()
        new.noises+=self.noises
        if type(other) is dict:
            new.noises+=Noise.from_dict(other)
        elif hasattr(other,'noises'):
            new.noises.extend(copy.copy(other.noises))
        return new

    def __iadd__(self, other):
        if type(other) is dict:
            self.noises+=Noise.from_dict(other)
        elif hasattr(other,'noises'):
            self.noises.extend(copy.copy(other.noises))
        return self

    def without_noise_on(self,gate: str):
        new=NoiseModel()
        for noise in self.noises:
            if noise.gate==names_dict[gate]:
                pass
            else:
                new.noises.append(noise)
        return new

    @staticmethod
    def wrap_noise(other):
        return NoiseModel(noises=other)

def BitFlip(p:float,gate:str):

    new=NoiseModel.wrap_noise(Noise(name='bit flip',probs=list_assignement(p),gate=gate))
    return new

def PhaseFlip(p:float,gate:str):
    new=NoiseModel.wrap_noise(Noise(name='phase flip',probs=list_assignement(p),gate=gate))
    return new


def PhaseDamp(p:float,gate:str):
    new=NoiseModel.wrap_noise(Noise(name='phase damp',probs=list_assignement(p),gate=gate))
    return new


def AmplitudeDamp(p:float,gate:str):
    new=NoiseModel.wrap_noise(Noise(name='amplitude damp',probs=list_assignement(p),gate=gate))
    return new

def PhaseAmplitudeDamp(p1:float,p2:float,gate:str):
    new=NoiseModel.wrap_noise(Noise(name='phase-amplitude damp',probs=list_assignement([p1,p2]),gate=gate))
    return new

def DepolarizingError(p:float,gate:str):
    new = NoiseModel.wrap_noise(Noise(name='depolarizing', probs=list_assignement(p), gate=gate,form='depolarizing'))
    return new