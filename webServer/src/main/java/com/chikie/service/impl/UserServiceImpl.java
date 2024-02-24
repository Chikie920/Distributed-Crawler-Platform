package com.chikie.service.impl;

import com.chikie.dao.UserDao;
import com.chikie.entity.User;
import com.chikie.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserDao userDao;
    @Override
    public List<User> checkAll() {
        return userDao.selectAllUsers();
    }
    @Override
    public User checkOne(int id) {
        return userDao.selectOneUser(id);
    }
}
