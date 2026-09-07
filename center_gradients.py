import inkex
from lxml import etree

# Core function I want to achieve: 
# Group several objects
# assign one (1) gradient to the group 
# the extension should center them all to their objects, and scale them accordingly 
# resetting to object center: works but currently needs ungrouping ✔️ 
# scaled gradient: pending  ✖️  (gradient currently gets resized to former parent object) update: works in experiment 2d ✔️  

# Errors: 
# 1. For some reason, element.bounding_box().left procudes a scalar, top produces a tuple 'left=-0.00029229975262476393, top=(0.0,) '
# TODOs: 
# 1. In the cases I testes with one gradient for two objects, Inkscape seems to have copied the gradient by the time the extension ran. 
# I must look into this, how this is intended to be handled, maybe better create a copy inside the extension, to be safe. 
# 2. Oops, the attribute is: gradientTransform, not gradientTransformation. Must fix this. 

class CenterGradients(inkex.EffectExtension):

    def effect(self):
        # """Add a visible marker so the extension can be smoke-tested."""
        # marker = etree.SubElement(
        #     self.svg.get_current_layer(), inkex.addNS("circle", "svg")
        # )
        # marker.set("cx", "50")
        # marker.set("cy", "50")
        # marker.set("r", "10")
        # marker.set("style", "fill:#ff0066;stroke:#000000;stroke-width:1")
        # self.msg("Center Gradients test ran: added a pink circle.")

        """Actual code."""
        # get selected objects: 
        for element in self.svg.selection:  # self.svg.selection = Give me the objects the user selected. 
            style = element.style          
            fill = style.get("fill")

            self.msg(f"Selected: {element.tag.split('}')[-1]}") # split into an array, give me LAST ITEM in that list ([-1]). 
            self.msg(f"Selected: {element.tag}")

            if not fill or not fill.startswith("url("):
                continue    

            gradient_id = fill[5:-1]
            # use gradient id to find it using inkex
            gradient = self.svg.getElementById(gradient_id)

            # fx and fy specify the focal point of a radial gradient.
            # For a normal centered radial gradient, they usually match cx and cy.
            self.msg(f"Gradient element: {gradient.tag}")
            self.msg(f"cx={gradient.get('cx')}")
            self.msg(f"cy={gradient.get('cy')}")
            self.msg(f"r={gradient.get('r')}")
            self.msg(f"fx={gradient.get('fx')}")
            self.msg(f"fy={gradient.get('fy')}")
            self.msg(f"gradientUnits={gradient.get('gradientUnits')}")
            self.msg(f"gradientTransform={gradient.get('gradientTransform')}")

            self.msg(f"Gradient attributes: ")
            for key, value in gradient.attrib.items(): 
                self.msg(f"  {key} = {value}")

            self.msg(f"Fill: {style.get('fill')}")
            # bounding box has the transformed, rotated or nested object, better than directly reading cx, cy, rx, ry.
            bbox = element.bounding_box() 
            center_x = bbox.left + bbox.width / 2 
            center_y = bbox.top + bbox.height / 2 
            
            self.msg(
                f"left={bbox.left}, top={bbox.top,} "
                f"width={bbox.width}, height={bbox.height}"
            )
            self.msg(
                f"center_x={center_x}, center_y={center_y}"
            )

            """  Manipulate the object's gradient:  """
            self.msg("Output: ...")

            # if radial gradient:
                # center it
                # center its focal point
                # remove its transformation

            if gradient.tag != inkex.addNS("radialGradient", "svg"): 
                self.msg("Not a radial gradient, skipping")
                continue 

            # Center the gradient's center point and focal point, setting it to the object's center. 
            gradient.set("cx", str(center_x))
            gradient.set("cy", str(center_y))
            gradient.set("fx", str(center_x))
            gradient.set("fy", str(center_y))
            # removing the matrix seems a necessary step, otherwise, 
            # # the resetting to center points is not performed correctly (wrong scale -> wrong coordinate)
            gradient.attrib.pop("gradientTransform", None)

            # Experiment 1
            # Delete the Transformation Matrix, which centers the gradient and resets the handles
            # only run: gradient.attrib.pop("gradientTransform", None): 
            #gradient.attrib.pop("gradientTransform", None) # -> correctly places each gradient to the center point 
            # of their object, but scales the handles up to the size of the original (grouped) object, which is wrong for some parts. 
            # it should be set to the default size of the child object it belongs to (like, width/2 and height/2)

            # Experiment 2
            # #Replace the gradientTransform with the reset and scaled one

            # Experiment 2a
            # # This requires normalizing the radius to 1 
            # gradient.set("r", "1") # nope that doesn't work 
            # # scale gradient handles: 
            # gradient.set(
            #     "gradientTransformation", 
            #     f"matrix({bbox.width/2} 0 0 {bbox.height/2} {center_x} {center_y})"
            # ) # -> correctly places each gradient to the center point 
            # of their object, but scales the handles all he way down now, which is wrong. 
            # note that gradient.attrib.pop("gradientTransform", None) is necessar to run before. 

            # Experiment 2b
            # #Replace the gradientTransform with the reset and scaled one
            # This requires normalizing the radius to 1 
            # gradient.set("r", "1") # nope that doesn't work 
            # # scale gradient handles: 
            # gradient.set(
            #     "gradientTransformation", 
            #     f"matrix({1} 0 0 {1} 0 0)"
            # ) # same as above 

            # # Experiment 2c 
            # # # Replace the gradientTransform with the reset and scaled one
            # gradient.set("r", str(bbox.width/2))
            # radius = float(gradient.get("r"))
            # self.msg(f"radius saved as: {radius}")
            # gradient.set(
            #                 "gradientTransformation", 
            #                 f"matrix({bbox.width/2/radius} 0 0 {bbox.height/2/radius} {center_x} {center_y} )"
            #             ) 


            # Experiment 2d 🥴🎉
            rx = bbox.width / 2
            ry = bbox.height / 2

            gradient.set("cx", "0")
            gradient.set("cy", "0")
            gradient.set("fx", "0")
            gradient.set("fy", "0")
            gradient.set("r", "1")

            gradient.set(
                "gradientTransform",
                f"matrix({rx} 0 0 {ry} {center_x} {center_y})"
            ) # This one produces the desired result. 

            

            # Show all relevant values again: 
            self.msg(f"Gradient attributes after manipulation: ")
            for key, value in gradient.attrib.items(): 
                self.msg(f"  new  {key} = {value}")


            # helper point to indicate the middle 
            # marker = inkex.Circle()
            # marker.set("cx", str(center_x))
            # marker.set("cy", str(center_y))
            # marker.set("r", "1")
            # self.svg.get_current_layer().append(marker)

            


if __name__ == "__main__":
    CenterGradients().run()
