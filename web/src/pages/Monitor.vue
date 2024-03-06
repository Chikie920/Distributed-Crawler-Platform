<template>
    <h2 style="margin-top: 0;">数据概况</h2>

    <h2>主机管理</h2>
    <!-- <div class="row" style="width: 100%;">
        <div class="col-md-2">
            <mdui-card clickable variant="filled" style="width: 200px;height: 124px;background-color: #84b9cb;">
                <h5 class="text-center">主机总数</h5>
                <h1 class="text-center">1</h1>
            </mdui-card>
        </div>
        <div class="col-md-2">
            <mdui-card clickable variant="filled" style="width: 200px;height: 124px;background-color: #99CC99;">
                <h5 class="text-center">已连接主机</h5>
                <h1 class="text-center">1</h1>
            </mdui-card>
        </div>
        <div class="col-md-2">
            <mdui-card clickable variant="filled" style="width: 200px;height: 124px;background-color: #d4dcd6;">
                <h5 class="text-center">未连接主机</h5>
                <h1 class="text-center">1</h1>
            </mdui-card>
        </div>
    </div> -->
    <table class="table table-hover table-condensed">
        <thead>
            <tr>
                <th>主机名</th>
                <th>IP地址:端口号</th>
                <th>Running</th>
                <th>Pending</th>
                <th>Finished</th>
                <th>运行状态</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody class="table-group-divider">
            <tr v-for="host, idx in host_list" :key="idx">
                <td>{{ host.node_name }}</td>
                <td>{{ hosts[idx].ip }}:{{ hosts[idx].port }}</td>
                <td>{{ host.running }}</td>
                <td>{{ host.pending }}</td>
                <td>{{ host.finished }}</td>
                <td>
                    <span v-if="host.status == 'ok'" class="badge text-bg-success">正常</span>
                    <span v-if="host.status != 'ok'" class="badge text-bg-danger">离线</span>
                </td>
                <td><a @click="updateHost(idx)">编辑</a><a @click="deleteHost(idx)" style="margin-left: 1rem;">删除</a></td>
            </tr>
        </tbody>
    </table>
    <button @click="addHost" type="button" class="btn btn-light btn-sm float-end"
        style="font-weight: 600; opacity: 0.8;">新建连接</button>
    <h2>任务管理</h2>
    <table class="table table-hover table-condensed">
        <thead>
            <tr>
                <th>任务名</th>
                <th>任务ID</th>
                <th>开始时间</th>
                <th>结束时间</th>
                <th>实时状态</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody class="table-group-divider">
            <tr v-for="task, idx in task_running_list" :key="idx">
                <td>{{ task.project + "." + task.spider }}</td>
                <td><span class="d-inline-block text-truncate" style="max-width: 100px;">{{ task.id }}</span></td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.start_time }}</span>
                </td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.end_time }}</span></td>
                <td><span class="badge text-bg-success">正在运行</span></td>
                <td><a>挂起</a><a style="margin-left: 1rem;">终止</a></td>
            </tr>
            <tr v-for="task, idx in task_pending_list" :key="idx">
                <td>{{ task.project + "." + task.spider }}</td>
                <td><span class="d-inline-block text-truncate" style="max-width: 100px;">{{ task.id }}</span></td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.start_time }}</span>
                </td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.end_time }}</span></td>
                <td><span class="badge text-bg-secondary">挂起</span></td>
                <td><a>继续</a><a style="margin-left: 1rem;">删除</a></td>
            </tr>
            <tr v-for="task, idx in task_finished_list" :key="idx">
                <td>{{ task.project + "." + task.spider }}</td>
                <td><span class="d-inline-block text-truncate" style="max-width: 100px;">{{ task.id }}</span></td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.start_time }}</span>
                </td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.end_time }}</span></td>
                <td><span class="badge text-bg-danger">运行结束</span></td>
                <td><a>启动</a><a style="margin-left: 1rem;">删除</a></td>
            </tr>
        </tbody>
    </table>

    <h2>日志信息</h2>
    <mdui-text-field readonly rows="8" style="width: 95%;" :value="info">
    </mdui-text-field>

    <!-- 操作对话框 -->
    <mdui-dialog ref="dialog" fullscreen close-on-overlay-click class="example-action" headline="新建连接">
        <h5 style="margin-top: 2rem;">IP</h5>
        <mdui-text-field v-model="ip"></mdui-text-field>
        <h5>PORT</h5>
        <mdui-text-field v-model="port"></mdui-text-field>
        <mdui-button @click="cancel_operate" slot="action" variant="tonal">取消</mdui-button>
        <mdui-button @click="save_operate" slot="action" variant="tonal">保存</mdui-button>
    </mdui-dialog>

    <mdui-dialog ref="dialog_update" fullscreen close-on-overlay-click class="example-action" headline="更新连接">
        <h5 style="margin-top: 2rem;">IP</h5>
        <mdui-text-field v-model="ip"></mdui-text-field>
        <h5>PORT</h5>
        <mdui-text-field v-model="port"></mdui-text-field>
        <mdui-button @click="cancel_operate" slot="action" variant="tonal">取消</mdui-button>
        <mdui-button @click="update_operate" slot="action" variant="tonal">保存</mdui-button>
    </mdui-dialog>

    <!-- 消息提示 -->
    <mdui-snackbar ref="snackbar_success" placement="top" auto-close-delay="1000"
        class="example-close-delay">操作成功!</mdui-snackbar>
    <mdui-snackbar ref="snackbar_fail" placement="top" auto-close-delay="1000"
        class="example-close-delay">操作失败!</mdui-snackbar>
</template>

<script setup>
import 'mdui/components/text-field.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import moment from 'moment';
import 'mdui/components/dialog.js';
import 'mdui/components/snackbar.js';

let task_running_list = ref([]); // 正在运行任务列表
let task_pending_list = ref([]); // 暂停任务列表
let task_finished_list = ref([]); // 运行结束任务列表
let host_list = ref([]); // 主机列表存放主机状态信息的列表
let hosts = ref([]); // 存储所有主机ip与port的列表
let info = ref(""); // 日志信息
let dialog = ref(); // 新建连接对话框
let dialog_update = ref(); // 更新连接对话框
let ip = ref(""); // 连接的ip
let port = ref(""); // 连接的port 
let id = ref(""); // 连接的id
let snackbar_success = ref(); // 操作成功
let snackbar_fail = ref(); // 操作失败


function get_tasks() {
    let project_list = [];
    let idx;
    for (idx in hosts) {
        axios.get("http://localhost:6800/listprojects.json")
            .then(function (response) {
                // console.log(response.data.projects)
                project_list = response.data.projects;
                let index;
                for (index in project_list) {
                    // console.log(project_list[index])
                    axios.get("http://localhost:6800/listjobs.json?project=" + project_list[index])
                        .then(function (response) {
                            // console.log(response.data)
                            task_finished_list.value = task_finished_list.value.concat(response.data.finished);
                            task_pending_list.value = task_pending_list.value.concat(response.data.pending);
                            task_running_list.value = task_running_list.value.concat(response.data.running);
                        }).catch(function (error) {
                            console.error(error)
                        });
                }
            }).catch(function (error) {
                console.error(error)
            });
    }

} // 获取任务列表

function get_hosts() {
    let index;
    axios.get("http://localhost:8080/host").then(function (response) {
        hosts.value = response.data;
        // console.log(hosts)
        for (index in hosts.value) {
            // console.log(hosts[index])
            let url = "http://" + hosts.value[index].ip + ":" + hosts.value[index].port + "/daemonstatus.json"
            axios.get(url)
                .then(function (response) {
                    // console.log(response.data);
                    if (response.data.status == 'ok') {
                        // console.log("ok")
                        host_list.value.push(response.data)
                    }
                }).catch(function (error) {
                    // console.error(error)
                    // console.log("error")
                    host_list.value.push({ finished: '未知', node_name: '未知', pending: '未知', running: '未知', status: 'breakdown' })
                });
        }
    }).catch(function (error) {
        console.error(error)
    });
} // 获取主机

function deleteHost(idx) {
    axios.delete("http://localhost:8080/host/" + hosts.value[idx].id).then(function (response) {
        if (response.data == 1) {
            snackbar_success.value.open = true;
        } else {
            snackbar_fail.value.open = true;
        }
    }).catch(function (error) {
        console.error(error);
    })
} // 删除主机

function updateHost(idx) {
    dialog_update.value.open = true;
    id.value = hosts.value[idx].id;
    ip.value = hosts.value[idx].ip;
    port.value = hosts.value[idx].port;
} // 更新主机

function addHost() {
    ip.value = "";
    port.value = "";
    dialog.value.open = true;
} // 新建主机

function get_info() {
    axios.get('/logs/spider/baidu/2858cb9bdb6711ee8b74c8b29ba4ee5d.log', {
    }).then(function (response) {
        // console.log(response.data);
        info.value = response.data;
    }).catch(function (error) {
        console.log(error)
    })
} // 获取日志信息

function cancel_operate() {
    dialog.value.open = false;
    dialog_update.value.open = false;
} // 取消操作

function save_operate() {
    let id = moment().format('YYYYMMDDHHmmss');
    let data = { "id": id, "ip": ip.value, "port": port.value };
    console.log(data)
    axios.post('http://localhost:8080/host', data, {
        headers: { 'Content-Type': 'application/json' }
    }
    ).then(function (response) {
        // console.log("insert")
        // console.log(response.data)
        if (response.data == 1) {
            snackbar_success.value.open = 1;
        } else {
            snackbar_fail.value.open = 1;
        }
    }).catch(function (error) {
        console.error(error)
    })
    dialog.value.open = false;
} // 提交连接

function update_operate() {
    let data = {
        "id": id.value,
        "ip": ip.value,
        "port": port.value
    }
    axios.put("http://localhost:8080/host", data, {
        headers: { 'Content-Type': 'application/json' }
    }).then(function (response) {
        if (response.data == 1) {
            snackbar_success.value.open = 1;
        } else {
            snackbar_fail.value.open = 1;
        }
    }).catch(function (error) {
        console.error(error)
    })
    dialog_update.value.open = false;
}

onMounted(() => {
    get_hosts();
    get_tasks();
    get_info();
})

</script>

<style scoped>
h5 {
    font-weight: 600;
    opacity: 0.8;
}

h2 {
    margin-top: 2rem;
}

mdui-text-field::part(container) {
    background-color: #E0E0E0;
}

mdui-dialog::part(panel) {
    background-color: #fafdfd;
}

mdui-button {
    background-color: #e8ecef;
}
</style>