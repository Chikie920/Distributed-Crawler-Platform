package com.chikie.service;

import com.chikie.entity.Task;

import java.util.List;

public interface TaskService {
    List<Task> getAllTasks(); // 获取所有任务信息
    int createTask(Task task); // 创建任务
    int updateTask(Task task); // 更新任务
    List<String> getAllTaskName(); // 获取所有任务名
    int updateRunTimes(String taskName); // 运行次数加一
}
