import Vue from 'vue'
import Vuex from 'vuex'

import NewsStore from './NewsStore'
import GlobalStore from './GlobalStore'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    NewsStore,
    GlobalStore
  }
})
