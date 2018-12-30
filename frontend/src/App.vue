<template>

  <v-app>

  <v-layout justify-center>
    <v-flex xs12 sm10 md8 lg6>
  <v-card
    class="mx-auto"
    style="max-width: 500px;height:100%;"
  >
 

  <div id="app">
    <keep-alive><router-view></router-view></keep-alive>
  </div>
  </v-card>

  </v-flex>
  </v-layout>
 
  </v-app>
</template>

<script>

export default {
  name: 'app',
  components: {
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
