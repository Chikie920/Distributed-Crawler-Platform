package com.chikie.service;


import com.chikie.entity.User;
import java.util.List;

public interface UserService {
    public List<User> checkAll();
    public User checkOne(int id);
}
