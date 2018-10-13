<template>
  <div id="app">
      <router-view></router-view>
      <bottom-menu></bottom-menu>
  </div>
</template>

<script>
import TabMenu from '@/components/TabMenu'

export default {
  name: 'app',
  components: {
    'bottom-menu': TabMenu
  }
}
</script>

<style lang="less">
@import '~vux/src/styles/reset.less';

html,body {
  background-color: #fbf9fe;
  margin: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>
