# -*- encoding=utf8 -*-
__author__ = "sa"

from airtest.core.api import *

auto_setup(__file__)
touch(Template(r"tpl1537926930039.png", record_pos=(-0.361, 0.808), resolution=(1080, 1920)))
sleep(1.0)

touch(Template(r"tpl1537926938535.png", record_pos=(-0.11, 0.806), resolution=(1080, 1920)))
sleep(1.0)
touch(Template(r"tpl1537926943572.png", record_pos=(0.135, 0.808), resolution=(1080, 1920)))
sleep(5.0)
touch(Template(r"tpl1537926948015.png", record_pos=(0.392, 0.816), resolution=(1080, 1920)))
sleep(1.0)
touch(Template(r"tpl1537927085016.png", record_pos=(-0.152, -0.597), resolution=(1080, 1920)))

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

poco("com.loulifang.house:id/userName").set_text(18800191395)

poco("com.loulifang.house:id/verCode").set_text(180205)



touch(Template(r"tpl1537927129711.png", record_pos=(-0.014, 0.174), resolution=(1080, 1920)))


touch(Template(r"tpl1537926930039.png", record_pos=(-0.361, 0.808), resolution=(1080, 1920)))
sleep(1.0)




