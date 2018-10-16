// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import FastClick from 'fastclick'
import VueRouter from 'vue-router'
import VueScroller from 'vue-scroller'
import VueJsonp from 'vue-jsonp'

import App from './App'
import store from './store'
import News from './components/News'
import NewsDetail from './components/NewsDetail'

import { ToastPlugin } from 'vux'

Vue.use(VueRouter)
Vue.use(VueJsonp)
Vue.use(VueScroller)
Vue.use(ToastPlugin)

const routes = [
  {
    path: '/',
    component: News
  },
  {
    path: '/detail',
    component: NewsDetail
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
