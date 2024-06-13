from netgen.geom2d import CSG2d, Circle, Rectangle
from netgen.geom2d import EdgeInfo as EI, PointInfo as PI, Solid2d
from netgen.geom2d import SplineGeometry
import netgen.occ as occ

def magneticWire(r1 = 0.01, r2 = 0.02, r3 = 0.03, r4 = 0.04):
    geo = SplineGeometry()
    geo.AddCircle(c=(0,0),r=r4 ,leftdomain=1, rightdomain=0, bc = "out")
    geo.AddCircle(c=(0,0),r=r3 ,leftdomain=2, rightdomain=1)
    geo.AddCircle(c=(0,0),r=r2 ,leftdomain=3, rightdomain=2)
    geo.AddCircle(c=(0,0),r=r1 ,leftdomain=4, rightdomain=3)
    
    geo.SetMaterial (1, "air")
    geo.SetMaterial (2, "copper")
    geo.SetMaterial (3, "air")
    geo.SetMaterial (4, "iron")
    return geo


def inductance(hmin=0.1):
    inch2m = 0.0254
    hairgap = hmin*5
    hiron = 5*hairgap;
    hout = 20*hiron
    depth = 1;
    
    R = 1.2*inch2m

    x0 = 0*inch2m
    y0 = (-2.750000e-1+0.75)/2*inch2m
    z0 = depth/2*inch2m
    
    out1 = occ.Sphere((x0,y0,z0),R);
    
    big_box = occ.Box(occ.Pnt(x0, y0-100*inch2m, z0), 
                      occ.Pnt(x0+100*inch2m, y0+100*inch2m, z0+100*inch2m))
    bb1 = big_box*out1 

    coil_ext = occ.Box(occ.Pnt(5.000000e-1*inch2m, 0*inch2m, (depth+2.5e-1)*inch2m),
                       occ.Pnt(0, 5.000000e-1*inch2m, depth*inch2m))
    coil_int = occ.Box(occ.Pnt(5.000000e-1*inch2m, 0*inch2m, depth*inch2m),
                       occ.Pnt(2.500000e-1*inch2m, 5.000000e-1*inch2m, depth/2*inch2m))
    coil = coil_ext + coil_int
    bar = occ.Box(occ.Pnt(7.500000e-1*inch2m, -2.750000e-1*inch2m, depth*inch2m),
                  occ.Pnt(0, -2.500000e-02*inch2m, depth/2*inch2m))
    airgap = occ.Box(occ.Pnt(7.500000e-1*inch2m, -2.500000e-02*inch2m, depth*inch2m),
                     occ.Pnt(0, 0*inch2m, depth/2*inch2m))

    core = occ.Box(occ.Pnt(7.500000e-1*inch2m, 0*inch2m, depth*inch2m),
                   occ.Pnt(0, 7.500000e-1*inch2m, depth/2*inch2m))
    core = core - coil
    outer_box = bb1 - coil - bar - airgap - core

    # mesh size
    bar.maxh = hiron ; core.maxh = hiron ; coil.maxh = hiron ; airgap.maxh = hairgap
    
    outer_box.maxh = hout
    
    airgap.mat("Airgap")
    bar.mat("Bar")
    core.mat("Core")
    coil.mat("Coil")
    outer_box.mat("Out") 
    full = occ.Glue([bar, core, airgap, coil, outer_box])

    # identification of faces
    full.faces[25].name = "currentInput"
    full.faces[35].name = "currentOutput"
    
    antiSymmetryFaces = [0, 6, 17, 36, 4, 11, 23, 45]
    for i in antiSymmetryFaces : full.faces[i].name = "antiSymmetry"
    full.faces[46].name = "out"; full.faces[47].name = "out"
    full.faces[27].name = "botCoil" ;  full.faces[41].name = "botCoil"
    full.faces[30].name = "topCoil" ;  full.faces[39].name = "topCoil"
    full.faces[32].name = "outCoil" ;  full.faces[49].name = "outCoil"; 
    full.faces[40].name = "outCoil"
    full.faces[31].name = "intCoil" ;  full.faces[34].name = "intCoil"

    #for i in range(len(full.faces)): full.faces[i].name = str(i)
    #for i in range(len(full.edges)): full.edges[i].name = str(i)
        
    geoOCC = occ.OCCGeometry(full)  
    return geoOCC