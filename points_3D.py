import numpy as np
import matplotlib.pyplot as plt

class Point():
    def __init__(self, x=0, y=0, z=0):
        self.xyz = np.array([x, y, z])
        self.x = x
        self.y = y
        self.z = z

    def basic_plot(self, ax):

        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_zlabel('z', fontsize=12)


    def plot_point(self, ax, col='r', size=5):
        self.basic_plot(ax)
        ax.plot3D(self.x, self.y, self.z, 'o', color=col, ms=size)


class Line():
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def plot_line(self, extend=True):
        # self.basic_plot()
        plt.plot([self.point1.x, self.point2.x], [self.point1.y, self.point2.y], 
                  ls='--', color='k', lw=0.5)
        
        if extend:
            x_disp = self.point2.x - self.point1.x 
            y_disp = self.point2.y - self.point1.y 
            
            plt.plot([self.point2.x, self.point2.x+x_disp], [self.point2.y, self.point2.y + y_disp], 
                  ls='--', color='k', lw=0.5)
        
    def isLeft(self, other_points):
        lefts = []

        for c in other_points:
            dist1 = (self.point2.x - self.point1.x)*(c.y - self.point1.y)
            dist2 = (self.point2.y - self.point1.y)*(c.x - self.point1.x)
            lefts.append(dist1 - dist2 > 0)
        
        return lefts
    
    def within(self, point_):

        eps = 0.00001

        cond1 = (self.point1.x+eps < point_.x) and (point_.x < self.point2.x-eps)
        cond2 = (self.point2.x+eps < point_.x) and (point_.x < self.point1.x-eps)
        cond3 = (self.point1.y+eps < point_.y) and (point_.y < self.point2.y-eps)
        cond4 = (self.point2.y+eps < point_.y) and (point_.y < self.point1.y-eps)

        return (cond1 or cond2) and (cond3 or cond4)
    
    def midpoint(self):
        p1 = self.point1
        p2 = self.point2
        return Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)
    


def intersect(line1, line2):

    a1 = [line1.point1.x, line1.point1.y]
    a2 = [line1.point2.x, line1.point2.y]
    b1 = [line2.point1.x, line2.point1.y]
    b2 = [line2.point2.x, line2.point2.y]

    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        raise ZeroDivisionError("division by zero")
    return Point(x/z, y/z)



class Plane():
    def __init__(self, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

        self.line1 = Line(point1, point2)
        self.line2 = Line(point2, point3)
        self.line3 = Line(point3, point1)

        self.normal = np.cross(point2.xyz-point1.xyz, point3.xyz-point1.xyz)

        self.centroid = np.mean(np.vstack([point1.xyz, point2.xyz, point3.xyz]), axis=0)


    def plot_plane(self, ax):

        X = np.array([self.point1.x, self.point2.x, self.point3.x])
        Y = np.array([self.point1.y, self.point2.y, self.point3.y])
        Z = np.array([self.point1.z, self.point2.z, self.point3.z])

        ax.plot_trisurf(X, Y, Z, color='grey')


    def plot_normal(self, ax):

        x = self.centroid[0]
        y = self.centroid[1]
        z = self.centroid[2]

        u = self.normal[0]
        v = self.normal[1]
        w = self.normal[2]

        ax.quiver(x, y, z, u, v, w, length=0.3)

    def plot_points(self, ax):
        self.point1.plot_point(ax)
        self.point2.plot_point(ax)
        self.point3.plot_point(ax)

    def isLeft(self, other_points):

        lefts = []

        for point_ in other_points:

            a = self.normal[0]
            b = self.normal[1]
            c = self.normal[2]
            d = -np.dot(np.array([a,b,c]), self.point1.xyz)

            x = point_.x
            y = point_.y
            z = point_.z

            lefts.append(np.dot((a,b,c,d), (x,y,z,1)) > 0)

        return lefts


