package com.chikie.controller;

import com.chikie.entity.Setting;
import com.chikie.service.SettingService;
import com.sun.tools.jconsole.JConsoleContext;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@CrossOrigin
@RestController
public class SettingController {
    @Autowired
    private SettingService settingService;
    @GetMapping("/setting")
    Setting getSetting(){
        System.out.println("GetSetting....");
        return  settingService.getSetting();
    }

    @PutMapping("/setting")
    int updateSetting(@RequestBody Setting setting) {
        System.out.println("PutSetting....");
        System.out.println(setting);
        return settingService.updateSetting(setting);
    }
}
