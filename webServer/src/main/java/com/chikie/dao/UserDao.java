package com.chikie.dao;

import com.chikie.entity.User;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserDao {

    @Select("SELECT * FROM user")
    public List<User> selectAllUsers();

    @Select("SELECT * FROM user WHERE id = #{id}")
    public User selectOneUser(int id);
}
