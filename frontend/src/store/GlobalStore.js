import Vue from 'vue'
import VueJsonp from 'vue-jsonp'

Vue.use(VueJsonp)

export default {
  state: {
    logined: false,
    username: '',
    userid: '',
    phone: '',
    token: '',
    total: 0,
    available: 0,
    withdrawaling: 0,
    locked: 0
  },
  mutations: {
    set_logined (state) {
      state.logined = true
    }
  },
  actions: {
    set_login_info ({commit, state}, info) {
      state.logined = true
      state.username = info.username
      state.userid = info.user_id
      state.phone = info.phone
      state.total = info.total
      state.available = info.available
      state.locked = info.locking
      state.withdrawaling = info.withdrawing
    },
    create_topic ({commit, state}, topicInfo) {
      let req = {
        username: state.username,
        topic_title: topicInfo.topicTitle,
        topic_desc: topicInfo.topicDesc,
        create_time: topicInfo.CreateTime,
        options: [],
        deadline: topicInfo.deadlile
      }
      console.log(req)
    }
  }
}
