package com.chikie.service.impl;

import com.chikie.dao.HostDao;
import com.chikie.entity.Host;
import com.chikie.service.HostService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HostServiceImpl implements HostService {
    @Autowired
    private HostDao hostDao;
    @Override
    public List<Host> getAllHosts() {
        return hostDao.getAllHosts();
    }

    @Override
    public int updateHost(Host host) {
        return hostDao.updateHost(host);
    }

    @Override
    public int deleteHost(String id) {
        return hostDao.deleteHost(id);
    }

    @Override
    public int addHost(Host host) {
        return hostDao.addHost(host);
    }
}
