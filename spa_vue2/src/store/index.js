import Vue from 'vue'
import Vuex from 'vuex'

// import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: null,
    role: null,
  },
  getters: {
  },
  mutations: {
  },
  actions: {
    login(context, token){
      let tokenData = JSON.parse(atob(token.split('.')[1]));
      console.log(tokenData)
      this.state.username = tokenData.username
      this.state.role = tokenData.role
    },
    logout(){
      this.state.username = null
      this.state.role = null
    }
  },
  modules: {
  }
})
