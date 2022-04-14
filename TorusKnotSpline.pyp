"""
  author  : Jose Murillo
  version : 1.0.0
  website : https://josemurillo.com
"""


import os
import c4d
from c4d import plugins, bitmaps, Vector, SplineObject
from math import cos, sin, pi


class TorusKnotSpline (plugins.ObjectData):

    def __init__ (self):
        self.SetOptimizeCache(True)

    def Init(self, node):
        # Parameter initialization
        self.InitAttr(node, float, [c4d.KNOT_PARAM_RADIUS])
        self.InitAttr(node, float, [c4d.KNOT_PARAM_TUBULAR])
        self.InitAttr(node, float, [c4d.KNOT_PARAM_P])
        self.InitAttr(node, float, [c4d.KNOT_PARAM_Q])

        self.InitAttr(node, bool, [c4d.KNOT_CUBIC_INTERPOLATION])
        self.InitAttr(node, bool, [c4d.KNOT_CLOSE_SPLINE])

        self.InitAttr(node, str, [c4d.KNOT_POINT_COUNT])

        # Set default values
        node[c4d.KNOT_PARAM_RADIUS] = 10.0
        node[c4d.KNOT_PARAM_TUBULAR] = 64.0
        node[c4d.KNOT_PARAM_P] = 2.0
        node[c4d.KNOT_PARAM_Q] = 3.0

        node[c4d.KNOT_CUBIC_INTERPOLATION] = False
        node[c4d.KNOT_CLOSE_SPLINE] = True

        node[c4d.KNOT_POINT_COUNT] = '0'

        return True

    def GetVirtualObjects(self, op, hh):
        # Retreive UI data values
        is_cubic = op[c4d.KNOT_CUBIC_INTERPOLATION]

        radius = op[c4d.KNOT_PARAM_RADIUS]
        tubular_segments = op[c4d.KNOT_PARAM_TUBULAR]
        p = op[c4d.KNOT_PARAM_P]
        q = op[c4d.KNOT_PARAM_Q]

        # Calculate all points' position
        points = []
        t = 0
        while t < tubular_segments:
            u = t / tubular_segments * p * pi * 2
            cu = cos( u )
            su = sin( u )
            quOverP = q / p * u
            cs = cos( quOverP )
            x = radius * ( 2 + cs ) * 0.5 * cu
            y = radius * ( 2 + cs ) * su * 0.5
            z = radius * sin( quOverP ) * 0.5
            points.append(Vector(x, y, z))
            t += 1

        # Spline initialization
        point_count = len(points)
        spline_type = c4d.SPLINETYPE_CUBIC if is_cubic else c4d.SPLINETYPE_LINEAR
        spline = SplineObject(point_count, spline_type)

        if spline is None: return

        # Update spline points
        for index, point in enumerate(points):
            spline.SetPoint(index, point)

        # Update UI point count
        op[c4d.KNOT_POINT_COUNT] = str(point_count)

        # Close the spline if needed
        spline[c4d.SPLINEOBJECT_CLOSED] = op[c4d.KNOT_CLOSE_SPLINE]

        # Send update message
        spline.Message(c4d.MSG_UPDATE)

        return spline


if __name__ == "__main__":
    # Load the plugin icon
    icon_absolute_path = os.path.join(os.path.dirname(__file__), 'res/icons', 'knot.png')
    plugin_icon = bitmaps.BaseBitmap()
    plugin_icon.InitWith(icon_absolute_path)

    # Register the plugin
    plugins.RegisterObjectPlugin(
        id = 1053564,
        str = 'Torus Knot Spline',
        g =  TorusKnotSpline,
        description = 'Oknot',
        info = c4d.OBJECT_GENERATOR | c4d.OBJECT_ISSPLINE,
        icon = plugin_icon
    )
