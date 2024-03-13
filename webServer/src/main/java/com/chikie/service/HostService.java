package com.chikie.service;

import com.chikie.entity.Host;
import org.springframework.stereotype.Service;

import java.util.List;

public interface HostService {
    List<Host> getAllHosts();
    int updateHost(Host host);
    int deleteHost(String id);
    int addHost(Host host);
}
