<template>
<div>

<v-app>
      <v-card>

        <v-img
          class="white--text"
          height="200px"
          src="https://cdn.vuetifyjs.com/images/cards/docks.jpg">
          <v-container>

            <v-layout row>
              <v-flex xs6>
                <span v-if="logined" class="headline">{{username}}</span>
                <span v-else  class="headline">
                  <router-link to="/login">登陆/注册</router-link>
                </span>
              </v-flex>


              <v-flex xs6>
                <span class="headline">账户余额(ZHI)</span><br><span class="headline">{{total}}</span>
              </v-flex>
            </v-layout>

            <br><br>

            <v-layout row>
              <v-flex xs4>
                <span>可用(ZHI)</span><br><span>{{available}}</span>
              </v-flex>
              <v-flex xs4>
                <span>锁定(ZHI)</span><br><span>{{locked}}</span>
              </v-flex>
              <v-flex xs4>
                <span>提现中(ZHI)</span><br><span>{{withdrawaling}}</span>
              </v-flex>
            </v-layout>

          </v-container>

        </v-img>

        <v-card-title>
          <v-layout row>
            <v-flex xs6 sm6>
              <v-btn>充值</v-btn>
            </v-flex>

            <v-flex xs6 sm6>
              <v-btn>提现</v-btn>
            </v-flex>

          </v-layout>
        </v-card-title>

        <v-card-text>

        <v-list>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>home</v-icon>
            </v-list-tile-action>
            <v-list-tile-title>参与的话题</v-list-tile-title>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>home</v-icon>
            </v-list-tile-action>
            <v-list-tile-title>收藏</v-list-tile-title>
          </v-list-tile>

        </v-list>

        </v-card-text>

      </v-card>
</v-app>

<bottom-menu></bottom-menu>
</div>
</template>

<script>

import { mapState } from 'vuex'
import TabMenu from '@/components/TabMenu'

export default {
  components: {
    'bottom-menu': TabMenu
  },
  data () {
    return {
    }
  },
  computed: {
    ...mapState({
      logined: state => state.GlobalStore.logined,
      username: state => state.GlobalStore.username,
      total: state => state.GlobalStore.total,
      available: state => state.GlobalStore.available,
      withdrawaling: state => state.GlobalStore.withdrawaling,
      locked: state => state.GlobalStore.locked
    })
  }
}
</script>

<style lang="less">
</style>
