import axios from 'axios'

export default {
  state: {
    newsList: [],
    tailNewsList: []
  },
  mutations: {
  },
  actions: {
    get_news_api ({commit, state}, url, isTop) {
      axios({
        method: 'get',
        url: url
      })
      .then(function (response) {
        console.log(response.data)
        let newsList = JSON.parse(response.data.data)
        for (let i in newsList) {
          let news = newsList[i]
          console.log(news)
          let d = {src: news.src, fallbackSrc: news.fallbackSrc, title: news.title, url: news.url, meta: {source: news.meta.source, date: news.meta.date, other: news.meta.other}}
          if (isTop) {
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
    }
  }
}
