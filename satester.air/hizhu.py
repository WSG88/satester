# -*- encoding=utf8 -*-
__author__ = "sa"

from airtest.core.api import *

auto_setup(__file__)

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

poco("com.loulifang.house:id/userName").set_text(18800191395)

sleep(1.0)

poco("com.loulifang.house:id/verCode").set_text(180205)
