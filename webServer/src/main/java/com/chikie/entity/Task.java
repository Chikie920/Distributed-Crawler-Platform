package com.chikie.entity;

public class Task {
    private String taskName;
    private String createTime;
    private String runTimes;

    public Task() {
    }

    public Task(String taskName, String createTime, String runTimes) {
        this.taskName = taskName;
        this.createTime = createTime;
        this.runTimes = runTimes;
    }

    public String getTaskName() {
        return taskName;
    }

    public void setTaskName(String taskName) {
        this.taskName = taskName;
    }

    public String getCreateTime() {
        return createTime;
    }

    public void setCreateTime(String createTime) {
        this.createTime = createTime;
    }

    public String getRunTimes() {
        return runTimes;
    }

    public void setRunTimes(String runTimes) {
        this.runTimes = runTimes;
    }

    @Override
    public String toString() {
        return "Task{" +
                "taskName='" + taskName + '\'' +
                ", createTime='" + createTime + '\'' +
                ", runTimes='" + runTimes + '\'' +
                '}';
    }
}
