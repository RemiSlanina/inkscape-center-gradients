# Inkscape Center Gradients

> WIP: An experimental Inkscape extension for centering radial gradients on selected objects.

Core function I want to achieve:
Group several objects assign one (1) gradient to the group the extension should center them all to their objects, and scale them accordingly. Which it does, surprisingly.

## Current state

- Finds selected objects.
- Finds their fill.
- Detects radial gradients.
- Skips linear gradients.
- Calculates the object's bounding-box center.
- Sets `cx`, `cy`, `fx`, and `fy` to the object's center.

- centers radial gradients
- resets focal point
- removes previous gradient transform
- normalizes the gradient radius to 1
- reconstructs gradientTransform from object geometry
- works on individual selected objects
- linear gradients are skipped
- groups are not yet recursively processed
- Works on multiple selected objects.

- Currently operates on directly selected objects, not the individual objects inside a selected group.

## Next steps

1. Decide how to resize the radial gradient to approximately the object's size.
2. Test different object sizes/aspect ratios.
3. Handle groups by recursively processing their child objects.
4. Investigate shared gradient definitions.
5. Deal properly with transformed gradients instead of simply removing `gradientTransform`.

## Notes

The current approach deliberately resets transformed radial gradients to a simple untransformed radial gradient.

`element.bounding_box()` gives the approximate object bounds used to calculate the center.

## Output

Output something like

![Screenshot 1](/assets/screenshots/early-screenshot-1.png)
-->
![Screenshot 2](/assets/screenshots/early-screenshot-2.png)

## Next steps

- work on groups (without prior ungrouping)
- make another version that changes colors while preserving edits to gradients (scaling, rotating, ...)
