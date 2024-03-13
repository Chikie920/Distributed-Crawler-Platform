package com.chikie.dao;

import com.chikie.entity.Task;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TaskDao {
    @Select("SELECT task_name taskName, create_time createTime, run_times runTimes FROM task")
    List<Task> getAllTasks();

    @Select("SELECT task_name FROM task")
    List<String> getAllTaskName();

    @Insert("INSERT INTO task(task_name, create_time, run_times) VALUES(#{taskName}, #{createTime}, #{runTimes})")
    int createTask(Task task);

    @Update("UPDATE task SET run_times = #{runTimes} WHERE task_name = #{taskName}")
    int updateTask(Task task);

    @Update("UPDATE task SET run_times = run_times+1 WHERE task_name = #{taskName}")
    int updateRunTimes(String taskName);
}
