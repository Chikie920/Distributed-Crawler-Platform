package com.chikie.service.impl;

import com.chikie.dao.TaskDao;
import com.chikie.entity.Task;
import com.chikie.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TaskServiceImpl implements TaskService {
    @Autowired
    private TaskDao taskDao;

    @Override
    public int updateRunTimes(String taskName) {
        return taskDao.updateRunTimes(taskName);
    }

    @Override
    public int createTask(Task task) {
        return taskDao.createTask(task);
    }

    @Override
    public List<String> getAllTaskName() {
        return taskDao.getAllTaskName();
    }

    @Override
    public int updateTask(Task task) {
        return taskDao.updateTask(task);
    }

    @Override
    public List<Task> getAllTasks() {
        return taskDao.getAllTasks();
    }
}
