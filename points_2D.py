class Point():
    def __init__(self, x=0, y=0):
        self.xy_value = np.array([x, y])
        self.x = x
        self.y = y
        self.line_angle1 = 1
        self.line_angle2 = 1

    def basic_plot(self, title="Unit Square"):
        plt.title(title)
        plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xlim([0,1])
        plt.ylim([0,1])

    def plot_point(self, col='r', size=5):
        self.basic_plot()
        plt.plot(self.x, self.y, 'o', color=col, ms=size)


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
        return point((p1.x+p2.x)/2, (p1.y+p2.y)/2)
    


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
        return (float('inf'), float('inf'))
    return point(x/z, y/z)


