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
    public List<Task> getAllTasks() {
        return taskDao.getAllTasks();
    }
}
