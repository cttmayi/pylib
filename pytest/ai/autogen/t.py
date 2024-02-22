import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

fig, ax = plt.subplots()

agent_1_start, agent_1_height = 0.1, 0.8
agent_2_start, agent_2_height = 0.5, 0.8
rectangle_width, rectangle_height = 0.3, 0.15

# Draw agents
agent_1 = Rectangle((agent_1_start, agent_1_height), rectangle_width, rectangle_height)
agent_2 = Rectangle((agent_2_start, agent_2_height), rectangle_width, rectangle_height)
plt.text(agent_1_start, agent_1_height+rectangle_height, 'Agent 1')
plt.text(agent_2_start, agent_2_height+rectangle_height, 'Agent 2')

plt.gca().add_patch(agent_1)
plt.gca().add_patch(agent_2)

# Add dialog
dialog_1 = TextArea('Hello Agent 2')
ab = AnnotationBbox(dialog_1, (agent_1_start+rectangle_width/2, agent_1_height-0.1),
                        xybox=(-80, 60),
                        boxcoords='offset points',
                        arrowprops=dict(arrowstyle='-|>', color='black'))
ax.add_artist(ab)

dialog_2 = TextArea('Hello Agent 1')
ab = AnnotationBbox(dialog_2, (agent_2_start+rectangle_width/2, agent_2_height-0.1),
                        xybox=(30, 60),
                        boxcoords='offset points',
                        arrowprops=dict(arrowstyle='-|>', color='black'))
ax.add_artist(ab)

plt.axis('off')