from IPython.display import IFrame
import json
import uuid

def vis_network(nodes, edges, physics=False):
    html = """
    <html>
    <head>
      <script type="text/javascript" src="../lib/vis/dist/vis.js"></script>
      <link href="../lib/vis/dist/vis.css" rel="stylesheet" type="text/css">
    </head>
    <body>
    <div id="{id}"></div>
    <script type="text/javascript">
      var nodes = {nodes};
      var edges = {edges};
      var container = document.getElementById("{id}");
      var data = {{
        nodes: nodes,
        edges: edges
      }};
      var options = {{
          nodes: {{
              shape: 'dot',
              size: 25,
              font: {{
                  size: 14
              }}
          }},
          edges: {{
              font: {{
                  size: 14,
                  align: 'middle'
              }},
              color: 'gray',
              arrows: {{
                  to: {{enabled: true, scaleFactor: 0.5}}
              }},
              smooth: {{enabled: false}}
          }},
          physics: {{
              enabled: {physics}
          }}
      }};
      var network = new vis.Network(container, data, options);
    </script>
    </body>
    </html>
    """

    unique_id = str(uuid.uuid4())
    html = html.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))

    filename = "figure/graph-{}.html".format(unique_id)

    file = open(filename, "w")
    file.write(html)
    file.close()

    return IFrame(filename, width="100%", height="400")


def draw(G, options=None, physics=False):
    '''
    Draw a networkx graph for the panama papers project.
    G : the graph (use .get_graph() method)
    options : node labels (see below)
    physics : to have magnetic nodes :)
    '''
    if options is None:
        options = {
        "Officer": "name",
        "Entity": "name",
        "Intermediary": "name",
        "Address": "address"
        }

    def get_info(node, id):
        key = node['labels'][0]
        prop = options[key]
        label = node.get(prop, '')
        return {'id':id,'label':label,'group':key,'title':repr(node)}

    nodes, edges = [], []
    for u_id,v_id,d in G.edges(data=True):
        u = G.node[u_id]
        source = get_info(u, u_id)
        if source not in nodes:
            nodes.append(source)
        if d is not None:
            v = G.node[v_id]
            target = get_info(v, v_id)
            if target not in nodes:
                nodes.append(target)
            edges.append({'from':u_id,'to':v_id,'label':d['type']})
    # If there's no edge, still plot the nodes:
    for n_id,n in G.nodes(data=True):
        node = get_info(n, n_id)
        if node not in nodes:
            nodes.append(node)
    return vis_network(nodes, edges, physics=physics)
