import { createRouter, createWebHistory } from 'vue-router'
import Monitor from '@/pages/Monitor.vue'
import ResourceManage from '@/pages/ResourceManage.vue'
import Settings from '@/pages/Settings.vue'
import TaskAssign from '@/pages/TaskAssign.vue'
import DataAnalysis from '@/pages/DataAnalysis.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: Monitor
        },
        {
            path: '/resmag',
            component: ResourceManage
        },
        {
            path: '/settings',
            component: Settings
        },
        {
            path: '/taskasg',
            component: TaskAssign
        },
        {
            path: '/data',
            component: DataAnalysis
        }
    ]
})

export default router