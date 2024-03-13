<template>
    <h2>数据概览</h2>
    <div class="row">
        <div class="col-md-4" ref="news_platform_data" style="width: 400px; height: 200px; display: block;"></div>
        <div class="col-md-4" ref="daily_data" style="width: 400px; height: 200px;margin-left: 1.5rem; display: block;">
        </div>
    </div>
    <h2>词云</h2>
    <h2 style="margin-top: 1rem;">情感分析</h2>
    <h2 style="margin-top: 1rem;">关键字提取</h2>
</template>

<script setup>
import { ref, onMounted, onBeforeMount } from 'vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import * as echarts from 'echarts';
import axios from 'axios';
import moment from 'moment/moment.js';

let news_platform_data = ref(); // 用于展示各个新闻平台的数据采集量
let taskName_list = ref([]); // 任务名称列表
let taskData_list = ref([]); // 任务数据列表
let daily_data = ref(); // 用于展示每日采集数据量
let fiveDays_data = ref([]); // 存储五日数据量

async function get_task_name() {
    await axios.get('http://localhost:8080/taskName')
        .then(function (response) {
            // 请求成功
            taskName_list.value = response.data;
            // console.log(taskName_list.value);
            // console.log("GET TASK***********")
            // console.log(task_list.value)

            // console.log(task_info.value)
        })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        }); // 获取任务数据
} // 获取任务名称

async function get_task_data_counts() {
    for (let task of taskName_list.value) {
        await axios.get('http://localhost:8080/resmag/' + task)
            .then(function (response) {
                // 请求成功
                // console.log(response.data)
                // dataCounts_list.value.push(response.data.length)
                // console.log('#########')
                // console.log(task)
                // console.log(news_list.value[0].id)
                // console.log(response.data.length)
                taskData_list.value.push(response.data.length);
                // console.log(taskData_list.value)
            })
            .catch(function (error) {
                // 请求失败
                console.log(error);
            }); // 根据任务名称获取新闻数据
    }
} // 获取任务的数据量

async function get_5days_counts() {
    let date_list = [moment().subtract(4, 'days').format('YYYYMMDD'), moment().subtract(3, 'days').format('YYYYMMDD'), moment().subtract(2, 'days').format('YYYYMMDD'), moment().subtract(1, 'days').format('YYYYMMDD'), moment().format('YYYYMMDD')];
    // console.log(date_list)
    for(let date of date_list) {
        // console.log(date)
        await axios.get('http://localhost:8080/resmag/counts/' + date)
            .then(function (response) {
                fiveDays_data.value.push(response.data);
            })
            .catch(function (error) {
                // 请求失败
                console.log(error);
            });
    }
    // console.log(fiveDays_data.value)
} // 获取近五日数据量

onBeforeMount(() => {
    // console.log('before')

})

onMounted(async () => {
    // console.log('on')
    await get_task_name();
    await get_task_data_counts();
    await get_5days_counts();
    let Chart_news_platform_data = echarts.init(news_platform_data.value);

    let option_news_platform_data = {
        title: {
            text: '各爬虫采集新闻数据量'
        },
        tooltip: {},
        legend: {
        },
        xAxis: {
            data: taskName_list.value
        },
        yAxis: {
            minInterval: 1
        },
        series: [
            {
                type: 'bar',
                data: taskData_list.value
            }
        ],
        grid: {
            left: "30px",
            top: "40px",
            right: "30px",
            bottom: "30px"
        }
    };
    Chart_news_platform_data.setOption(option_news_platform_data);

    let Chart_daily_data = echarts.init(daily_data.value);
    // console.log(Now.format('YYYY/MM/DD'))
    // console.log(Now.subtract(1, 'days').format('YYYY/MM/DD'))

    let option_daily_data = {
        title: {
            text: '每日数据采集量(近五日)'
        },
        xAxis: {
            data: [moment().subtract(4, 'days').format('YY/MM/DD'), moment().subtract(3, 'days').format('YY/MM/DD'), moment().subtract(2, 'days').format('YY/MM/DD'), moment().subtract(1, 'days').format('YY/MM/DD'), moment().format('YY/MM/DD')],
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
                data: fiveDays_data.value,
                type: 'line',
                label: {
                    show: true,
                    position: 'top',
                    textStyle: {
                        fontSize: 10
                    }
                }
            }
        ],
        grid: {
            left: "30px",
            top: "40px",
            right: "30px",
            bottom: "30px"
        }
    };

    Chart_daily_data.setOption(option_daily_data);

});

</script>

<style scoped></style>