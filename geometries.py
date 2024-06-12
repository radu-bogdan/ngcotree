from netgen.geom2d import CSG2d, Circle, Rectangle
from netgen.geom2d import EdgeInfo as EI, PointInfo as PI, Solid2d
from netgen.geom2d import SplineGeometry


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