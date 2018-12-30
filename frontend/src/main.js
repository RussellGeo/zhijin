// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import FastClick from 'fastclick'
import VueRouter from 'vue-router'
import VueScroller from 'vue-scroller'
import VueJsonp from 'vue-jsonp'
import { ToastPlugin } from 'vux'

import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

import App from './App'
import store from './store'
import News from './components/News'
import NewsDetail from './components/NewsDetail'
import Topic from './page/Topic'
import TopicDetail from './page/TopicDetail'
import Account from './page/Account'
import Register from './page/Register'
import Login from './page/Login'
import CreateTopic from './page/CreateTopic'

import VueCookies from 'vue-cookies'

Vue.use(ToastPlugin)
Vue.use(VueJsonp)
Vue.use(VueRouter)
Vue.use(VueScroller)
Vue.use(Vuetify)

Vue.use(VueCookies)

const routes = [
  {
    path: '/',
    component: News
  },
  {
    path: '/detail',
    component: NewsDetail
  },
  {
    path: '/topic',
    component: Topic
  },
  {
    path: '/create_topic',
    component: CreateTopic
  },
  {
    path: '/topic_detail',
    component: TopicDetail
  },
  {
    path: '/account',
    component: Account
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/register',
    component: Register
  }
]

const router = new VueRouter({
  history: true,
  routes
})

FastClick.attach(document.body)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
