import networkx as nx 
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import requests





def getMapXML(left, bottom, right, top):
    result = []
    url = 'https://www.openstreetmap.org/api/0.6/map?bbox=' + str(left) + ',' + str(bottom) + ',' + str(right) + ',' + str(top)
    payload = {}
    headers = {}
    print(url)
    print('Requesting map data')
    res = requests.request("GET", url, headers=headers, data=payload)
    print(res.text.encode('utf-8'))
    if(res.text.encode('utf-8')[:4] == b'You '):
        print('Requested too many nodes: trying on a smaller region')
        result.append(getMapXML(left, bottom, (left + right)/2, (top + bottom)/2))
    else:
        print('success')
        result.append(res)
    print(res.text.encode('utf-8'))
    return [res.text]

G = nx.Graph()

osmFiles = getMapXML(-0.09, 51.4, -0.07, 51.42)
textFile = open("map2.osm", "w", encoding = "utf8")
textFile.write(osmFiles[0])
textFile.close()

for f in osmFiles:
    tree = ET.parse('map2.osm')
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
        for attr in attrs: 
            G.add_edges_from(zip(nodes[:-1], nodes[1:]), way_id=way_id)




def is_road_edge(u,v):
    return 'highway' in G[u][v]


pos = {node: (lon, lat) for node, (lat, lon) in nx.get_node_attributes(G, 'pos').items()}
nx.draw_networkx_edges(G, pos)
plt.show()
print(G)