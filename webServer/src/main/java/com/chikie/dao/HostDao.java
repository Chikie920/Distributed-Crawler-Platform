package com.chikie.dao;

import com.chikie.entity.Host;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HostDao {
    @Select("SELECT * FROM host")
    List<Host> getAllHosts();

    @Update("UPDATE host SET ip = #{ip}, port = #{port} WHERE id = #{id}")
    int updateHost(Host host);

    @Delete("DELETE FROM host WHERE id = #{id}")
    int deleteHost(String id);

    @Insert("INSERT INTO host (id, ip, port) VALUES(#{id}, #{ip}, #{port})")
    int addHost(Host host);
}
