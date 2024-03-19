<template>
    <h2 style="margin-top: 0;">实时数据采集情况</h2>
    <div ref="last_three_hours_data" style="width: 500px; height: 300px; display: block;"></div>
    <h2>主机管理</h2>
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
        <tbody class="table-group-divider" v-for="hostAndTask, idx in hostAndTask_list" :key="idx">
            <tr @click="get_info(task.project, task.spider, task.id)" v-for="task in hostAndTask.running"
                :key="task.id">
                <td><u>{{ task.project + "." + task.spider }}</u></td>
                <td><span class="d-inline-block text-truncate" style="max-width: 100px;">{{ task.id }}</span></td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.start_time
                        }}</span>
                </td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.end_time }}</span>
                </td>
                <td><span class="badge text-bg-success">正在运行</span></td>
                <td><a @click="cancel_job(hostAndTask.ip, hostAndTask.port, task.project, task.id)">终止</a></td>
            </tr>
            <tr @click="get_info(task.project, task.spider, task.id)" v-for="task in hostAndTask.pending"
                :key="task.id">
                <td><u>{{ task.project + "." + task.spider }}</u></td>
                <td><span class="d-inline-block text-truncate" style="max-width: 100px;">{{ task.id }}</span></td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.start_time
                        }}</span>
                </td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.end_time }}</span>
                </td>
                <td><span class="badge text-bg-secondary">挂起</span></td>
                <td><a @click="reboot_job(hostAndTask.ip, hostAndTask.port, task.project, task.spider, task.id)">继续</a>
                </td>
            </tr>
            <tr v-for="task in hostAndTask.finished" :key="task.id">
                <td @click="get_info(task.project, task.spider, task.id)"><u>{{ task.project + "." + task.spider }}</u>
                </td>
                <td><span class="d-inline-block text-truncate" style="max-width: 100px;">{{ task.id }}</span></td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.start_time
                        }}</span>
                </td>
                <td><span class="d-inline-block text-truncate" style="max-width: 180px;">{{ task.end_time }}</span>
                </td>
                <td><span class="badge text-bg-danger">运行结束</span></td>
                <td><a @click="reboot_job(hostAndTask.ip, hostAndTask.port, task.project, task.spider, task.id)">启动</a>
                </td>
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
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import moment from 'moment';
import 'mdui/components/dialog.js';
import 'mdui/components/snackbar.js';
import emitter from '@/tools/emitter.js';
import * as echarts from 'echarts';

let host_list = ref([]); // 主机列表存放主机状态信息的列表
let hosts = ref([]); // 存储所有主机ip与port的列表
let info = ref("******日志信息******"); // 日志信息
let dialog = ref(); // 新建连接对话框
let dialog_update = ref(); // 更新连接对话框
let ip = ref(""); // 连接的ip
let port = ref(""); // 连接的port 
let id = ref(""); // 连接的id
let snackbar_success = ref(); // 操作成功
let snackbar_fail = ref(); // 操作失败
let hostAndTask_list = ref([]); // 存放主机以及其项目与任务数据
let online_host_list = ref([]); // 可用主机列表
let last_three_hours_data = ref(); // 监控实时数据采集情况
let fiveminutes_data = ref([]); // 最近五分钟数据采集情况
let timer = ref() // 定时器

async function get_hosts() {
    let index;
    await axios.get("http://localhost:8080/host").then(async function (response) {
        hosts.value = response.data;
        // console.log("######")
        // console.log(hosts.value[0].ip)
        for (index in hosts.value) {
            // console.log(hosts.value[index]);
            let hostId = hosts.value[index].id;
            let hostIp = hosts.value[index].ip;
            let hostPort = hosts.value[index].port;
            let url = "http://" + hostIp + ":" + hostPort + "/daemonstatus.json";
            // console.log(url)
            await axios.get(url, {
                timeout: 1000,
            }).then(function (response) {
                // console.log(response.data);
                if (response.data.status == 'ok') {
                    // console.log("ok");
                    // console.log(hostIp + " " + hostPort);
                    get_tasks(hostIp, hostPort); // 获取主机任务
                    online_host_list.value.push({ id: hostId, ip: hostIp, port: hostPort });
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
    get_tasks();
} // 获取主机

function get_tasks(hostIp, hostPort) {
    let project_list = [];
    // console.log("******")
    // console.log(hostIp + " " + hostPort)
    let data = {}; // 存放主机及其任务的临时对象
    axios.get("http://" + hostIp + ":" + hostPort + "/listprojects.json") // 获取主机项目
        .then(function (response) {
            // console.log(response.data.projects)
            project_list = response.data.projects;
            let index;
            for (index in project_list) {
                // console.log(idx)
                // let url = "http://"+ip+":"+port+"/listjobs.json?project=" + project_list[index];
                // console.log(url);
                axios.get("http://" + hostIp + ":" + hostPort + "/listjobs.json?project=" + project_list[index]) // 获取主机项目内任务
                    .then(function (response) {
                        // console.log(response.data)
                        // task_finished_list.value = task_finished_list.value.concat(response.data.finished);
                        // task_pending_list.value = task_pending_list.value.concat(response.data.pending);
                        // task_running_list.value = task_running_list.value.concat(response.data.running);
                        // console.log(task_finished_list.value);
                        // console.log(task_pending_list.value);
                        // console.log(task_running_list.value);
                        data['ip'] = hostIp;
                        data['port'] = hostPort;
                        data['finished'] = response.data.finished;
                        data['pending'] = response.data.pending;
                        data['running'] = response.data.running;
                        hostAndTask_list.value.push(data);
                        // console.log("###########")
                        // console.log(hostAndTask_list.value)
                    }).catch(function (error) {
                        console.error(error)
                    });
            }
        }).catch(function (error) {
            console.error('主机连接超时')
        });
} // 获取任务列表

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

function get_info(project, spider, id) {
    axios.get('/logs/' + project + '/' + spider + '/' + id + '.log', {
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
    // console.log(data)
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
} // 更新连接操作

function reboot_job(hostIp, hostPort, project, spider, Spiderid) {
    axios.post("http://" + hostIp + ":" + hostPort + "/schedule.json", 'project=' + project + "&spider=" + spider + "&jobid=" + Spiderid, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function (response) {
        // console.log(response.data)
    }).then(function (error) {
        console.error(error);
    })

    axios.put('http://127.0.0.1:8080/task/' + spider).then(response => {
        // console.log("put")
        if (response.data == 1) {
            snackbar_success.value.open = true;
        } else {
            snackbar_fail.value.open = true;
        }
    }).catch(error => {
        console.error(error);
    }); // 更新运行次数
} // 重启任务

async function cancel_job(hostIp, hostPort, project, Spiderid) {
    await axios.post("http://" + hostIp + ":" + hostPort + "/cancel.json", 'project=' + project + "&job=" + Spiderid, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function (response) {
        // console.log(response.data)
    }).then(function (error) {
        console.error(error);
    });
    await axios.get('http://localhost:2233/kill_driver')
        .then(function (response) {
            console.log("kill driver")
            console.log(response.data)
        })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        });
} // 取消任务

function get_online_host() {
    // console.log(online_host_list.value)
    emitter.emit('getOnlineHost', online_host_list.value);
} // 返回在线主机

async function get_fiveminutes_data() {
    // console.log(moment().format('YYYYMMDDHHmm'))
    let date_list = [moment().subtract(4, 'm').format('YYYYMMDDHHmms'), moment().subtract(3, 'm').format('YYYYMMDDHHmm'), moment().subtract(2, 'm').format('YYYYMMDDHHmm'), moment().subtract(1, 'm').format('YYYYMMDDHHmm'), moment().format('YYYYMMDDHHmm')];
    // console.log(date_list)
    for (let date of date_list) {
        // console.log(date)
        await axios.get('http://localhost:8080/resmag/counts/' + date)
            .then(function (response) {
                // console.log(response.data)
                fiveminutes_data.value.push(response.data);
            })
            .catch(function (error) {
                // 请求失败
                console.log(error);
            });
    }
    // console.log(fiveminutes_data.value)
} // 获取近五分钟数据

onMounted(async () => {
    await get_hosts();
    await get_fiveminutes_data();
    let Chart_last_three_hours_data = echarts.init(last_three_hours_data.value);
    let option_last_three_hours_data = {
        title: {
            text: '实时数据采集量(近五分钟)'
        },
        xAxis: {
            data: [moment().subtract(4, 'm').format('mm分ss'), moment().subtract(3, 'm').format('mm分ss'), moment().subtract(2, 'm').format('mm分ss'), moment().subtract(1, 'm').format('mm分ss'), moment().format('mm分ss')],
            alignWithLabel: true,
            axisLabel: {
                interval: 0
            },
        },
        yAxis: {
            minInterval: 1
        },
        series: [
            {
                data: fiveminutes_data.value,
                type: 'line',
                smooth: true,
                label: {
                    show: true,
                    position: 'top',
                    textStyle: {
                        fontSize: 10
                    }
                },
            }
        ],
        grid: {
            left: "30px",
            top: "40px",
            right: "30px",
            bottom: "30px"
        }
    };

    Chart_last_three_hours_data.setOption(option_last_three_hours_data);
    timer.value = setInterval(function () {
        axios.get('http://127.0.0.1:2233/data_sync'
        ).then(function (response) {
            if (response.data == 'ok') {
                console.log("data_async");
            }
        }).catch(error => {
            console.error(error);
        }); // 新增目标url
    }, 1000 * 30); // 定时执行数据库同步
    // get_tasks();
}); // DOM加载时调用

onUnmounted(() => {
    get_online_host(); // 触发事件
    clearInterval(timer.value); // 移除定时器
}); // DOM被移除时调用



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