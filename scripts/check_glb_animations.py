#!/usr/bin/env python3
"""Script to check for animations in GLB files."""

import sys
from pygltflib import GLTF2

def check_glb_animations(glb_path):
    """Check for animations in a GLB file."""

    print(f"\n{'='*60}")
    print(f"CHECKING: {glb_path}")
    print('='*60)

    gltf = GLTF2().load(glb_path)

    # Check for animations
    print("\n--- ANIMATIONS ---")
    if gltf.animations:
        print(f"Found {len(gltf.animations)} animation(s):")
        for i, anim in enumerate(gltf.animations):
            print(f"\n  Animation {i}: '{anim.name}'")
            print(f"    Channels: {len(anim.channels)}")
            print(f"    Samplers: {len(anim.samplers)}")
            for j, channel in enumerate(anim.channels):
                node_idx = channel.target.node
                node_name = gltf.nodes[node_idx].name if node_idx is not None else "Unknown"
                print(f"      Channel {j}: Node '{node_name}' - {channel.target.path}")
    else:
        print("No animations found in the GLB file.")

    # Look for door-related nodes
    print("\n--- DOOR-RELATED NODES ---")
    door_nodes = []
    for i, node in enumerate(gltf.nodes):
        if node.name and 'door' in node.name.lower():
            door_nodes.append((i, node))

    if door_nodes:
        for idx, node in door_nodes:
            print(f"\n  Node {idx}: '{node.name}'")
            print(f"    Translation: {node.translation}")
            print(f"    Rotation: {node.rotation}")
            print(f"    Scale: {node.scale}")
            if node.children:
                print(f"    Children: {len(node.children)} nodes")
    else:
        print("No door-related nodes found.")

    # Look for pivot nodes
    print("\n--- PIVOT NODES ---")
    pivot_nodes = []
    for i, node in enumerate(gltf.nodes):
        if node.name and 'pivot' in node.name.lower():
            pivot_nodes.append((i, node))

    if pivot_nodes:
        for idx, node in pivot_nodes:
            print(f"\n  Node {idx}: '{node.name}'")
            print(f"    Translation: {node.translation}")
            print(f"    Rotation: {node.rotation}")
            if node.children:
                print(f"    Children: {len(node.children)} child nodes")
                # List some children
                for child_idx in node.children[:5]:
                    child = gltf.nodes[child_idx]
                    print(f"      - '{child.name}'")
                if len(node.children) > 5:
                    print(f"      ... and {len(node.children) - 5} more")
    else:
        print("No pivot nodes found.")

    # Summary of all nodes
    print(f"\n--- SUMMARY ---")
    print(f"Total nodes: {len(gltf.nodes)}")
    print(f"Total meshes: {len(gltf.meshes) if gltf.meshes else 0}")
    print(f"Total materials: {len(gltf.materials) if gltf.materials else 0}")
    print(f"Total animations: {len(gltf.animations) if gltf.animations else 0}")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_glb_animations(sys.argv[1])
    else:
        # Check the latest GLB
        check_glb_animations("/home/user/creepy-building-blender-automated/exports/glb/building_phase_2_iter_001.glb")
