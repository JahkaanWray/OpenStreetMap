import networkx as nx 
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

G = nx.Graph()

tree = ET.parse('map.osm')
root = tree.getroot()

for node in root.findall('.//node'):
    nodeId = node.attrib['id']
    lat = float(node.attrib['lat'])
    lon = float(node.attrib['lon'])
    G.add_node(nodeId, pos=(lat, lon))

for way in root.findall('.//way'):
    way_id = way.attrib['id']
    nodes = [node.attrib['ref'] for node in way.findall('.//nd')]
    attrs = [{tag.attrib['k']: tag.attrib['v']} for tag in way.findall('.//tag')]
    print(attrs)
    for attr in attrs: 
        if 'highway' in attr.keys() and attr['highway'] != 'footway':
            G.add_edges_from(zip(nodes[:-1], nodes[1:]), way_id=way_id)



def is_road_edge(u,v):
    return 'highway' in G[u][v]


pos = {node: (lon, lat) for node, (lat, lon) in nx.get_node_attributes(G, 'pos').items()}
nx.draw_networkx_edges(G, pos)
plt.show()