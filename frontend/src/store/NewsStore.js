import axios from 'axios'
import Vue from 'vue'
import VueJsonp from 'vue-jsonp'

Vue.use(VueJsonp)
axios.defaults.withCredentials = true

export default {
  state: {
    newsCreated: false,
    serverIp: 'http://106.12.124.186:8899',
    newsList: [],
    tailNewsList: []
  },
  mutations: {
    set_newscreated (state) {
      state.newsCreated = true
    }
  },
  actions: {
    // info {url:'', isTop: ture}
    get_news_api ({commit, state}, info) {
      let url = info.url
      let isTop = info.isTop
      console.log('getnewapi' + isTop)
      axios({
        method: 'get',
        url: state.serverIp + url
      })
      .then(function (response) {
        console.log(response.data)
        let newsList = JSON.parse(response.data.data)
        for (let i in newsList) {
          let news = newsList[i]
          console.log(news)
          let d = {src: news.src, fallbackSrc: news.fallbackSrc, title: news.title, url: news.url, desc: news.desc, meta: {source: news.meta.source, date: news.meta.date, other: news.meta.other}}
          console.log(isTop)
          if (isTop === true) {
            console.log('front insert')
            state.newsList.push(d)
          } else {
            console.log('tail insert')
            state.tailNewsList.push(d)
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    j_get_news_api ({commit, state}, info) {
      let url = info.url
      let isTop = info.isTop
      console.log('jsonp request')
      Vue.jsonp(state.serverIp + url).then(data => {
        console.log(data.data)
        let newsList = JSON.parse(data.data)
        for (let i in newsList) {
          let news = newsList[i]
          let d = {src: news.src, fallbackSrc: news.fallbackSrc, title: news.title, url: news.url, desc: news.desc, meta: {source: news.meta.source, date: news.meta.date, other: news.meta.other}}
          if (isTop) {
            console.log('front insert')
            state.newsList.push(d)
            // state.tailNewsList.push(d)
          } else {
            console.log('tail insert')
            state.tailNewsList.push(d)
          }
        }
        // if (isTop) {
        //   state.newsList = l.concat(state.newsList)
        // } else {
        //   state.newsList = state.newsList.concat(l)
        // }
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}
