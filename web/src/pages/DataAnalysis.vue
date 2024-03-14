<template>
    <h2>数据概览</h2>
    <div class="row" style="width: 80vw;">
        <div class="col-md-4" ref="news_platform_data" style="width: 400px; height: 200px; display: block;"></div>
        <div class="col-md-4" ref="daily_data" style="width: 400px; height: 200px;margin-left: 1.5rem; display: block;">
        </div>
    </div>
    <h2>词云</h2>
    <div style="width: 600px; height: 300px; display: block;">
        <img :src="wordCloud" style="width: 100%; height: auto; max-height: 100%;">
    </div>
    <h2 style="margin-top: 1rem;">情感分析</h2>
    <div ref="sentiment_pie" style="width: 400px; height: 200px;margin-left: 1.5rem; display: block;"></div>
    <h2 style="margin-top: 1rem;">关键字提取</h2>
    <div ref="keyWords_bar" style="width: 80vw; height: 40vh;margin-left: 1.5rem; display: block;"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeMount } from 'vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import * as echarts from 'echarts';
import axios from 'axios';
import moment from 'moment/moment.js';
import queryString from 'query-string';

let news_platform_data = ref(); // 用于展示各个新闻平台的数据采集量
let taskName_list = ref([]); // 任务名称列表
let taskData_list = ref([]); // 任务数据列表
let daily_data = ref(); // 用于展示每日采集数据量
let fiveDays_data = ref([]); // 存储五日数据量
let wordCloud = ref(); // 词云图片
let sentiment_pie = ref(); // 情感分析饼图
let sentiment_grade = ref(); // 存放情感数据
let keyWords_bar = ref(); // 关键词柱状图
let contents = ref(); // 存放新闻关键词
let keyWords = ref(); // 存放关键词

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
    for (let date of date_list) {
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

async function get_contents() {
    let content = '';
    await axios.get('http://localhost:8080/resmag/contents')
        .then(function (response) {
            let news_content_list = response.data;
            for (let item of news_content_list) {
                content += item;
            }
            contents.value = content;
        })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        });
} // 获取所有新闻信息

async function get_wordCloud() {
    await axios.post('http://127.0.0.1:2233/wordCloud', queryString.stringify({ 'content': contents.value }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function (response) {
        wordCloud.value = "data:image/jpg;base64," + response.data
    }).catch(function (error) {
        console.error(error);
    });
} // 获取所有新闻内容

async function get_sentiment() {
    await axios.post('http://127.0.0.1:2233/sentiment', queryString.stringify({ 'content': contents.value }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function (response) {
        // console.log(response.data);
        sentiment_grade.value = response.data;
    }).catch(function (error) {
        console.error(error);
    });
} // 获取情感数据

async function get_keyWords() {
    await axios.post('http://127.0.0.1:2233/keyWords', queryString.stringify({ 'content': contents.value }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function (response) {
        // console.log(response.data);
        // sentiment_grade.value = response.data;
        keyWords.value = response.data;
        // console.log(keyWords.value)
    }).catch(function (error) {
        console.error(error);
    });
} // 获取新闻关键词

onBeforeMount(() => {
    // console.log('before')

});

onMounted(async () => {
    // console.log('on')
    await get_task_name();
    await get_task_data_counts();
    await get_contents();
    await get_5days_counts();
    await get_sentiment();
    await get_keyWords();
    let Chart_news_platform_data = echarts.init(news_platform_data.value);

    let option_news_platform_data = {
        title: {
            text: '各爬虫采集新闻数据量'
        },
        tooltip: {},
        legend: {
        },
        xAxis: {
            data: taskName_list.value,
            axisLabel: {
                //x轴文字的配置
                show: true,
                interval: 0,//使x轴文字显示全
            }
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
    // 柱状图

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
    // 折线图


    let Chart_sentiment_pie = echarts.init(sentiment_pie.value);
    let option_sentiment_pie = {
        series: [
            {
                type: 'pie',
                data: [
                    {
                        value: sentiment_grade.value['pos_grade'],
                        name: '正面新闻'
                    },
                    {
                        value: sentiment_grade.value['neg_grade'],
                        name: '负面新闻'
                    }
                ],
                label: {
                    formatter: '{b}{d}%',
                    position: "outer",
                    alignTo: "edge",
                    margin: 0
                }
            }
        ]
    };

    Chart_sentiment_pie.setOption(option_sentiment_pie);
    // 饼图

    keyWords_bar

    let Chart_keyWords_bar = echarts.init(keyWords_bar.value);
    let option_keyWords_bar = {
        title: {
            text: '新闻关键词'
        },
        xAxis: {
            type: 'category',
            data: keyWords.value['keys'],
            axisLabel: {
                //x轴文字的配置
                show: true,
                interval: 0,//使x轴文字显示全
            }

        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: keyWords.value['weight'],
            type: 'bar',
            itemStyle: {
                normal: {
                    color: function (params) {
                        var colorList = ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#1685a9', '#f47983', '#21a675', '#574266', '#88ada6', '#cb3a56', '#edd1d8', '#549688', '#827100', '#00a381', '#fdeff2', '#767c6b', '#cc7eb1'];
                        return colorList[params.dataIndex]
                    }
                }
            }
        }],
        grid: {
            left: "30px",
            top: "40px",
            right: "30px",
            bottom: "30px"
        }
    };

    Chart_keyWords_bar.setOption(option_keyWords_bar);

    await get_wordCloud();

});

</script>

<style scoped>
img {
    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    -khtml-user-selece: none;
    user-select: none;
}
</style>