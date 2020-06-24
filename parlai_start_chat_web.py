from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any
from parlai.scripts.script import ParlaiScript
import random
import sys

SHARED: Dict[Any, Any] = {}

def _interactive_running(self, reply_text):
    reply = {'episode_done': False, 'text': reply_text}
    SHARED['agent'].observe(reply)
    model_res = SHARED['agent'].act()
    return model_res

# @st.cache(allow_output_mutation=True)
def setup_interweb_args():
    parser = setup_args()
    return parser


def interactive_web(opt, parser):
    SHARED['opt'] = parser.opt
    SHARED['opt']['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'

    # Create model and assign it to the specified task
    agent = create_agent(SHARED.get('opt'), requireModelExists=True)
    SHARED['agent'] = agent
    SHARED['world'] = create_task(SHARED.get('opt'), SHARED['agent'])

    # show args after loading model
    parser.opt = agent.opt
    parser.print_args()


class InteractiveWeb(ParlaiScript):
    @classmethod
    def setup_args(cls):
        return setup_interweb_args()

    def run(self):
        return interactive_web(self.opt, self.parser)


random.seed(42)
sys.argv.append("-t")
sys.argv.append("blended_skill_talk")
sys.argv.append("-mf")
sys.argv.append("zoo:blender/blender_90M/model")

InteractiveWeb.main()
