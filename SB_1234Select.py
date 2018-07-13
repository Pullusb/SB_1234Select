# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "1234Select",
    "author": "Samuel Bernou",
    "version": (1, 4),
    "blender": (2, 75, 0),
    "location": "View3D/UVeditor(editmode) > 1,2,3,4 keys",
    "description": "Quick switch for selection mode ",
    "warning": "Incompatible with emulate numpad",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy

mesh_sel_keymap = {
    'ONE': "True, False, False",
    'TWO': "False, True, False",
    'THREE': "False, False, True"
}

uv_sel_keymap = {
    'ONE': "VERTEX",
    'TWO': "EDGE",
    'THREE': "FACE",
    'FOUR': "ISLAND"
}

quickSelect_keymaps = [] # list of new custom keymap

def register():
    if not bpy.app.background:
        wm = bpy.context.window_manager

        # keymap set for view3D only in editmode
        #km = wm.keyconfigs.default.keymaps['Mesh']#not working for some users...
        km = wm.keyconfigs.addon.keymaps.new(name = "Mesh", space_type = "EMPTY")
        for k, v in mesh_sel_keymap.items():
            kmi = km.keymap_items.new('wm.context_set_value', k, 'PRESS')
            kmi.properties.data_path = 'tool_settings.mesh_select_mode'
            kmi.properties.value = v
            quickSelect_keymaps.append((km,kmi))

        kmi = km.keymap_items.new('wm.context_toggle', 'FOUR', 'PRESS')
        kmi.properties.data_path = 'space_data.use_occlude_geometry'
        quickSelect_keymaps.append((km,kmi))

        # keymap set for UVeditor
        #using default'UV Editor' doesn't work after a restart so creating a new km
        #km = wm.keyconfigs.default.keymaps['UV Editor']
        km = wm.keyconfigs.addon.keymaps.new('UV Editor', space_type='EMPTY', region_type='WINDOW')
        for k, v in uv_sel_keymap.items():
            kmi = km.keymap_items.new('wm.context_set_enum', k, 'PRESS')
            kmi.properties.data_path = 'tool_settings.uv_select_mode'
            kmi.properties.value = v
            quickSelect_keymaps.append((km,kmi))

def unregister():
    if not bpy.app.background:
        wm = bpy.context.window_manager
        # remove the keymap
        for km, kmi in quickSelect_keymaps:
            km.keymap_items.remove(kmi)
        # clear the list
        quickSelect_keymaps.clear()

if __name__ == "__main__":
    register()
