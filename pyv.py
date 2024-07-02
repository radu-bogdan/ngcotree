import vtk
import ngsolve as ng
import numpy as np

def createVTK(mesh):
    
    points = vtk.vtkPoints()
    grid = vtk.vtkUnstructuredGrid()

    p0 = int(str(mesh.vertices[0])[1:])
    p1 = int(str(mesh.vertices[0])[1:])
    p2 = int(str(mesh.vertices[0])[1:])

    # for i in range(mesh.nv): points.InsertPoint(i, (mesh.p[i,0], mesh.p[i,1], mesh.p[i,2]))
    for i in range(mesh.nv): points.InsertPoint(i, (p0,p1,p2))
    
    def create_cell(i):
        tetra = vtk.vtkTetra()
        ids = tetra.GetPointIds()
        t0 = int(str(list(mesh.Elements(ng.VOL))[i].vertices[0])[1:])
        t1 = int(str(list(mesh.Elements(ng.VOL))[i].vertices[1])[1:])
        t2 = int(str(list(mesh.Elements(ng.VOL))[i].vertices[2])[1:])
        t3 = int(str(list(mesh.Elements(ng.VOL))[i].vertices[3])[1:])
        ids.SetId(0, t0)
        ids.SetId(1, t1)
        ids.SetId(2, t2)
        ids.SetId(3, t3)
        return tetra

    elems = [create_cell(i) for i in range(mesh.ne)]
    grid.Allocate(mesh.ne, 1)
    grid.SetPoints(points)

    for elem in elems: grid.InsertNextCell(elem.GetCellType(), elem.GetPointIds())

    scalars = mesh.ngmesh.Elements2D().NumPy()['index'].astype(np.uint64).shape
    data = vtk.vtkDoubleArray()
    data.SetNumberOfValues(mesh.ne)
    for i,p in enumerate(scalars): data.SetValue(i,p)
    grid.GetCellData().SetScalars(data)
    
    return grid


# def add_H1_Scalar(grid,x,name):
#     np = grid.GetPoints().GetNumberOfPoints()
#     vecJ = vtk.vtkFloatArray()
#     vecJ.SetNumberOfValues(np)
#     vecJ.SetNumberOfComponents(1)
#     for i in range(np):
#         vecJ.SetValue(i,x[i])
#     vecJ.SetName(name)
#     grid.GetPointData().AddArray(vecJ)


# def add_L2_Vector(grid,x,y,z,name):
#     nt = grid.GetCells().GetNumberOfCells()
#     vecJ = vtk.vtkFloatArray()
#     vecJ.SetNumberOfComponents(3)
#     for i in range(nt):
#         vecJ.InsertNextTuple([x[i],y[i],z[i]])
#     vecJ.SetName(name)
#     grid.GetCellData().AddArray(vecJ)


# def add_L2_Scalar(grid,x,name):
#     nt = grid.GetCells().GetNumberOfCells()
#     vecJ = vtk.vtkFloatArray()
#     vecJ.SetNumberOfComponents(1)
#     for i in range(nt):
#         vecJ.InsertNextTuple([x[i]])
#     vecJ.SetName(name)
#     grid.GetCellData().AddArray(vecJ)
    
def writeVTK(grid,name):
    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetFileName(name)
    writer.SetInputData(grid)
    writer.Write()