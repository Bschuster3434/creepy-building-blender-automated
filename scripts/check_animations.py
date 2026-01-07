#!/usr/bin/env python3
"""Script to check for animations in the Blender file."""

import bpy
import sys

def check_animations():
    """Check for animations in the current Blender file."""

    print("\n" + "="*60)
    print("ANIMATION CHECK REPORT")
    print("="*60)

    # Check for actions (animation data)
    print("\n--- ACTIONS (Animations) ---")
    if bpy.data.actions:
        for action in bpy.data.actions:
            print(f"\nAction: '{action.name}'")
            print(f"  Frame range: {action.frame_range[0]:.0f} - {action.frame_range[1]:.0f}")
            print(f"  FCurves (animated properties): {len(action.fcurves)}")
            for fcurve in action.fcurves:
                print(f"    - {fcurve.data_path} [{fcurve.array_index}]: {len(fcurve.keyframe_points)} keyframes")
    else:
        print("No actions found in the file.")

    # Check for objects with animation data
    print("\n--- OBJECTS WITH ANIMATION DATA ---")
    animated_objects = []
    for obj in bpy.data.objects:
        if obj.animation_data:
            animated_objects.append(obj)
            print(f"\nObject: '{obj.name}'")
            if obj.animation_data.action:
                print(f"  Active action: '{obj.animation_data.action.name}'")
            if obj.animation_data.nla_tracks:
                print(f"  NLA tracks: {len(obj.animation_data.nla_tracks)}")
                for track in obj.animation_data.nla_tracks:
                    print(f"    - Track: '{track.name}'")
                    for strip in track.strips:
                        print(f"      Strip: '{strip.name}' (action: {strip.action.name if strip.action else 'None'})")

    if not animated_objects:
        print("No objects with animation data found.")

    # Specifically look for door objects
    print("\n--- DOOR-RELATED OBJECTS ---")
    door_objects = [obj for obj in bpy.data.objects if 'door' in obj.name.lower()]
    if door_objects:
        for obj in door_objects:
            print(f"\nDoor object: '{obj.name}'")
            print(f"  Type: {obj.type}")
            print(f"  Location: {obj.location[:]}")
            print(f"  Rotation: {[round(r, 3) for r in obj.rotation_euler[:]]}")
            if obj.animation_data:
                print(f"  Has animation data: YES")
                if obj.animation_data.action:
                    print(f"  Active action: '{obj.animation_data.action.name}'")
            else:
                print(f"  Has animation data: NO")

            # Check if it's part of a collection that might indicate front/back
            for coll in obj.users_collection:
                print(f"  Collection: '{coll.name}'")
    else:
        print("No door objects found in the file.")

    # Check scene timeline settings
    print("\n--- SCENE TIMELINE ---")
    scene = bpy.context.scene
    print(f"Frame start: {scene.frame_start}")
    print(f"Frame end: {scene.frame_end}")
    print(f"Current frame: {scene.frame_current}")
    print(f"FPS: {scene.render.fps}")

    # List all objects for reference
    print("\n--- ALL OBJECTS IN SCENE ---")
    for obj in bpy.data.objects:
        parent_info = f" (parent: {obj.parent.name})" if obj.parent else ""
        print(f"  {obj.name} [{obj.type}]{parent_info}")

    print("\n" + "="*60)
    print("END OF REPORT")
    print("="*60 + "\n")

if __name__ == "__main__":
    check_animations()
