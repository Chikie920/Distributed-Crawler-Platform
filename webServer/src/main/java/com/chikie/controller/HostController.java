package com.chikie.controller;

import com.chikie.entity.Host;
import com.chikie.service.HostService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin
@RestController
public class HostController {
    @Autowired
    private HostService hostService;

    @GetMapping("/host")
    public List<Host> getAllHosts() {
        System.out.println("Get All Hosts....");
        return hostService.getAllHosts();
    }

    @PutMapping("/host")
    public int updateHost(@RequestBody Host host) {
        System.out.println("Update Host....");
        return hostService.updateHost(host);
    }

    @DeleteMapping("/host/{id}")
    public int deleteHost(@PathVariable("id") String id) {
        System.out.println("Delete Host....");
        return hostService.deleteHost(id);
    }

    @PostMapping("/host")
    public int addHost(@RequestBody Host host) {
        System.out.println("Add Host....");
        System.out.println(host);
        return hostService.addHost(host);
    }
}
