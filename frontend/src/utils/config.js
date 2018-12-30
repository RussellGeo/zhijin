let ip = '127.0.0.1:8899'
const settings = {
  URL: 'http://' + ip,
  RegisterURL: 'http://' + ip + '/register',
  LoginURL: 'http://' + ip + '/login',
  CreateTopicURL: 'http://' + ip + '/create_topic',
  GetTopicURL: 'http://' + ip + '/topiclist',
  GetTopicDetailURL: 'http://' + ip + '/topicdetail',
  TopicVoteURL: 'http://' + ip + '/topicvote'
}

export default settings
