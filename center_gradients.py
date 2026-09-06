import inkex
from lxml import etree

# Errors: 
# 1. For some reason, element.bounding_box().left procudes a scalar, top produces a tuple 'left=-0.00029229975262476393, top=(0.0,) '

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

            self.msg(f"Gradient element: {gradient.tag}")
            self.msg(f"cx={gradient.get('cx')}")
            self.msg(f"cy={gradient.get('cy')}")
            self.msg(f"r={gradient.get('r')}")
            self.msg(f"fx={gradient.get('fx')}")
            self.msg(f"fy={gradient.get('fy')}")
            self.msg(f"gradientUnits={gradient.get('gradientUnits')}")
            self.msg(f"gradientTransform={gradient.get('gradientTransform')}")

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

            # helper point to indicate the middle 
            marker = inkex.Circle()
            marker.set("cx", str(center_x))
            marker.set("cy", str(center_y))
            marker.set("r", "1")
            self.svg.get_current_layer().append(marker)

            


if __name__ == "__main__":
    CenterGradients().run()
