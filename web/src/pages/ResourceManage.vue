<template>
    <mdui-layout full-height>
        <mdui-layout-main class="resourceManageContainer table-responsive">
            <h1>Task Information</h1>

            <table class="table table-hover table-condensed">
                <thead>
                    <tr>
                        <th>Task Name</th>
                        <th>Create Time</th>
                        <th>Run Times</th>
                        <th>Data Counts</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="task, idx in task_list" :key="idx">
                        <td @click="selectTask(task.taskName)"><u>{{ task.taskName }}</u></td>
                        <td>{{ task.createTime }}</td>
                        <td>{{ task.runTimes }}</td>
                        <td>{{ task.dataCounts }}</td>
                    </tr>

                </tbody>
            </table>

            <h6 v-if="taskCounts == 0" class="text-center">暂无数据</h6>

            <h1 style="margin-top: 20vh;">Task Data</h1>

            <!-- 新闻展示表格 -->
            <table class="table table-hover table-condensed">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Url</th>
                        <th>Date</th>
                        <th>Content</th>
                        <th>OPeration</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="news, idx in news_list" :key="idx">
                        <td>
                            <span class="d-inline-block text-truncate" style="max-width: 200px;">
                                {{ news.title }}
                            </span>

                        </td>
                        <td><a class="d-inline-block text-truncate" style="max-width: 200px;">URL
                                https://www.bilibili.com/video/BV1Za4y1r7KE/?spm_id_from=333.337.search-card.all.click&vd_source=8b25b2877285ef96d28dc58462081a5a</a>
                        </td>
                        <td>{{ news.date }}</td>
                        <td>
                            <span class="d-inline-block text-truncate" style="max-width: 300px;">
                                {{ news.content }}
                            </span>
                        </td>
                        <td><a @click="modify_click(idx)">编辑</a><a @click="delete_operate(idx)"
                                style="margin-left: 1rem;">删除</a></td>
                    </tr>
                </tbody>
            </table>

            <h6 v-if="dataCounts == 0" class="text-center">暂无数据</h6>

            <!-- 操作对话框 -->
            <mdui-dialog v-if="index != -1" ref="dialog" fullscreen close-on-overlay-click headline="数据编辑"
                class="example-action">
                <h5>Title</h5>
                <mdui-text-field v-model="news_list[index].title"></mdui-text-field>
                <h5>Url</h5>
                <mdui-text-field placeholder="news_list[index].Url"></mdui-text-field>
                <h5>Date</h5>
                <mdui-text-field v-model="news_list[index].date"></mdui-text-field>
                <h5>Content</h5>
                <mdui-text-field rows="5" v-model="news_list[index].content"></mdui-text-field>
                <mdui-button @click="cancel_operate" slot="action" variant="tonal">取消</mdui-button>
                <mdui-button @click="save_operate" slot="action" variant="tonal">保存</mdui-button>
            </mdui-dialog>

            <!-- 消息提示 -->
            <mdui-snackbar ref="snackbar_success" placement="top" auto-close-delay="1000"
                class="example-close-delay">操作成功!</mdui-snackbar>
            <mdui-snackbar ref="snackbar_fail" placement="top" auto-close-delay="1000"
                class="example-close-delay">操作失败!</mdui-snackbar>

        </mdui-layout-main>
    </mdui-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import 'mdui/components/layout.js';
import 'mdui/components/layout-item.js';
import 'mdui/components/layout-main.js';
import 'mdui/components/button.js';
import 'mdui/components/dialog.js';
import 'mdui/components/text-field.js';
import 'mdui/components/snackbar.js';

let news_list = ref(); // 存储新闻数组
let task_list = ref(); // 存储任务数组
let dialog = ref(); // 获取dom元素-对话框
let index = ref(-1); // 用于dialog根据下标确定数据
let snackbar_success = ref() // 操作结果提示消息条-操作成功
let snackbar_fail = ref() // 操作结果提示消息条-操作失败
let taskCounts = ref(0); // 记录任务个数
let dataCounts = ref(0); // 记录数据个数

function modify_click(idx) { // 数据编辑操作点击事件
    // console.log(modify.value[idx])
    // console.log(dialog.value)
    index.value = idx;
    dialog.value.open = true;
}

function cancel_operate() { // 取消编辑操作
    dialog.value.open = false;
}

function save_operate() { // 提交数据更新
    let Data = {
        "id": news_list.value[index.value].id,
        "title": news_list.value[index.value].title,
        "date": news_list.value[index.value].date,
        "content": news_list.value[index.value].content
    };
    axios.put('http://localhost:8080/resmag', Data, {
        headers: { 'Content-Type': 'application/json' },
    }).then(function (response) {
        // 请求成功
        // console.log("*****save*****");
        // console.log(response.data);
        if (response.data == 1) {
            snackbar_success.value.open = true;
        } else {
            snackbar_fail.value.open = true;
        }
    })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        }); // 获取新闻数据
    dialog.value.open = false;
}

function delete_operate(idx) {
    axios.delete('http://localhost:8080/resmag/' + news_list.value[idx].id)
        .then(function (response) {
            // 请求成功
            news_list.value = news_list.value.splice(idx + 1);
            if (response.data == 1) {
                snackbar_success.value.open = true;
            } else {
                snackbar_fail.value.open = true;
            }
        })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        }); // 获取新闻数据
}

function selectTask(taskName) {
    axios.get('http://localhost:8080/resmag/'+taskName)
        .then(function (response) {
            // 请求成功
            news_list.value = response.data;
            dataCounts.value = news_list.value.length;
            // console.log(news_list.value[0].id)
        })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        }); // 根据任务名称获取新闻数据
} // 选中任务事件

onMounted(() => { // 钩子函数，页面挂载到DOM完成后调用
    axios.get('http://localhost:8080/resmag')
        .then(function (response) {
            // 请求成功
            news_list.value = response.data;
            dataCounts.value = news_list.value.length;
            // console.log(news_list.value[0].id)
        })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        }); // 获取新闻数据

    axios.get('http://localhost:8080/task')
        .then(function (response) {
            // 请求成功
            task_list.value = response.data;
            taskCounts.value = task_list.value.length;
            // console.log(news_list.value[0].id)
        })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        }); // 获取任务数据
})
</script>

<style scoped>
mdui-dialog::part(panel) {
    background-color: #fafdfd;
}

mdui-button {
    background-color: #e8ecef;
}

mdui-text-field::part(container) {
    background-color: #e0eee8;
}

th,
h5,
mdui-dialog {
    font-weight: 600;
}

h5 {
    margin-top: 1.5rem;
}
</style>