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
import Topic from './page/Topic'
import TopicDetail from './page/TopicDetail'

import VueCookies from 'vue-cookies'

Vue.use(ToastPlugin)
Vue.use(VueJsonp)
Vue.use(VueRouter)
Vue.use(VueScroller)

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
    path: '/topic_detail',
    component: TopicDetail
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
