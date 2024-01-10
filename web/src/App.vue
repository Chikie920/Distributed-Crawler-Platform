<template>
    <mdui-layout full-height>
        <TopBar></TopBar>
        <Navi></Navi>
        <Container></Container>
    </mdui-layout>
</template>

<script setup>

/*
    引入MDUI组件
*/

import 'mdui/mdui.css'
import 'mdui/components/layout.js'
import 'mdui/components/layout-item.js'
import 'mdui/components/layout-main.js'



/*
    引入项目组件
*/

import TopBar from '@/components/TopBar.vue'
import Navi from '@/components/Navi.vue'
import Container from '@/components/Container.vue'

</script>

<style scoped>
</style>
