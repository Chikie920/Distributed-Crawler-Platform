<template>
    <h2>创建方式</h2>

    <!-- 使用模板创建 -->
    <select @change="create_type_change" class="form-select" style="width: 20%; display: block; margin-top: 1rem;">
        <option value="1">#使用模板创建任务</option>
        <option value="2">#自定义创建任务</option>
    </select>
    <div v-show="select_type == '1'">
        <h2 style="margin-top: 1rem;">主机选择</h2>
        <select ref="hostValue" @change="select_host" class="form-select"
            style="width: 25%; display: block; margin-top: 1rem;">
            <option selected>选择主机</option>
            <option v-for="host, index in available_host_list" :key="index" :value="host.ip + ':' + host.port">{{
        host.ip + ':' + host.port }}</option>
        </select>
        <h2 style="margin-top: 2rem;">模板选择</h2>
        <select ref="jobValue" @change="select_job" class="form-select"
            style="width: 15%; margin-top: 1rem; display: block;">
            <option selected>选择模板</option>
            <option v-for="job, index in job_list" :key="index" :value="index">{{ job }}</option>
        </select>
        <mdui-button @click="create_job_by_template" variant="outlined" style="margin-top: 2rem;">提交</mdui-button>
    </div>

    <!-- 使用自定义创建 -->
    <div v-show="select_type == '2'">
        <h2 style="margin-top: 1rem;">相关参数</h2>
        <mdui-text-field v-model="job_name" style="width: 20%; margin-top: 1rem; display: block;"
            label="任务名称"></mdui-text-field>
        <mdui-text-field v-model="job_url" style="width: 40%; margin-top: 1rem; display: block;"
            label="目标网址"></mdui-text-field>

        <div style="display: flex;text-align: center;margin-top: 1rem;">
            <h2 style="margin: auto 0;">高级设置</h2>
            <mdui-switch @change="change_option_status" style="margin-left: 1rem;"></mdui-switch>
        </div>
        <div v-show="advanced_option">
            <mdui-text-field v-model="job_delay" style="width: 20%; margin-top: 1rem; display: block;"
                label="采集延迟/s(默认为2)"></mdui-text-field>
            <mdui-text-field v-model="job_request" style="width: 20%; margin-top: 1rem; display: block;"
                label="并发请求参数(默认100)"></mdui-text-field>
            <!-- <mdui-text-field v-model="job_cookie" rows="3" style="width: 40%; margin-top: 1rem; display: block;"
                label="目标网站COOKIE设置">
            </mdui-text-field> -->
            <mdui-text-field v-model="job_rules" rows="3" style="width: 40%; margin-top: 1rem; display: block;"
                label="链接提取规则Rules(输入目标Url关键字, 请用英文逗号隔开)">
            </mdui-text-field>
            <div style="display: flex;text-align: center;margin-top: 1rem;">
                <p style="margin: auto 0;">启用ChromeDriver代理访问(会影响采集速度)</p>
                <mdui-switch @change="change_use_driver" style="margin-left: 1rem;"></mdui-switch>
            </div>
        </div>

        <h2 style="margin-top: 1rem;">主机选择</h2>
        <select ref="hostValue" @change="select_host" class="form-select"
            style="width: 25%; display: block; margin-top: 1rem;">
            <option selected>选择主机</option>
            <option v-for="host, index in available_host_list" :key="index" :value="host.ip + ':' + host.port">{{
        host.ip + ':' + host.port }}</option>
        </select>
        <mdui-button @click="create_job_custom" variant="outlined" style="margin-top: 2rem;">提交</mdui-button>
    </div>

    <!-- 消息提示 -->
    <mdui-snackbar ref="snackbar_success" placement="top" auto-close-delay="1000"
        class="example-close-delay">操作成功!</mdui-snackbar>
    <mdui-snackbar ref="snackbar_fail" placement="top" auto-close-delay="1000"
        class="example-close-delay">操作失败!</mdui-snackbar>

</template>

<script setup>
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mdui/components/radio-group.js';
import 'mdui/components/radio.js';
import 'mdui/components/text-field.js';
import 'mdui/components/select.js';
import 'mdui/components/menu-item.js';
import 'mdui/components/button.js';
import 'mdui/components/switch.js';
import { ref, onMounted } from 'vue';
import emitter from '../tools/emitter.js';
import axios from 'axios';
import queryString from 'query-string';

let select_type = ref("1"); // 选择创建方式
let available_host_list = ref([]); // 在线主机列表
let job_list = ref(['百度新闻', '网易新闻', '新浪新闻', '凤凰新闻', '澎湃新闻', '搜狐新闻']); // 存放爬虫模板
let advanced_option = ref(false); // 高级设置开关
let snackbar_success = ref(); // 操作结果提示消息条-操作成功
let snackbar_fail = ref(); // 操作结果提示消息条-操作失败
let hostValue = ref(); // 选择主机控件
let hostUrl = ref(); // 目标主机url
let job = ref(); // 目标作业
let jobValue = ref(); // 选择模板控件
let job_name = ref(); // 任务名称
let job_url = ref(); // 任务目标网址
let job_delay = ref(); // 任务延迟
// let job_cookie = ref(); // 任务cookie
let driver_open = ref(false); // 是否开启浏览器代理
let job_request = ref(); // 并发请求参数
let job_rules = ref(); // 连接提取规则

function create_type_change() {
    if (select_type.value == "1") {
        select_type.value = "2";
    } else {
        select_type.value = "1";
    }
} // 选择任务创建方式

function change_option_status() {
    if (advanced_option.value) {
        advanced_option.value = false;
    } else {
        advanced_option.value = true;
    }
    // console.log("触发"+advanced_option.value)
} // 更改设置状态

function create_job_by_template() {
    let job_dict = { '百度新闻': 'baidu', '网易新闻': '163', '新浪新闻': 'sina', '凤凰新闻': 'ifeng', '澎湃新闻': 'pengpai', '搜狐新闻': 'sohu' }
    // console.log("http://" + hostUrl.value + "/schedule.json", 'project=' + 'spider' + "&spider=" + job_dict[job.value])
    axios.post("http://" + hostUrl.value + "/schedule.json", 'project=' + 'spider' + "&spider=" + job_dict[job.value], {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function (response) {
        // console.log(response.data)
        if (response.data.status == 'ok') {
            snackbar_success.value.open = true;
        } else {
            snackbar_fail.value.open = true;
        }
    }).then(function (error) {
        console.error(error);
    })
} // 根据模板创建任务

function create_job_custom() {
    // console.log(hostUrl.value);
    let data = {
        'name': job_name.value,
        'url': job_url.value,
        'delay': job_delay.value,
        // 'cookie': job_cookie.value,
        'driver_open': driver_open.value,
        'request_counts': job_request.value,
        'rules': job_rules.value
    };
    axios.post('http://'+hostUrl.value.split(':')[0]+':2233', queryString.stringify(data), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function (response) {
        if (response.data == 'ok') {
            snackbar_success.value.open = true;
        } else {
            snackbar_fail.value.open = true;
        }
    }).catch(error => {
        console.error(error);
    })
} // 提交自定义任务

function select_host() {
    hostUrl.value = hostValue.value.selectedOptions[0].text;
} // 主机选择事件

function select_job() {
    job.value = jobValue.value.selectedOptions[0].text;
} // 模板选择事件

function change_use_driver() {
    if (driver_open.value == false) {
        driver_open.value = true;
    } else {
        driver_open.value = false;
    }
} // 是否使用浏览器代理


emitter.on('getOnlineHost', (res) => {
    // console.log(value);
    // available_host_list.value = toRaw(value)[0];
    // console.log(JSON.parse(JSON.stringify(res)))
    available_host_list.value = res;
    // console.log(available_host_list.value);
}); // 绑定事件，获取可用主机列表

onMounted(() => {
});

</script>

<style scoped>
mdui-text-field::part(container) {
    /* background-color: #E0E0E0; */
    background-color: #fafdfd;
}
</style>