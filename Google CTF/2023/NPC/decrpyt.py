import dataclasses
import re
import sys

# from pyrage import passphrase


def get_word_list():
  with open('USACONST.TXT', encoding='ISO8859') as f:
    text = f.read()
  return list(set(re.sub('[^a-z]', ' ', text.lower()).split()))


def generate_password(num_words):
  word_list = get_word_list()
  return ''.join(secrets.choice(word_list) for _ in range(num_words))


@dataclasses.dataclass
class Node:
  letter: str
  id: int


@dataclasses.dataclass
class Edge:
  a: Node
  b: Node


@dataclasses.dataclass
class Graph:
  nodes: list[Node]
  edges: list[Edge]


class IdGen:
  def __init__(self):
    self.ids = set()

  def generate_id(self):
    while True:
      new_id = secrets.randbelow(1024**3)
      if new_id not in self.ids:
        self.ids.add(new_id)
        return new_id


def generate_hint(password):
  random = secrets.SystemRandom()
  id_gen = IdGen()
  graph = Graph([],[])
  for letter in password:
    graph.nodes.append(Node(letter, id_gen.generate_id()))
  for a, b in zip(graph.nodes, graph.nodes[1:]):
    graph.edges.append(Edge(a, b))
  for _ in range(int(len(password)**1.3)):
    a, b = random.sample(graph.nodes, 2)
    graph.edges.append(Edge(a, b))
  random.shuffle(graph.nodes)
  random.shuffle(graph.edges)
  for edge in graph.edges:
    if random.random() % 2:
      edge.a, edge.b = edge.b, edge.a
  return graph

def write_hint(graph, out_file):
  out_file.write('graph {\n')
  for node in graph.nodes:
    out_file.write(f'    {node.id} [label={node.letter}];\n')
  for edge in graph.edges:
    out_file.write(f'    {edge.a.id} -- {edge.b.id};\n')
  out_file.write('}\n')


# def encrypt(num_words, secret):
#   password = generate_password(num_words)
#   hint = generate_hint(password)
#   with open('hint.dot', 'w') as hint_file:
#     write_hint(hint, hint_file)
#   filename = 'secret.age'
#   with open(filename, 'wb') as f:
#     f.write(passphrase.encrypt(secret, password))
#   print(f'Your secret is now inside password-protected file {filename}.')
#   print(f'Use the password {password} to access it.')
#   print(
#       'In case you forgot the password, maybe hint.dot will help your memory.')

from parse import parse

def read_graph():
  with open("hint.dot", "r") as f:
    for line in f.readlines()[1:-1]:
      print(line.strip())
      print(parse("{} [label={}];", line.strip()))

read_graph()