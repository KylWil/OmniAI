from pyftg import FrameData, CommandCenter, Key
from OmniAI import OmniAI

def test_omni_frame_data():
    frame = FrameData()
    agent = OmniAI()
    agent.initialize(None, None)
    agent.get_information(frame_data=frame, is_control=True)
    frame_dict = agent.frame_data.to_dict()
    assert frame_dict.get("current_frame_number") == -1, "Wrong Frame Number"
    assert frame_dict.get("current_round") == -1, "Wrong Round Number"
    assert frame_dict.get("empty_flag") == True, "Wrong Flag Boolean"

def test_cc_frame_data():
    frame = FrameData()
    agent = OmniAI()
    agent.initialize(None, None)
    agent.get_information(frame_data=frame, is_control=True)
    frame_dict = agent.cc.frame_data.to_dict()
    assert frame_dict.get("current_frame_number") == -1, "Wrong Frame Number"
    assert frame_dict.get("current_round") == -1, "Wrong Round Number"
    assert frame_dict.get("empty_flag") == True, "Wrong Flag Boolean"

def test_name():
    agent = OmniAI()
    assert agent.name() == "OmniAI", "Wrong Class Name"

def test_cc():
    agent = OmniAI()
    agent.initialize(None, None)
    assert isinstance(agent.cc, CommandCenter), "CommandCenter Attribute Invalid"

def test_key():
    agent = OmniAI()
    agent.initialize(None, None)
    assert isinstance(agent.input(), Key), "Key Attribute Invalid"