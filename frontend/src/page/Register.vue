<template>
  
<v-app>

  <scroller style="top:auto;">
    
  <v-card
    class="mx-auto"
    style="max-width: 500px;"
  >
    <v-system-bar
      color="deep-purple darken-4"
      dark
    >
      <v-spacer></v-spacer>
      <v-icon small>mdi-square</v-icon>
      <v-icon
        class="ml-1"
        small
      >mdi-circle</v-icon>
      <v-icon
        class="ml-1"
        small
      >mdi-triangle</v-icon>
    </v-system-bar>
    <v-toolbar
      color="deep-purple accent-4"
      cards
      dark
      flat
    >
      <v-btn icon>
        <v-icon>arrow-back</v-icon>
      </v-btn>
      <v-card-title class="title font-weight-regular">注册</v-card-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-form
      ref="form"
      v-model="form"
      class="pa-3 pt-4"
    >
      <v-text-field
        v-model="phone"
        box
        color="deep-purple"
        label="手机号码"
      ></v-text-field>

      <v-text-field
        v-model="password"
        :rules="[rules.password]"
        box
        color="deep-purple"
        label="密码"
        style="min-height: 96px"
        type="password"
      ></v-text-field>
      <v-text-field
        v-model="username"
        box
        color="deep-purple"
        label="用户名"
      ></v-text-field>
      <v-checkbox
        v-model="agreement"
        :rules="[rules.required]"
        color="deep-purple"
      >
        <template slot="label">
          I agree to the&nbsp;
          <a href="#" @click.stop.prevent="dialog = true">Terms of Service</a>
          &nbsp;and&nbsp;
          <a href="#" @click.stop.prevent="dialog = true">Privacy Policy</a>*
        </template>
      </v-checkbox>
    </v-form>
    <v-divider></v-divider>
      <v-btn
        :disabled="!form"
        :loading="isLoading"
        class="white--text"
        color="deep-purple accent-4"
        @click="doRegister"
        depressed
      >注册</v-btn>
    </v-card-actions>
    <v-dialog
      v-model="dialog"
      absolute
      max-width="400"
      persistent
    >
      <v-card>
        <v-card-title class="headline grey lighten-3">Legal</v-card-title>
        <v-card-text>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn
            flat
            @click="agreement = false, dialog = false"
          >
            No
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            class="white--text"
            color="deep-purple accent-4"
            @click="agreement = true, dialog = false"
          >
            Yes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
  <br>
  <br>
  <br>

  </scroller>
</v-app>
</template>

<script>

import { mapActions, mapMutations } from 'vuex'
import settings from '@/utils/config'
import Vue from 'vue'
import VueJsonp from 'vue-jsonp'

Vue.use(VueJsonp)

export default {
  data: () => ({
    agreement: false,
    dialog: false,
    email: undefined,
    username: undefined,
    form: false,
    isLoading: false,
    password: undefined,
    phone: undefined,
    rules: {
      email: v => (v || '').match(/@/) || 'Please enter a valid email',
      length: len => v => (v || '').length >= len || `Invalid character length, required ${len}`,
      password: v => (v || '').length >= 6 || '至少6位',
      username: v => (v || '').length >= 1 || '不能为空',
      required: v => !!v || 'This field is required'
    }
  }),
  methods: {
    ...mapMutations([
      'set_logined'
    ]),
    ...mapActions([
      'set_login_info'
    ]),
    doRegister () {
      alert(settings.RegisterURL)
      let _this = this
      console.log(settings.RegisterURL + '?phone=' + this.phone + '&password=' + this.password + '&username=' + this.username)
      Vue.jsonp(settings.RegisterURL + '?phone=' + this.phone + '&password=' + this.password + '&username=' + this.username).then(data => {
        if (data.retcode !== 0) {
          alert('登录失败！' + data.errmsg)
          return
        }
        console.log(data.data)
        let userInfo = JSON.parse(data.data)
        _this.set_login_info(userInfo)
        _this.$router.push({ path: '/account' })
      })
      .catch(error => {
        console.log(error)
        alert('登录失败！')
      })
    },
    gotoRegister () {
      this.$router.push({ path: '/register' })

      // Vue.jsonp(settings.URL).then(data => {
      //   console.log(data.data)
      // })
      // .catch(error => {
      //   console.log(error)
      // })
    }

  }
}
</script>

<style lang="less">
</style>


