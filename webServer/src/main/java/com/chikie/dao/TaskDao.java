package com.chikie.dao;

import com.chikie.entity.Task;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TaskDao {
    @Select("SELECT task_name taskName, create_time createTime, run_times runTimes, data_counts dataCounts FROM task")
    List<Task> getAllTasks();
}
