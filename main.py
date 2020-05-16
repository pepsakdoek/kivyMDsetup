from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu, RightContent
from kivy.properties import ObjectProperty
import time

import datatables as dt

class RightContentCls(RightContent):
    pass

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Tusk Inspection App"
        self.screen = Builder.load_file("main.kv")

        # Create this in Init because we can...
        componentgroupitems = [
            {"text": f"{i}"}
            for i in dt.componentgroups
        ]

        self.componentgroupmenu = MDDropdownMenu(
            caller=self.screen.ids.componentgroup,
            items=componentgroupitems,
            position="bottom",
            callback=self.setcomponentgroup,
            width_mult=4
        )
        projectgroupitems = [
            {"text":"Project 1"},{"text":"Project 2"}
        ]
        self.projectgroupmenu = MDDropdownMenu(
            caller=self.screen.ids.project,
            items=projectgroupitems,
            position="bottom",
            callback=self.setproject,
            width_mult=4
        )
        roomitems = [
            {"text": "Room 1"}, {"text": "Room 2"}
        ]
        self.roommenu = MDDropdownMenu(
            caller=self.screen.ids.room,
            items=roomitems,
            position="bottom",
            callback=self.setroom,
            width_mult=4
        )
        conditionitems = [
            {"text": "Excellent"}, {"text": "Good"}, {"text": "Fair"} , {"text": "Poor"} , {"text": "Very Poor"}
        ]
        self.conditionmenu = MDDropdownMenu(
            caller=self.screen.ids.condition,
            items=conditionitems,
            position="bottom",
            callback=self.setcondition,
            width_mult=4
        )


    def callprojectmenu(self):
        self.projectgroupmenu.open()

    def callroommenu(self):
        self.roommenu.open()

    def callcomponentgroupmenu(self):
        self.componentgroupmenu.open()

    def callcomponentmenu(self):
        if self.screen.ids.componentgroup.text in dt.components:
            self.componentmenu.open()

    def calldefectmenu(self):
        if self.screen.ids.component.text in dt.defecttypes:
            self.defectmenu.open()

    def callconditionmenu(self):
        self.conditionmenu.open()

    def setcomponentgroup(self, instance):
        # set the text to the selected itm
        self.screen.ids.componentgroup.text = instance.text
        print("set the component group to " + instance.text)

        # update the dropdown of the next menu as soon as we get the new value
        if self.screen.ids.componentgroup.text in dt.components:
            componentitems = dt.components[self.screen.ids.componentgroup.text]
            items = [{"text": f"{i}"}
                for i in componentitems
            ]
            #print("Created the component items")

            self.componentmenu = MDDropdownMenu(
                caller=self.screen.ids.component,
                items=items,
                position="bottom",
                callback=self.setcomponent,
                width_mult=4,
            )
            #print("Created the Content Menu Drop Down")
        else:
            print("Did not find the components for component group : " + instance.text)

    def setcomponent(self, instance):
        # update the dropdown of the next menu as soon as we get the new value
        self.screen.ids.component.text = instance.text

        if self.screen.ids.component.text in dt.defecttypes:
            defectitems = dt.defecttypes[self.screen.ids.component.text]
            items = [{"text": f"{i}"}
                for i in defectitems
            ]

            self.defectmenu = MDDropdownMenu(
                caller=self.screen.ids.defect,
                items=items,
                position="bottom",
                callback=self.setdefect,
                width_mult=4,
            )


    def setproject(self, instance):
        self.screen.ids.project.text = instance.text

    def setroom(self, instance):
        self.screen.ids.room.text = instance.text

    def setcondition(self, instance):
        self.screen.ids.condition.text = instance.text

    def setdefect(self, instance):
        self.screen.ids.defect.text = instance.text
        key = self.screen.ids.componentgroup.text + self.screen.ids.component.text + self.screen.ids.defect.text

        if key in dt.defectactions:
            self.screen.ids.action.text = dt.defectactions[key]

    def callcamera(self):
        print('calling camera')
        camera = self.screen.ids.cam
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("img_{}.png".format(timestr))

    def submitroom(self):
        print('submitting data to cloud/spreadsheet/database')

    def build(self):
        return self.screen


MainApp().run()
