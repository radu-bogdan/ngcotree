import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import ngsolve as ng

# Python program for Kruskal's algorithm to find 
# Minimum Spanning Trees of given connected or disconnected, 
# undirected graph, with edges provided as an Nx3 list

# Class to represent a graph 
class Graph: 
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = []
        self.MST = []
  
    def addEdges(self, edge_list): 
        for edge in edge_list:
            self.graph.append(tuple(edge))
  
    def find(self, parent, i):
        if parent[i] != i: 
            parent[i] = self.find(parent, parent[i]) 
        return parent[i]
  
    def union(self, parent, rank, x, y): 
        if rank[x] < rank[y]: 
            parent[x] = y 
        elif rank[x] > rank[y]: 
            parent[y] = x 
        else:
            parent[y] = x 
            rank[x] += 1
    
    def KruskalMST(self): 
        result = []
        
        parent = []
        rank = []
        for node in range(self.V): 
            parent.append(node) 
            rank.append(0)
        i = 0
        while i < len(self.graph): 
            u, v, idx = self.graph[i] 
            i += 1
            x = self.find(parent, u) 
            y = self.find(parent, v) 
            if x != y: 
                result.append([u,v,idx]) 
                self.union(parent, rank, x, y) 
        self.MST = result
        return self.MST

def CoTreeBitArray(mesh, HCurlfes, plot = False):
    
    ###################################################################
    # Preparing edge list appropriately
    ###################################################################
    i = 0; edges = []

    for edge in mesh.edges:
        index = HCurlfes.FreeDofs()[i]
        edge = [int(str(edge.vertices[0])[1:]), int(str(edge.vertices[1])[1:]), i]
        i = i + 1
        
        if HCurlfes.CouplingType(i) != ng.comp.COUPLING_TYPE.UNUSED_DOF:
            if index == 1:
                # Append only FreeDof edges.
                edges.append(edge)
            else:
                # Non-Freedof edges appended at start!
                edges.insert(0, edge)

    edges = np.array(edges)

    ###################################################################
    # Building tree
    ###################################################################
    g = Graph(mesh.nv)
    g.addEdges(edges)
    mst = g.KruskalMST()

    tree_indices = np.array(mst)[:,2]

    import pyngcore as pyng
    CoTreeBitArray = pyng.BitArray(HCurlfes.FreeDofs())
    for i,j in enumerate(tree_indices): CoTreeBitArray.Clear(j)

    if plot:
        points = []
        for vertex in mesh.vertices:
            points.append(list(vertex.point))
        points = np.array(points)
        nmst = np.array(mst)

        fig = plt.figure()
        if mesh.dim == 2:
            lc = LineCollection(points[nmst[:,:2]])
            plt.gca().add_collection(lc)
            plt.plot(points[:,0], points[:,1], 'r.')
        
        if mesh.dim == 3:
            ax = fig.add_subplot(projection='3d')
            edges = [(points[start], points[end]) for start, end in nmst[:,:2]]
            lc = Line3DCollection(edges)
            ax.add_collection(lc)
            ax.scatter(points[:,0], points[:,1], points[:,2], color = 'red')
            ax.set_axis_off()

            # Adjust the subplot to fill the figure
            fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
            # fig.set_aspect('equal', adjustable='box')

        plt.show()

    return CoTreeBitArray