// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import FastClick from 'fastclick'
import VueRouter from 'vue-router'
import VueScroller from 'vue-scroller'
import VueJsonp from 'vue-jsonp'
import { ToastPlugin } from 'vux'

import App from './App'
import store from './store'
import News from './components/News'
import NewsDetail from './components/NewsDetail'

Vue.use(ToastPlugin)
Vue.use(VueJsonp)
Vue.use(VueRouter)
Vue.use(VueScroller)

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
